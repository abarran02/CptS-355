-- CptS 355 - Lab 2 (Haskell) - Spring 2023
-- Name: Alec Barran
-- Collaborated with: 

module Lab2
     where

-- 1
{- (a) merge2 -}
merge2 :: [a] -> [a] -> [a]
-- base cases
merge2 [] iL2 = iL2
merge2 iL1 [] = iL1
merge2 (x:xs) (y:ys) = (x:y: (merge2 xs ys))

{- (b) merge2Tail -}
merge2Tail :: [a] -> [a] -> [a]
-- pass to helper function with empty buffer to use tail recursion
merge2Tail iL1 iL2 = merge2TailAux iL1 iL2 []
     -- adding to front of buffer requires reverse at last step
     where merge2TailAux [] [] buf = reverse buf
           -- continue recursion with single list
           merge2TailAux [] (y:ys) buf = merge2TailAux [] ys (y:buf)
           merge2TailAux (x:xs) [] buf = merge2TailAux xs [] (x:buf)
           -- recursion with both lists, add to front of buffer
           merge2TailAux (x:xs) (y:ys) buf = merge2TailAux xs ys (y:x:buf)

{- (c) mergeN -}
mergeN :: [[a]] -> [a]
mergeN list = foldl merge2 [] list

-- 2
{- (a) count -}
count :: Eq a => a -> [a] -> Int
-- filter to condense list down to only matching items, and return length
count item list = length $ filter (==item) list

{- (b) histogram  -}
histogram :: Eq a => [a] -> [(a, Int)]
histogram list = map (\item -> (item, count item list)) (eliminateDuplicates [] list)
     where eliminateDuplicates y [] = y
           eliminateDuplicates [] (x:xs) = eliminateDuplicates [x] xs
           eliminateDuplicates y (x:xs) = if x `elem` y then eliminateDuplicates y xs 
                                          else eliminateDuplicates (x:y) xs

-- 3                
{- (a) concatAll -}
concatAll :: [[String]] -> String
-- map concat into all sublists
-- then concat result of all sublists
concatAll list = concat' $ map (concat') list
     where concat' l = foldr (++) [] l

{- (b) concat2Either -}               
data AnEither  = AString String | AnInt Int
                deriving (Show, Read, Eq)

concat2Either:: [[AnEither]] -> AnEither
concat2Either list = concat' $ map (concat') list
     where concat' l = foldr (convert) (AString "") l
           convert (AString x) (AnInt y) = AString(x ++ (show y))
           convert (AString x) (AString y) = AString(x ++ y)
           convert (AnInt x) (AString y) = AString((show x) ++ y) 

-- 4      
{-  concat2Str -}
concat2Str:: [[AnEither]] -> String
concat2Str list = foldr convert "" $ concat list
     where concat l = foldr (++) [] l
           convert (AString x) y = (x ++ y)
           convert (AnInt x) y = (show(x) ++ y)

-- 5 
{- evaluateTree -}
data Op = Add | Sub | Mul | Pow
          deriving (Show, Read, Eq)

evaluate:: Op -> Int -> Int -> Int
evaluate Add x y =  x+y
evaluate Sub x y =  x-y
evaluate Mul x y =  x*y
evaluate Pow x y =  x^y

data ExprTree a = ELEAF a | ENODE Op (ExprTree a) (ExprTree a)
                  deriving (Show, Read, Eq)

evaluateTree :: ExprTree Int -> Int
evaluateTree (ELEAF x) = x
evaluateTree (ENODE p x y) = evaluate p (evaluateTree x) (evaluateTree y)

-- 6
{- printInfix -}
printInfix:: Show a => ExprTree a -> String
printInfix (ELEAF x) = show x
printInfix (ENODE p x y) = "(" ++ (printInfix x) ++ " `" ++ (show p) ++ "` " ++ (printInfix y) ++ ")"

--7
{- createRTree -}
data ResultTree a  = RLEAF a | RNODE a (ResultTree a) (ResultTree a)
                     deriving (Show, Read, Eq)

createRTree :: ExprTree Int -> ResultTree Int 
createRTree (ELEAF x) = (RLEAF x)
-- obviously the time complexity of this solution is awful, but it works
createRTree (ENODE p x y) = RNODE (evaluateTree (ENODE p x y)) (createRTree x) (createRTree y)
