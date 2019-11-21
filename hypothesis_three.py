import sqlite3 as lite
import xlrd
import csv
import re
import numpy
from datetime import date

con = lite.connect('learning.db')
cur = con.cursor()
def create_new_table():
    done = 0
    cur.execute('DROP TABLE IF EXISTS HYPTHREE')
    cur.execute("""CREATE TABLE HYPTHREE (analytics_id integer, 
                                academic_term_code integer,
                                term_desc integer,
                                cat_num integer,
                                sub_code text,
                                sub_desc text,
                                class_num integer,
                                class_sec_num integer,
                                title text,
                                grade text,
                                grade_desc text,
                                grading_basis text,
                                grading_basis_desc text)""")
    con.commit()
    loc = ('C:/Users/rdere/Desktop/anonymized data/Classes Taken.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    for i in range(1, rows):
        row = sheet.row_values(i)
        if row[9] != 'x' and row[9] != '0' and row[9] != '' and row[12] == 'Letter Grade':
            cur.execute("""INSERT INTO HYPTHREE (analytics_id, 
                                academic_term_code,
                                term_desc,
                                cat_num,
                                sub_code,
                                sub_desc,
                                class_num,
                                class_sec_num,
                                title,
                                grade,
                                grade_desc,
                                grading_basis,
                                grading_basis_desc) VALUES (:analytics_id, 
                                :academic_term_code,
                                :term_desc,
                                :cat_num,
                                :sub_code,
                                :sub_desc,
                                :class_num,
                                :class_sec_num,
                                :title,
                                :grade,
                                :grade_desc,
                                :grading_basis,
                                :grading_basis_desc)""",
                        {'analytics_id': row[0], 'academic_term_code': row[1], 'term_desc': row[2], 'cat_num': row[3],
                         'sub_code': row[4], 'sub_desc': row[5], 'class_num': row[6], 'class_sec_num': row[7],
                         'title': row[8], 'grade': row[9], 'grade_desc': row[10], 'grading_basis': row[11],
                         'grading_basis_desc': row[12]})
            con.commit()
        if i < 10:
            print(row)
        if i % 1000 == 0:
            print(done)
            done = done + 1000


def comparePaths(class_A_cat_num, class_B_cat_num):
    cur.execute("SELECT * FROM HYPTHREE WHERE cat_num = ?",(class_A_cat_num ,))
    class_A_info=cur.fetchall()
    con.commit()
    cur.execute("SELECT * FROM HYPTHREE")
    class_all_info = cur.fetchall()
    con.commit()
    cur.execute("SELECT * FROM HYPTHREE WHERE cat_num = ?",(class_B_cat_num ,))
    class_B_info=cur.fetchall()
    con.commit()
    print(len(class_B_info))
    print(len(class_all_info))
    for i in range(20):
        print(class_B_info[i][0])

def close_table():
    con.close()

def grade_points(letter):
    if letter == 'A+' or letter == 'A':
        return 4.0
    if letter == 'A-':
        return 3.75
    if letter == 'B+':
        return 3.25
    if letter == 'B':
        return 3.0
    if letter == 'B-':
        return 2.75
    if letter == 'C+':
        return 2.25
    if letter == 'C':
        return 2.0
    if letter == 'C-':
        return 1.75
    if letter == 'D+':
        return 1.25
    if letter == 'D':
        return 1.0
    if letter == 'D-':
        return 0.75
    if letter == 'F':
        return 0
    return -1