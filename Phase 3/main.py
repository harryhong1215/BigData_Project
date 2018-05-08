from pymongo import MongoClient
import pymongo
import scrapy
import datetime
import subprocess
import re
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import pandas
import time
from keras.layers import Masking


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
        if (url == "default"):
            url = 'http://comp4332.com/trial'
            with open('url.txt', 'w') as f:
                f.write(url)
            strCommand = "scrapy crawl mongo"
            subprocess.run(strCommand, shell=True)
            print("Data are crawled from project webpage.")
            print("Data Crawling is successful and all data are inserted into the database.")
        else:
            with open('url.txt', 'w') as f:
                f.write(url)
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
            {"$unwind": "$sections"},
    {"$match": {'$or': [{'title': {'$regex': REGEX}}, {'description':{'$regex': REGEX}},{'intendedLearningOutcomes': {'$regex': REGEX}}
        ]}},
            {"$project": {"CourseCode": "$code", "CourseName": "$title", "NumberofCredit": "$credits",
                        "SectionID": "$sections.sectionId", "DateAndTime": "$sections.offerings.dateAndTime",
                          "Quota": "$sections.quota",
                          "Enrol": "$sections.enrol", "Wait": "$sections.wait","Avail":"$sections.avail", "_id": 0}},
            {"$sort":{"CourseCode":1}}
        ])

    print(list(listOfCourse))


# to achiveve program requirement 5.3.2
def courseSeachbyWaitingListSize(db):
    f = input(
        "Please enter the multiple of the waiting list size with enrolled student which is a non-negative number: ")
    while (float(f) < 0):
        f = input("The number is invalid. Please input again: ")
    start_ts = input("Please enter the starting time slot: ")
    end_ts = input("Please enter the ending time slot: ")
    startTimeSlot = datetime.datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%S")
    endTimeSlot = datetime.datetime.strptime(end_ts, "%Y-%m-%dT%H:%M:%S")

    print("Searching...")
    listOfCourse = db.courses.aggregate(
        [
            {"$unwind": "$sections"},
            {"$project": {
                "comparedTimeSlotResult1": {"$gte": ["$sections.recordTime", startTimeSlot]},
                "comparedTimeSlotResult2": {"$lte": ["$sections.recordTime", endTimeSlot]},
                "comparedWaitListSizeResult": {"$gte": ["$sections.wait", {"$multiply": ["$sections.enrol", float(f)]}]}
                          }},
            {"$match": {"$and": [{"comparedTimeSlotResult1": True}, {"comparedTimeSlotResult2": True},{"comparedWaitListSizeResult":True}]}},
            {"$project": {"CourseCode": "$code","TimeSlot": "$recordTime", "Section": "$sections.sectionId"
                          }},
            {"$sort": {"TimeSlot":1,"CourseCode": 1, "Section": 1}},
            {"$project": {"CourseCode": 1, "TimeSlot": 1, "Section": 1}},
            {"$group": {"_id": "$sections.sectionId","MatchedTimeSlot": {"$last": "$recordTime"}}},
            {"$project": {"CourseCode": "$code", "CourseName": "$title", "NumberofCredit": "$credits",
                          "TimeSlot": "$MatchedTimeSlot", "Code": "$_id",
                          "DateAndTime": "$sections.offerings.dateAndTime", "Quota": "$sections.quota",
                          "Enrol": "$sections.enrol", "Wait": "$sections.wait","Satisfied":"Yes"}}
        ]
    )


    print(list(listOfCourse))


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
def waitingListSizeTraining(db,ln):
    # Write all the attributes to csv
    listOfWaitingList = db.courses.aggregate(
        [
            # {'$match': {{"code": ^COMP42, "class_name": ln}}},
            # {'$match': {{"code": ^COMP43, "class_name": ln}}},
            # {'$match': {{"code": ^RMBI, "class_name": ln}}},
            {'$match': {{"code": "COMP1942", "class_name": ln}}},
            {'$project': {"TimeSlot": "$recordTime", "Enrol": "$sections.enrol", "Wait": "$sections.wait", "_id": 0}},
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
        row = listOfWaitingList["Timeslot"] + "," + listOfWaitingList["Enrol"] + "," + listOfWaitingList["Wait"] + "\n"
        csv.write(row)

    # Model 1: Neural Network (Parameter set A)
    # Train the csv
    dataframe = pandas.read_csv(filename, usecols=[1])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)

    look_back = 3
    dataX, dataY = [], []
    for i in range(len(data_float_TwoDim) - look_back):
        a = data_float_TwoDim[i:(i + look_back), 0]
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
    scores = model.evaluate(numpyX,numpyY)

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
    for i in range(len(data_float_TwoDim) - look_back):
        a = data_float_TwoDim[i:(i + look_back), 0]
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
    scores = model.evaluate(numpyX,numpyY)

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
    for i in range(len(data_float_TwoDim) - look_back):
        a = data_float_TwoDim[i:(i + look_back), 0]
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
    scores = model.evaluate(numpyX,numpyY)

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
        a = data_float_TwoDim[i:(i + look_back), 0]
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
    scores = model.evaluate(numpyX,numpyY)

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
    scores = model.evaluate(numpyX,numpyY)

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
