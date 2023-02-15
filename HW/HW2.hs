-- CptS 355 - Spring 2023 -- Homework2 - Haskell
-- Name: Alec Barran
-- Collaborators: 

module HW2
     where

{- P1 - remove_every, remove_every_tail  -}
-- (a) remove_every – 7%
remove_every n [] = []
remove_every 0 _ = [] -- added pattern instead of requiring recursion for this case
remove_every n lst = remove_helper n lst n
     where remove_helper _ [] _ = [] -- encountered non-exhaustive pattern error, must specify handling end of list
           remove_helper 0 (x:xs) k = remove_helper k xs k -- was missing last argument of remove_helper, added k
           remove_helper n (x:xs) k = x:(remove_helper (n-1) xs k) -- was also missing last element of remove_helper

-- (b) remove_every_tail –  10%
-- base cases
remove_every_tail n [] = []
remove_every_tail 0 _ = []
-- pass to helper function with empty accumulator
remove_every_tail n lst = tail_helper n lst n []
     where tail_helper _ [] _ buf = reverse buf -- end of list, return buffer
           tail_helper 0 (x:xs) k buf = tail_helper k xs k buf -- skip item and reset counter n
           tail_helper n (x:xs) k buf = tail_helper (n-1) xs k (x:buf) -- decrement 1 and add x to buffer

------------------------------------------------------
{- P2  get_outof_range and count_outof_range  -}
-- (a) get_outof_range – 6%
-- check whether each is less than v1 or greater than v2
get_outof_range v1 v2 xs = filter (\x -> x < v1 || x > v2) xs

-- (b) count_outof_range – 10%
count_outof_range v1 v2 xs = length $ concat $ reduce v1 v2 xs -- concat out of range sublists, and return length of concat
     where reduce v1 v2 lst = map (get_outof_range v1 v2) xs -- get out of range items of each sublist

------------------------------------------------------
{- P3  find_routes - 10% -}
find_routes stop lst = map fst $ reduce stop lst -- get first item of tuple (name) of each route with matching stop
     where reduce stop lst = filter (\(x,y) -> stop `elem` y) lst -- check desired stop is element of stop list

------------------------------------------------------
{- P4  add_lengths and add_nested_lengths -}

data LengthUnit =  INCH  Int | FOOT  Int | YARD  Int
                   deriving (Show, Read, Eq)

-- convert LengthUnit to Int so that math operations can be performed
convert :: LengthUnit -> Int
convert (INCH x) = x
convert (FOOT x) = x * 12
convert (YARD x) = x * 36

-- (a) add_lengths - 6%
add_lengths :: LengthUnit -> LengthUnit -> LengthUnit
add_lengths x y =  INCH $ (convert x) + (convert y) -- convert to x and y to Ints, add, and place back in INCH

-- (b) add_nested_lengths - 10%
add_nested_lengths :: [[LengthUnit]] -> LengthUnit
add_nested_lengths [] = INCH 0 -- base case
add_nested_lengths lst = add_lengths_list $ map add_lengths_list lst -- add up lengths of each sublist, then add sublist results
     where add_lengths_list [] = INCH 0 -- base case
           add_lengths_list lst = foldr add_lengths (INCH 0) lst -- add each length in list to a base INCH 0

------------------------------------------------------
{- P5 sum_tree and create_sumtree -}

data Tree  = LEAF Int | NODE Int Tree Tree | NULL
                     deriving (Show, Read, Eq)

-- (a) sum_tree - 8%
sum_tree :: Tree -> Int
sum_tree (LEAF a) = a
sum_tree NULL = 0
-- add current NODE value to sum of each subtree
sum_tree (NODE a x y) = a + sum_tree x + sum_tree y

-- (b) create_sumtree - 10%
create_sumtree :: Tree -> Tree
create_sumtree (LEAF a) = LEAF a
create_sumtree NULL = NULL
-- create NODE with sum of current value plus subtrees, and do the same for all subtrees
create_sumtree (NODE a x y) = NODE (sum_tree (NODE a x y)) (create_sumtree x) (create_sumtree y)

------------------------------------------------------
{- P6 list_tree - 16% -}
data ListTree a = LEAFs [a] | NODEs [ListTree a]
                  deriving (Show, Read, Eq)

list_tree f base t = operate f base t -- pass to helper function
     -- perform given operation on NODE list, after doing the same for all sublists
     where operate f base (NODEs a) = foldl f base $ map (operate f base) a
           operate f base (LEAFs lst) = foldl f base lst -- perform given operation on LEAF list

-- Tree examples - 4%
-- INCLUDE YOUR TREE EXAMPLES HERE

example1 = NODE 2 (NODE 1 (LEAF (-1)) (LEAF 4)) (NODE 4 (LEAF 6) (NODE 5 (LEAF 8) (NODE 9 (LEAF 3) (NODE 1 (LEAF 4) (LEAF 10)))))
example2 = NODE 3 (NODE 4 (NODE 5 (NODE 6 (NODE 7 (LEAF 6) (LEAF 5)) (LEAF 4)) (LEAF 3)) (LEAF 2)) (NODE 1 (LEAF (-1)) (LEAF (-2)))

-- Assignment rules 3%
