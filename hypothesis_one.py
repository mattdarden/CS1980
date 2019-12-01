import sqlite3 as lite
import re
import numpy
from scipy.stats.stats import pearsonr

"""
get user input for which database to use
capstone.sqlite = database that contains the official anonymized data
unittest.sqlite = database with fake data used for unit testing
"""
print("Enter database: ")
database = input()


# connect to the database
con = lite.connect(database)
cur = con.cursor()

"""
1.) create a table to get all grades for students who took CS0401 and CS0445
	a.) need to create a unique dataset that only takes a letter grade
	b.) select the analytics ID, category number, subject code, and grades from each class
	c.) join the CS0401 and CS0445 tables based on analytics_id 
	d.) filter out students that did not take CS0401 AND CS0445, and students that received a grade 'x' or 'N' or 'R' or 'S' or '0'
		(x = redacted, N = noncredit, R = resignation, S = satisfactory, 0 = unknown)
"""
def create_table(class1_number, class1_subject, class2_number, class2_subject):
	# creating a table of students who took CS0445, filtering out students with distinct letter grades
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


"""
2.) update the table to reformat the letter grades into a numerical format
	a.) update the grades using the UPDATE, SET, and CASE functions
	b.) the corresponding numerical quality points number is based on an official grading system published by the University of Pittsburgh
		* grading system can be found at this link: https://www.registrar.pitt.edu/sites/default/files/pdf/Grading%20System.pdf
"""
def update_table():
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

	java_grades = """
	SELECT java_grade
	FROM bothclasses
	"""	
	rows = cur.execute(java_grades)

	java_grades_list = []
	for row in rows:
		for r in row:
			java_grades_list.append(float(r))

	data_grades = """
	SELECT datastructures_grade
	FROM bothclasses
	"""

	data_grades_list = []
	rows = cur.execute(data_grades)
	for row in rows:
		for r in row:
			data_grades_list.append(float(r))

	return java_grades_list, data_grades_list

"""
4.) calculate the average and standard deviation of the grades_list from CS0401 
	a.) using python library numPy
	b.) also calculating half a standard deviation below the mean in order to create a list
		of students who achieved a grade lower than that
"""
def calculate_mean(grades_list):
	return(numpy.mean(grades_list))

def calculate_half_std(grades_list):
	standard_deviation = numpy.std(grades_list)
	average = calculate_mean(grades_list)
	half_std_below = average - (standard_deviation/2)
	print(type(half_std_below))
	return half_std_below


def update_table_below_avg(half_std_below):
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

	below_avg_java = """
	SELECT java_grade
	FROM bothclasses
	WHERE java_grade < ?
	"""

	below_avg_java_grades = []
	rows = cur.execute(below_avg_java, (half_std_below.astype(float),))
	for row in rows:
		for r in row:
			below_avg_java_grades.append(float(r))

	below_avg_datastructures = """
	SELECT datastructures_grade
	FROM bothclasses
	WHERE java_grade < ?
	"""
	below_avg_datastructures_grades = []
	rows = cur.execute(below_avg_datastructures, (half_std_below.astype(float),))
	for row in rows:
		for r in row:
			below_avg_datastructures_grades.append(float(r))

	return below_avg_java_grades, below_avg_datastructures_grades

"""
6.) Find the pearson correlation coefficient for all CS0401 and corresponding CS0445 grades
	a.) query for all CS0401 grades and put them into an array
	b.) query for all corresponding CS0445 grades and put them into an arry
	c.) use the SciPy.stats.pearsonr() function to find the pearson correllation coefficient
	d.) output is: (pearson correlation coefficient, significance)
"""
def pearson_coefficient(java_grades_list, data_grades_list):	
	return pearsonr(java_grades_list, data_grades_list)


################### MAIN ##########################
def main():
	create_table("0401", "CS", "0445", "CS")
	java_grades_list, data_grades_list = update_table()
	pearson_all = pearson_coefficient(java_grades_list, data_grades_list)
	half_std_below = calculate_half_std(java_grades_list)

	create_table("0401", "CS", "0445", "CS")
	java_grades_list, data_grades_list = update_table_below_avg(half_std_below)
	pearson_below_grades = pearson_coefficient(java_grades_list, data_grades_list)

	print(pearson_below_grades)
	print(pearson_all)

if __name__ == '__main__':
	main()


