import sqlite3 as lite
import xlrd
from numpy import mean
import csv
from scipy import stats

database = 'databases/capstone.sqlite'
con = lite.connect(database)
cur = con.cursor()


#enter two courses category number. It will then determine when a student should take class_B in relation to class_A to have a higher chance of producing
#a higher grade
def comparePaths(class_A_cat_num, class_B_cat_num):
    correction = 0.0166667
    alpha = 0.05

    #first find all the student who took the CS class_A_cat_num course and the class_B_cat_num course
    cur.execute("SELECT * FROM Classes_taken WHERE sub_code='CS' AND cat_num = ? AND grading_basis_desc='Letter Grade' ",(class_A_cat_num ,))
    class_A_info=cur.fetchall()
    con.commit()

    cur.execute("SELECT * FROM Classes_taken WHERE sub_code='CS' AND cat_num = ? AND grading_basis_desc='Letter Grade' ",(class_B_cat_num ,))
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
    amount = 0
    for i in range(len(class_B_info)):
        grade = grade_points(class_B_info[i][8])
        time = class_B_info[i][1]
        key = class_B_info[i][0]


        #if the grade is a -1 then the student did not receieve a A+ to F grade and may have received a S, W, or I
        #so they are added to none of the lists
        #else if the id for students in class B aren't in class_A_times key then the student never took class A and goes in the BA list
        #else we compare the earliest time they took class A to determine which list the grade should go AB, BA, or same
        if grade == -1:
            continue
        elif key not in class_A_times.keys():
            BA.append(grade)
        else:
            group = compare_term_code(class_A_times[key], time)
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
    BAmean = mean(BA)
    ABmean = mean(AB)
    same_mean = mean(same)
    print("############################## HYPOTHESIS 3 RESULTS ##############################\n")
    print('The average grade for students who took CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + ' is ' + str(BAmean))
    print('The average grade for students who took CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + ' is ' + str(ABmean))
    print('The average grade for students who took CS ' + class_B_cat_num + ' and CS ' + class_A_cat_num + ' at the same time is ' + str(same_mean))
    print("The p value from the ANOVA test is "+str(pvalue))
    print("")
    if pvalue > alpha:
        print('According to the ANOVA test when the p value was compared to an alpha of 0.05 the order students take these two classes should not effect there overall grade in CS ' + class_B_cat_num + '.')
        return

    #if the groups are found to have a statistically significant difference we use the
    #Bonferroni correction to determine which pair of groups contains the difference
    ABtoBA = False
    ABtosame = False
    BAtosame = False

    #we do a 2-way t test on each different path pair to look for the pair that is statistically significant
    r, p = stats.ttest_ind(AB, BA)
    if p <= correction:
        ABtoBAp = p
        ABtoBA = True
    r, p = stats.ttest_ind(AB, same)
    if p <= correction:
        ABtosamep = p
        ABtosame = True
    r, p = stats.ttest_ind(BA, same)
    if p <= correction:
        BAtosamep = p
        BAtosame = True


    #if a path does contain a statistically significant difference we look at the means of the group. The group with the higher means is the path the student should take
    print('By anazlying the data with an ANOVA test and a Post-hoc test that used Bonferroni correction the data shows that the best paths to take CS ' + class_B_cat_num + ' are:')
    print("")
    if ABtoBA:
        if ABmean > BAmean:
            great = 'after'
            small = 'before'
        else:
            great = 'before'
            small = 'after'
        print('It is better to take CS ' + class_B_cat_num + ' ' + great + ' CS ' + class_A_cat_num + ' instead of taking CS ' + class_B_cat_num + ' ' + small + ' CS ' + class_A_cat_num + '.')
        print('Its t-test p-value = '+str(ABtoBAp))
        print("")

    if BAtosame:
        if BAmean > same_mean:
            print('It is better to take CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + ' instead of taking the two classes in the same semester.')
        else:
            print('It is better to take the two classes in the same semester instead of taking CS ' + class_B_cat_num + ' before CS ' + class_A_cat_num + '.')
            print('Its t-test p-value = ' + str(BAtosamep))
            print("")

    if ABtosame:
        if ABmean > same_mean:
            print('It is better to take CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + ' instead of taking the two classes in the same semester.')
        else:
            print('It is better to take the classes in the same semester instead of taking CS ' + class_B_cat_num + ' after CS ' + class_A_cat_num + '.')
            print('Its t-test p-value =' + str(ABtosamep))
            print("")

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
def main():
    comparePaths('447','449')
    input('Press ENTER to exit')
if __name__ == '__main__':
	main()
