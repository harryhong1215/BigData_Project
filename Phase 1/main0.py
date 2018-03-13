# to achiveve program requirement 5.1
def collectionDroppingandEmptyCollectionCreating():
    print ("Collection dropping and empty collection creating are successful.")

# to achiveve program requirement 5.2
def dataCrawling(address):
	if (address == "default"):
		print ("Data are crawled from project webpage.")
		print ("Data Crawling is successful and all data are inserted into the database.")
	else:
		print ("Data are crawled from inputted URL.")
		print ("Data Crawling is successful and all data are inserted into the database.")

# to achiveve program requirement 5.3.1
def courseSeachbyKeyword(keyword):
	print ("COMP 1001 - Exploring Multimedia and Internet Computing (3 units)")
	print ("L1 (1756)	Th 03:00PM - 04:50PM	67	4	63	0") 
    print ("LA1 (1757)	Tu 03:00PM - 04:50PM	67	4	63	0")
	print ("COMP 1022P - Introduction to Computing with Java (3 units)")
	print ("L1 (1770)	MoWe 10:30AM - 11:20AM	80	14	66	0")	 
	print ("L2 (1772)	MoWe 12:00PM - 12:50PM	80	14	66	0")	 
	print ("LA1 (1774)	Tu 01:00PM - 02:50PM	54	10	44	0")	 
	print ("LA2 (1776)	Th 11:00AM - 12:50PM	54	8	46	0") 
	print ("LA3 (1777)	Tu 09:00AM - 10:50AM	54	10	44	0")

# to achiveve program requirement 5.3.2
def courseSeachbyWaitingListSize(f, start_ts, end_ts):
	print ("COMP 1001 - Exploring Multimedia and Internet Computing (3 units)")
	print ("03:00PM - 04:50PM")
	print ("L1 (1756)	Th 03:00PM - 04:50PM	67	4	63	0") 
    print ("LA1 (1757)	Tu 03:00PM - 04:50PM	67	4	63	0")

# to achiveve program requirement 5.4
def waitingListSizePrediction(cc, ln, ts):
	print ("40,43,45,39,40")

# to achiveve program requirement 5.5
def waitingListSizeTraining():
	print ("Waiting list size training is successful")

# to display the menu
def main():

	# display the menu
	choice = "0"
	while (choice != "7"):
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
		
		# allow the user to choose one of the functions in the menu
		choice = input("Please input your choice (1-7): ")
		
		print("")
		
		# check the input and call the correspondence function
		if (choice == "1"):
			collectionDroppingandEmptyCollectionCreating()
		elif (choice == "2"):
			address = input("Please enter the URL of the website you want to crawl: ")
			dataCrawling(address)
		elif (choice == "3"):
			keyword = input("Please enter the keyword(s) of the course you want to search: ")
			courseSeachbyKeyword(keyword)
		elif (choice == "4"):
			f = input("Please enter the size of the waiting size which is a non-negative number: ")
			if (f <= 0):
				f = input("The number is invalid. Please input again: ")
			start_ts = input("Please enter the starting time slot: ")
			end_ts = input("Please enter the ending time slot: ")
			courseSeachbyWaitingListSize(f, start_ts, end_ts)
		elif (choice == "5"):
			cc = input("Please enter the course code: ")
			ln = input("Please enter the lecture number (ln): ")
			ts = input("Please enter the time slot: ")
			waitingListSizePrediction(cc, ln, ts)
		elif (choice == "6"):
			waitingListSizeTraining()
		elif (choice == "7"):
			print("")																				
		else:
			print("Invalid Input!")

main()


