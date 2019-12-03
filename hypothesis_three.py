import sqlite3 as lite
import xlrd
from numpy import mean
from scipy import stats
con = lite.connect('capstone.sqlite')
cur = con.cursor()

#call this function when a new table needs to be created. This function works on xlsx files
#enter the xlsx file location and it'll take the Classes_taken file and turn it into the Classess_taken table
def create_new_table(fileLoc):
    done = 0
    cur.execute('DROP TABLE IF EXISTS Classes_taken')
    cur.execute("""CREATE TABLE Classes_taken (analytics_id integer, 
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
            cur.execute("""INSERT INTO Classes_taken (analytics_id, 
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

#enter two courses category number. It will then determine when a student should take class_B in relation to class_A to have a higher chance of producing
#a higher grade
def comparePaths(class_A_cat_num, class_B_cat_num):
    correction = 0.0166667
    alpha = 0.05

    #first find all the student who took the CS class_A_cat_num course and the class_B_cat_num course
    cur.execute("SELECT * FROM Classes_taken WHERE sub_code='CS' AND cat_num = ?",(class_A_cat_num ,))
    class_A_info=cur.fetchall()
    con.commit()

    cur.execute("SELECT * FROM Classes_taken WHERE sub_code='CS' AND cat_num = ?",(class_B_cat_num ,))
    class_B_info=cur.fetchall()
    con.commit()
    class_A_times = {}

    #first loop through the class_A info. There are student who have retaken classes and we want the earliest class they took in relation to class_B
    #by using a dict we can determine if a student has been added to a list and if so we check the current academic_term_code to see if they took the course at an eariler time
    for i in range(len(class_A_info)):
        key = class_A_info[i][0]
        time = class_A_info[i][1]
        if key in class_A_times.keys():
            if compare_term_code(time,class_A_times[key]) == -1:
                class_A_times[key] = time
        else:
            class_A_times[key] = time

    #AB are students who took class B after class A
    #BA are students who took class B before A or have not taken A yet
    #same are for students who took the 2 classes in the same semester
    AB = []
    BA = []
    same = []

    #We loop through the class_B list and add the grade to either AB, BA, or same
    #since the grades are letter grade we class the function grade_points to convert the letter to a floating point grade
    #we also need the student term code and student id
    for i in range(len(class_B_info)):
        grade = grade_points(class_B_info[i][9])
        time = class_B_info[i][1]
        id = class_B_info[i][0]

        #if the grade is a -1 then the student did not receieve a A+ to F grade and may have received a S, W, or I
        #so they are added to none of the lists
        #else if the id for students in class B aren't in class_A_times key then the student never took class A and goes in the BA list
        #else we compare the earliest time they took class A to determine which list the grade should go AB, BA, or same
        if grade == -1:
            continue
        elif id not in class_A_times.keys():
            BA.append(grade)
        else:
            group = compare_term_code(class_A_times[id], time)
            if group == 0:
                same.append(grade)
            elif group == -1:
                AB.append(grade)
            else:
                BA.append(grade)

    #f_oneway preforms an one-way ANOVA tests on the three lists
    results, pvalue = stats.f_oneway(AB, BA, same)

    #if the pvalue recieved greater than the alpha then differences between the means are not statistically significant
    #that means class B grades are no impacted from the order a student takes class A in relation to class B
    if pvalue > alpha:
        print('The order students take these two classes should not effect there overall grade in CS ' + class_B_cat_num + '.')
        return

    #if the groups are found to have a statistically significant difference we use the
    #Bonferroni correction to determine which pair of groups contains the difference
    ABtoBA = False
    ABtosame = False
    BAtosame = False
    BAmean = mean(BA)
    ABmean = mean(AB)
    same_mean = mean(same)

    #we do a 2-way t test on each different path pair to look for the pair that is statistically significant
    r, p = stats.ttest_ind(AB, BA)
    if p < correction:
        ABtoBA = True
    r, p = stats.ttest_ind(AB, same)
    if p < correction:
        ABtosame = True
    r, p = stats.ttest_ind(BA, same)
    if p < correction:
        BAtosame = True
    print('The average grade for students who took CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + ' is ' + str(BAmean))
    print('The average grade for students who took CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + ' is ' + str(ABmean))
    print('The average grade for students who took CS ' + class_B_cat_num + ' and CS ' + class_A_cat_num + ' at the same time is ' + str(same_mean))
    print("")

    #if a path does contain a statistically significant difference we look at the means of the group. The group with the higher means is the path the student should take
    print('By anazlying the data with an ANOVA test and a Post-hoc test that used Bonferroni correction the data shows that the best paths to take CS ' + class_B_cat_num + ' are:')
    if ABtoBA:
        if ABmean > BAmean:
            great = 'after'
            small = 'before'
        else:
            great = 'before'
            small = 'after'
        print('It is better to take CS ' + class_B_cat_num + ' ' + great + ' CS ' + class_A_cat_num + ' instead of taking CS ' + class_B_cat_num + ' ' + small + ' CS ' + class_A_cat_num + '.')

    if BAtosame:
        if BAmean > same_mean:
            print('It is better to take CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + ' instead of taking the two classes in the same semester.')
        else:
            print('It is better to take the two classes in the same semester instead of taking CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + '.')

    if ABtosame:
        if ABmean > same_mean:
            print('It is better to take CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + ' instead of taking the two classes in the same semester.')
        else:
            print('It is better to take the classes in the same semester instead of taking CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + '.')

    if not ABtosame and not BAtosame and not ABtoBA:
        print("Check the math something went wrong")


def close_table():
    con.close()

#if A and B are the same return 0
def compare_term_code(A,B):
    if A == B:
        return 0

    #the first 3 digits of the code give us the year the course was taken
    a = int(A / 10)
    b = int(B / 10)
    if a < b:
        return -1
    if a > b:
        return 1

    #if the year was the same check the season
    #if a is greater than b a was taken in a season before b
    #4 = spring
    #7 = summer
    #1 = fall
    if a == b:
        a = A%10
        b = B%10
        if a == 4:
            return -1
        if a == 7 and b == 1:
            return -1
        else:
            return 1
    return -9

#enter a letter grade and get a floating point number grade
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

comparePaths('447','449')