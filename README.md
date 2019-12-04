# CS1980 Data Mining for Student Scheduling
###### Project Group: Alex Kim, Matt Darden, Ruth Dereje
###### Project Supervisors: Dr. Daniel Mosse, Nathan Ong
#

# PROJECT INTRODUCTION
###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; At the University of Pittsburgh, there is a wide variety of options available for undergraduate students to schedule their courses. In the current system, students are often left to select courses through an extensive list of classes with only the knowledge of basic general education requirements and classes required for their major. In order to create their schedule, students must schedule meetings with their school advisor. However, advisors are limited to screenshots of other schedule building software and prior knowledge. The decision process can oftentimes be overwhelming for students to choose from, as well as for advisors trying to find the best options for students. There are many factors such as professors, course difficulty, work load, prerequisites, and others to consider when scheduling for classes that make the process far more difficult than choosing a predetermined or generic suggested path.
###### 	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Our goal is to analyze student data within the computer science major to build a tool that will find correlations pertinent to helping students and advisors predict the best path to academic success. 

##
##### HYPOTHESIS 1
* if students receive a lower than average grade in CS 401 will receive lower than average grades in CS 445. 

##### HYPOTHESIS 2
* If a student has a semester buffer between a low level course (CS 445) and its corresponding upper level course (CS 1501), then their score will be lower than a student with a similar grade who took the upper level course the semester after the prerequisite.

##### HYPOTHESIS 3
* If a student has taken CS 447 then they will receive a higher than average grade for CS 449 than a student who has not taken CS 447.

# USAGE GUIDE
##### FORMATTING THE DATA
1. format the provided data files:
	1. delete the header row on each file
	1. export each file as a .csv file
1. create a folder **'anonymized_data'**
1. within the folder create another folder called **'csv'**
1. add formatted data to the 'csv' folder

##### HOW TO RUN ALL SCRIPTS
1. in command line
1. type _**chmod +x run_all.sh**_ and enter
1. type _**./run_all.sh**_ and enter
1. when prompted for a database for hypothesis_one: type _**databases/capstone.sqlite**_ and enter
1. when prompted for a database for hypothesis_two: type _**databases/capstone.sqlite**_ and enter
* output for all three hypotheses should appear in the command line

##### HOW TO RUN ALL TEST SCRIPTS
1. in command line
1. type _**chmod +x run_tests.sh**_ and enter
1. type _**./run_tests.sh**_ and enter
1. when prompted for a database for hypothesis_one: type _**databases/unittest1.sqlite**_ and enter
1. when prompted for a database for hypothesis_two: type _**databases/unittest2.sqlite**_ and enter
* output for tests on hypothesis_one and hypothesis_two should appear in the command line

##### FILE DESCRIPTIONS
* **databases** Folder - holds all of the sqlite databases and the python scripts to create the databases
   * **db.py** - creates the main capstone.sqlite database that all hypotheses query from
   * **test_db1.py** - creates the unittest1.sqlite database for testing hypothesis_one
   * **test_db2.py** - create the unnittest2.sqlite database for testing hypothesis_two
* **midterm test data** folder - contains fake data that we created to test our skeleton code for our midterm progress presentation
* **old** folder - contains old skeleton code that we used before we received the official data
* **testdata** folder - contains fake data used for unit testing purposes
* **hypothesis_one.py** - code that implements a solution to our first hypothesis for the project
* **hypothesis_two.py** - code that implements a solution to our second hypothesis for the project 
* **hypothesis_three.py** - code that implements a solution to our third hypothesis for the project
* **test_hypothesis_one.py** - unit tests for hypothesis_one implementation
* **test_hypothesis_two.py** - unit tests for hypothesis_two implementation
* **run_all.sh** - shell script that creates the database and runs all the hypotheses
* **run_tests.sh** - shell script that creates the test databases and runs all the unit tests for hypothesis 1 and 
* **corrstats.py** - Functions for calculating the statistical significant differences between two dependent or independent correlation
coefficients. Author: Philipp Singer (www.philippsinger.info)