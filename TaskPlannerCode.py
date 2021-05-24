import pandas as pd
import sqlite3


try:
    db = sqlite3.connect("")
    print("opened")
    planner = db.cursor()
except sqlite3.DatabaseError as error:
    print(error)


def create_table():
    '''
    Creates a table with column headers within the database using SQL query.
    :arguments: none
    :returns: Database table
    '''
    with db:
        planner.execute('''CREATE TABLE IF NOT EXISTS Assignments
                        (ID INTEGER PRIMARY KEY  NULL,
                        Course         CHAR(10)  NOT NULL,
                        TaskName       CHAR(13)  NOT NULL,
                        DueDate        CHAR(10)  NOT NULL,
                        TimeNeeded     INT  NOT NULL,
                        Completed      Char(10)   NOT NULL)
                        ;''')


class Entry:
    '''
    Class for entry variables and new entry function used throughout program.
    '''
    def __init__(self, tsk_cls, task_name, due_date, est_time, comp):
        '''
        Initializes variables
        :param tsk_cls: task course: course
        :param task_name: task (str): task name
        :param due_date: due date (str): date
        :param est_time: estimated time (str)
        :param comp: completed (str)
        '''
        # Initializes variables. arg: self, [variables]
        self.tsk_cls = tsk_cls
        self.task = task_name
        self.due_date = due_date
        self.est_time = est_time
        self.comp = comp

    def new_entry(self, tsk_cls, task_name, due_date, est_time, comp):
        '''
        SQL Query to create a new instance in the database rows
        :arg: tsk_cls, task_name, due_date, est_time, comp
        :return:
        '''
        planner.execute('INSERT INTO Assignments VALUES (NULL,?,?,?,?,?);',[tsk_cls, task_name, due_date, est_time, comp])


def add_entry():
    '''
    Add new entry to database with user inputs
    :return: new assignment instance in database row
    '''
    while True:
        tsk_cls = input("Enter Course Name: ")
        task_name = input("Enter Assignment Name: ")
        due_date = input("Enter Due Date: ")
        est_time = input("Enter Estimated Time To Complete: ")
        comp = input("Is it Completed?: (Yes/No) ").upper()
        if comp == 'YES':
            new_task = Entry(tsk_cls, task_name, due_date, est_time, comp)
            new_task.new_entry(tsk_cls, task_name, due_date, est_time, comp)
            user_add = input("Would you like to add a new entry?: (Yes/No) ").upper()
            if user_add == 'YES':
                continue
            elif user_add == 'NO':
                view_menu()
                break
            else:
                print("Please Enter a Valid Input!")
                break
        if comp == 'NO':
            new_task = Entry(tsk_cls, task_name, due_date, est_time, comp)
            new_task.new_entry(tsk_cls, task_name, due_date, est_time, comp)
            user_add = input("Would you like to add a new entry?: (Yes/No) ")
            if user_add == 'Yes'.casefold():
                continue
            elif user_add == 'No'.casefold():
                view_menu()
                break
            else:
                print("Please Enter a Valid Input!")
                break


def del_entry():
    '''
    Deletes row within database
    '''
    print("Enter the Assignment ID?: ")
    tsk_num = input()
    query = "DELETE FROM Assignments WHERE ID=?"
    planner.execute(query, (int(tsk_num),))
    db.commit()


def done_entry():
    '''
    Marks assignment row completed in 'completed' column = yes
    '''
    tsk_num = input("Enter the completed Assignment ID?: ")
    update_col = str(input("Are you sure you completed this assignment?: (Yes/No) ").upper())
    if update_col == 'YES':
        update_col = 'Completed'
        new_val = 'YES'
    elif update_col == 'NO':
        view_menu()
    else:
        print("Please Enter a Valid Input!")
        return
    planner.execute("UPDATE Assignments SET {0}=? WHERE ID=?".format(update_col), [new_val,(int(tsk_num))])
    db.commit()

def mod_entry():
    '''
    modifies entry at row id entered by user
    '''
    tsk_num = input("Enter Assignment ID to update: ")
    update_col = int(input("What data do you want to update?: (1)Course, (2)Task Name, (3)DueDate, (4)TimeNeeded, (5)Completed "))
    if update_col == 1:
        update_col = 'Course'
        new_val = input("Enter Course Name: ")
    elif update_col == 2:
        update_col = 'TaskName'
        new_val = input("Enter Assignment Name: ")
    elif update_col == 3:
        update_col = 'DueDate'
        new_val = input("Enter Due Date: ")
    elif update_col == 4:
        update_col = 'TimeNeeded'
        new_val = input("Enter Estimated Time To Complete: ")
    elif update_col == 5:
        update_col = 'Completed'
        new_val = input("Is it Completed?: (Yes/No) ").upper()
    else:
        print("Please Enter a Valid Input!")
        return
    planner.execute("UPDATE Assignments SET {0}=? WHERE ID=?".format(update_col), [new_val,(int(tsk_num))])
    db.commit()


def view_menu():
    '''
    Prompts menu for user choice and navigation throughout the program
    '''
    while True:
        print("""\n Menu: 1. Add a new Assignment, 2. Mark an Assignment Complete, 3. Modify an Assignment,
        4. View Current Tasks, 5. Delete an Assignment
        """)
        choice = input("What would you like to do? ")
        if choice == '1':
            add_entry()
        elif choice == '2':
            done_entry()
        elif choice == '3':
            mod_entry()
        elif choice == '4':
            print("\n")
            print(pd.read_sql_query("SELECT * FROM Assignments", db))
            print("\n")
        elif choice == '5':
            del_entry()
        else:
            print("Please Enter a Valid Input!")


# Call functions list and close database after use:
create_table()
view_menu()
planner.close()