# CptS 355 - Spring 2023 - Assignment 3 - Python
# Name: Alec Barran

debugging = False
def debug(*s): 
     if debugging: 
          print(*s)

from functools import reduce

## problem 1(a) - aggregate_log  - 5%
def aggregate_log(data: dict) -> dict:
     agg = {}
     # iterate over each course
     for week in data.values():
          # iterate over each day in the course
          for (day, hours) in week.items():
               # get next day and add hours to aggregate
               cur = agg.get(day, 0)
               agg[day] = hours + cur

     return agg

## problem 1(b) - combine_dict– 6%
def combine_dict(dict1: dict, dict2: dict) -> dict:
     # copy list so that original dict1 is not changed
     combined = dict1.copy()
     # iterate over key value pairs of second dict
     for (k, v) in dict2.items():
          # get next key and add to combined dict
          cur = combined.get(k, 0)
          combined[k] = v + cur

     return combined

## problem 1(c) - merge_logs– 12%
def merge_logs(log_list: list) -> dict:
     agg = {}
     # iterate over each class log
     for log in log_list:
          # iterate of course and week of class log
          for (course, week) in log.items():
               # get next course and combine week data with aggregate
               cur = agg.get(course, {})
               agg[course] = combine_dict(cur, week)
     
     return agg

## problem 2(a) - most_hours – 15%
def most_hours(data: dict) -> tuple:
     # calculate the sum of hours in each course
     sum_week = lambda z: reduce(lambda x, y: x+y, z.values())
     # map sum_week to each course and pack in tuple, making [('CptS360', 1), ...]
     result = map(lambda item: (item[0], sum_week(item[1])), data.items())
     # find course with maximum hours and return tuple
     return reduce(lambda x, y: maxValueTuple(x, y), result, (None, -1))

def maxValueTuple(course1: tuple, course2: tuple) -> tuple:
    # compare tuple values, and return tuple of greater value
    if (course1[1] >= course2[1]):
        return course1
    else:
        return course2

## problem 2(b) - filter_log – 15%
def filter_log(data: dict, day: str, hours: int) -> list:
     # filter data dictionary to only courses with enough hours on given day
     result = filter(lambda item: sufficient_hours(item[1], day, hours), data.items())
     # return only list of course names
     return list(map(lambda elem: elem[0], result))

def sufficient_hours(week: dict, day: str, hours: int) -> bool:
     # determine in day exists and has enough hours
     return day in week and week[day] >= hours

## problem 3 - graph_cycle – 12% 
def graph_cycle(graph: dict, node: str) -> list:
     # create list of start node and next node
     cyc = [node, graph[node][0]]
     # pass to helper function
     return graph_cycle_helper(graph, node, cyc)

def graph_cycle_helper(graph: dict, node: str, cycle: list) -> list:
     # get most recent node and next node
     last = cycle[-1]
     next = graph[last][0]
     
     if next in cycle:
          # cycle has been found
          # check that it isn't a node pointing to itself
          if cycle[-1] != next:
               cycle.append(next)
          # get index of first instance of cycle node
          start = cycle.index(next)
          # return list from start index to end
          return cycle[start:]
     elif len(cycle) == len(graph):
          # no cycle is found as all paths have been searched
          return None
     else:
          # add next node to cycle and continue recursion
          cycle.append(next)
          return graph_cycle_helper(graph, node, cycle)

## problem 4 - filter_iter – 15% 
class Numbers():
    def __init__(self,init):
        self.current = init
    def __next__(self):
        result = self.current
        self.current += 1
        return result
    def __iter__(self):
        return self

class filter_iter:
     def __init__(self, it, op):
          self.it = it
          self.op = op
     
     def __next__(self):
          # next element in iterator
          nxt = self.it.__next__()
          if self.op(nxt):
               # if next element meets op conditions
               return nxt
          else:
               # otherwise continue to next element
               return self.__next__()
          
     def __iter__(self):
          return self

## problem 5 - merge – 10% 
def merge(iter1, iter2, n: int) -> list:
     merged = []
     try:
          # get first element of each iterator
          nxt1 = iter1.__next__()
          nxt2 = iter2.__next__()
          # continue until n elements in list
          while len(merged) < n:
               # keep list sorted
               if (nxt1 <= nxt2):
                    # append to list and get next element
                    merged.append(nxt1)
                    nxt1 = iter1.__next__()
               else:
                    merged.append(nxt2)
                    nxt2 = iter2.__next__()

     except StopIteration:
          # or end of either finite iterator is reached
          pass
     
     return merged
