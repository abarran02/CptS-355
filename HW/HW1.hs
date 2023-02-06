-- CptS 355 - Spring 2023 -- Homework1 - Haskell
-- Name: Alec Barran
-- Collaborators: 

module HW1
     where

-- P1(a) count ;  6%
-- base case
count _ [] = 0
-- if next element in list is target item, increment count
-- else just continue recursion
count item (x:xs) | x == item = 1 + (count item xs)
                  | otherwise = count item xs

-- P1(b) diff ;  6%
-- base cases for empty input lists
diff iL1 [] = iL1
diff [] _ = []
-- if x exists in iL2 then continue recursion
-- else append x result before continuing
diff (x:xs) iL2 | x `elem` iL2 = diff xs iL2
                | otherwise = (x: (diff xs iL2))

-- P1(c) bag_diff ; 8%
-- base cases
bag_diff iL1 [] = iL1
bag_diff [] _ = []
-- if list 1 has more instances of an element than list 2, add to result
-- this includes not existing in list 2
bag_diff (x:xs) iL2 | (count x (x:xs)) > (count x iL2) = (x: (bag_diff xs iL2))
                    | otherwise = bag_diff xs iL2
                                            
-- P2  everyN ; 10%
-- base cases
everyN [] _ = []
everyN _ 0 = []
-- pass arguments to helper function with empty buffer
everyN iL n = 
     if (length iL) >= n then iL
     else everyNHelper iL n n []
     -- helper function keeps track of every n elements, where m is the number of elements until the next match
     where everyNHelper [] _ _ buffer = buffer -- base case, empty input list and return buffer
           -- when matched, append element x to end of buffer and reset m to n
           -- else decrement m and continue recursion
           everyNHelper (x:xs) n m buffer | m == 1 = everyNHelper xs n n (buffer ++ [x])
                                          | otherwise = everyNHelper xs n (m-1) buffer

-- P3(a) make_sparse ; 15%
-- base case
make_sparse [] = []
make_sparse iL = make_sparseHelper iL 0
     -- helper function tracks current index on sparsed buffer
     where make_sparseHelper [] _ = [] -- base case, empty tuple list
           -- add append element when correct index is reached, continue to next tuple
           -- else increment index and recurse with same tuple
           make_sparseHelper ((x,y):xs) index | x == index = (y: make_sparseHelper xs (index+1))
                                              | otherwise = (0: make_sparseHelper ((x,y):xs) (index+1))

-- P3(b) compress ; 15%
-- base case
compress [] = []
compress iL = compressHelper iL 0
     -- helper function tracks the index of any non-zero elements, and appends tuple
     where compressHelper [] _ = [] -- base case, empty input list
           -- increment index on each 0
           -- else append index tuple for each non-zero element
           compressHelper (x:xs) index | x == 0 = compressHelper xs (index+1)
                                       | otherwise = ((index,x): compressHelper xs (index+1))

-- P4 added_sums ; 8%
-- base case
added_sums [] = []
-- pass arguments to helper function with 0 sum and empty buffer
added_sums iL = added_sumsHelper iL 0
     -- helper function keeps total sum with each recursion step
     where added_sumsHelper [] _ = [] -- base case, empty input list
           -- continue recursion with next total sum and append total sum
           added_sumsHelper (x:xs) sum = ((sum+x): added_sumsHelper xs (sum+x))

-- P5 find_routes ; 8%
-- base case
find_routes _ [] = []
-- if stop is an element of the stop list of a route, append the route name
-- else continue recursion to next route
find_routes stop ((x,y):xs) | stop `elem` y = (x: find_routes stop xs)
                            | otherwise = find_routes stop xs

-- P6 group_sum ; 15%
-- base case
group_sum [] _ = []
-- pass arguments to helper function with k=0, sum=0, and empty buffer
group_sum iL n = group_sumHelper iL n 0 0 []
     -- helper function tracks exponent k, sum of each group, and all groups in buffer
     -- base case, buffer empty and return empty list
     -- else return reverse of buffer concatenated with empty list to finalize last group
     where group_sumHelper _ 0 _ _ _ = []
           group_sumHelper [] _ _ _ buffer | buffer == [] = []
                                           | otherwise = ((reverse buffer):[])
           -- if sum plus next term is greater than 2*n^k, then reverse buffer and concatenate next group
           -- as x is added to front of list in recursive step, buffer must be reversed for correct order
           -- recursion is continued with the next term and all excess, increment k, sum=0 and empty buffer
           group_sumHelper (x:xs) n k sum buffer | (sum+x) > (n*(2^k)) = ((reverse buffer): group_sumHelper (x:xs) n (k+1) 0 [])
                                                  -- else continue in same group with new sum and x added to front of buffer
                                                 | otherwise = group_sumHelper xs n k (sum+x) (x:buffer)

-- Assignment rules ; 3%
-- Your own tests; please add your tests to the HW1Tests.hs file ; 6%
