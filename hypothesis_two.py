import sqlite3 as lite
import re
from scipy.stats.stats import pearsonr
from corrstats import independent_corr

"""
get user input for which database to use
capstone.sqlite = database that contains the official anonymized data
unittest2.sqlite = database with fake data used for unit testing for hypothesis_two
"""
print("Enter database for hypothesis_two:")
database = input()

#connect to the database
con = lite.connect(database)
cur = con.cursor()


def create_table(class1_number, class1_subject, class2_number, class2_subject):
	"""
	get a table of all students who have taken CS0445 and CS1501
		a.) exclude all grades that are: x, R, N, 0, S, NC, W, G
			- grades are defined by the University of Pittsburgh here: http://www.pitt.edu/~graduate/reggrades.html#defs

		PARAMETERS: 
			- String class1_number: the course number code of the first class you are comparing (i.e. 0445)
			- String class1_subject: the subject of the first class you are comparing (i.e. CS)
			- String class2_number: the course number of the second class you are comparing (i.e. 1501)
			- String class2_subject: the subject of the second class you are comparing (i.e. CS)
		RETURN:
			- String[] bothclasses_output: an array of the students who have taken both class1 and class2
			- format: [(analytics_id, class1.academic_term_code, class1.cat_num, class1.sub_code, class1.grade, class2.academic_term_code, class2.cat_num, class2.sub_code, class2.grade]
	"""
	algorithms_table = """
	CREATE TABLE algorithms AS
		SELECT DISTINCT analytics_id as alg_id, academic_term_code as alg_term, cat_num as alg_num, sub_code as alg_cs, grade as alg_grade
		FROM Classes_taken
		WHERE alg_num = ?
		AND alg_cs = ?
		AND alg_grade IS NOT 'x' 
		AND alg_grade IS NOT 'R' 
		AND alg_grade IS NOT 'N' 
		AND alg_grade IS NOT '0'
		AND alg_grade IS NOT 'S'
		AND alg_grade IS NOT 'NC'
		AND alg_grade IS NOT 'W'
		AND alg_grade IS NOT 'G'
		ORDER BY alg_id
	"""
	cur.execute("DROP TABLE IF EXISTS algorithms")
	cur.execute(algorithms_table, (class2_number, class2_subject))


	grades = """
	CREATE TABLE bothclasses AS 
		SELECT a.analytics_id as data_id, a.academic_term_code as data_term, a.cat_num as data_num, a.sub_code as data_cs, grade as data_grade, b.alg_term, b.alg_num, b.alg_cs, b.alg_grade
		FROM Classes_taken a
		INNER JOIN algorithms b ON b.alg_id = a.analytics_id
		WHERE data_num = ?
		AND data_cs = ?
		AND data_grade IS NOT 'x' 
		AND data_grade IS NOT 'R' 
		AND data_grade IS NOT 'N' 
		AND data_grade IS NOT '0' 
		AND data_grade IS NOT 'S'
		AND data_grade IS NOT 'NC'
		AND data_grade IS NOT 'W'
		AND data_grade IS NOT 'G'
		ORDER BY data_id
	"""

	cur.execute("DROP TABLE IF EXISTS bothclasses")
	cur.execute(grades, (class1_number, class1_subject))


	test = """
	SELECT * FROM bothclasses
	"""

	rows = cur.execute(test)
	test_output = []
	for row in rows:
		test_output.append(row)
	return test_output

def get_semesters_reference_list():
	"""
	function that creates a sorted ascending list of all possible academic term codes 
		- the purpose of this function is to help determine how many semesters in between each class there has been
		- the list is in chronological order which will help to determine how semesters there were between each class by indexing the list
		RETURN:
			- String[] semester_list: list of academic term codes in order of when they occurred
	"""
	century = list(range(1,3))
	year1 = list(range(0,10))
	year2 = list(range(0,10))
	semester = list(range(1,4))
	semester_list = []

	for a in century:
		for b in year1:
			for c in year2:
				for d in semester:
					semester_list.append(int(str(a) + str(b) + str(c) + str(d)))
	return semester_list

def fix_terms(term):
	"""
	function that fixes the last part of the term code into a more easily readable format
		- specifically to make the reference list easier to create and put in chronological
		- instead of having to iterate 1, 4, and 7
		- SPRING (4) is now 1
		- SUMMER(7) is now 2 
		- FALL(1) is now 3
		PARAMETERS: 
			- String term: the term that needs to be fixed
		RETURN:
			- String term: term with last digit fixed to be either 1, 2, or 3
	"""
	fixed_term = 0
	t = list(term)
	if(int(t[3]) == 4):
		fixed_term = int(t[0] + t[1] + t[2] + '1')		# SPRING (4) = 1
	if(int(t[3]) == 7):
		fixed_term = int(t[0] + t[1] + t[2] + '2')		# SUMMER (7) = 2
	if(int(t[3]) == 1):
		fixed_term = int(t[0] + t[1] + t[2] + '3')		# FALL (1) = 3
	return fixed_term

def compare_academic_term(class1_term, class2_term, semester_reference_list):
	"""
	compare academic terms to see if there is a gap in time between two classes
		a.) Official University of Pittsburgh academic term code conventions can be found here:
			https://www.registrar.pitt.edu/assets/pdf/PS%20Term%20Naming%20Convention.pdf
		b.) chronological order by year is SPRING -> SUMMER -> FALL
		
		PARAMETERS: 
			- String class1_term: the term code for the first class
			- String class2_term: the term code for the second class
		RETURN: 
			- int century_gap: the number of years between centuries
			- int year_gap: the number of years between classes
			- int semester_gap: the number of semesters between classes
	"""

	fixed_class1 = fix_terms(class1_term)
	fixed_class2 = fix_terms(class2_term)
	
	class1 = list(str(fixed_class1))	# split the term code up into individual integers
	class2 = list(str(fixed_class2))

	class1_century = int(class1[0])					# the first digit indicates which century the year is in
	class2_century = int(class2[0])

	class1_year = int(class1[1] + class1[2])		# the second and third digit indicate the year
	class2_year = int(class2[1] + class2[2])


	class1_semester = int(class1[3])				# the last digit indicates the semester
	class2_semester = int(class2[3])

	century_gap = class2_century - class1_century	# difference in century
	year_gap = class2_year - class1_year			# difference in year

	fixed_class1 = fix_terms(class1_term)			#fix the semester part of the term to easily find the difference in semesters
	fixed_class2 = fix_terms(class2_term)

	# the classes index in the reference list subtracted from each other equals the number of semesters that have occurred in between
	semester_gap = semester_reference_list.index(fixed_class2) - semester_reference_list.index(fixed_class1) 		

	#print(semester_gap)
	return century_gap, year_gap, semester_gap
		

def get_class_group(gap_size, students_list, semester_reference_list):
	"""
	function that gets a list of students that took (gap_size) semesters between class1 and class2
		- compares academic term codes using function compare_academic_term()
	
	PARAMETERS:
		- int gap_size: the number of semesters between class1 and class2
		- students_list: the list of students that data is taken from
		- semster_reference_list: the reference list that is used to find the distance between class1 and class2
	"""
	student_gap = []
	for student in students_list:
		century_gap,year_gap, semester_gap = compare_academic_term(str(student[1]), str(student[5]), semester_reference_list)
		if semester_gap == gap_size:
			student_gap.append(student)
	return student_gap


def get_grades(students_list):
	"""
	function that updates the grades in the list from letter grades to numerical quality points
		- grading system can be found at this link: https://www.registrar.pitt.edu/sites/default/files/pdf/Grading%20System.pdf
	PARAMETERS
		- list[] students_list: specified list of students from which to pull grades from
	RETURN
		- Int[] class1_grades: list of numerical quality point grades from first class (CS 0445)
		- Int[] class2_grades: list of numerical quality point grades from second class (CS 1501)
	"""
	class1_grades = []
	class2_grades = []
	for student in students_list:
		if student[4] == 'A+':
			class1_grades.append(4.0)
		elif student[4] == 'A':
			class1_grades.append(4.0)
		elif student[4] == 'A-':
			class1_grades.append(3.75)
		elif student[4] == 'B+':
			class1_grades.append(3.25)
		elif student[4] == 'B':
			class1_grades.append(3.00)
		elif student[4] == 'B-':
			class1_grades.append(2.75)
		elif student[4] == 'C+':
			class1_grades.append(2.25)
		elif student[4] == 'C':
			class1_grades.append(2.00)
		elif student[4] == 'C-':
			class1_grades.append(1.75)
		elif student[4] == 'D+':
			class1_grades.append(1.25)
		elif student[4] == 'D':
			class1_grades.append(1.00)
		elif student[4] == 'D-':
			class1_grades.append(0.75)
		elif student[4] == 'F':
			class1_grades.append(0.00)

		if student[8] == 'A+':
			class2_grades.append(4.0)
		elif student[8] == 'A':
			class2_grades.append(4.0)
		elif student[8] == 'A-':
			class2_grades.append(3.75)
		elif student[8] == 'B+':
			class2_grades.append(3.25)
		elif student[8] == 'B':
			class2_grades.append(3.00)
		elif student[8] == 'B-':
			class2_grades.append(2.75)
		elif student[8] == 'C+':
			class2_grades.append(2.25)
		elif student[8] == 'C':
			class2_grades.append(2.00)
		elif student[8] == 'C-':
			class2_grades.append(1.75)
		elif student[8] == 'D+':
			class2_grades.append(1.25)
		elif student[8] == 'D':
			class2_grades.append(1.00)
		elif student[8] == 'D-':
			class2_grades.append(0.75)
		elif student[8] == 'F':
			class2_grades.append(0.00)

	return class1_grades, class2_grades

def get_pearson_coefficient(class1_grades, class2_grades):
	"""
	gets the pearson correlation coeffiient using scipy.pearsonr()
		- class1_grades and class2_grades must be the same size
		- class1_grades and class2_grades must be corresponding values (although they do not have to be in order)
	PARAMETERS:
		- class1_grades: list of grades for class 1 (must be a list of numerical values)
		- class2_grades: list of grades for class2 (must be a list of numerical values)
	RETURN
		- coefficient: the pearson correlation coefficient value between the range of [-1, 1]
		- p_value: the significance of the correlation in the range [0 1]
	"""
	p_tuple = pearsonr(class1_grades, class2_grades)
	coefficient = p_tuple[0]
	p_value = p_tuple[1]
	return coefficient, p_value

def print_results(gap_size, sample_size, pearson_coeff, p_value):
	print("Students that took CS1501 (" + str(gap_size) + ") semester(s) after CS0445:")
	print("--------------------------------------" + "--------------------------------")
	print("                        SAMPLE SIZE:  " + str(sample_size))
	print("    PEARSON CORRELATION COEFFICIENT:  " + str(pearson_coeff))
	print("                            P-VALUE:  " + str(p_value))
	print("--------------------------------------" + "--------------------------------")


############## MAIN ##############
def main():
	student_list = create_table("0445", "CS", "1501", "CS")
	reference_list = get_semesters_reference_list()
	
	# getting the lists of students who took a specified amount of gap semesters 
	gap_one = get_class_group(1, student_list, reference_list)
	gap_three = get_class_group(3, student_list, reference_list)
	gap_four = get_class_group(4, student_list, reference_list)
	gap_five = get_class_group(5, student_list, reference_list)

	# getting the grades of the students who took a specified amount of gap semesters
	gap_one_class1, gap_one_class2 = get_grades(gap_one)
	gap_three_class1, gap_three_class2 = get_grades(gap_three)
	gap_four_class1, gap_four_class2 = get_grades(gap_four)
	gap_five_class1, gap_five_class2 = get_grades(gap_five)

	# getting the pearson correlation coefficients of the specified class groups
	gap_one_coeff, gap_one_p = get_pearson_coefficient(gap_one_class1, gap_one_class2)
	gap_three_coeff, gap_three_p = get_pearson_coefficient(gap_three_class1, gap_three_class2)
	gap_four_coeff, gap_four_p = get_pearson_coefficient(gap_four_class1, gap_four_class2)
	gap_five_coeff, gap_five_p = get_pearson_coefficient(gap_five_class1, gap_five_class2)
	

	z, p = independent_corr(gap_one_coeff, gap_three_coeff, len(gap_one_class1), len(gap_three_class1))
	
	

	print("############################## HYPOTHESIS 2 RESULTS ##############################\n")
	print_results(1, len(gap_one_class1), gap_one_coeff, gap_one_p)
	print()
	print_results(3, len(gap_three_class1), gap_three_coeff, gap_three_p)
	print_results(4, len(gap_four_class1), gap_four_coeff, gap_four_p)
	print_results(5, len(gap_five_class1), gap_five_coeff, gap_five_p)

	print("############################ FISHER Z-TRANSFORMATION #############################\n")
	z, p = independent_corr(gap_one_coeff, gap_three_coeff, len(gap_one_class1), len(gap_three_class1))
	print("fisher z-transformation for (GAP = 1) and (GAP = 3): z = " + str(z) + ", p-val = " + str(p))
	print()

	z, p = independent_corr(gap_one_coeff, gap_four_coeff, len(gap_one_class1), len(gap_four_class1))
	print("fisher z-transformation for (GAP = 1) and (GAP = 4): z =" + str(z) + ", p-val =" + str(p))
	print()

	z, p = independent_corr(gap_one_coeff, gap_five_coeff, len(gap_one_class1), len(gap_five_class1))
	print("fisher z-transformation for (GAP = 1) and (GAP = 5): z =" + str(z) + ", p-val = " + str(p))
	print()




if __name__ == '__main__':
	main()


