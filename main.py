import threading
import sys
from time import ctime
import simple_term_menu
import sqlite3
from colorama import Fore
from time import sleep
import tabulate
import os
from time import time
class TaskManager:
    def __init__(self):
        self.database_connector()
    def database_connector(self):
        self.database = sqlite3.connect('.database.db')
        self.cursor = self.database.cursor()
    def chronometer_reader(self):
        fetch = self.cursor.execute('''
                SELECT * FROM chronometer  ;
            ''')
        fetch = fetch.fetchall()
        return fetch
    def daemon_runner(self):
        self.break_flag = input()
        self.break_flag = True
    def chronometer(self):
        self.task_name = input("[*] Enter the task name for the chronometer to start with : ")
        input(Fore.LIGHTYELLOW_EX+"[*] Hit enter to start to chronometer !")
        self.start_time = time()
        self.start_date = ctime()
        self.counter = 0
        self.break_flag = False
        threading.Thread(target=self.daemon_runner).start()
        while not self.break_flag:
            self.hour = self.counter //3600
            self.minute = self.counter // 60 - (self.hour * 3600 )
            self.second = self.counter - ((self.minute * 60) + (self.hour * 3600))
            # print(self.second)
            print(Fore.LIGHTWHITE_EX+f"[*] time pass : {self.hour}:{self.minute}:{self.second}\t press CRTL+c to stop ... ", end='\r\r')
            self.counter += 1
            sleep(1)

        if self.break_flag:
            self.end_time = time()
            t_time = self.end_time - self.start_time
            t_hour = t_time // 3600
            t_minute = t_time // 60 - (t_hour * 3600)
            t_second = t_time - ((t_minute * 60 )+(t_hour * 3600 ))
            self.end_date = ctime()
            self.t_date = f"start at : {self.start_date} || end at : {self.end_date}"
            print(Fore.LIGHTWHITE_EX+f"[+] Total time taken :  {self.hour}:{self.minute}:{self.second}\n[+] Program total time taken : {t_hour}:{t_minute}:{t_second}")
            self.database_commander('''
                INSERT INTO chronometer ("task_name","start_time","end_time","date","time_spend") VALUES ("{}", {}, {}, "{}", {})
            '''.format(self.task_name,int(self.start_time), int(self.end_time), self.t_date, int(self.end_time - self.start_time)))
            out = self.chronometer_reader()
            for i in range(len(out)):
                out[i] = list(out[i])
            headers = ["ID", "Task Name ", "Start Time", "End Time", "Date", "Time Spend"]
            print(tabulate.tabulate(out, headers, tablefmt="fancy_grid"))
            input("[*] Hit enter to go back to the menu ....")
            self.menu()

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS `tasks` (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "task_name"	TEXT NOT NULL UNIQUE,
                    "task_time_unit"	INTEGER NOT NULL DEFAULT 1,
                    "date"	DATE NOT NULL,
                    "time_spend"	INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS `chronometer` (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "task_name"     TEXT NOT NULL ,
                    "start_time"	INTEGER NOT NULL UNIQUE,
                    "end_time"	INTEGER NOT NULL DEFAULT 1,
                    "date"	DATE NOT NULL,
                    "time_spend"	INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            ''')
            self.cursor.connection.commit()
            print(Fore.LIGHTGREEN_EX+"[+] Database has been created successfully , going back to the menu in 4 seconds .....")
            sleep(4)
            self.menu()
        except:
            print(Fore.LIGHTRED_EX+"[X] Failed creating the database's tables , going back to the menu in 4 seconds ....")
            sleep(4)
            self.menu()
    def database_commander(self, command):
        self.cursor.execute(command)
        self.cursor.connection.commit()
    def database_reader(self):
        fetch = self.cursor.execute('''
                SELECT * FROM tasks ;
            ''')
        fetch = fetch.fetchall()
        return fetch
    def timer(self, time):
        for i in range(time):
            sleep(1)
            min = i//60
            sec = i - (min * 60)
            Max_min = time // 60
            Max_sec = time - (Max_min * 60)
            print(Fore.LIGHTYELLOW_EX+"\r{}:{}/{}:{}".format(Max_min, Max_sec, min, sec), end='\r\r')
    def menu(self):
        os.system("clear")
        self.headers = ["ID", "Task Name", "Task Unit Time", "Date", "Time Spend"]
        self.options = ['0: create database ', '1: insert new task', '2: read database', '3: update a task', '4: delete a task', '5: start a timer for a task', '6: chronometer', '7: exit']
        self.terminal_menu = simple_term_menu.TerminalMenu(self.options)
        self.selected_index = self.terminal_menu.show()
        # if self.selected_index == 3
        if self.selected_index == 0:
            print(Fore.LIGHTYELLOW_EX+"[*] Creating the database , please wait a little ....")
            self.create_table()
            self.menu()
        if self.selected_index == 1:
            task_name = input(Fore.LIGHTYELLOW_EX+"[*] Enter the task name : ")
            task_time_unit = int(input(Fore.LIGHTYELLOW_EX+"[*] Enter the task unit time (int): "))
            date = ctime()
            time_spend = 0
            self.database_commander(
                '''
                    INSERT INTO `tasks` 
                        (
                            "task_name",
                            "task_time_unit",
                            "date",
                            "time_spend"
                        ) 
                        VALUES 
                        (
                            "{}",
                             {}, 
                             "{}", 
                             {}
                         );
                '''.format(task_name, task_time_unit, date, time_spend))
            self.menu()
        if self.selected_index == 2:
            out = self.database_reader()
            for i in range(len(out)) :
                out[i] = list(out[i])
            print(tabulate.tabulate(out, self.headers, tablefmt="fancy_grid"))
            input(Fore.LIGHTYELLOW_EX+"[*] Hit enter to go back to the menu ....")
            self.menu()
        if self.selected_index == 3:
            out = self.database_reader()
            for i in range(len(out)):
                out[i] = list(out[i])
            print(tabulate.tabulate(out, self.headers, tablefmt="fancy_grid"))
            ID = int(input("[*] Select ID : "))
            try:
                for i in range(len(out)):
                    out[i] = list(out[i])
                    if ID == out[i][0]:
                        os.system("clear")
                        new_time_spend = int(input(Fore.LIGHTGREEN_EX+"[+] Requested ID where found :\nenter the new time spend (int): "))
                        self.database_commander("UPDATE tasks SET time_spend = {} WHERE id is {};".format(new_time_spend, ID))
                        break
            except:
                print(Fore.LIGHTRED_EX+"[X] Selected ID not found !")
            self.menu()
        if self.selected_index == 4:
            out = self.database_reader()
            for i in range(len(out)):
                out[i] = list(out[i])
            print(tabulate.tabulate(out, self.headers, tablefmt="fancy_grid"))
            ID = int(input("[*] Select ID : "))
            try:
                for i in range(len(out)):
                    out[i] = list(out[i])
                    if ID == out[i][0]:
                        os.system("clear")
                        new_time_spend = input(Fore.LIGHTGREEN_EX+"[+] Requested ID where found :\nare you sure about deleting this row (y/n): ")
                        if 'y' in new_time_spend.lower():
                            self.database_commander("DELETE FROM tasks WHERE id is {}".format(ID))
                        else:
                            pass
                        break
            except:
                print(Fore.LIGHTRED_EX+"[X] Selected ID not found !")
            self.menu()
        if self.selected_index == 5:
            out = self.database_reader()
            for i in range(len(out)):
                out[i] = list(out[i])
            print(tabulate.tabulate(out, self.headers, tablefmt="fancy_grid"))
            ID = int(input("[*] Select ID : "))
            try:
                for i in range(len(out)):
                    out[i] = list(out[i])
                    if ID == out[i][0]:
                        os.system("clear")
                        new_time_spend = input(Fore.LIGHTGREEN_EX + "[+] Requested ID where found :\nfor starting the timer for ({} minutes) hit enter ! ".format(out[i][2]))
                        self.timer(out[i][2])
                        new_spend_time = out[i][4] + out[i][2]
                        self.database_commander("UPDATE tasks SET time_spend = {} WHERE id IS {}".format(new_spend_time, ID))
                        break
            except:
                print(Fore.LIGHTRED_EX + "[X] Selected ID not found !")
            self.menu()
        if self.selected_index == 6:
            self.chronometer()
        if self.selected_index == 7:
            sys.exit(1)
    def run(self):
        pass
t = TaskManager()
t.menu()