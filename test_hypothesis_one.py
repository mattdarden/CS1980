import unittest
import numpy
from hypothesis_one import create_table
from hypothesis_one import update_table
from hypothesis_one import calculate_mean
from hypothesis_one import calculate_half_std
from hypothesis_one import update_table_below_avg
from hypothesis_one import pearson_coefficient


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
		java_grades, data_grades = update_table()
		self.assertEqual(java_grades, [4.0, 4.0, 1.0, 3.0, 1.0, 2.0, 2.0, 3.0])
		self.assertEqual(data_grades, [4.0, 4.0, 1.0, 3.0, 1.0, 2.0, 2.0, 3.0])

	def test_calculate_mean(self):
		grades_list = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
		mean = calculate_mean(grades_list)
		self.assertEqual(mean, 4.0)

	def test_calculate_half_std(self):
		grades_list = [1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0]
		std_dev = calculate_half_std(grades_list)
		self.assertEqual(std_dev, 1.25)

	def test_update_table_below_avg(self):
		std_dev = numpy.std([4.0, 3.0, 2.0, 1.0, 4.0, 3.0, 2.0, 1.0])
		java_grades, data_grades = update_table_below_avg(std_dev)
		self.assertEqual(java_grades, [])
		self.assertEqual(data_grades, [])

	def test_pearson_coefficient(self):
		java_grades_list = [4.0, 3.0, 2.0, 1.0, 4.0, 3.0, 2.0, 1.0]
		data_grades_list = [4.0, 3.0, 2.0, 1.0, 4.0, 3.0, 2.0, 1.0]
		pearsoncoeff = pearson_coefficient(java_grades_list, data_grades_list)
		self.assertEqual(pearsoncoeff, (1.0, 0.0))



if __name__ == '__main__':
	unittest.main()