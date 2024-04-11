import os 
import pprint
def printData():
    f = open("demofile2.txt", "r")
    pprint.pprint(f.read())

while True:
    userinput = input("You want to print the data y/n ? : ")
    if userinput == "y" or userinput == "Y":
        printData()
    elif userinput == "n" or userinput == "N":
        break