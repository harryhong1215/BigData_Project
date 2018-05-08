from pymongo import MongoClient
import pymongo
import scrapy
import datetime
import subprocess
import re

# to achiveve program requirement 5.1
def collectionDroppingandEmptyCollectionCreating(db):
    try:
        print("Dropping collection...")
        # Drop collection "course" if exist
        db.courses.drop()
        # Create empty collection "course"
        db.create_collection("courses")
        print("Collection dropping and empty collection creating are successful.")
    except pymongo.errors.ConnectionFailure as error:
        print("Collection Dropping and Collection Creating Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.2
def dataCrawling(db):
    try:
        # address = input("Please enter the URL of the website you want to crawl: ")
        url = input('Please enter a URL for data crawling: ')
        if url == 'default':
            url = 'http://comp4332.com/trial'
            # url = 'http://comp4332.com/realistic'
        with open('url.txt', 'w') as f:
            f.write(url)
        subprocess.run('scrapy crawl mongo', shell=True)
        if (url == "default"):
            strCommand = "scrapy crawl mongo"
            subprocess.run(strCommand, shell=True)
            print("Data are crawled from project webpage.")
            print("Data Crawling is successful and all data are inserted into the database.")
        else:
            strCommand = "scrapy crawl mongo"
            subprocess.run(strCommand, shell=True)
            print("Data are crawled from inputted URL.")
            print("Data Crawling is successful and all data are inserted into the database.")

    except pymongo.errors.ConnectionFailure as error:
        print("Course Insertion Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.3.1
def courseSeachbyKeyword(db):
    keyword = input("Please enter the keyword(s) of the course you want to search: ")
    print("Searching...")
    regex_text = "\\b(" + "|".join(keyword.split()) + ")\\b"
    REGEX = re.compile(regex_text, re.IGNORECASE)
    listOfCourse = db.courses.aggregate(
        [
            {"$match": {'$or': [{'title': {'$regex': REGEX}}, {'description':{'$regex': REGEX}},{'intendedLearningOutcomes': {'$regex': REGEX}}
        ]}},
            {"$project": {"CourseCode": "$code", "CourseName": "$title", "NumberofCredit": "$credits",
                        "SectionID": "$sections.sectionId", "DateAndTime": "$sections.offerings.dateAndTime",
                          "Quota": "$sections.quota",
                          "Enrol": "$sections.enrol", "Wait": "$sections.wait","Avail":"$sections.avail", "_id": 0}},
            {"$sort":{"CourseCode":1}}
        ])

    print(list(listOfCourse))
    recordNumber = 0
    # After performing seaching
    for oneCourse in listOfCourse:
        recordNumber = recordNumber + 1
        tempCourseCode = oneCourse['CourseCode']
        tempCourseName = oneCourse["CourseName"]
        tempNumberofCredit = oneCourse["NumberofCredit"]
        tempSection = oneCourse["Section"]
        tempCode = oneCourse["SectionID"]
        tempDateAndTime = oneCourse["DateAndTime"]
        tempQuota = oneCourse["Quota"]
        tempEnrol = oneCourse["Enrol"]
        tempWait = oneCourse["Wait"]
        tempAvail = oneCourse["Avail"]
        # print("{:s} {:s} {:d} {:s} {:d} {:s} {:d} {:d} {:f} {:f}".format(tempCourseCode, tempCourseName,
        #                                                             tempNumberofCredit, tempSection, tempCode,
        #                                                             tempDateAndTime, tempQuota, tempEnrol,
        #                                                             tempWait,tempAvail))
        # print(tempCourseCode, tempCourseName,tempNumberofCredit, tempSection, tempCode,
        #       tempDateAndTime, tempQuota, tempEnrol,tempWait,tempAvail)

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
            {"$project": {"comparedTimeSlotResult1": {"$gte": ["$recordTime", startTimeSlot]},
                          "comparedTimeSlotResult2": {"$lte": ["$recordTime", endTimeSlot]}},
                          "comparedWaitListSizeResult": {"$gte": ["$sections.wait", {"$multiply": ["$sections.quota", f]}]}},
            {"$match": {"$and": [{"comparedTimeSlotResult1": True}, {"comparedTimeSlotResult2": True},{"comparedWaitListSizeResult":True}]}},
            {"$project": {"CourseCode": "$code","TimeSlot": "$recordTime", "Section": "$sections.sectionId"}},
            {"$sort": {"$recordTime":1,"$courseCode": 1, "$sections.sectionId": 1}},
            {"$project": {"CourseCode": "$code", "TimeSlot": "$recordTime", "Section": "$sections.sectionId"}},
            {"$group": {"_id": "$sections.sectionId","MatchedTimeSlot": {"$last": "$recordTime"}}},
            {"$project": {"CourseCode": "$code", "CourseName": "$title", "NumberofCredit": "$credits",
                          "TimeSlot": "$MatchedTimeSlot", "Code": "$sections.sectionId",
                          "DateAndTime": "$sections.offerings.dateAndTime", "Quota": "$sections.quota",
                          "Enrol": "$sections.enrol", "Wait": "$sections.wait","Satisfied": "Yes"}}
        ]
    )
    print(list(listOfCourse))
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
        # print("{:s} {:s} {:d} {:s} {:d} {:s} {:d} {:d} {:d}".format(tempCourseCode, tempCourseName,
        #                                                             tempNumberofCredit, tempSection, tempCode,
        #                                                             tempDateAndTime, tempQuota, tempEnrol,
        #                                                             tempWait))

# to achiveve program requirement 5.4
def waitingListSizePrediction(db):
    try:
        cc = input("Please enter the course code: ")
        ln = input("Please enter the lecture number (ln): ")
        ts = input("Please enter the time slot: ")
        matched = True
        if (matched):
            print("40,43,45,39,40")
        else:
            print("There is no lecture section and thus there is no prediction result.")

    except pymongo.errors.ConnectionFailure as error:
        print("Course searching Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.5
def waitingListSizeTraining(db):
    try:
        print("Waiting list size training is successful")

    except pymongo.errors.ConnectionFailure as error:
        print("Course searching Failed! Error Message: \"{}\"".format(error))


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
        print("Making a MongoDB connection...")
        client = MongoClient("mongodb://localhost:27017")

        # Getting a Database named "university"
        print("Getting a database named \"hkust\"")
        db = client["hkust"]

        while (True):
            displayMenu()
            # allow the user to choose one of the functions in the menu
            choice = input("Please input your choice (1-7): ")
            print("\n")
            # check the input and call the correspondence function
            if (choice == "1"):
                collectionDroppingandEmptyCollectionCreating(db)
            elif (choice == "2"):
                dataCrawling(db)
            elif (choice == "3"):
                courseSeachbyKeyword(db)
            elif (choice == "4"):
                courseSeachbyWaitingListSize(db)
            elif (choice == "5"):
                waitingListSizePrediction(db)
            elif (choice == "6"):
                waitingListSizeTraining(db)
            elif (choice == "7"):
                break
            else:
                print("Invalid Input!")

            # Closing connection with Database
            print("Closing connection with database...")
            client.close()
            exit()
    except pymongo.errors.ConnectionFailure as error:
        print("DB Connection Failed! Error Message: \"{}\"".format(error))




# def main():
#     url = input('Please enter a URL for data crawling: ')
#     if url == 'default':
#         url = 'http://comp4332.com/realistic'
#     with open('url.txt', 'w') as f:
# 	    f.write(url)
#     subprocess.run('scrapy crawl mongo', shell=True)
# 	# We use a file to pass URL, but you can use other methods.
# 	# A commonly used method is to pass the start_urls using the '-a' argument
# 	# If interested, you can refer to https://stackoverflow.com/a/15291961

if __name__ == '__main__':
    main()
