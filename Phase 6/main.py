import pymongo
import datetime
import subprocess
import scrapy
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import pandas
from keras.layers import Masking
import time

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
    listOfCourse = db.courses.aggregate(
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
def waitingListSizePrediction(db):
    cc = input("Please enter the course code: ")
    ln = input("Please enter the lecture number (ln): ")
    ts = input("Please enter the time slot: ")
    
    matched = db.courses.aggregate({'$project': {"comparedTimeSlotResult1": {'$eq': ["$sections.class_name", ln]}}})
    predictedResult = []
    if (matched):
        if (cc == "COMP1942"):
            dataframe1 = pandas.read_csv("COMP1942Result_1", usecols=[1])
            dataframe2 = pandas.read_csv("COMP1942Result_2", usecols=[1])
            dataframe3 = pandas.read_csv("COMP1942Result_3", usecols=[1])
            dataframe4 = pandas.read_csv("COMP1942Result_4", usecols=[1])
            dataframe5 = pandas.read_csv("COMP1942Result_5", usecols=[1])
            if (dataframe1 == ts):
                result = pandas.read_csv("COMP1942Result_1", usecols=[2])
                predictedResult[1] = result
            if (dataframe2 == ts):
                result = pandas.read_csv("COMP1942Result_2", usecols=[2])
                predictedResult[2] = result
            if (dataframe3 == ts):
                result = pandas.read_csv("COMP1942Result_3", usecols=[2])
                predictedResult[3] = result
            if (dataframe4 == ts):
                result = pandas.read_csv("COMP1942Result_4", usecols=[2])
                predictedResult[4] = result
            if (dataframe5 == ts):
                result = pandas.read_csv("COMP1942Result_5", usecols=[2])
                predictedResult[5] = result
            for i in range(predictedResult):
                print(predictedResult[i])
                if (i == range(predictedResult)):
                    break
                else:
                    print(",")
    else:
        print("There is no lecture section and thus there is no prediction result.")

# to achiveve program requirement 5.5
def waitingListSizeTraining(db, ln):
    
    # Write all the attributes to csv
    listOfWaitingList = db.courses.aggregate(
    [
        #{'$match': {{"code": ^COMP42, "class_name": ln}}},
        #{'$match': {{"code": ^COMP43, "class_name": ln}}},
        #{'$match': {{"code": ^RMBI, "class_name": ln}}},
        {'$match': {{"code": "COMP1942", "class_name": ln}}},
        {'$project': {"TimeSlot": "$recordTime", "Enrol": "$sections.enrol", "Wait": "$sections.wait", _id: 0}},
        {'$sort': {"TimeSlot": 1}}
    ]
    )
    recordNumber = 0

    for oneCourse in listOfWaitingList:
        recordNumber = recordNumber + 1
        listOfWaitingList["Timeslot"] = oneCourse["Timeslot"]
        listOfWaitingList["Enrol"] = oneCourse["Enrol"]
        listOfWaitingList["Wait"] = oneCourse["Wait"]

    filename = "COMP1942Training_Timestamp.csv"
    csv = open(filename, "w") 
    recordNumber = 0
    for recordNumber in listOfWaitingList:
        row = listOfWaitingList["Timeslot"] + "," + listOfWaitingList["Enrol"] + ","+  listOfWaitingList["Wait"] +"\n"
        csv.write(row)


    # Model 1: Neural Network (Parameter set A)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    look_back = 3
    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim)-look_back):
        a = data_float_TwoDim[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(data_float_TwoDim[i + look_back, 0])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)

    # Generate random seed
    numpy.random.seed(time.time())

    # Define the 1st model
    model = Sequential()
    model.add(Dense(20, input_dim=look_back, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the 1st model
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    # Fit the 1st model
    model.fit(numpyX, numpyY, epochs=2000, batch_size=20)

    # Evaluate the 1st model
    scores = model.evaluate(numpyX, numpyY)

    # Predict the 1st set of result using 1st model
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    
    # Save the 1st set of predicted target attribute of the new data into a file
    numpy.savetxt("COMP1942Result_1", newY_TwoDim, delimiter=",", fmt="%.10f")
    
    print("Waiting list size training is successful")

    # Model 2: Neural Network (Parameter set B)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    look_back = 3
    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim)-look_back):
        a = data_float_TwoDim[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(data_float_TwoDim[i + look_back, 0])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)

    # Generate random seed
    numpy.random.seed(time.time())

    # Define the 2nd model
    model = Sequential()
    model.add(Dense(30, input_dim=look_back, activation='relu'))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the 2nd model
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    # Fit the 2nd model
    model.fit(numpyX, numpyY, epochs=2000, batch_size=20)

    # Evaluate the 2nd model
    scores = model.evaluate(numpyX, numpyY)

    # Predict the 2nd set of result using 2nd model
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    
    # Save the 2nd set of predicted target attribute of the new data into a file
    numpy.savetxt("COMP1942Result_2", newY_TwoDim, delimiter=",", fmt="%.10f")
    
    print("Waiting list size training is successful")

    # Model 3: Neural Network (Parameter set C)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    look_back = 4
    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim)-look_back):
        a = data_float_TwoDim[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(data_float_TwoDim[i + look_back, 0])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)

    # Generate random seed
    numpy.random.seed(time.time())

    # Define the 3rd model
    model.add(Dense(30, input_dim=look_back, activation='relu'))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the 3rd model
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    # Fit the 3rd model
    model.fit(numpyX, numpyY, epochs=1500, batch_size=4)

    # Evaluate the 3rd model
    scores = model.evaluate(numpyX, numpyY)

    # Predict the 3rd set of result using 3rd model
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    
    # Save the 3rd set of predicted target attribute of the new data into a file
    numpy.savetxt("COMP1942Result_3", newY_TwoDim, delimiter=",", fmt="%.10f")
    
    print("Waiting list size training is successful")

    # Model 4: LSTM (Parameter set A)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim)):
        a = data_float_TwoDim[i, 0]
        dataX.append(a)
        dataY.append(data_float_TwoDim[i, 0])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)

    # Generate random seed
    numpy.random.seed(time.time())

    # Define the 4th model
    model = Sequential()
    model.add(Masking(mask_value=-1, input_shape=(4, 2)))
    model.add(LSTM(1))
    model.add(Dense(1, activation='relu'))
    
    # Compile the 4th model
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])
    
    # Fit the 4th model
    model.fit(numpyX, numpyY, validation_split=0.2, epochs=3000, batch_size=1)

    # Evaluate the 4th model
    scores = model.evaluate(numpyX, numpyY)

    # Predict the 4th set of result using 4th model
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    
    # Save the 4th set of predicted target attribute of the new data into a file
    numpy.savetxt("COMP1942Result_4", newY_TwoDim, delimiter=",", fmt="%.10f")
    
    print("Waiting list size training is successful")

    # Model 5: LSTM (Parameter set B)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim)):
        a = data_float_TwoDim[i:(i, 0)]
        dataX.append(a)
        dataY.append(data_float_TwoDim[i, 0])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)

    # Generate random seed
    numpy.random.seed(time.time())

    # Define the 5th model
    model = Sequential()
    model.add(Masking(mask_value=-1, input_shape=(4, 2)))
    model.add(LSTM(1))
    model.add(Dense(1, activation='relu'))
    
    # Compile the 5th model
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])
    
    # Fit the 5th model
    model.fit(numpyX, numpyY, validation_split=0.2, epochs=4000, batch_size=1)

    # Evaluate the 5th model
    scores = model.evaluate(numpyX, numpyY)

    # Predict the 5th set of result using 5th model
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    
    # Save the 5th set of predicted target attribute of the new data into a file
    numpy.savetxt("COMP1942Result_5", newY_TwoDim, delimiter=",", fmt="%.10f")
    
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
                waitingListSizePrediction(self.db)
            elif (choice == "6"):
                waitingListSizeTraining(self.db)
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

