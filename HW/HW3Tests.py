#------------------------------------------------------
#-- INCLUDE YOUR OWN TESTS IN THIS FILE
#------------------------------------------------------
import unittest
from HW3 import *
class HW3SampleTests(unittest.TestCase):
    "Unittest setup file. Unittest framework will run this before every test."
    def setUp(self):
        pass

    log_input = {'Phys202': {'Tue': 4, 'Thu': 5},  
                'CptS122': {'Mon': 6, 'Sat': 3},  
                'Eng402': {'Mon': 1, 'Sat':1, 'Sun': 4},  
                'Phil201': {'Tue': 5, 'Thu': 9}}

    #--- Problem 1(a)----------------------------------
    def test_aggregate_log(self):
        actual = aggregate_log(self.log_input)
        expected = {'Mon':7, 'Tue':9, 'Thu':14, 'Sat':4, 'Sun':4}
        self.assertEqual(actual, expected)
    
    #--- Problem 1(b)----------------------------------
    def test_combine_dict(self):
        log1 = {'Tue':6, 'Thu':5, 'Sat':8} 
        log2 = {'Mon':1, 'Wed':2, 'Fri':1, 'Sun':4} 
        actual = combine_dict(log1,log2)
        expected = {'Mon':1, 'Tue':6, 'Wed':2, 'Thu':5, 'Fri':1, 'Sat':8, 'Sun':4}
        self.assertEqual(actual, expected)
    
    #--- Problem 1(c) ----------------------------------
    def test_merge_logs(self):
        log_list = [self.log_input,
                    {'Phys202': {'Wed':1}, 'Eng402': {'Mon':3}},
                    {'CptS122' : {'Sat':1, 'Sun':4}, 'Phil201': {'Tue':1}}]
        actual = merge_logs(log_list)
        expected = {'Phys202': {'Tue': 4, 'Wed':1, 'Thu': 5},  
                    'CptS122': {'Mon': 6, 'Sat': 4, 'Sun':4},  
                    'Eng402': {'Mon': 4, 'Sat':1, 'Sun': 4},  
                    'Phil201': {'Tue': 6, 'Thu': 9}}
        self.assertEqual(actual, expected)

    #--- Problem 2(a)----------------------------------
    def test_most_hours(self):        
        actual = most_hours(self.log_input)
        expected = ('Phil201', 14)
        self.assertEqual(actual, expected)
            
    #--- Problem 2(b) ----------------------------------
    def test_filter_log(self):        
        actual = filter_log(self.log_input,'Tue', 6)
        self.assertEqual(actual, [])
    
    #--- Problem 3----------------------------------
    def test_graph_cycle(self):
        graph = {'A':('B',3), 'B':('C',4), 'C':(None,8)}
        actual = graph_cycle(graph, 'A')
        self.assertEqual(actual, None)
    
    #--- Problem 4----------------------------------
    def test_filter_iter(self):
        it = filter_iter(iter(range(0, 50)), lambda x: int(x**(0.5)) == x**(0.5))
        actual = list(it)
        expected = [0, 1, 4, 9, 16, 25, 36, 49]
        self.assertEqual(actual, expected)
    
    #--- Problem 5----------------------------------
    def test_merge(self):
        it1 = iter(range(0, 100, 2))
        it2 = iter(range(1, 101, 2))
        actual = merge(it1, it2, 5)
        expected = [0,1,2,3,4]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
