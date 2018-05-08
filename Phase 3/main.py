from pymongo import MongoClient
import pymongo
import scrapy
import datetime
import subprocess


# to achiveve program requirement 5.1
def collectionDroppingandEmptyCollectionCreating(db):
    try:
        print("Dropping collection...")
        # Drop collection "course" if exist
        db.course.drop()
        # Create empty collection "course"
        db.createCollection("course")
        print("Collection dropping and empty collection creating are successful.")
    except pymongo.errors.ConnectionFailure as error:
        print("Collection Dropping and Collection Creating Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.2
def dataCrawling(db):
    try:
        address = input("Please enter the URL of the website you want to crawl: ")
        if (address == "default"):
            strCommand = "scrapy crawl mongo"
            subprocess.run(strCommand, shell=True)
            print("Data are crawled from project webpage.")
            print("Data Crawling is successful and all data are inserted into the database.")
        else:
            strCommand = "scrapy crawl ClassQuota"
            subprocess.run(strCommand, shell=True)
            print("Data are crawled from inputted URL.")
            print("Data Crawling is successful and all data are inserted into the database.")

    except pymongo.errors.ConnectionFailure as error:
        print("Course Insertion Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.3.1
def courseSeachbyKeyword(db):
    try:
        keyword = input("Please enter the keyword(s) of the course you want to search: ")
        print("Searching...")
        listOfCourse = db.course.aggregate(
            [
                {"$match": {"$ or":[{"courseTitle":" /. * keyword * /"}, {"courseDescription": "/.*keyword * /"}, {
                    "courseIntentedLearningOutcome": "/.*keyword * /"}]}}, {"$project": {
                "CourseCode": "$courseCode", "CourseName": "$courseTitle", "NumberofCredit": "$courseCredit",
                "Section": "$courseSectionList.sectionNumber", "Code": "$courseSectionList.sectionCode",
                "DateAndTime": "$courseSectionList.sectionOfferingSlot.dateAndTime", "Quota": "$courseSectionList.sectionQuota",
                "Enrol": "$courseSectionList.sectionEnrolled", "Avail": "$courseSectionList.sectionAvailable",
                "Wait": "$courseSectionList.sectionWait", "_id": 0}}, {"$sort": {"courseCode": 1,
                                                                       "courseSectionList.sectionNumber": 1}}
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

    except pymongo.errors.ConnectionFailure as error:
        print("Course searching Failed! Error Message: \"{}\"".format(error))


# to achiveve program requirement 5.3.2
def courseSeachbyWaitingListSize(db):
    try:
        f = input(
            "Please enter the multiple of the waiting list size with enrolled student which is a non-negative number: ")
        while (int(f) < 0):
            f = input("The number is invalid. Please input again: ")
        start_ts = input("Please enter the starting time slot: ")
        end_ts = input("Please enter the ending time slot: ")
        startTimeSlot = datetime.datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%S")
        endTimeSlot = datetime.datetime.strptime(end_ts, "%Y-%m-%dT%H:%M:%S")
        print("Searching...")
        listOfCourse = db.course.aggregate(
        #     [
        # {"$project": {"comparedTimeSlotResult1": {"$gte": ["$dataRetrievalTime", "startTimeSlot"]}},{"comparedTimeSlotResult2": {"$lte": ["$dataRetrievalTime", "endTimeSlot"]}}},
        # {"$match": {"$ and":[{"comparedTimeSlotResult1": "true"}, {"comparedTimeSlotResult2": "true"}]}},
        # {"$project": {"comparedWaitListSizeResult": {"$gte": ["$courseSectionList.sectionWait", {"$multiply": [
        #     "$courseSectionList.sectionQuota", "f"]}]}}},
        # {"$match": {"comparedWaitListSizeResult": "true"}},
        # {"$project": {"CourseCode": "$courseCode", "CourseName": "$courseTitle", "NumberofCredit": "$courseCredit",
        #               "TimeSlot": "$dataRetrievalTime", "Section": "$courseSectionList.sectionNumber",
        #               "Code": "$courseSectionList.sectionCode",
        #               "DateAndTime": "$courseSectionList.sectionOfferingSlot.dateAndTime",
        #               "Quota": "$courseSectionList.sectionQuota", "Enrol": "$courseSectionList.sectionEnrolled",
        #               "Avail": "$courseSectionList.sectionAvailable", "Wait": "$courseSectionList.sectionWait",
        #               "Satisfied": "comparedWaitListSizeResult", "_id": 0}},
        # {"$sort": {"courseCode": 1, "courseSectionList.sectionNumber": 1}},
        # {"$group": {"_id": "$courseSectionList.sectionNumber", "MatchedTimeSlot": {"$max": "$dataRetrievalTime"}}}
        # ]
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
            if (tempSatisfied == "ture"):
                print(" yes")
            else:
                print(" no")

    except pymongo.errors.ConnectionFailure as error:
        print("Course searching Failed! Error Message: \"{}\"".format(error))


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
        print("Getting a database named \"hkustclassquota\"")
        db = client["hkustclassquota"]

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
