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

REGULARFILE = "SAMPLE CALC JA Wage Calculation - Regular Hours.csv"
OVERTIMEFILE = "SAMPLE CALC JA Wage Calculation - Overtime.csv"
SUMMARYFILE = "SAMPLE CALC JA Wage Calculation - Summary.csv"
TOTALFILE = "SAMPLE CALC JA Wage Calculation - Total Hours.csv"
PRODUCTIONFILE = "SAMPLE CALC JA Wage Calculation - Production.csv"
SALESFILE = "SAMPLE CALC JA Wage Calculation - Sales.csv"

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
    global CONNECTION, CURSOR, REGULARFILE, TOTALFILE, OVERTIMEFILE, SUMMARYFILE, PRODUCTIONFILE, SALESFILE

    REGULARFILE = open(REGULARFILE)
    REGULARDATA = REGULARFILE.readlines()
    SUMMARYFILE = open(SUMMARYFILE)
    SUMMARYDATA = SUMMARYFILE.readlines()
    OVERTIMEFILE = open(OVERTIMEFILE)
    OVERTIMEDATA = OVERTIMEFILE.readlines()
    TOTALFILE = open(TOTALFILE)
    TOTALDATA = TOTALFILE.readlines()
    PRODUCTIONFILE = open(PRODUCTIONFILE)
    PRODUCTIONDATA = PRODUCTIONFILE.readlines()
    SALESFILE = open(SALESFILE)
    SALESDATA = SALESFILE.readlines()

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
            if SUMMARYDATA[i][j].isnumeric():
                SUMMARYDATA[i][j] = int(SUMMARYDATA[i][j])
            if SUMMARYDATA[i][j] == '':
                SUMMARYDATA[i][j] = 0

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

    # PRODUCTION DATA
    for i in range(len(PRODUCTIONDATA)):
        if PRODUCTIONDATA[i][-1] == "\n":
                PRODUCTIONDATA[i] = PRODUCTIONDATA[i][:-1] 
        PRODUCTIONDATA[i] = PRODUCTIONDATA[i].split(",")
        for j in range(len(PRODUCTIONDATA[i])):
            if PRODUCTIONDATA[i][j].isnumeric():
                PRODUCTIONDATA[i][j] = int(PRODUCTIONDATA[i][j])
            if PRODUCTIONDATA[i][j] == '':
                PRODUCTIONDATA[i][j] = 0

    # SALES DATA
    for i in range(len(SALESDATA)):
        if SALESDATA[i][-1] == "\n":
                SALESDATA[i] = SALESDATA[i][:-1] 
        SALESDATA[i] = SALESDATA[i].split(",")
        for j in range(len(SALESDATA[i])):
            if SALESDATA[i][j].isnumeric():
                SALESDATA[i][j] = int(SALESDATA[i][j])
            if SALESDATA[i][j] == '':
                SALESDATA[i][j] = 0

    return REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA, PRODUCTIONDATA, SALESDATA

def setupDatabase(REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA, PRODUCTIONDATA, SALESDATA) -> None:
    """
    creates database using data from files 
    :param REGULARDATA: list
    :param OVERTIMEDATA: list
    :param SUMMARYDATA: list
    :param TOTALDATA: list 
    :param PRODUCTIONDATA: list
    :param SALESDATA: list
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

    for i in range(1, len(REGULARDATA)):
        CURSOR.execute(f"""
            INSERT INTO 
                regular_hours
            VALUES (
                ?,
                ?
            );
        """, [REGULARDATA[i][0], REGULARDATA[i][-1]])

    # create multiple tables for each row of data each time
    for i in range(1, len(REGULARDATA[0])-1):
        CURSOR.execute(f"""
            CREATE TABLE
                {REGULARDATA[0][i]} (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    {REGULARDATA[0][i]} TEXT NOT NULL
                );
        """)
        for j in range(1, len(REGULARDATA)):
            CURSOR.execute(f"""
                INSERT INTO
                    {REGULARDATA[0][i]}
                VALUES (
                    ?,
                    ?
                );
            """, [REGULARDATA[j][0], REGULARDATA[j][i]])

    # OVERTIME 
    CURSOR.execute("""
            CREATE TABLE 
                overtime (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    total_overtime REAL NOT NULL
                );
        """)

    for i in range(1, len(OVERTIMEDATA)):
        CURSOR.execute(f"""
            INSERT INTO 
                overtime
            VALUES (
                ?,
                ?
            );
        """, [OVERTIMEDATA[i][0], OVERTIMEDATA[i][-1]])

    # create multiple tables for each row of data each time
    for i in range(1, len(OVERTIMEDATA[0])-1):
        CURSOR.execute(f"""
            CREATE TABLE
                {OVERTIMEDATA[0][i]} (
                    member_name TEXT NOT NULL PRIMARY KEY,
                    {OVERTIMEDATA[0][i]} TEXT NOT NULL
                );
        """)
        for j in range(1, len(OVERTIMEDATA)):
            CURSOR.execute(f"""
                INSERT INTO
                    {OVERTIMEDATA[0][i]}
                VALUES (
                    ?,
                    ?
                );
            """, [OVERTIMEDATA[j][0], OVERTIMEDATA[j][i]])

    # SUMMARY 
    CURSOR.execute("""
        CREATE TABLE 
            summary (
                name_of_event TEXT NOT NULL PRIMARY KEY,
                overtime INTEGER NOT NULL, 
                total_duration INTEGER NOT NULL, 
                total_attendance INTEGER NOT NULL
            );
    """) 

    for i in range(1, len(SUMMARYDATA)):
        CURSOR.execute("""
            INSERT INTO 
                summary
            VALUES (
                ?,
                ?,
                ?, 
                ?
            );
        """, [SUMMARYDATA[i][0], SUMMARYDATA[i][1], SUMMARYDATA[i][2], SUMMARYDATA[i][3]])

    # TOTAL
    CURSOR.execute("""
        CREATE TABLE
            total_hours (
                total_hours REAL NOT NULL
            );
    """)

    for i in range(1, len(TOTALDATA)):
        CURSOR.execute("""
            INSERT INTO
                total_hours
            VALUES (
                ?
            );
        """, [TOTALDATA[i][0]])

    # PRODUCTION
    CURSOR.execute("""
        CREATE TABLE
            production (
                member_name TEXT NOT NULL PRIMARY KEY,
                amount_produced INTEGER NOT NULL
            );
    """)

    for i in range(1, len(PRODUCTIONDATA)):
        CURSOR.execute("""
            INSERT INTO
                production
            VALUES (
                ?,
                ?
            );
        """, [PRODUCTIONDATA[i][0], PRODUCTIONDATA[i][1]])

    # SALES
    CURSOR.execute("""
        CREATE TABLE
            sales (
                member_name TEXT NOT NULL PRIMARY KEY,
                amount_sold INTEGER NOT NULL
            );
    """)

    for i in range(1, len(SALESDATA)):
        CURSOR.execute("""
            INSERT INTO
                sales
            VALUES (
                ?,
                ?
            );
        """, [SALESDATA[i][0], SALESDATA[i][1]])

    CURSOR.execute("""
            CREATE TABLE 
                wages (
                    member_name TEXT NOT NULL PRIMARY KEY , 
                    percent_wages REAL NOT NULL 
                );
        """)

    CONNECTION.commit()

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
3. Exit
    """)
    CHOICE = input("> ")
    CHOICE = checkInt(CHOICE, 1, 3)
    return CHOICE 

def getMember():
    """
    user inputs member name to search for 
    :return: str
    """
    global CURSOR
    print("Please input member name: ")
    NAME = input("> ")
    return NAME

# PROCESSING # 

def calculateWages() -> list:
    """
    calculates percentage wages for all members in the database 
    :return: list (each members wages in order)
    """
    TOTALHOURS = CURSOR.execute("""
        SELECT
            *
        FROM
            total_hours;
    """).fetchone()

    MEMBERREGULAR = CURSOR.execute("""
        SELECT
            *
        FROM 
            regular_hours;
    """).fetchall()

    MEMBEROVERTIME = CURSOR.execute("""
        SELECT 
            * 
        FROM    
            overtime;
    """).fetchall()

    MEMBERPRODUCTION = CURSOR.execute("""
        SELECT
            *
        FROM
            production;
    """).fetchall()

    MEMBERSALES = CURSOR.execute("""
        SELECT
            *
        FROM
            sales; 
    """).fetchall()

    # calculate total hours 
    TOTALHOURS = TOTALHOURS[0]

    # calculate each members percentage 
    TOTALWAGES = []
    TOTALPERCENTAGE = 100

    for i in range(len(MEMBERREGULAR)): # the length of MEMBERREGULAR should be the same as the other lists 
        # distributes all wages based solely on hours 
        TOTALMEMBER = MEMBERREGULAR[i][1] + MEMBEROVERTIME[i][1]
        MEMBERWAGES = TOTALMEMBER/TOTALHOURS * 100
        # calculates regular hours 
        MEMBERREGULAR[i] = list(MEMBERREGULAR[i])
        while MEMBERREGULAR[i][1] >= 20:
            TOTALMEMBER = TOTALMEMBER * 1.02
            MEMBERWAGES = TOTALMEMBER/TOTALHOURS * 100
            MEMBERREGULAR[i][1] = MEMBERREGULAR[i][1] - 20
        # calculates production 
        MEMBERPRODUCTION[i] = list(MEMBERPRODUCTION[i])
        while MEMBERPRODUCTION[i][1] >= 20:
            TOTALMEMBER = TOTALMEMBER * 1.02
            MEMBERWAGES = TOTALMEMBER/TOTALHOURS * 100
            MEMBERPRODUCTION[i][1] = MEMBERPRODUCTION[i][1] - 20
        # calculates sales 
        MEMBERSALES[i] = list(MEMBERSALES[i])
        while MEMBERSALES[i][1] >= 20:
            TOTALMEMBER = TOTALMEMBER * 1.02
            MEMBERWAGES = TOTALMEMBER/TOTALHOURS * 100
            MEMBERSALES[i][1] = MEMBERSALES[i][1] - 20
        # calculates overtime hours 
        MEMBEROVERTIME[i] = list(MEMBEROVERTIME[i])
        while MEMBEROVERTIME[i][1] >= 20:
            TOTALMEMBER = TOTALMEMBER * 1.1
            MEMBERWAGES = TOTALMEMBER/TOTALHOURS * 100
            MEMBEROVERTIME[i][1] = MEMBEROVERTIME[i][1] - 20
        TOTALPERCENTAGE = TOTALPERCENTAGE - MEMBERWAGES
        TOTALWAGES.append(MEMBERWAGES)
    
    # distributes any overcompensations equally 
    if TOTALPERCENTAGE < 0:
        for i in range(len(TOTALWAGES)):
            PERCENTAGE = TOTALPERCENTAGE / len(TOTALWAGES)
            TOTALWAGES[i] = TOTALWAGES[i] + PERCENTAGE

    for i in range(len(TOTALWAGES)):
        TOTALWAGES[i] = round(TOTALWAGES[i], 2)
    return(TOTALWAGES)

def wageDatabase(TOTALWAGES) -> None:
    """
    creates a database with wage information 
    :return: None
    """
    global CURSOR, CONNECTION

    MEMBERREGULAR = CURSOR.execute("""
        SELECT
            member_name
        FROM 
            regular_hours;
    """).fetchall()

    for i in range(len(TOTALWAGES)):
        CURSOR.execute("""
            INSERT INTO 
                wages
            VALUES (
                ?,
                ?
            );
        """, [MEMBERREGULAR[i][0], TOTALWAGES[i]])

    CONNECTION.commit()

# PROCESSING # 

def conglomerateTable(REGULARDATA, OVERTIMEDATA) -> None:
    """
    joins all tables that uses member_name as a primary key together 
    :param REGULARDATA: list
    :param OVERTIMEDATA: list 
    :return: None
    """
    global CURSOR, CONNECTION
    
    #MEMBERDATA = []

    #for i in range(1, len(REGULARDATA[0])-1):
    MEMBERDATA = CURSOR.execute(f"""
        SELECT
            regular_hours.member_name,
            _2022_12_15._2022_12_15,
            regular_hours.total_regular,
            _2022_12_18_discord._2022_12_18_discord,
            overtime.total_overtime,
            production.amount_produced,
            sales.amount_sold,
            wages.percent_wages
        FROM
            regular_hours
        JOIN
            _2022_12_15
        ON
            _2022_12_15.member_name = regular_hours.member_name
        JOIN 
            _2022_12_18_discord
        ON
            _2022_12_18_discord.member_name = regular_hours.member_name
        JOIN 
            overtime
        ON 
            overtime.member_name = regular_hours.member_name
        JOIN
            production
        ON
            production.member_name = regular_hours.member_name
        JOIN 
            sales
        ON
            sales.member_name = regular_hours.member_name
        JOIN 
            wages
        ON
            wages.member_name = regular_hours.member_name;
    """).fetchall()
    print(MEMBERDATA)
    CONNECTION.commit()

def queryWages(NAME) -> None:
    """
    queries the wages table for a members wages
    :param NAME: str
    :return: None
    """
    global CURSOR
    WAGE = CURSOR.execute(f"""
        SELECT
            percent_wages
        FROM
            wages
        WHERE
            member_name = "{NAME}";
    """).fetchone()

    print(f"The percent of profit that {NAME} will receive is {WAGE[0]}%.")

# OUTPUTS # 

### MAIN PROGRAM CODE ###
if __name__ == "__main__":
# INPUTS #
    welcome()
    if FIRSTRUN:
        REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA, PRODUCTIONDATA, SALESDATA = extractFiles()
        setupDatabase(REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA, PRODUCTIONDATA, SALESDATA)
        TOTALWAGES = calculateWages()
        wageDatabase(TOTALWAGES)
    CHOICE = menu()
# PROCESSING #
    if CHOICE == 1:
        REGULARDATA, OVERTIMEDATA, SUMMARYDATA, TOTALDATA, PRODUCTIONDATA, SALESDATA = extractFiles()
        conglomerateTable(REGULARDATA, OVERTIMEDATA)
        # will print a table in the flask app
    elif CHOICE == 2:
        NAME = getMember()
        queryWages(NAME)
# OUTPUTS #
    elif CHOICE == 3:
        exit()