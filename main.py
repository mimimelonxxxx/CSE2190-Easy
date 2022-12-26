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
if (pathlib.Path.cwd() / DBNAME).exists():
    FIRSTRUN = False

CONNECTION = sqlite3.connect(DBNAME)
CURSOR = CONNECTION.cursor()

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
                    return checkInt(NEWVALUE, MINVALUE, MAXVALUE)
                return VALUE
            except ValueError:
                print("Please input a valid number! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE)
    else:
        try:
            VALUE = int(VALUE)
            if VALUE > MAXVALUE or VALUE < MINVALUE:
                print("Please input a valid number within the range! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE)
            return VALUE
        except ValueError:
            print("Please input a valid number! ")
            NEWVALUE = input("> ")
            return checkInt(NEWVALUE, MINVALUE, MAXVALUE)

def createInitialTables() -> None:
    """
    creates initial tables within the database from the csv files
    """
    global CONNECTION, CURSOR
    CURSOR.execute("""
        CREATE TABLE 
            member_hours (
                member_name TEXT NOT NULL,
                total_member_hours REAL NOT NULL
            );
    """)

    CURSOR.execute("""
        CREATE TABLE 
            overtime (
                name_of_event TEXT NOT NULL,
                overtime INTEGER NOT NULL,
                total_duration REAL NOT NULL
            );
    """)

    CURSOR.execute("""
        CREATE TABLE 
            total_hours (
                total_hours REAL NOT NULL
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
    createInitialTables()
    CHOICE = menu()
# PROCESSING #

# OUTPUTS #