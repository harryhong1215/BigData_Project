# to achiveve program requirement 5.1
def collectionDroppingandEmptyCollectionCreating():
    print("Collection dropping and empty collection creating are successful.")


# to achiveve program requirement 5.2
def dataCrawling():
    address = input("Please enter the URL of the website you want to crawl: ")
    if (address == "default"):
        print("Data are crawled from project webpage.")
        print("Data Crawling is successful and all data are inserted into the database.")
    else:
        print("Data are crawled from inputted URL.")
        print("Data Crawling is successful and all data are inserted into the database.")


# to achiveve program requirement 5.3.1
def courseSeachbyKeyword():
    keyword = input("Please enter the keyword(s) of the course you want to search: ")
    print("COMP 1942 - Exploring and Visualizing Data (3 units)")
    print("L1	WeFr 03:00PM - 04:20PM	140	140	0	49")
    print("T1	Fr 01:30PM - 02:20PM	73	73	0	36")
    print("T2	We 11:00AM - 11:50AM	67	67	0	14")


# to achiveve program requirement 5.3.2
def courseSeachbyWaitingListSize():
    f = input("Please enter the multiple of the waiting list size with enrolled student which is a non-negative number: ")
    while (int(f) < 0):
        f = input("The number is invalid. Please input again: ")
    start_ts = input("Please enter the starting time slot: ")
    end_ts = input("Please enter the ending time slot: ")
    # After performing searching
    match_ts = 1200
    print("ISOM 1380 - Technology and Innovation: Social and Business Perspectives)")
    print("Matched Time Slot: 12:00")
    print("03:00PM - 04:50PM")
    print("L1	Mo 01:30PM - 02:50PM   	70	70	0	169")


# to achiveve program requirement 5.4
def waitingListSizePrediction():
    cc = input("Please enter the course code: ")
    ln = input("Please enter the lecture number (ln): ")
    ts = input("Please enter the time slot: ")
    matched = True
    if (matched):
        print("40,43,45,39,40")
    else:
        print("There is no lecture section and thus there is no prediction result.")


# to achiveve program requirement 5.5
def waitingListSizeTraining():
    print("Waiting list size training is successful")

# to display the menu
def displayMenu():
    print("")
    print("         Menu")
    print("=======================")
    print("1. Collection Dropping and Empty Collection Creating")
    print("2. Data Crawling")
    print("3. Course Search by Keyword")
    print("4. Course Search by Waiting List Size ")
    print("5. Waiting List Size Prediction")
    print("6. Waiting List Size Training")
    print("7. Exit")
    print("")

def main():
    while (True):
        displayMenu()

        # allow the user to choose one of the functions in the menu
        choice = input("Please input your choice (1-7): ")
        print("")

        # check the input and call the correspondence function
        if (choice == "1"):
            collectionDroppingandEmptyCollectionCreating()
        elif (choice == "2"):
            dataCrawling()
        elif (choice == "3"):
            courseSeachbyKeyword()
        elif (choice == "4"):
            courseSeachbyWaitingListSize()
        elif (choice == "5"):
            waitingListSizePrediction()
        elif (choice == "6"):
            waitingListSizeTraining()
        elif (choice == "7"):
            break
        else:
            print("Invalid Input!")
    exit()
main()


