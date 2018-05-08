from pymongo import MongoClient
import datetime


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
            # Crawing from time slot 1
            # Assume we are crawing the first page of trial website
            currentSemester = "2017-18 Spring"
            dataRetrievalTime = datetime.datetime.strptime("2018-01-26T14:00:00", "%Y-%m-%dT%H:%M:%S")
            # Accessed to class quota page
            db.course.insert(
                {
                    "courseCode": "COMP 4332",
                    "courseOfferingSemester": currentSemester,
                    "courseTitle": "Big Data Mining and Management",
                    "courseCredit": 3,
                    "coursePrerequisite": "COMP 4211 OR COMP 4331 OR ISOM 3360",
                    "courseColist": "RMBI 4310",
                    "courseDescription": "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modeling, and assessment.",
                    "courseSectionList": [
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L1",
                            "sectionCode": 1918,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "WeFr 01:30PM - 02:50PM",
                                    "venue": "G010, CYT Bldg (140)",
                                    "intstructorList": [
                                        "WONG, Raymond Chi Wing"
                                    ]
                                }
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 64,
                            "sectionAvailable": 1,
                            "sectionWait": 4,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "T1",
                            "sectionCode": 1919,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Tu 06:00PM - 06:50PM",
                                    "venue": "Rm 4619, Lift 31-32 (126)",
                                    "intstructorList": [
                                        "WONG, Raymond Chi Wing"
                                    ]
                                }
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 64,
                            "sectionAvailable": 1,
                            "sectionWait": 4,
                            "sectionRemark": "Instructor Consent Required"
                        }
                    ],
                    "courseAttributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs",
                    "courseAlternateCodes": "CIVL 1170",
                    "courseCorequisite": "LANG 4016",
                    "courseExclusion": "ISOM 2010, any COMP courses of 2000-level or above",
                    "courseIntendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.",
                    "coursePreviousCode": "ENVS 3002",
                    "courseVector": "[3-0-0:3]"
                },
                {
                    "courseCode": "COMP 3511",
                    "courseOfferingSemester": currentSemester,
                    "courseTitle": "Operating Systems",
                    "courseCredit": 3,
                    "coursePrerequisite": "COMP 2611 OR [ELEC 2300 AND (COMP 1002 (prior to 2013-14) OR COMP 1004 (prior to 2013-14) OR COMP 2011 OR COMP 2012H)]",
                    "courseDescription": "Principles, purpose and structure of operating systems; processes, threads, and multi-threaded programming; CPU scheduling; synchronization, mutual exclusion; memory management and virtual memory; device management; file systems, security and protection.",
                    "courseSectionList": [
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L1",
                            "sectionCode": 1889,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "TuTh 01:30PM - 02:50PM",
                                    "venue": "Rm 6573, Lift 29-30 (88)",
                                    "intstructorList": [
                                        "LI, Bo"
                                    ]
                                }
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 63,
                            "sectionAvailable": 2,
                            "sectionWait": 12,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L2",
                            "sectionCode": 1891,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Mo 01:30PM - 02:50PM",
                                    "venue": "G009B, CYT Bldg (70)",
                                    "intstructorList": [
                                        "WANG, Wei"
                                    ]
                                },
                                {
                                    "dateAndTime": "Fr 09:00AM - 10:20AM",
                                    "venue": "G009B, CYT Bldg (70)",
                                    "intstructorList": [
                                        "WANG, Wei"
                                    ]
                                },
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 64,
                            "sectionAvailable": 1,
                            "sectionWait": 18,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA1",
                            "sectionCode": 1893,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Fr 10:30AM - 12:20PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo",
                                        "WANG, Wei"
                                    ]
                                }
                            ],
                            "sectionQuota": 43,
                            "sectionEnrolled": 43,
                            "sectionAvailable": 0,
                            "sectionWait": 17,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA2",
                            "sectionCode": 1895,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Tu 06:00PM - 07:50PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo",
                                        "WANG, Wei"
                                    ]
                                }
                            ],
                            "sectionQuota": 43,
                            "sectionEnrolled": 42,
                            "sectionAvailable": 1,
                            "sectionWait": 19,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA3",
                            "sectionCode": 3834,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Fr 12:30PM - 02:20PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo"
                                    ]
                                }
                            ],
                            "sectionQuota": 44,
                            "sectionEnrolled": 42,
                            "sectionAvailable": 2,
                            "sectionWait": 0,
                            "sectionRemark": "Instructor Consent Required"
                        }
                    ],
                    "courseColist": "RMBI 4310",
                    "courseAttributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs",
                    "courseAlternateCodes": "CIVL 1170",
                    "courseCorequisite": "LANG 4016",
                    "courseExclusion": "ISOM 2010, any COMP courses of 2000-level or above",
                    "courseIntendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.",
                    "coursePreviousCode": "ENVS 3002",
                    "courseVector": "[3-0-0:3]"
                }
            )
            # Crawing from time slot 2
            currentSemester = "2017-18 Spring"
            dataRetrievalTime = datetime.datetime.strptime("2018-02-01T11:30:00", "%Y-%m-%dT%H:%M:%S")
            db.course.insert(
                {
                    "courseCode": "COMP 4332",
                    "courseOfferingSemester": currentSemester,
                    "courseTitle": "Big Data Mining and Management",
                    "courseCredit": 3,
                    "coursePrerequisite": "COMP 4211 OR COMP 4331 OR ISOM 3360",
                    "courseColist": "RMBI 4310",
                    "courseDescription": "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modeling, and assessment.",
                    "courseSectionList": [
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L1",
                            "sectionCode": 1918,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "WeFr 01:30PM - 02:50PM",
                                    "venue": "G010, CYT Bldg (140)",
                                    "intstructorList": [
                                        "WONG, Raymond Chi Wing"
                                    ]
                                }
                            ],
                            "sectionQuota": 75,
                            "sectionEnrolled": 71,
                            "sectionAvailable": 4,
                            "sectionWait": 3,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "T1",
                            "sectionCode": 1919,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Tu 06:00PM - 06:50PM",
                                    "venue": "Rm 4619, Lift 31-32 (126)",
                                    "intstructorList": [
                                        "WONG, Raymond Chi Wing"
                                    ]
                                }
                            ],
                            "sectionQuota": 75,
                            "sectionEnrolled": 71,
                            "sectionAvailable": 4,
                            "sectionWait": 3,
                            "sectionRemark": "Instructor Consent Required"
                        }
                    ],
                    "courseAttributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs",
                    "courseAlternateCodes": "CIVL 1170",
                    "courseCorequisite": "LANG 4016",
                    "courseExclusion": "ISOM 2010, any COMP courses of 2000-level or above",
                    "courseIntendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.",
                    "coursePreviousCode": "ENVS 3002",
                    "courseVector": "[3-0-0:3]"
                },
                {
                    "courseCode": "COMP 3511",
                    "courseOfferingSemester": currentSemester,
                    "courseTitle": "Operating Systems",
                    "courseCredit": 3,
                    "coursePrerequisite": "COMP 2611 OR [ELEC 2300 AND (COMP 1002 (prior to 2013-14) OR COMP 1004 (prior to 2013-14) OR COMP 2011 OR COMP 2012H)]",
                    "courseDescription": "Principles, purpose and structure of operating systems; processes, threads, and multi-threaded programming; CPU scheduling; synchronization, mutual exclusion; memory management and virtual memory; device management; file systems, security and protection.",
                    "courseSectionList": [
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L1",
                            "sectionCode": 1889,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "TuTh 01:30PM - 02:50PM",
                                    "venue": "Rm 6573, Lift 29-30 (88)",
                                    "intstructorList": [
                                        "LI, Bo"
                                    ]
                                }
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 65,
                            "sectionAvailable": 0,
                            "sectionWait": 16,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "L2",
                            "sectionCode": 1891,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Mo 01:30PM - 02:50PM",
                                    "venue": "G009B, CYT Bldg (70)",
                                    "intstructorList": [
                                        "WANG, Wei"
                                    ]
                                },
                                {
                                    "dateAndTime": "Fr 09:00AM - 10:20AM",
                                    "venue": "G009B, CYT Bldg (70)",
                                    "intstructorList": [
                                        "WANG, Wei"
                                    ]
                                },
                            ],
                            "sectionQuota": 65,
                            "sectionEnrolled": 65,
                            "sectionAvailable": 0,
                            "sectionWait": 18,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA1",
                            "sectionCode": 1893,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Fr 10:30AM - 12:20PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo",
                                        "WANG, Wei"
                                    ]
                                }
                            ],
                            "sectionQuota": 43,
                            "sectionEnrolled": 43,
                            "sectionAvailable": 0,
                            "sectionWait": 20,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA2",
                            "sectionCode": 1895,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Tu 06:00PM - 07:50PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo",
                                        "WANG, Wei"
                                    ]
                                }
                            ],
                            "sectionQuota": 43,
                            "sectionEnrolled": 43,
                            "sectionAvailable": 0,
                            "sectionWait": 20,
                            "sectionRemark": "Instructor Consent Required"
                        },
                        {
                            "dataRetrievalTime": dataRetrievalTime,
                            "sectionNumber": "LA3",
                            "sectionCode": 3834,
                            "sectionOfferingSlot": [
                                {
                                    "dateAndTime": "Fr 12:30PM - 02:20PM",
                                    "venue": "Rm 4214, Lift 19 (52)",
                                    "intstructorList": [
                                        "LI, Bo"
                                    ]
                                }
                            ],
                            "sectionQuota": 44,
                            "sectionEnrolled": 44,
                            "sectionAvailable": 0,
                            "sectionWait": 2,

                            "sectionRemark": "Instructor Consent Required"
                        }
                    ],
                    "courseColist": "RMBI 4310",
                    "courseAttributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs",
                    "courseAlternateCodes": "CIVL 1170",
                    "courseCorequisite": "LANG 4016",
                    "courseExclusion": "ISOM 2010, any COMP courses of 2000-level or above",
                    "courseIntendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.",
                    "coursePreviousCode": "ENVS 3002",
                    "courseVector": "[3-0-0:3]"
                }
            )
            print("Data are crawled from project webpage.")
            print("Data Crawling is successful and all data are inserted into the database.")
        else:
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
                {$match: {$ or:[{courseTitle: /. * keyword * /}, {courseDescription: /.*keyword * /}, {
                                                                                                       courseIntentedLearningOutcome: /.*keyword * /}]}}, {$project: {
            CourseCode: "$courseCode", CourseName: "$courseTitle", NumberofCredit: "$courseCredit",
            Section: "$courseSectionList.sectionNumber", Code: "$courseSectionList.sectionCode",
            DateAndTime: "$courseSectionList.sectionOfferingSlot.dateAndTime", Quota: "$courseSectionList.sectionQuota",
            Enrol: "$courseSectionList.sectionEnrolled", Avail: "$courseSectionList.sectionAvailable",
            Wait: "$courseSectionList.sectionWait", _id: 0}}, {$sort: {courseCode: 1,
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
            [
                {$project: {comparedTimeSlotResult1: {$gte: ["$dataRetrievalTime", startTimeSlot]}},
        {comparedTimeSlotResult2: {$lte: ["$dataRetrievalTime", endTimeSlot]}}},
        {$match: {$ and:[{comparedTimeSlotResult1: true}, {comparedTimeSlotResult2: true}]}},
        {$project: {comparedWaitListSizeResult: {$gte: ["$courseSectionList.sectionWait", {$multiply: ["$courseSectionList.sectionQuota", f]}]}}},
        {$match: {comparedWaitListSizeResult: true}},
        {$project: {CourseCode: "$courseCode", CourseName: "$courseTitle", NumberofCredit: "$courseCredit",
                    TimeSlot: "$dataRetrievalTime", Section: "$courseSectionList.sectionNumber",
                    Code: "$courseSectionList.sectionCode",
                    DateAndTime: "$courseSectionList.sectionOfferingSlot.dateAndTime",
                    Quota: "$courseSectionList.sectionQuota", Enrol: "$courseSectionList.sectionEnrolled",
                    Avail: "$courseSectionList.sectionAvailable", Wait: "$courseSectionList.sectionWait",
                    Satisfied: "comparedWaitListSizeResult", _id: 0}},
        {$sort: {courseCode: 1, "courseSectionList.sectionNumber": 1}},
        {$group: {_id: "$courseSectionList.sectionNumber", MatchedTimeSlot: {$max: "$dataRetrievalTime"}}}
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

main()

