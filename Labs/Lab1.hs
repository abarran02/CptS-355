-- CptS 355 - Lab 1 (Haskell) - Spring 2023
-- Name: Alec Barran

module Lab1
     where

-- 1.insert 
insert :: (Eq t1, Num t1) => t1 -> t2 -> [t2] -> [t2]
insert 0 item [] = [item]
insert n item [] = []
insert n item (x:xs) | n == 0 = (item:x:xs)
                     | otherwise = (x: insert (n-1) item xs)

-- 2. insertEvery
insertEvery :: (Eq t, Num t) => t -> a -> [a] -> [a]
insertEvery n item xs = counter n xs 
     where counter 0 xs = item:counter n xs
           counter _ [] = []
           counter m (x:xs) = x:counter (m-1) xs

-- 3. getSales
getSales :: (Num p, Eq t) => t -> [(t, p)] -> p
getSales day [] = 0
getSales day ((x,y):xs) | day == x = y + getSales day xs
                        | otherwise = getSales day xs
                                                  
-- 4. sumSales
sumSales:: (Num p) => String -> String -> [(String,[(String,p)])] -> p
sumSales store day [] = 0
sumSales store day ((name,log):xs) | name == store = (sumSales store day xs) + (getSales day log)
                                   | otherwise = sumSales store day xs

-- 5. split
split :: Eq a => a -> [a] -> [[a]]
split _ [] = []
split c (x:xs) = splitHelper c (x:xs) []
     where splitHelper c [] buffer | buffer == [] = []
                                   | otherwise = ((reverse buffer):[])
           splitHelper c (x:xs) buffer | c == x = ((reverse buffer): splitHelper c xs [])
                                       | otherwise = splitHelper c xs (x:buffer)

-- 6. nSplit
nSplit :: (Ord a1, Num a1, Eq a2) => a2 -> a1 -> [a2] -> [[a2]]
nSplit c n [] = [[]]
nSplit c 0 (x:xs) = [x:xs]
nSplit c n (x:xs) | c == x = []:(rear (n-1))
                  | otherwise = (x: (head (rear n))):(tail (rear n))
    where rear m = nSplit c m xs
