import sqlite3 as lite
import csv
import re

con = lite.connect('capstone.sqlite')

with con:
	cur = con.cursor()

	######################### CREATE TABLES #########################
	# Classes_taken table (Classes Taken.xlsx)
	cur.execute('DROP TABLE IF EXISTS Classes_taken')
	cur.execute("CREATE TABLE Classes_taken(analytics_id INT, academic_term_code INT,term_desc VARCHAR(30), cat_num INT, sub_code INT, sub_desc VARCHAR(5), class_num INT, class_sec_num INT, title VARCHAR(10), grade VARCHAR(2), grading_basis INT, grading_desc VARCHAR(20), PRIMARY KEY(analytics_id))")

	# Courses_info table (Courses Info.xlsx)
	cur.execute('DROP TABLE IF EXISTS Courses_info')
	cur.execute("CREATE TABLE Courses_info(term_code INT, term_desc VARCHAR(30), cat_num INT, sub_code INT, sub_desc VARCHAR(30), class_num INT, class_sec_num INT, title VARCHAR(30), inst_name VARCHAR(30), facility VARCHAR(20), building_code CHAR(5), room CHAR(5), room_cap INT, enroll_cap INT, wait_cap INT, start_date DATE, end_date DATE, start_time TIME, end_time TIME, PRIMARY KEY(term_code))")

	# Demographics table (Demographics 1i.xlsx)
	cur.execute('DROP TABLE IF EXISTS Demographics')
	cur.execute("CREATE TABLE Demographics(analytics_id INT, max_age INT, ethinic_group_code CHAR(5), ethnic_group_desc VARCHAR(30), gender VARCHAR(10), citizen_status VARCHAR(10), first_gen_desc VARCHAR(10), in_out_state CHAR(2), home_state VARCHAR(15), citizen_country INT, PRIMARY KEY(analytics_id))")

	# Finance table (FAFSA, income, housing (1.e,1.l,2.n).xlsx)
	cur.execute('DROP TABLE IF EXISTS Finance')
	cur.execute("CREATE TABLE Finances(analytics_id INT, aid_year INT, aid_year_desc VARCHAR(30), fafsa_flag CHAR(1), income_lvl_desc VARCHAR(30), house_desc VARCHAR(30), PRIMARY KEY(analytics_id))")

	# Hs_tests table (High School GPA, SAT, ACT, AP.xlsx)
	cur.execute('DROP TABLE IF EXISTS Hs_tests')
	cur.execute("CREATE TABLE Hs_tests(analytics_id INT, hs_gpa REAL, test_name VARCHAR(10), test_comp VARCHAR(25), test_date DATE, PRIMARY KEY(analytics_id))")
	
	# Major table (Major, school acceptances 1j, 1k .xlsx)
	cur.execute('DROP TABLE IF EXISTS Major')
	cur.execute("CREATE TABLE Major(analytics_id INT, app_num INT, admit_term_code INT, admit_term_desc VARCHAR(25), acdm_plan_desc VARCHAR(25), acdm_plan_type VARCHAR(10), acdm_sub_plan_type VARCHAR(10), acdm_group_code varchar(40), acdm_prgm_code VARCHAR(40), acdm_prgm_desc VARCHAR(40), app_cnt_code INT, app_cnt_desc INT, admit_type_code INT, admit_type_desc VARCHAR(25), prgm_action_code VARCHAR(25), prgm_action_desc VARCHAR(25), house_intst_desc VARCHAR(25), res_code INT, res_desc VARCHAR(25), PRIMARY KEY(analytics_id) )")

	# Academics table (PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).xlsx)
	cur.execute('DROP TABLE IF EXISTS Academics')
	cur.execute("CREATE TABLE Academics(analytics_id INT, acdm_term_code INT, acdm_term_desc VARCHAR(25), pell_elg_flag INT, curr_gpa REAL, acdm_std_act_code INT, acdm_std_act_desc VARCHAR(25), degree_chkt_status_code INT, degree_chkt_status_desc VARCHAR(25), acdm_career_code INT, PRIMARY KEY(analytics_id) )")
	######################### END #########################

	######################### READ DATA FROM FILES #########################
	classestaken = []
	with open('Classes Taken.xlsx') as classescsv:
		reader = csv.reader(classescsv)
		for row in reader:
			classes_taken.append(row)

	coursesinfo = []
	with open ('Courses Info.xlsx') as coursescsv:
		 reader = csv.reader(coursescsv)
		 for row in reader:
		 	coursesinfo.append(row)

	demographics = []
	with open('Demographics 1i.xlsx') as demographicscsv:
		reader = csv.reader(demographicscsv)
		for row in reader:
			demographics.append(row)

	finance = []
	with open('FAFSA, income, housing (1.e,1.l,2.n).xlsx') as financecsv:
		reader = csv.reader(financecsv)
		for row in reader:
			finance.append(row)

	hstests = []
	with open('High School GPA, SAT, ACT, AP.xlsx') as hscsv:
		reader = csv.reader(hscsv)
		for row in reader:
			hs_tests.append(row)

	major = []
	with open('Major, school acceptances 1j, 1k .xlsx') as majorcsv:
		reader = csv.reader(majorcsv)
		for row in reader:
			major.append(row)

	academics = []
	with open('PELL, GPA, Acad Standing, Degree (1.m,2.e,2.k,4.a).xlsx') as academicscsv:
		reader = csv.reader(academicscsv)
		for row in reader:
			academics.append(row)
	######################### END #########################

	######################### INSERT DATA INTO DATABASE #########################
	for classes in classestaken:
		for text in classes:
			text.replace("'", "''")
		cur.execute("INSERT INTO Classes_taken VALUES(" + classes[0] + ", '" + classes[1] + "', '" + classes[2] + "', '" + classes[3] + "', '" + classes[4] + "', '" + classes[5] + "', '" + classes[6] + "', '" + classes[7] + "', '" + classes[8] + "', '" + classes[9] + "', '" + classes[10] + "', '" + classes[11] + "')")  

	for courses in courseinfo:
		for text in courses:
			text.replace("'", "''")
		cur.execute("INSERT INTO Courses_info VALUES(" + courses[0] + ", '" + courses[1] + "', '" + courses[2] + "', '" + courses[3] + "', '" + courses[4] + "', '" + courses[5] + "', '" + courses[6] + "', '" + courses[7] + "', '" + courses[8] + "', '" + courses[9] + "', '" + courses[10] + "', '" + courses[11] + "', '" + courses[12] + "', '" + courses[13] + "', '" + courses[14] + "', '" + courses[15] + "', '" + courses[16] + "', '" + courses[17] + "', '" + courses[18] + "', '" + courses[19] + "')")
	
	for dems in demographics:
		for text in dems:
			text.replace("'", "''")
		cur.execute("INSERT INTO Demographics VALUES(" + dems[0] + ", '" + dems[1] + "', '" + dems[2] + "', '" + dems[3] + "', '" + dems[4] + "', '" + dems[5] + "', '" + dems[6] + "', '" + dems[7] + "', " + dems[8] + ", '" + dems[9] + "')" )

	for fin in finance:
		for text in fin:
			text.replace("'", "''")
		cur.execute("INSERT INTO Finance VALUES(" + fin[0] + ", '" + fin[1] + "', '" + fin[2] + "', '" + ", '" + fin[3] + "', '" + fin[4] + "', '" + fin[5] + "')" )

	for hs in hstests:
		for text in hs:
			text.replace("'", "''")
		cur.execute("INSERT INTO Hs_tests VALUES(" + hs[0] + ", '" + hs[1] + "', '" + hs[2] + "', '" + hs[3] + "', '" + hs[4] + "')")

	for maj in major:
		for text in maj:
			text.replace("'", "''")
		cur.execute("INSERT INTO Major VALUES (" + maj[0] + ", '" + maj[1] + "', '" + maj[2] + "', '" + maj[3] + "', '" + maj[4] + "', '" + maj[5] + "', '" + maj[6] + "', '" + maj[7] + "', '" + maj[8] + "', '" + maj[9] + "', '" + maj[10] + "', '" + maj[11] + "', '" + maj[12] + "', '" + maj[13] + "', '" + maj[14] + "', '" + maj[15] + "', '" + maj[16] + "', '" + maj[17] + "', '" + maj[18] + "')")

	for acad in academics:
		for text in acad:
			text.replace("'", "''")
		cur.execute("INSERT INTO Academics VALUES (" + acad[0] + ", '" + acad[1] + "', '" + acad[2] + "', '" + acad[3] + "', '" + acad[4] + "', '" + acad[5] + "', '" + acad[6] + "', '" + acad[7] + "', '" + acad[8] + "', '" + acad[9] + "')")
	con.commit()
	######################### END #########################
