"""
author: Michelle Jiang
title: JA Wage Calculator
date-created: 2022-12-25
"""
import pathlib
import sqlite3

# Testing SQLite and Python here without using Flask 

### VARIABLES ### 

DBNAME = "wage_calculator.db"
FIRSTRUN = True 
if (pathlib.Path.cwd() / DBNAME).exists(): # checks if there is already a database file 
    FIRSTRUN = False

CONNECTION = sqlite3.connect(DBNAME)
CURSOR = CONNECTION.cursor()

REGULARFILE = "JA Wage Calculation - Regular Hours.csv"
OVERTIMEFILE = "JA Wage Calculation - Overtime.csv"
SUMMARYFILE = "JA Wage Calculation - Summary.csv"
TOTALFILE = "JA Wage Calculation - Total Hours.csv"

### FUNCTIONS ###

def checkInt(VALUE, MINVALUE=0, MAXVALUE=5000, NULLNESS=False) -> int:
    """
    checks if the value is a valid integer
    :param VALUE: str
    :param MINVALUE: int
    :param MAXVALUE: int
    :param NULLNESS: bool
    :return: int
    """
    if NULLNESS:
        if VALUE == None or VALUE == "":
            VALUE = None
            return VALUE
        else:
            try:
                VALUE = int(VALUE)
                if VALUE > MAXVALUE or VALUE < MINVALUE:
                    print("Please input a valid number within the range! ")
                    NEWVALUE = input("> ")
                    return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
                return VALUE
            except ValueError:
                print("Please input a valid number! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
    else:
        try:
            VALUE = int(VALUE)
            if VALUE > MAXVALUE or VALUE < MINVALUE:
                print("Please input a valid number within the range! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
            return VALUE
        except ValueError:
            print("Please input a valid number! ")
            NEWVALUE = input("> ")
            return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)

def checkFloat(VALUE) -> bool:
    """
    checks if a string contains a float 
    :param VALUE: str
    :return: bool
    """
    try:
        float(VALUE)
        return True
    except ValueError:
        return False

def extractFiles() -> list:
    """
    reads files and extracts data from csv files
    :return: REGULARDATA list, OVERTIMEDATA list, SUMMARYDATA list, TOTALDATA list
    """
    global CONNECTION, CURSOR, REGULARFILE, TOTALFILE, OVERTIMEFILE, SUMMARYFILE

    REGULARFILE = open(REGULARFILE)
    REGULARDATA = REGULARFILE.readlines()
    SUMMARYFILE = open(SUMMARYFILE)
    SUMMARYDATA = SUMMARYFILE.readlines()
    OVERTIMEFILE = open(OVERTIMEFILE)
    OVERTIMEDATA = OVERTIMEFILE.readlines()
    TOTALFILE = open(TOTALFILE)
    TOTALDATA = TOTALFILE.readlines()

    # REGULAR HOURS DATA 
    for i in range(len(REGULARDATA)):
        if REGULARDATA[i][-1] == "\n":
                REGULARDATA[i] = REGULARDATA[i][:-1] 
        REGULARDATA[i] = REGULARDATA[i].split(",")
        for j in range(len(REGULARDATA[i])):
            if checkFloat(REGULARDATA[i][j]):
                REGULARDATA[i][j] = float(REGULARDATA[i][j])

    # OVERTIME DATA 
    for i in range(len(OVERTIMEDATA)):
        if OVERTIMEDATA[i][-1] == "\n":
                OVERTIMEDATA[i] = OVERTIMEDATA[i][:-1] 
        OVERTIMEDATA[i] = OVERTIMEDATA[i].split(",")
        for j in range(len(OVERTIMEDATA[i])):
            if OVERTIMEDATA[i][j] == '':
                OVERTIMEDATA[i][j] = 0
            if checkFloat(OVERTIMEDATA[i][j]):
                OVERTIMEDATA[i][j] = float(OVERTIMEDATA[i][j])
    
    # SUMMARY DATA
    for i in range(len(SUMMARYDATA)):
        if SUMMARYDATA[i][-1] == "\n":
                SUMMARYDATA[i] = SUMMARYDATA[i][:-1] 
        SUMMARYDATA[i] = SUMMARYDATA[i].split(",")
        for j in range(len(SUMMARYDATA[i])):
            if SUMMARYDATA[i][j] == '':
                SUMMARYDATA[i][j] = 0
            if SUMMARYDATA[i][j].isnumeric():
                SUMMARYDATA[i][j] = int(SUMMARYDATA[i][j])

    # TOTAL DATA
    for i in range(len(TOTALDATA)):
        if TOTALDATA[i][-1] == "\n":
                TOTALDATA[i] = TOTALDATA[i][:-1] 
        TOTALDATA[i] = TOTALDATA[i].split(",")
        for j in range(len(TOTALDATA[i])):
            if TOTALDATA[i][j] == '':
                TOTALDATA[i][j] = 0
            if checkFloat(TOTALDATA[i][j]):
                TOTALDATA[i][j] = float(TOTALDATA[i][j])

    return REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA

def setupDatabase(REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA):
    """
    creates database using data from files 
    :param REGULARDATA: list
    :param OVERTIMEDATA: list
    :param SUMMARYDATA: list
    :param TOTALDATA: list 
    :return: None
    """
    # REGULAR
    global CURSOR, CONNECTION
    CURSOR.execute("""
            CREATE TABLE 
                regular_hours (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    total_regular REAL NOT NULL
                );
        """)
    # create multiple tables for each row of data each time
    for i in range(1, len(REGULARDATA[0])-1):
        CURSOR.execute(f"""
            CREATE TABLE
                {REGULARDATA[0][i]} (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    {REGULARDATA[0][i]} TEXT NOT NULL
                );
        """)

    # OVERTIME 
    CURSOR.execute("""
            CREATE TABLE 
                overtime (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    total_overtime REAL NOT NULL
                );
        """)
    # create multiple tables for each row of data each time
    for i in range(1, len(OVERTIMEDATA[0])-1):
        CURSOR.execute(f"""
            CREATE TABLE
                {OVERTIMEDATA[0][i]} (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    {OVERTIMEDATA[0][i]} TEXT NOT NULL
                );
        """)

    # SUMMARY 
    CURSOR.execute("""
        CREATE TABLE 
            summary (
                name_of_event TEXT NOT NULL PRIMARY KEY,
                overtime INTEGER NOT NULL, 
                total_duration INTEGER NOT NULL
            );
    """) 

    # TOTAL
    CURSOR.execute("""
        CREATE TABLE
            total_hours (
                total_regular REAL NOT NULL,
                total_overtime REAL NOT NULL
            );
    """)

# INPUTS # 

def welcome() -> None:
    """
    displays a welcome message to the user 
    """
    print("Welcome to the Wage Calculator! ")

def menu() -> int:
    """
    displays a menu with options for the user to choose from
    :return: int
    """
    print("""
Please choose one of the following:
1. View all data
2. Search for member data 
    """)
    CHOICE = input("> ")
    CHOICE = checkInt(CHOICE, 1, 2)
    return CHOICE 

# PROCESSING # 

# OUTPUTS # 

### MAIN PROGRAM CODE ###
if __name__ == "__main__":
# INPUTS #
    welcome()
    REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA = extractFiles()
    setupDatabase(REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA)
    CHOICE = menu()
# PROCESSING #

# OUTPUTS #