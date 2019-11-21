import sqlite3 as lite
import xlrd
import csv
import re
import numpy
from datetime import date

con = lite.connect('learning.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS HYPTHREE')
cur.execute("""CREATE TABLE HYPTHREE (analytics_id integer, 
                    academic_term_code integer,
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
loc = ('C:/Users/rdere/Desktop/anonymized data/small_test.xlsx')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
cols = sheet.ncols
for i in range(1,rows):
    row = sheet.row_values(i)
    if row[8] != 'x' or row[8] != '0':
        cur.execute("""INSERT INTO HYPTHREE (analytics_id, 
                    academic_term_code,
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
                    :cat_num,
                    :sub_code,
                    :sub_desc,
                    :class_num,
                    :class_sec_num,
                    :title,
                    :grade,
                    :grade_desc,
                    :grading_basis,
                    :grading_basis_desc)""", {'analytics_id':row[0], 'academic_term_code':row[1], 'cat_num':row[2], 'sub_code':row[3], 'sub_desc':row[4], 'class_num':row[5], 'class_sec_num':row[6], 'title':row[7], 'grade':row[8], 'grade_desc':row[9], 'grading_basis':row[10], 'grading_basis_desc':row[11]})

con.close()
