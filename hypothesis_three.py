import sqlite3 as lite
import xlrd
from numpy import mean

con = lite.connect('learning.db')
cur = con.cursor()

def create_new_table(fileLoc):
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
    loc = (fileLoc)
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
    cur.execute("SELECT * FROM HYPTHREE WHERE sub_code='CS' AND cat_num = ?",(class_A_cat_num ,))
    class_A_info=cur.fetchall()
    con.commit()

    cur.execute("SELECT * FROM HYPTHREE WHERE sub_code='CS' AND cat_num = ?",(class_B_cat_num ,))
    class_B_info=cur.fetchall()
    con.commit()
    class_A_times = {}
    for i in range(len(class_A_info)):
        key = class_A_info[i][0]
        time = class_A_info[i][1]
        if key in  class_A_times.keys():
            if compare_term_code(time,class_A_times[key]) == -1:
                class_A_times[key] = time
        else:
            class_A_times[key] = time

    AB = []
    BA = []
    same = []
    si = 0
    di = 0
    for i in range(len(class_B_info)):
        grade = grade_points(class_B_info[i][9])
        time = class_B_info[i][1]
        id = class_B_info[i][0]
        if grade == -1:
            continue
        elif id not in class_A_times.keys():
            BA.append(grade)
            di = di +1
        else:
            si = si +1
            group = compare_term_code(class_A_times[id], time)
            if group == 0:
                same.append(grade)
            elif group == -1:
                AB.append(grade)
            else:
                BA.append(grade)

    print(mean(AB))
    print(mean(BA))
    print(mean(same))
def close_table():
    con.close()

def compare_term_code(A,B):
    if A == B:
        return 0
    a = A/10
    b = B/10
    if a < b:
        return -1
    if a > b:
        return 1
    if a == b:
        a = A%10
        b = B%10
        if a == 7:
            return -1
        if a == 4 and b == 1:
            return -1
        else:
            return 1
    return -9

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
    else:
        return -1