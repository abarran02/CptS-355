{- Example of using the HUnit unit test framework.  See  http://hackage.haskell.org/package/HUnit for additional documentation.
To run the tests type "run" at the Haskell prompt.  -} 
-- by Alec Barran

module HW1Tests
    where

import Test.HUnit
import Data.Char
import Data.List (sort)
import HW1

-- P1(a) count tests  
p1a_test1 = TestCase (assertEqual "(count-test1)"
                                  2
                                  (count 'o' "Knowledge is power.") )
p1a_test2 = TestCase (assertEqual "(count-test2)"
                                  0
                                  (count 'x' []) )                       

-- P1(b) diff tests
p1b_test1 = TestCase (assertEqual "(diff-test1)"
                                  []
                                  (diff [] [1,2,3]) )
p1b_test2 = TestCase (assertEqual "(diff-test2)"
                                  [1,2,3]
                                  (diff [1,2,3] []) )

-- P1(c) bag_diff tests
p1c_test1 = TestCase (assertEqual "(bag_diff-test1)"
                                  []
                                  (bag_diff [] [1,2,3]) )
p1c_test2 = TestCase (assertEqual "(bag_diff-test2)"
                                  []
                                  (bag_diff [] [1,2,3]) )

-- P2  everyN tests
p2_test1 = TestCase (assertEqual "(everyN-test1)"
                                  []
                                  (everyN "haskell" 0) )
p2_test2 = TestCase (assertEqual "(everyN-test2)"
                                  "haskell"
                                  (everyN "haskell" 7) )

-- P3(a) make_sparse tests
p3a_test1 = TestCase (assertEqual "(make_sparse-test1)"
                                  [3]
                                  (make_sparse [(0,3)]) )
p3a_test2 = TestCase (assertEqual "(make_sparse-test2)"
                                  [0]
                                  (make_sparse [(0,0)]) )

-- P3(b) compress tests
p3b_test1 = TestCase (assertEqual "(compress-test1)"
                                  [(0,1),(2,2)]
                                  (compress [1,0,2]) )
p3b_test2 = TestCase (assertEqual "(compress-test2)"
                                  []
                                  (compress [0,0,0]) )

-- P4 added_sums tests
p4_test1 = TestCase (assertEqual "(added_sums-test1)"
                                  [0,0,0,0]
                                  (added_sums [0,0,0,0]) )
p4_test2 = TestCase (assertEqual "(added_sums-test2)"
                                  [-1,-2,-3,-4]
                                  (added_sums [-1,-1,-1,-1]) )

-- P5 find_routes tests
routes_empty = [("Lentil",[])]
p5_test = TestCase (assertEqual "(find_routes-test)"
                                  []
                                  (find_routes "Main" routes_empty) )

-- P6 group_sum tests
p6_test1 = TestCase (assertEqual "(group_sum-test1)"
                                  [[1,2,3]]
                                  (group_sum [1,2,3] 10) )
p6_test2 = TestCase (assertEqual "(group_sum-test2)"
                                  []
                                  (group_sum [1,2,3] 0) )

-- add the test cases you created to the below list. 
tests = TestList [ 
                    TestLabel "Problem 1a- test1" p1a_test1,
                    TestLabel "Problem 1a- test2" p1a_test2,
                    TestLabel "Problem 1b- test1" p1b_test1,
                    TestLabel "Problem 1b- test2" p1b_test2,
                    TestLabel "Problem 1c- test1" p1c_test1,
                    TestLabel "Problem 1c- test2" p1c_test2,
                    TestLabel "Problem 2- test1" p2_test1,
                    TestLabel "Problem 2- test2" p2_test2,
                    TestLabel "Problem 3a- test1" p3a_test1,
                    TestLabel "Problem 3a- test2" p3a_test2,
                    TestLabel "Problem 3b- test1" p3b_test1,
                    TestLabel "Problem 3b- test2" p3b_test2,
                    TestLabel "Problem 4- test1" p4_test1,
                    TestLabel "Problem 4- test2" p4_test2,
                    TestLabel "Problem 5- test" p5_test,
                    TestLabel "Problem 6- test1" p6_test1,
                    TestLabel "Problem 6- test2" p6_test2
                 ] 
                  
-- shortcut to run the tests
run = runTestTT  tests
