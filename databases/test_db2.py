import sqlite3 as lite
import csv
import re

# create a local database using sqlite3
con = lite.connect('databases/unittest2.sqlite')

with con:
	cur = con.cursor()

	######################### CREATE TABLES #########################
	""" The following section of code is used to create tables within the database labeled 'capstone.sqlite'
	
	Each table corresponds with an xlsx document provided by Dr. Mosse:
	* Classes_taken: Classes Taken.xlsx
	* Demographics: Demographics 1i.xlsx
	* Finances: FAFSA, income, housing (1.e,1.l, 2.n).xlsx
	* Major: Major, school acceptances, 1j, 1k .xlsx
	* Academics: PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).xlsx

	The following documents were provided, but not used, because it wasn't pertinent to our project:
	* High School GPA, SAT, ACT, AP.xlsx
	* CS 0445 CS 1502 class info.xlsx
	* Courses Info.xlsx
	"""
	cur.execute('DROP TABLE IF EXISTS Classes_taken')
	cur.execute("CREATE TABLE Classes_taken(analytics_id VARCHAR(45), academic_term_code INT, cat_num INT, sub_code VARCHAR(10), sub_desc VARCHAR(30), class_num INT, class_sec_num INT, title VARCHAR(50), grade VARCHAR(2), grade_desc VARCHAR(20), grading_basis VARCHAR(20), grading_basis_desc VARCHAR(40), PRIMARY KEY(analytics_id, academic_term_code, class_num, class_sec_num))")

	cur.execute('DROP TABLE IF EXISTS Demographics')
	cur.execute("CREATE TABLE Demographics(analytics_id VARCHAR(45), max_age INT, ethinic_group_code CHAR(5), ethnic_group_desc VARCHAR(30), gender VARCHAR(10), citizen_status VARCHAR(20), first_gen_desc VARCHAR(45), in_out_state CHAR(2), home_state VARCHAR(2), citizen_country VARCHAR(3), PRIMARY KEY(analytics_id))")

	cur.execute('DROP TABLE IF EXISTS Finances')
	cur.execute("CREATE TABLE Finances(analytics_id VARCHAR(45), aid_year INT, fafsa_flag CHAR(1), income_lvl_desc VARCHAR(50), house_desc VARCHAR(30), PRIMARY KEY(analytics_id, aid_year))")
	
	cur.execute('DROP TABLE IF EXISTS Major')
	cur.execute("CREATE TABLE Major(analytics_id VARCHAR(45), app_num INT, admit_term_code INT, admit_plan_desc VARCHAR(40), acdm_plan_type_desc VARCHAR(10), acdm_sub_plan_type VARCHAR(10), career_lvl VARCHAR(30), acdm_group_code varchar(20), acdm_grp_desc VARCHAR(50), acdm_prgm_code VARCHAR(10), acdm_prgm_desc VARCHAR(5), app_cnt_code VARCHAR(10), app_cnt_desc VARCHAR(50), admit_type_code VARCHAR(4), admit_type_desc VARCHAR(50), prgm_action_code VARCHAR(5), prgm_action_desc VARCHAR(25), house_intst_desc VARCHAR(40), res_code VARCHAR(3), res_desc VARCHAR(15), PRIMARY KEY(app_num, admit_plan_desc, acdm_sub_plan_type))")

	# Academics table (PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).xlsx)
	cur.execute('DROP TABLE IF EXISTS Academics')
	cur.execute("CREATE TABLE Academics(analytics_id VARCHAR(45), acdm_term_code INT, pell_elg_flag INT, curr_gpa REAL, acdm_std_act_code VARCHAR(4), acdm_std_act_desc VARCHAR(40), degree_chkt_status_code VARCHAR(3), degree_chkt_status_desc VARCHAR(30), acdm_career_code VARCHAR(4), PRIMARY KEY(analytics_id, acdm_term_code) )")

	######################### END #########################

	######################### READ DATA FROM FILES #########################
	""" The data files were formatted as .xlsx files so we reformatted them to .csv files to code the read easily
	.xlsx files with multiple pages were reformatted to multiple .csv files
	
	the following tables correspond with these .csv filepaths:
	* Classes_taken: anonymized_data/csv/Classes Taken1.csv', anonymized_data/csv/Classes Taken2.csv, anonymized_data/csv/Classes Taken3.csv
	* Demographics: anonymized_data/csv/Demographics 1i.csv
	* Finances: anonymized_data/csv/FAFSA, income, housing (1.e,1.l, 2.n).csv
	* Major: anonymized_data/csv/Major, school acceptances 1j, 1k .csv'
	* Academics: anonymized_data/csv/PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).csv
	"""
	classestaken = []
	with open('testdata/h2/Classes Taken.csv', mode = 'r', encoding='utf-8-sig') as classes1csv:
		reader = csv.reader(classes1csv)
		for row in reader:
			classestaken.append(row)

	demographics = []
	with open('testdata/h2/Demographics 1i.csv', mode = 'r', encoding='utf-8-sig') as demographicscsv:
		reader = csv.reader(demographicscsv)
		for row in reader:
			demographics.append(row)

	finance = []
	with open('testdata/h2/FAFSA, income, housing (1.e, 1.l, 2.n).csv', mode = 'r', encoding='utf-8-sig') as financecsv:
		reader = csv.reader(financecsv)
		for row in reader:
			finance.append(row)

	major = []
	with open('testdata/h2/Major, school acceptances 1j, 1k .csv', mode = 'r', encoding='utf-8-sig') as majorcsv:
		reader = csv.reader(majorcsv)
		for row in reader:
			major.append(row)

	academics = []
	with open('testdata/h2/PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).csv', mode = 'r', encoding='utf-8-sig') as academicscsv:
		reader = csv.reader(academicscsv)
		for row in reader:
			academics.append(row)

	######################### END #########################

	######################### INSERT DATA INTO DATABASE #########################
	
	for classes in classestaken:
		for text in classes:
			text.replace("'", "''")
		temp1 = [(classes[0], classes[1], classes[2], classes[3], classes[4], classes[5], classes[6], classes[7], classes[8], classes[9], classes[10], classes[11])]
		cur.executemany("INSERT INTO Classes_taken VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", temp1)

	for dems in demographics:
		for text in dems:
			text.replace("'", "''")
		temp2 = [(dems[0], dems[1], dems[2], dems[3], dems[4], dems[5], dems[6], dems[7], dems[8], dems[9])]
		cur.executemany("INSERT INTO Demographics VALUES(?,?,?,?,?,?,?,?,?,?)", temp2)

	for fin in finance:
		for text in fin:
			text.replace("'", "''")
		temp3 = [(fin[0], fin[1], fin[2], fin[3], fin[4])]
		cur.executemany("INSERT INTO Finances VALUES(?,?,?,?,?)", temp3)

	for maj in major:
		for text in maj:
			text.replace("'", "''")
		temp4 = [(maj[0], maj[1], maj[2], maj[3], maj[4], maj[5], maj[6], maj[7], maj[8], maj[9], maj[10], maj[11], maj[12], maj[13], maj[14], maj[15], maj[16], maj[17], maj[18], maj[19])]
		cur.executemany("INSERT INTO Major VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", temp4)

	for acad in academics:
		for text in acad:
			text.replace("'", "''")
		temp5 = [(acad[0], acad[1], acad[2], acad[3], acad[4], acad[5], acad[6], acad[7], acad[8])]
		cur.executemany("INSERT INTO Academics VALUES (?,?,?,?,?,?,?,?,?)", temp5)

	######################### END #########################


	# #################### UN-COMMENT THIS SECTION IF TESTING IS NECESSARY #####################
	# ######################### QUERIES #########################
	# queries = {}

	# ################## DATABASE FUNCTIONALITY TEST  ######################
	# queries['all_classes_taken'] = '''
	# SELECT * FROM Classes_taken
	# LIMIT 100
	# '''

	# queries['all_demographics'] = '''
	# SELECT * FROM Demographics
	# LIMIT 100
	# '''

	# queries['all_finances'] = '''
	# SELECT * FROM Finances
	# LIMIT 100
	# '''

	# queries['all_major'] = '''
	# SELECT * FROM Major
	# LIMIT 100
	# '''

	# queries['all_academics'] = '''
	# SELECT * FROM Academics
	# LIMIT 100
	# '''

	# ######################### END #########################

	# ######################### PRINT RESULTS #########################
	
	# for (qkey, qstring) in sorted(queries.items()):
	# 	cur.execute(qstring)
	# 	all_rows = cur.fetchall()
			
	# 	print ("=========== ",qkey," QUERY ======================")
	# 	print (qstring)
	# 	print ("----------- ",qkey," RESULTS --------------------")
	# 	for row in all_rows:
	# 		print (row)
	# 	print (" ")
	
	# ######################### END #########################
