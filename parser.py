

"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014
Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:
1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def writeToFile(item, file, key):
    if key in item:
        file.write(item[key] + " | ")
    return

def writeToFileDollars(item, file, key):
    if key in item:
        file.write(transformDollar(item[key]) + " | ")
    return

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        with open('ebay_data/item.dat', 'w') as item_file:
            item_file.write("Item_ID | Name | Currently | Buy_Price | First_Bid"
                            " | Number_of_Bids | Started | Ends | Seller | Description | \n")
            with open('ebay_data/user.dat', 'w') as userFile:
                userFile.write("User_ID | Location | Country | Rating \n")
            with open("ebay_data/bid.dat", 'w') as bidFile:
                bidFile.write("Item_ID | Bidder|  Time | Amount \n")
            with open("ebay_data/bid.dat", 'w') as itemBidFile:
                itemBidFile.write("Item_ID | Bidder_ID \n")
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            standard_out = sys.stdout
            with open('ebay_data/item.dat', 'a') as itemFile:
                writeToFile(item, itemFile, "ItemID")
                writeToFile(item, itemFile, "Name")
                writeToFileDollars(item, itemFile, "Currently")
                writeToFileDollars(item, itemFile, "Buy_Price")
                writeToFileDollars(item, itemFile, "First_Bid")
                writeToFile(item, itemFile, "Number_of_Bids")
                writeToFile(item, itemFile, "Started")
                writeToFile(item, itemFile, "Ends")
                writeToFile(item["Seller"], itemFile, "UserID")
                if item["Description"] is not None:
                    writeToFile(item, itemFile, "Description")
                itemFile.write("\n")

            with open('ebay_data/bid.dat', 'a') as bidFile:
                writeToFile(item, bidFile, "ItemID")
                if item["Bids"] is not None:
                    for bidders in item["Bids"]:
                        # writeToFile(bidders, bidFile, "UserID")
                        # bidFile.write(str(bidders))
                        bidFile.write(bidders["Bid"]["Bidder"]["UserID"] + " | ")
                        bidFile.write(bidders["Bid"]["Time"] + " | ")
<<<<<<< HEAD
                        bidFile.write(transformDollar(bidders["Bid"]["Amount"]))
                else: bidFile.write("NULL | NULL | NULL")
=======
                        bidFile.write(transformDollar(bidders["Bid"]["Amount"]) + " | ")
>>>>>>> b6bcc5419863ac27e034ba4696ac5a1b7791c48e
                bidFile.write("\n")

            with open('ebay_data/user.dat', 'a') as userFile:
                writeToFile(item["Seller"], userFile, "UserID")
                writeToFile(item, userFile, "Location")
                writeToFile(item, userFile, "Country")
                writeToFile(item["Seller"], userFile, "Rating")
                userFile.write("\n")

            with open('ebay_data/item_category.dat', 'a') as f:
                for cat in item["Category"]:
                    f.write(item["ItemID"] + " | ")
                    f.write(cat + "\n")
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)