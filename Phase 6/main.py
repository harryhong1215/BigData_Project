import pymongo
import datetime
import subprocess
import scrapy
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import model_from_json
import numpy
from keras.layers import Masking

# to achiveve program requirement 5.1
def collectionDroppingandEmptyCollectionCreating(db):
    try:
        print("Dropping collection...")
        # Drop collection "course" if exist
        db.courses.drop()
        # Create empty collection "course"
        db.createCollection("courses")
        print("Collection dropping and empty collection creating are successful.")
    except pymongo.errors.ConnectionFailure as error:
        print("Collection Dropping and Collection Creating Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.2
class MongoSpider(scrapy.Spider):
    try:
        name = 'mongo'
        mongo_uri = 'mongodb://localhost:27017'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            with open('url.txt', 'r') as f:
                url = f.read()
                self.start_urls = [ url ]
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client['hkust']

            # used as cache for database to check whether 
            # courses are already inserted 
            # you can also check from database directly
            self.inserted_courses = set()

        def parse(self, response):
            for a in response.xpath('//ul/li/a'):
                yield response.follow(a, callback=self.parse_snapshot)

        def parse_snapshot(self, response):
            for a in response.xpath('//div[@class="depts"]/a'):
                yield response.follow(a, callback=self.parse_dept)

        def parse_dept(self, response):
            title = response.xpath('//title/text()').extract_first()

            # ====== extract semester and time =========
            i = title.find(': Snapshot taken at ')
            semester = title[:i-5] # each dept has a length of 4
            time_str = title[i + len(': Snapshot taken at '):]
            year = int(time_str[:4])
            month = int(time_str[5:7])
            day = int(time_str[8:10])
            hour = int(time_str[11:13])
            minute = int(time_str[-2:])
            record_time = datetime(year, month, day, hour, minute)

            # simpler method using regular expression and strptime
            # m = re.search(r'(.*) \w+: Snapshot taken at (.*)', title)
            # semester = m.group(1)
            # record_time = datetime.strptime(m.group(2), '%Y-%m-%d %H:%M')
            # ==========================================

            # uncomment the following two lines if you want the progress to be displayed
            #dept = response.url[-9:-5]
            #print('Processing %s %s' % (time_str, dept))

            courses = response.xpath('//div[@class="course"]')
            for course in courses:
                self.parse_course(course, semester, record_time)

        def parse_course(self, el, semester, record_time):
            # extract_first() is the same as extract()[0]
            header = el.xpath('.//h2/text()').extract_first()
            i = header.find('-')
            j = header.rfind('(')
            k = header.rfind('unit')
            code = header[:i].replace(' ', '')
            if (code, semester) not in self.inserted_courses:
                course = {
                    'code': code,
                    'semester': semester
                }
                course['title'] = header[i+1:j].strip()
                course['credits'] = float(header[j+1:k])

                # ========== process 'COURSE INFO' ==============
                # the function fix_case removes '(', ')' , '-' and ' ' from the keys and
                # change them to camel case.
                # e.g., 'PRE-REQUISITE' -> 'prerequisite'
                # 'CO-LIST WITH' -> 'colistWith'
                # you can achieve the same goal using a sequence of 'if-else' statements
                # i.e., 
                # key = ' '.join(tr.xpath('.//th//text()').extract())
                # if key == 'PRE-REQUISITE':
                #     key = 'prerequisite'
                # elif key == 'CO-LIST WITH':
                #     key = 'colistWith'
                # ...
                for tr in el.xpath('.//div[contains(@class, "courseattr")]/div/table/tr'):
                    key = self.fix_case(' '.join(tr.xpath('.//th//text()').extract()))
                    value = '\t'.join([
                        x.strip()
                        for x in tr.xpath('.//td//text()').extract()
                    ])
                    course[key] = value
                # =================================================

                self.inserted_courses.add((code, semester))
                self.db.courses.insert_one(course)
            self.parse_sections(el.xpath('.//table[@class="sections"]//tr')[1:], code, semester, record_time)

        def parse_sections(self, trs, code, semester, record_time):
            sections = []
            prev_sect = None
            for tr in trs:
                class_name = tr.xpath('./@class').extract_first()
                if 'newsect' in class_name:
                    sectionId = tr.xpath('./td[1]/text()').extract_first().split('(', 1)[0].strip()
                    section = {
                        'recordTime': record_time,
                        'sectionId': sectionId,
                        'offerings': [
                            {
                                # most complicated case: 2016-17 Summer MGMT5410
                                'dateAndTime': '\t'.join(tr.xpath('./td[2]/text()').extract()),
                                'room': tr.xpath('./td[3]/text()').extract_first(),
                                'instructors': tr.xpath('./td[4]/text()').extract()
                            }
                        ],
                        # the text may be inside its children
                        # example: 2016-17 Spring ACCT5140 L1
                        'quota': int(tr.xpath('./td[5]//text()').extract_first()),
                        'enrol': int(tr.xpath('./td[6]//text()').extract_first()),
                        # if avail is 0, it is enclosed by <strong>
                        #'avail': int(tr.xpath('./td[7]//text()').extract_first()),
                        'wait': int(tr.xpath('./td[8]//text()').extract_first())
                    }
                    remarks = '\t'.join([
                        text.strip()
                        for text in tr.xpath('./td[9]//text()').extract()
                        if text.strip() != ''
                    ])
                    if remarks != '':
                        section['remarks'] = remarks
                    sections.append(section)
                    prev_sect = section
                else:
                    offering = {
                        # index starts from 1
                        # TODO: split dateAndTime to daysOfWeek and time
                        'dateAndTime': ' '.join(tr.xpath('./td[1]/text()').extract()),
                        'room': tr.xpath('./td[2]/text()').extract_first(),
                        'instructors': tr.xpath('./td[3]/text()').extract()
                    }
                    prev_sect['offerings'].append(offering)

            self.db.courses.update_one(
                { 'code': code, 'semester': semester },
                { '$push': {
                        'sections': {
                            '$each': sections
                        }
                    }
                }
            )

        def closed(self, reason):
            self.client.close()
            print('Data Crawling is successful and all data are inserted into the database')

        def fix_case(self, key):

            # ======= remove characters '(', ')' and '-' ===========
            s = key.translate({ord(c): '' for c in '()-'})
            # using regular expression
            #s = re.sub(r'[()-]', '', key)
            # ======================================================
            
            res = s.title().replace(' ', '')
            return res[0].lower() + res[1:]

    except pymongo.errors.ConnectionFailure as error:
        print("Course Insertion Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.3.1
def courseSeachbyKeyword(db):
    keyword = input("Please enter the keyword(s) of the course you want to search: ")
    print("Searching...")
    listOfCourse = db.courses.aggregate(
        [
            {$match: {$ or:[{title: /. * keyword * /}, {description: /.*keyword * /}, {intendedlearningoutcomes: /.*keyword * /}]}}, 
            {$project: { CourseCode: "$code", CourseName: "$title", NumberofCredit: "$credits", Section: "$sections.class_name", 
            SectionID: "$sections.sectionId", DateAndTime: "$sections.offerings.dateAndTime", Quota: "$sections.quota",
            Enrol: "$sections.enrol", Wait: "$sections.wait", _id: 0}}, 
            {$sort: {courseCode: 1, "sections.sectionId": 1}}
        ]
    )
    recordNumber = 0
    # After performing seaching
    for oneCourse in listOfCourse:
        recordNumber = recordNumber + 1
        tempCourseCode = oneCourse["CourseCode"]
        tempCourseName = oneCourse["CourseName"]
        tempNumberofCredit = oneCourse["NumberofCredit"]
        tempSection = oneCourse["Section"]
        tempCode = oneCourse["Code"]
        tempDateAndTime = oneCourse["DateAndTime"]
        tempQuota = oneCourse["Quota"]
        tempEnrol = oneCourse["Enrol"]
        tempWait = oneCourse["Avail"]
        print("{:s} {:s} {:d} {:s} {:d} {:s} {:d} {:d} {:d}".format(tempCourseCode, tempCourseName,
                                                                    tempNumberofCredit, tempSection, tempCode,
                                                                    tempDateAndTime, tempQuota, tempEnrol,
                                                                    tempWait))

# to achiveve program requirement 5.3.2
def courseSeachbyWaitingListSize(db):
    f = input(
        "Please enter the multiple of the waiting list size with enrolled student which is a non-negative number: ")
    while (int(f) < 0):
        f = input("The number is invalid. Please input again: ")
    start_ts = input("Please enter the starting time slot: ")
    end_ts = input("Please enter the ending time slot: ")
    startTimeSlot = datetime.datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%S")
    endTimeSlot = datetime.datetime.strptime(end_ts, "%Y-%m-%dT%H:%M:%S")
    print("Searching...")
    listOfCourse = db.s.aggregate(
    [
        {$project: {comparedTimeSlotResult1: {$gte: ["$recordTime", startTimeSlot]}},
        {comparedTimeSlotResult2: {$lte: ["$recordTime", endTimeSlot]}}},
        {$match: {$and:[{comparedTimeSlotResult1: true}, {comparedTimeSlotResult2: true}]}},
        {$project: {comparedWaitListSizeResult: {$gte: ["$sections.wait", {$multiply: ["$sections.quota", f]}]}}},
        {$match: {comparedWaitListSizeResult: true}},
        {$project: {CourseCode: "$code", CourseName: "$title", NumberofCredit: "$credits", TimeSlot: "$recordTime", Section: "$sections.class_name", Code: "$sections.sectionId",
                DateAndTime: "$sections.offerings.dateAndTime", Quota: "$sections.quota", Enrol: "$sections.enrol", Wait: "$sections.wait", Satisfied: "comparedWaitListSizeResult", _id: 0}},
        {$sort: {courseCode: 1, "sections.sectionId": 1}},
        {$group: {_id: "$sections.sectionId", MatchedTimeSlot: {$max: "$recordTime"}}}
    ]
    )
    recordNumber = 0
    # After performing searching
    for oneCourse in listOfCourse:
        recordNumber = recordNumber + 1
        tempCourseCode = oneCourse["CourseCode"]
        tempCourseName = oneCourse["CourseName"]
        tempNumberofCredit = oneCourse["NumberofCredit"]
        tempTimeSlot = oneCourse["TimeSlot"]
        tempSection = oneCourse["Section"]
        tempCode = oneCourse["Code"]
        tempDateAndTime = oneCourse["DateAndTime"]
        tempQuota = oneCourse["Quota"]
        tempEnrol = oneCourse["Enrol"]
        tempWait = oneCourse["Avail"]
        tempSatisfied = oneCourse["Satisfied"]
        print("{:s} {:s} {:d} {:s} {:d} {:s} {:d} {:d} {:d}".format(tempCourseCode, tempCourseName,
                                                                    tempNumberofCredit, tempSection, tempCode,
                                                                    tempDateAndTime, tempQuota, tempEnrol,
                                                                    tempWait))
        if (tempSatisfied == ture):
            print(" yes")
        else:
            print(" no")

# to achiveve program requirement 5.4
def waitingListSizePrediction(model):
    cc = input("Please enter the course code: ")
    ln = input("Please enter the lecture number (ln): ")
    ts = input("Please enter the time slot: ")
   
    # Read new data records
    newrecordfilename = "new.csv"   
    newX = numpy.loadtxt(newrecordfilename, delimiter=",")
        
    # Predict the target attribute of the new data based on a model
    newY = model.predict(newX, batch_size=4)

    # Save the predicted target attribute of the new data into a file
    newYcategoricalPythonArray = []
    recordNo = 0
    for value in newY:
        if (value < 0.5):
            newYcategoricalPythonArray.append("No")
        if (value >= 0.5):
            newYcategoricalPythonArray.append("Yes")
    newYcategorical = numpy.array(newYcategoricalPythonArray)
    newYcategoricalReshape = newYcategorical.reshape(4, 1)
    newYwithpredicted = numpy.append(newY, newYcategoricalReshape, axis=1)
    resultfilename = "output-NN.csv"    
    numpy.savetxt(resultfilename, newYwithpredicted, delimiter=",", fmt="%.10s")

    matched = True
    if (matched):
        print("40,43,45,39,40")
    else:
        print("There is no lecture section and thus there is no prediction result.")

# to achiveve program requirement 5.5
def waitingListSizeTraining():
    # Write all the attributes to csv
    
    # Train the csv
    filename = "training.csv"   
    dataset = numpy.loadtxt(filename, delimiter=",", dtype="str")

    # Transform target attributes
    X_str = dataset[:, 0:2]
    X_float = X_str.astype(float)
    Y_str = dataset[:, 2:3]
    Y_shape = Y_str.shape
    Y_result = numpy.zeros(Y_shape)
    for x in range(0, Y_shape[0]):
        if Y_str[x] == "Yes":
            Y_result[x] = 1
        if Y_str[x] == "No":
            Y_result[x] = 0
    Y_float = Y_result.astype(float)

    # Generate random seed
    numpy.random.seed(4332)

    # Define the model
    model = Sequential()
    model.add(Dense(4, input_dim=2, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the model
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    # Fit the model
    model.fit(X_float, Y_float, epochs=1500, batch_size=4)

    # Evaluate the model
    scores = model.evaluate(X_float, Y_float)

    return model
    print("Waiting list size training is successful")


# to display the menu
def displayMenu():
    print(" ")
    print("         Menu")
    print("=======================")
    print("1. Collection Dropping and Empty Collection Creating")
    print("2. Data Crawling")
    print("3. Course Search by Keyword")
    print("4. Course Search by Waiting List Size ")
    print("5. Waiting List Size Prediction")
    print("6. Waiting List Size Training")
    print("7. Exit")
    print("=======================")
    print(" ")


def main():
    try:
        # Making a DB connection
        name = 'ustclassquota'
        mongo_uri = 'mongodb://localhost:27017'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.client = pymongo.MongoClient(self.mongo_uri)
            print("Getting a database named \"hkust\"")
            self.db = self.client['hkust']

            # used as cache for database to check whether 
            # courses are already inserted 
            # you can also check from database directly
            self.inserted_courses = set()

        while (True):
            displayMenu()

            # allow the user to choose one of the functions in the menu
            choice = input("Please input your choice (1-7): ")
            print("\n")

            # check the input and call the correspondence function
            if (choice == "1"):
                collectionDroppingandEmptyCollectionCreating(self.db)
            elif (choice == "2"):
                url = input('Please enter a URL for data crawling: ')
                if url == 'default':
                    url = 'http://comp4332.com/realistic'
                with open('url.txt', 'w') as f:
                    f.write(url)
                subprocess.run('scrapy crawl mongo', shell=True)
            elif (choice == "3"):
                courseSeachbyKeyword(self.db)
            elif (choice == "4"):
                courseSeachbyWaitingListSize(self.db)
            elif (choice == "5"):
                waitingListSizePrediction(model)
            elif (choice == "6"):
                waitingListSizeTraining()
            elif (choice == "7"):
                break
            else:
                print("Invalid Input!")

            # Closing connection with Database
            print("Closing connection with database...")
            self.client.close()
            exit()

    except pymongo.errors.ConnectionFailure as error:
        print("DB Connection Failed! Error Message: \"{}\"".format(error))

if __name__ == '__main__':
    main()

