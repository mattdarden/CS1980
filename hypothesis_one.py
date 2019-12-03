import sqlite3 as lite
import re
import numpy
from scipy.stats.stats import pearsonr

"""
get user input for which database to use
capstone.sqlite = database that contains the official anonymized data
unittest1.sqlite = database with fake data used for unit testing for hypothesis_one
"""
print("Enter database for hypothesis_one: ")
database = input()


# connect to the database
con = lite.connect(database)
cur = con.cursor()

def create_table(class1_number, class1_subject, class2_number, class2_subject):
	"""
	creates a table that gets all students who took CS0401 and CS0445
		- CS0401 grades are unique, but CS0445 grades are not
		- clean data of students that received a grade 'x', 'N', 'R', 'S', '0', 'W', 'G', or 'NC'
		
	PARAMETERS:
		- String class1_number:	cat_num of the first class (i.e. '0401')
		- String class1_subject: sub_code of the first class (i.e. 'CS')
		- String class2_number:	cat_num of the second class (i.e. '0445')
		- String class2_subject: sub_code of the second class (i.e. 'CS')
	RETURNS:
		- list[] test_output: a list of students that took CS0401 and CS0445
			- format: (analytics_id, class1_number, class1_subject, class1_grade, class2_number, class2_subject, class2_grade)
	"""
	ds = """
	CREATE TABLE ds AS 
		SELECT DISTINCT analytics_id as ds_id, cat_num as datastructures, sub_code as datastructures_cs, grade AS datastructures_grade
		FROM Classes_taken
		WHERE datastructures = ?
		AND datastructures_cs = ?
		AND datastructures_grade IS NOT 'x' 
		AND datastructures_grade IS NOT 'R' 
		AND datastructures_grade IS NOT 'N' 
		AND datastructures_grade IS NOT '0'
		AND datastructures_grade IS NOT 'S'
		AND datastructures_grade IS NOT 'NC'
		AND datastructures_grade IS NOT 'W'
		AND datastructures_grade IS NOT 'G'
		ORDER BY analytics_id
	"""
	cur.execute('DROP TABLE IF EXISTS ds')
	cur.execute(ds, (class2_number, class2_subject))


	grades = """
	CREATE TABLE bothclasses AS
		SELECT a.analytics_id, a.cat_num AS java, a.sub_code AS java_cs, a.grade AS java_grade, b.datastructures, b.datastructures_cs, b.datastructures_grade
		FROM Classes_taken a
		INNER JOIN ds b on b.ds_id = a.analytics_id
		WHERE java = ? 
		AND java_cs = ? 
		AND a.grade IS NOT 'x' 
		AND a.grade IS NOT 'R' 
		AND a.grade IS NOT 'N' 
		AND a.grade IS NOT '0' 
		AND a.grade IS NOT 'S'
		AND a.grade IS NOT 'NC'
		AND a.grade IS NOT 'W'
		AND a.grade IS NOT 'G'
		
	"""
	cur.execute('DROP TABLE IF EXISTS bothclasses')
	cur.execute(grades, (class1_number, class1_subject))

	test = """
	SELECT * FROM bothclasses
	"""
	rows = cur.execute(test)
	test_output = []
	for row in rows:
		test_output.append(row)
	return test_output

def update_table():
	"""
	update the table of students who took class1 and class2 so that the letter grades are represented as numerical quality points
		- the corresponding numerical quality points number is based on an official grading system published by the University of Pittsburgh
		  grading system can be found at this link: https://www.registrar.pitt.edu/sites/default/files/pdf/Grading%20System.pdf
	
	RETURNS:
		- updated_list: updated list of students with numerical grades instead of letter grades
	"""
	update_java = """
	UPDATE bothclasses SET java_grade = CASE
		WHEN java_grade = 'A+' THEN 4.0
		WHEN java_grade = 'A' THEN 4.0
		WHEN java_grade = 'A-' THEN 3.75
		WHEN java_grade = 'B+' THEN 3.25
		WHEN java_grade = 'B' THEN 3.0
		WHEN java_grade = 'B-' THEN 2.75
		WHEN java_grade = 'C+' THEN 2.25
		WHEN java_grade = 'C' THEN 2.0
		WHEN java_grade = 'C-' THEN 1.75
		WHEN java_grade = 'D+' THEN 1.25
		WHEN java_grade = 'D' THEN 1.0
		WHEN java_grade = 'D-' THEN 0.75
		WHEN java_grade = 'F' THEN 0.0
	END
	"""
	cur.execute(update_java)

	update_datastructures = """
	UPDATE bothclasses SET datastructures_grade = CASE
		WHEN datastructures_grade = 'A+' THEN 4.0
		WHEN datastructures_grade = 'A' THEN 4.0
		WHEN datastructures_grade = 'A-' THEN 3.75
		WHEN datastructures_grade = 'B+' THEN 3.25
		WHEN datastructures_grade = 'B' THEN 3.0
		WHEN datastructures_grade = 'B-' THEN 2.75
		WHEN datastructures_grade = 'C+' THEN 2.25
		WHEN datastructures_grade = 'C' THEN 2.0
		WHEN datastructures_grade = 'C-' THEN 1.75
		WHEN datastructures_grade = 'D+' THEN 1.25
		WHEN datastructures_grade = 'D' THEN 1.0
		WHEN datastructures_grade = 'D-' THEN 0.75
		WHEN datastructures_grade = 'F' THEN 0.0
		WHEN datastructures_grade = 'G' THEN 0.0
		WHEN datastructures_grade = 'W' THEN 0.0
	END
	"""
	cur.execute(update_datastructures)

	updated_grades = """
	SELECT * FROM bothclasses
	"""
	updated_list = []
	rows = cur.execute(updated_grades)
	for row in rows:
		updated_list.append(row)
	return updated_list

def get_grades(students_list):
	"""
	get the grades for class1 and class2 from the list of the students who took both class1 and class2

	PARAMETERS:
		- list[] students_list: list of students who took both class1 and class2

	RETURNS:
		- list[] class1_grades: a list of grades from class1 (returned as float)
		- list[] class2_grades: a list of grades from class2 (returned as float)
	"""
	class1_grades = []
	class2_grades = []
	for student in students_list:
		class1_grades.append(float(student[3]))
		class2_grades.append(float(student[6]))
	return class1_grades, class2_grades

def calculate_half_std(grades_list):
	"""
	calculate 1/2 of the standard deviation 
	
	PARAMETERS:
		- list[] grades_list: list of grades from the class we are finding the std dev for (must be a numerical value)
	
	RETURNS:
		- float half_std: half of the standard deviation from the specified class
	"""
	standard_deviation = numpy.std(grades_list)
	half_std = float(standard_deviation)/2.0
	return float(half_std)

def get_below_avg_grades(students_list, half_std_below):
	below_avg = []
	for student in students_list:
		if float(student[3]) < half_std_below:
			below_avg.append(student)
	return below_avg

def get_above_avg_grades(students_list, half_std_above):
	above_avg = []
	for student in students_list:
		if float(student[3]) > half_std_above:
			above_avg.append(student)
	return above_avg	


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
	coeff = p_tuple[0]
	p_value = p_tuple[1]
	return float(coeff), float(p_value)

def print_results(category, sample_size, pearson_coeff, p_value):
	print(category.upper() + " GRADES:")
	print("--------------------------------------" + "--------------------------------")
	print("                        SAMPLE SIZE:  " + str(sample_size))
	print("    PEARSON CORRELATION COEFFICIENT:  " + str(pearson_coeff))
	print("                            P-VALUE:  " + str(p_value))
	print("--------------------------------------" + "--------------------------------")

################### MAIN ##########################
def main():
	create_table("0401", "CS", "0445", "CS")							# create table of students who took class1 (CS0401) and class2 (CS0445)
	students_list = update_table()										# update table so that letter grades are now represented by numerical quality points
	all_class1_grades, all_class2_grades = get_grades(students_list)	# get the list of grades from the updated students list
	average = float(numpy.mean(all_class1_grades))						# calculate the mean of class1 grades
	half_std = calculate_half_std(all_class1_grades)					# calculate half of the standard deviation
	half_std_below = average - half_std 								# calculate half standard deviation below the mean of class1 grades
	half_std_above = average + half_std 								# calculate half standard deviation above the mean of class1 grades
	
	# getting results for below average grades
	below_avg = get_below_avg_grades(students_list, half_std_below)						# get a list of students who did below avg
	below_class1, below_class2 = get_grades(below_avg)									# get class1 grades of students who did below avg
	below_coeff, below_p_value = get_pearson_coefficient(below_class1, below_class2)	# get the pearson correlation coefficient and p-value from students who did below avg

	#getting results for all grades
	all_coeff, all_p_value = get_pearson_coefficient(all_class1_grades, all_class2_grades)	# get the pearson correlation coefficient and p-value from all student grades 

	# getting resulst for above average grades
	above_avg = get_above_avg_grades(students_list, half_std_above)
	above_class1, above_class2 = get_grades(above_avg)
	above_coeff, above_p_value = get_pearson_coefficient(above_class1, above_class2)

	print("############################## HYPOTHESIS 1 RESULTS ##############################\n")
	print_results("below average", len(below_class1), below_coeff, below_p_value)
	print_results("all", len(all_class1_grades), all_coeff, all_p_value)
	print_results("above average", len(above_class1), above_coeff, above_p_value) 

if __name__ == '__main__':
	main()


