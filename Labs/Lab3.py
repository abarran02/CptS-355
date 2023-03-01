# CptS 355 - Spring 2023 - Lab 3
# Alec Barran
debugging = False
def debug(*s): 
     if debugging: 
          print(*s)

## problem 1 getNumCases
def getNumCases(data: dict, counties: list, months: list) -> int:
    num = 0
    for (county, cases) in data.items():
        if county in counties:
            matches = [count for (month, count) in cases.items() if month in months]
            num += sum(matches)
    return num

## problem 2 getMonthlyCases
def getMonthlyCases(data: dict) -> dict:
    monthlyCases = {}
    for (county, cases) in data.items():
        for (month, count) in cases.items():
            if month not in monthlyCases:
                monthlyCases[month] = {county:count}
            else:
                monthlyCases[month][county] = count
    
    return monthlyCases

## problem 3 mostCases
from functools import reduce
def mostCases(data: dict) -> tuple:
    # convert data to month grouping
    monthlyData = getMonthlyCases(data)
    # calculate the sum of cases in a given month
    sumMonth = lambda z: reduce(lambda x, y: x+y, z.values())
    # map sumMonth to each month, making [('Mon':1)]
    result = map(lambda item: (item[0], sumMonth(item[1])), monthlyData.items())

    # find month with maximum case and return corresponding tuple
    return reduce(lambda x, y: maxValueTuple(x, y), result, (None, -1))

def maxValueTuple(month1: tuple, month2: tuple) -> tuple:
    if (month1[1] >= month2[1]):
        return month1
    else:
        return month2

## problem 4a) searchDicts(L,k)
def searchDicts(L: list, k):
    for itm in reversed(L):
        if k in itm:
            return itm[k]

## problem 4b) searchDicts2(L,k)
def searchDicts2(tL: list, k):
    ind = len(tL) - 1
    while True:
        if k in tL[ind][1]:
            # match found and return value
            return tL[ind][1][k]
        elif ind == 0:
            # match is never found
            return None
        else:
            # go to next index
            ind = tL[ind][0]

## problem 5 - getLongest
def getLongest(L: list):
    longest = ""
    for itm in L:
        if type(itm) is list:
            itm = getLongest(itm)

        if len(itm) > len(longest):
            longest = itm
    
    return longest

## problem 6 - apply2nextN
class apply2nextN:
    def __init__(self, op, n: int, iterIn):
        self.op = op
        self.n = n
        self.iterIn = iterIn

    def __next__(self):
        lst = []
        for i in range(self.n):
            try:
                lst.append(self.iterIn.__next__())
            except StopIteration:
                if i != 0:
                    break
                else:
                    raise StopIteration
        
        return reduce(self.op, lst)
    
    def __iter__(self):
        return self

import unittest
class Lab3_Extra_Tests(unittest.TestCase):
    def test_searchDicts2(self):
        L3 = [(0, {'b':1, 'c':2}),
            (0, {'d':3, 'e':4}),
            (3, {'f':5,}),
            (1, {'g':6}),
            (2, {'h':7}),
            (4, {'q':8})]
        result = searchDicts2(L3,'b')
        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()
