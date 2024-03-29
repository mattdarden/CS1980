import unittest
from hypothesis_two import create_table
from hypothesis_two import get_semesters_reference_list
from hypothesis_two import fix_terms
from hypothesis_two import get_class_group
from hypothesis_two import get_grades
from hypothesis_two import compare_academic_term
from hypothesis_two import get_pearson_coefficient

class test_hypothesis_two(unittest.TestCase):

	def test_create_table(self):
		test_table = create_table("0445", "CS", "1501", "CS")
		self.assertEqual(test_table, [('573C3884232AD20E2EABDFD306DD3E106F82D25', 2084, 445, 'CS', 'A', 2121, 1501, 'CS', 'A'), 
								('60F9ECEBEF7EB31ABB7CC1A94CCDCE19ABE204DF', 2084, 445, 'CS', 'A', 1020, 1501, 'CS', 'A'),
								('62726D885F72767B4BE32F899143335DD0601214', 2084, 445, 'CS', 'D', 1020, 1501, 'CS', 'D'),
								('69A79FC7A1E9102E2295D409BDAB3AA4DE15CDDC', 2084, 445, 'CS', 'B', 1020, 1501, 'CS', 'B'),
								('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2084, 445, 'CS', 'D', 1020, 1501, 'CS', 'D'),
								('898741086138496C0FBB37B08ED1E15C88CFF8C5', 2084, 445, 'CS', 'C', 1020, 1501, 'CS', 'C'),
								('AFFB22CB72853AAFADB3CACAB4EF95', 2084, 445, 'CS', 'C', 1020, 1501, 'CS', 'C'),
								('C9C0E5C8C797911FFCF18541F3B08BCF48241B71', 2084, 445, 'CS', 'B', 2121, 1501, 'CS', 'B')])

	def test_get_semesters_reference_list(self):
		actual_list = [1001, 1002, 1003, 1011, 1012, 1013, 1021, 1022, 1023, 1031, 1032, 1033, 1041, 1042, 1043, 1051, 
							1052, 1053, 1061, 1062, 1063, 1071, 1072, 1073, 1081, 1082, 1083, 1091, 1092, 1093, 1101, 1102, 1103, 
							1111, 1112, 1113, 1121, 1122, 1123, 1131, 1132, 1133, 1141, 1142, 1143, 1151, 1152, 1153, 1161, 1162, 
							1163, 1171, 1172, 1173, 1181, 1182, 1183, 1191, 1192, 1193, 1201, 1202, 1203, 1211, 1212, 1213, 1221, 
							1222, 1223, 1231, 1232, 1233, 1241, 1242, 1243, 1251, 1252, 1253, 1261, 1262, 1263, 1271, 1272, 1273, 
							1281, 1282, 1283, 1291, 1292, 1293, 1301, 1302, 1303, 1311, 1312, 1313, 1321, 1322, 1323, 1331, 1332, 
							1333, 1341, 1342, 1343, 1351, 1352, 1353, 1361, 1362, 1363, 1371, 1372, 1373, 1381, 1382, 1383, 1391, 
							1392, 1393, 1401, 1402, 1403, 1411, 1412, 1413, 1421, 1422, 1423, 1431, 1432, 1433, 1441, 1442, 1443, 
							1451, 1452, 1453, 1461, 1462, 1463, 1471, 1472, 1473, 1481, 1482, 1483, 1491, 1492, 1493, 1501, 1502, 
							1503, 1511, 1512, 1513, 1521, 1522, 1523, 1531, 1532, 1533, 1541, 1542, 1543, 1551, 1552, 1553, 1561, 
							1562, 1563, 1571, 1572, 1573, 1581, 1582, 1583, 1591, 1592, 1593, 1601, 1602, 1603, 1611, 1612, 1613, 
							1621, 1622, 1623, 1631, 1632, 1633, 1641, 1642, 1643, 1651, 1652, 1653, 1661, 1662, 1663, 1671, 1672, 
							1673, 1681, 1682, 1683, 1691, 1692, 1693, 1701, 1702, 1703, 1711, 1712, 1713, 1721, 1722, 1723, 1731, 
							1732, 1733, 1741, 1742, 1743, 1751, 1752, 1753, 1761, 1762, 1763, 1771, 1772, 1773, 1781, 1782, 1783, 
							1791, 1792, 1793, 1801, 1802, 1803, 1811, 1812, 1813, 1821, 1822, 1823, 1831, 1832, 1833, 1841, 1842, 
							1843, 1851, 1852, 1853, 1861, 1862, 1863, 1871, 1872, 1873, 1881, 1882, 1883, 1891, 1892, 1893, 1901, 
							1902, 1903, 1911, 1912, 1913, 1921, 1922, 1923, 1931, 1932, 1933, 1941, 1942, 1943, 1951, 1952, 1953, 
							1961, 1962, 1963, 1971, 1972, 1973, 1981, 1982, 1983, 1991, 1992, 1993, 2001, 2002, 2003, 2011, 2012, 
							2013, 2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043, 2051, 2052, 2053, 2061, 2062, 2063, 2071, 
							2072, 2073, 2081, 2082, 2083, 2091, 2092, 2093, 2101, 2102, 2103, 2111, 2112, 2113, 2121, 2122, 2123, 
							2131, 2132, 2133, 2141, 2142, 2143, 2151, 2152, 2153, 2161, 2162, 2163, 2171, 2172, 2173, 2181, 2182, 
							2183, 2191, 2192, 2193, 2201, 2202, 2203, 2211, 2212, 2213, 2221, 2222, 2223, 2231, 2232, 2233, 2241, 
							2242, 2243, 2251, 2252, 2253, 2261, 2262, 2263, 2271, 2272, 2273, 2281, 2282, 2283, 2291, 2292, 2293, 
							2301, 2302, 2303, 2311, 2312, 2313, 2321, 2322, 2323, 2331, 2332, 2333, 2341, 2342, 2343, 2351, 2352, 
							2353, 2361, 2362, 2363, 2371, 2372, 2373, 2381, 2382, 2383, 2391, 2392, 2393, 2401, 2402, 2403, 2411, 
							2412, 2413, 2421, 2422, 2423, 2431, 2432, 2433, 2441, 2442, 2443, 2451, 2452, 2453, 2461, 2462, 2463, 
							2471, 2472, 2473, 2481, 2482, 2483, 2491, 2492, 2493, 2501, 2502, 2503, 2511, 2512, 2513, 2521, 2522, 
							2523, 2531, 2532, 2533, 2541, 2542, 2543, 2551, 2552, 2553, 2561, 2562, 2563, 2571, 2572, 2573, 2581, 
							2582, 2583, 2591, 2592, 2593, 2601, 2602, 2603, 2611, 2612, 2613, 2621, 2622, 2623, 2631, 2632, 2633, 
							2641, 2642, 2643, 2651, 2652, 2653, 2661, 2662, 2663, 2671, 2672, 2673, 2681, 2682, 2683, 2691, 2692, 
							2693, 2701, 2702, 2703, 2711, 2712, 2713, 2721, 2722, 2723, 2731, 2732, 2733, 2741, 2742, 2743, 2751, 
							2752, 2753, 2761, 2762, 2763, 2771, 2772, 2773, 2781, 2782, 2783, 2791, 2792, 2793, 2801, 2802, 2803, 
							2811, 2812, 2813, 2821, 2822, 2823, 2831, 2832, 2833, 2841, 2842, 2843, 2851, 2852, 2853, 2861, 2862, 
							2863, 2871, 2872, 2873, 2881, 2882, 2883, 2891, 2892, 2893, 2901, 2902, 2903, 2911, 2912, 2913, 2921, 
							2922, 2923, 2931, 2932, 2933, 2941, 2942, 2943, 2951, 2952, 2953, 2961, 2962, 2963, 2971, 2972, 2973, 
							2981, 2982, 2983, 2991, 2992, 2993]
		reference_list = get_semesters_reference_list()
		self.assertEqual(reference_list, actual_list)

	def test_fix_terms_spring(self):
		fixed_term = fix_terms('2094')
		self.assertEqual(fixed_term, 2091)

	def test_fix_terms_summer(self):
		fixed_term = fix_terms('2097')
		self.assertEqual(fixed_term, 2092)

	def test_fix_terms_fall(self):
		fixed_term = fix_terms('2091')
		self.assertEqual(fixed_term, 2093)

	def test_compare_academic_term(self):
		reference_list = [2091, 2092, 2093]
		century, year, semester = compare_academic_term('2094', '2091', reference_list)
		self.assertEqual(century, 0)
		self.assertEqual(year, 0)
		self.assertEqual(semester, 2)

	def test_get_grades(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2034, 1501,'CS', 'A+'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2034, 1501,'CS', 'A-'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','B+', 2034, 1501,'CS', 'B+'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','B',2034, 1501,'CS', 'B'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','B-', 2034, 1501,'CS', 'B-'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','C+', 2034, 1501,'CS', 'C+'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','C',  2034, 1501,'CS', 'C'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','C-', 2034, 1501,'CS', 'C-'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','D+',  2034, 1501,'CS', 'D+'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','D',  2034, 1501,'CS', 'D'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','D-',  2034, 1501,'CS', 'D-'),
						('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','F', 2034, 1501,'CS', 'F')]
		class1_grades, class2_grades = get_grades(student_list)
		self.assertEqual(class1_grades, [4.0, 4.0, 3.75, 3.25, 3.0, 2.75, 2.25, 2.0, 1.75, 1.25, 1.0, 0.75, 0.0])
		self.assertEqual(class2_grades, [4.0, 4.0, 3.75, 3.25, 3.0, 2.75, 2.25, 2.0, 1.75, 1.25, 1.0, 0.75, 0.0])

	def test_get_class_group_zero(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2037, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2031, 1501,'CS', 'A-')]
		reference_list = [2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043]
		students_gap_zero = get_class_group(0, student_list, reference_list)
		self.assertEqual(students_gap_zero, [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+')])

	def test_get_class_group_one(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2037, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2031, 1501,'CS', 'A-')]
		reference_list = [2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043]
		students_gap_one = get_class_group(1, student_list, reference_list)
		self.assertEqual(students_gap_one, [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A', 2034, 1501,'CS', 'A')])

	def test_get_class_group_two(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2037, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2031, 1501,'CS', 'A-')]
		reference_list = [2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043]
		students_gap_two = get_class_group(2, student_list, reference_list)
		self.assertEqual(students_gap_two, [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A-', 2037, 1501,'CS', 'A-')])
	
	def test_get_class_group_three(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2037, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2031, 1501,'CS', 'A-')]
		reference_list = [2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043]
		students_gap_three = get_class_group(3, student_list, reference_list)
		self.assertEqual(students_gap_three, [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A-', 2031, 1501,'CS', 'A-')])
	
	def test_get_class_group_four(self):
		student_list = [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A+', 2021, 1501,'CS', 'A+'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A', 2034, 1501,'CS', 'A'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2037, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2031, 1501,'CS', 'A-'),
				('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445, 'CS','A-', 2044, 1501,'CS', 'A-')]
		reference_list = [2021, 2022, 2023, 2031, 2032, 2033, 2041, 2042, 2043]
		students_gap_four = get_class_group(4, student_list, reference_list)
		self.assertEqual(students_gap_four, [('839B126C2A116CD3E93B7705D5FFE1F1B302E7FD', 2021, 445,'CS', 'A-', 2044, 1501,'CS', 'A-')])

	def test_get_pearson_coefficient(self):
		class_grades = [1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0]
		coeff, p_value = get_pearson_coefficient(class_grades, class_grades)
		self.assertEqual(coeff, 1)
		self.assertEqual(p_value, 0)



if __name__ == '__main__':
	unittest.main()