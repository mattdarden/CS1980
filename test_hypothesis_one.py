import unittest
import numpy
from hypothesis_one import create_table
from hypothesis_one import update_table
from hypothesis_one import get_grades
from hypothesis_one import calculate_half_std
from hypothesis_one import get_below_avg_grades
from hypothesis_one import get_above_avg_grades
from hypothesis_one import get_pearson_coefficient


class test_hypothesis_one(unittest.TestCase):
	def test_create_table(self):
		test_table = create_table("0401", "CS", "0445", "CS")
		self.assertEqual(test_table, [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', 'A', 445, 'CS', 'A'), 
										('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', 'A', 445, 'CS', 'A'),
										('62726D885F72767B4BE32F899143335DD0601214', 401, 'CS', 'D', 445, 'CS', 'D'),
										('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 401, 'CS', 'B', 445, 'CS', 'B'),
										('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 401, 'CS', 'D', 445, 'CS', 'D'),
										('898741086138496C0FBB37B08ED1E15C88CFF8C5', 401, 'CS', 'C', 445, 'CS', 'C'),
										('AFFB22CB72853AAFADB3CACAB4EF95', 401, 'CS', 'C', 445, 'CS', 'C'),
										('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 401, 'CS', 'B', 445, 'CS', 'B')])

	def test_update_table(self):
		students_list = update_table()
		self.assertEqual(students_list, [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', '4.0', 445, 'CS', '4.0'), 
										('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', '4.0', 445, 'CS', '4.0'),
										('62726D885F72767B4BE32F899143335DD0601214', 401, 'CS', '1.0', 445, 'CS', '1.0'),
										('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 401, 'CS', '3.0', 445, 'CS', '3.0'),
										('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 401, 'CS', '1.0', 445, 'CS', '1.0'),
										('898741086138496C0FBB37B08ED1E15C88CFF8C5', 401, 'CS', '2.0', 445, 'CS', '2.0'),
										('AFFB22CB72853AAFADB3CACAB4EF95', 401, 'CS', '2.0', 445, 'CS', '2.0'),
										('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 401, 'CS', '3.0', 445, 'CS', '3.0')])

	def test_get_grades(self):
		students_list = [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', 4.0, 445, 'CS', 4.0), 
							('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', 3.0, 445, 'CS', 3.0)]
		class1_grades, class2_grades = get_grades(students_list)
		self.assertEqual(class1_grades, [4.0, 3.0])
		self.assertEqual(class2_grades, [4.0, 3.0])

	def test_calculate_half_std(self):
		grades_list = [10, 12, 23, 23, 16, 23, 21, 16]
		half_std_dev = calculate_half_std(grades_list)
		self.assertEqual(half_std_dev, 2.449489742783178)

	def test_get_below_avg_grades(self):
		students_list = [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', '4.0', 445, 'CS', '4.0'), 
						('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', '4.0', 445, 'CS', '4.0'),
						('62726D885F72767B4BE32F899143335DD0601214', 401, 'CS', '1.0', 445, 'CS', '1.0'),
						('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 401, 'CS', '3.0', 445, 'CS', '3.0'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 401, 'CS', '1.0', 445, 'CS', '1.0'),
						('898741086138496C0FBB37B08ED1E15C88CFF8C5', 401, 'CS', '2.0', 445, 'CS', '2.0'),
						('AFFB22CB72853AAFADB3CACAB4EF95', 401, 'CS', '2.0', 445, 'CS', '2.0'),
						('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 401, 'CS', '3.0', 445, 'CS', '3.0')]
		half_std_dev_below = 3.1
		below_avg = get_below_avg_grades(students_list, half_std_dev_below)
		self.assertEqual(below_avg, [('62726D885F72767B4BE32F899143335DD0601214', 401, 'CS', '1.0', 445, 'CS', '1.0'),
									('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 401, 'CS', '3.0', 445, 'CS', '3.0'),
									('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 401, 'CS', '1.0', 445, 'CS', '1.0'),
									('898741086138496C0FBB37B08ED1E15C88CFF8C5', 401, 'CS', '2.0', 445, 'CS', '2.0'),
									('AFFB22CB72853AAFADB3CACAB4EF95', 401, 'CS', '2.0', 445, 'CS', '2.0'),
									('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 401, 'CS', '3.0', 445, 'CS', '3.0')])

	def test_get_above_avg_grades(self):
		students_list = [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', '4.0', 445, 'CS', '4.0'), 
				('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', '4.0', 445, 'CS', '4.0'),
				('62726D885F72767B4BE32F899143335DD0601214', 401, 'CS', '1.0', 445, 'CS', '1.0'),
				('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 401, 'CS', '3.0', 445, 'CS', '3.0'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 401, 'CS', '1.0', 445, 'CS', '1.0'),
				('898741086138496C0FBB37B08ED1E15C88CFF8C5', 401, 'CS', '2.0', 445, 'CS', '2.0'),
				('AFFB22CB72853AAFADB3CACAB4EF95', 401, 'CS', '2.0', 445, 'CS', '2.0'),
				('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 401, 'CS', '3.0', 445, 'CS', '3.0')]
		half_std_dev_above = 3.9
		above_avg = get_above_avg_grades(students_list, half_std_dev_above)
		self.assertEqual(above_avg, [('573C3884232AD20E2EABDFD306DD3E106F82D25', 401, 'CS', '4.0', 445, 'CS', '4.0'),
									('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 401, 'CS', '4.0', 445, 'CS', '4.0')])

	def test_get_pearson_coefficient(self):
		class_grades_list = [4.0, 3.0, 2.0, 1.0, 4.0, 3.0, 2.0, 1.0]
		pearsoncoeff, p_value = get_pearson_coefficient(class_grades_list, class_grades_list)
		self.assertEqual(pearsoncoeff, 1.0)
		self.assertEqual(p_value, 0.0)



if __name__ == '__main__':
	unittest.main()