import sys

from psparser import read
from psoperators import PSOperators
from psexpressions import StringValue, DictionaryValue, Literal, PSName, PSString
from colors import *

# Postscript examples that use arithmetic operators. 
testinput1 = """
    10 -2 add
    5 sub
    2 mul 
    20 3 mod
"""
#opstack : [6, 2]

# Postscript examples that use comparison operators. 
testinput2 = """
    10 20 lt
    20 15 gt
    (WSU) (WSU) eq
    (Go) dup eq 
    (Cougs) (cougs) eq
"""
# opstack : [True, True, True, True, False]

# Postscript examples that use def, dict, begin, end
testinput3 = """
    /x 1 def
    x
    /x 10 def
    x
"""
# opstack : [1, 10]

testinput4 = """
    /x 1 def
    1 dict begin /x 10 def x end
    x
"""
# opstack : [10, 1]

testinput5 = """
    /x 1 def
    1 dict begin /x 10 def  
        1 dict begin /x 100 def x end 
        x 
    end
    x
"""
# opstack : [100, 10, 1]

testinput6 = """
    /x 1 def
    /y 2 def
    1 dict begin /x 10 def  
        1 dict begin /x 100 def y end 
        y
    end
"""
# opstack : [2, 2]


# Postscript examples that use string operators. 

#test string creation
testinput7 = """
    3 string dup 
    0 80 put
"""
# opstack :  [StringValue('(P)')]   --  i.e.,  [StringValue('(P\x00\x00)')] where \x00 is the ASCII NUL character

#test string creation
testinput8 = """
    3 string dup dup dup
    0 80 put
    1 81 put
    2 83 put
"""
# opstack : [StringValue('(PQS)')]   

testinput9 = """
    /s (WSU Cougs) def
    s length
    s 0 3 getinterval
    length
"""
# opstack : [9, 3]

testinput10 = """
     (CptS 355) dup 5 (451) putinterval
     dup 5 get
"""
# opstack : [StringValue('(CptS 451)'), 52]

# Postscript examples that use dictionary operators. 

#test string creation
testinput11 = """
    /myd 1 dict def
    myd
"""
# opstack : [DictionaryValue({})]

#test string creation
testinput12 = """
    /myd 1 dict def
    myd
    myd 1 (one) put
    myd 2 (two) put
"""
# opstack : [DictionaryValue({1: StringValue('(one)'), 2: StringValue('(two)')})]

testinput13 = """
    /myd 1 dict def
    myd /x 1 put
    myd /y 2 put
    myd /x 10 put 
    myd /y get 
    myd /x get 
    myd
"""
# opstack : [2, 10, DictionaryValue({'/x': 10, '/y': 2})]

testinput14 = """
    /myd 1 dict def
    myd /x 10 put
    myd /y 20 put
    myd
    begin
    x 
    y 
    myd
"""
# opstack : [10, 20, DictionaryValue({'/x': 10, '/y': 20})]

testinput15 = """
    (355,322,451) (,) search 
"""
# opstack :  [StringValue('(322,451)'), StringValue('(,)'), StringValue('(355 )'), True]  

testinput16 = """
    (355,322,451) (0) search 
"""
# opstack : [StringValue('(355 ,322,451)'), False] 

# Postscript examples that use stack manipulation operators. 

testinput17 = """
     (WSU) dup /str exch def 
     (WSU) str eq
"""
# opstack : [StringValue('(WSU)'), True]

testinput18 = """
     1 2 3 4 5 3 copy count 
"""
# opstack : [1, 2, 3, 4, 5, 3, 4, 5, 8]


testinput19 = """
    /isNeg { 0 lt } def  -5 dup isNeg { -1 mul } if
"""
# opstack : [5]

testinput20 = """
    /isNeg { 0 lt } def  -1 dup isNeg { -2 mul } { 3 mul} ifelse
"""
#opstack : [2]

testinput21 = """
    1 1 5 {  } for 
"""
#opstack : [1, 2, 3, 4, 5]

testinput22 = """
    2 2 8 {2 mul } for 
"""
#opstack : [4, 8, 12, 16]

testinput23 = """
    /square {dup mul} def
    /mydict 1 dict def
    mydict /in 1 put 
    mydict /out 100 put
    mydict /in 10 put
    mydict /in get 
    square  
    mydict /out get
    eq 
    {(equal)} {(different)} ifelse
"""
#opstack :[StringValue('(equal)')]

testinput24 = """
    /x 1 def
    /y 2 def
    /x 10 def
    /y 20 def
    0 x 1 y {add} for
"""
#opstack :[165]

testinput25 = """
    /x 1 def
    /y 2 def
    /myd 1 dict def
    myd /x 10 put 
    myd /y 20 put
    myd begin
    x y mul
    end 
    x y mul 
"""
#opstack : [200, 2]

testinput26 = """
    /x 1 def
    /y 2 def
    1 dict begin
    /x 10 def
    1 dict begin /y 3 def x y end
    /y 20 def
    x y
    end
    x y
"""
#opstack : [10, 3, 10, 20, 1, 2]

testinput27 = """
        1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
"""
#opstack : [1, 2, 3, 4, 5, True]

testinput28 = """
    /first (CptS355 and CptS451) def
    /second (CptS321 and CptS322) def
    /cpy {  4 3 getinterval /str exch def 
            16 str putinterval } def
    first second cpy
    second first cpy
    first second 
"""   
#opstack : [StringValue('(CptS355 and CptS321)'), StringValue('(CptS321 and CptS355)')]
#    
testinput29 = """
    (WSU)
    dup dup dup 
    0 get 87 eq 
        {
            1 get 83 eq 
            { 
                2 get 85 eq 
                { (Go Cougs) }
                if
            } if
        } if
"""
#opstack : [StringValue('(WSU)'), StringValue('(Go Cougs)')]

testinput30 = """
        /n 5 def
        /fact {
            0 dict begin
            /n exch def
            n 2 lt
            { 1}
            {n 1 sub fact n mul }
            ifelse
            end
        } def
        n fact
"""
#opstack : [120]

testinput31 = """
    /fact {
            0 dict
            begin
                /n exch def
                1
                n -1 1 { mul /n n 1 sub def } for 
            end
        } def
        6 fact
"""
#opstack :  [720]

testinput32 = """
    3 string 
    dup
    0 87 put
    dup
    1 83 put
    dup 
    2 85 put  
    """
#opstack : [StringValue('(WSU)')]

tests = [testinput1,testinput2,testinput3,testinput4,testinput5,testinput6,testinput7,testinput8,testinput9,testinput10,
         testinput11,testinput12,testinput13,testinput14,testinput15,testinput16,testinput17,testinput18,testinput19,testinput20,testinput21,
         testinput22,testinput23,testinput24,testinput25,testinput26,testinput27,testinput28,testinput29,testinput30,testinput31,testinput32]

opstack = {
    'test1': [6, 2], 
    'test2': [True, True, True, True, False], 
    'test3': [1, 10], 
    'test4': [10, 1], 
    'test5': [100, 10, 1], 
    'test6': [2, 2], 
    'test7': [StringValue('(P)')], 
    'test8': [StringValue('(PQS)')], 
    'test9': [9, 3], 
    'test10': [StringValue('(CptS 451)'), 52], 
    'test11': [DictionaryValue({})], 
    'test12': [DictionaryValue({1: StringValue('(one)'), 2: StringValue('(two)')})], 
    'test13': [2, 10, DictionaryValue({'/x': 10, '/y': 2})], 
    'test14': [10, 20, DictionaryValue({'/x': 10, '/y': 20})], 
    'test15': [StringValue('(322,451)'), StringValue('(,)'), StringValue('(355 )'), True], 
    'test16': [StringValue('(355 ,322,451)'), False], 
    'test17': [StringValue('(WSU)'), True], 
    'test18': [1, 2, 3, 4, 5, 3, 4, 5, 8], 
    'test19': [5], 
    'test20': [2], 
    'test21': [1, 2, 3, 4, 5], 
    'test22': [4, 8, 12, 16], 
    'test23': [StringValue('(equal)')], 
    'test24': [165], 
    'test25': [200, 2], 
    'test26': [10, 3, 10, 20, 1, 2], 
    'test27': [1, 2, 3, 4, 5, True], 
    'test28': [StringValue('(CptS355 and CptS321)'), StringValue('(CptS321 and CptS355)')], 
    'test29': [StringValue('(WSU)'), StringValue('(Go Cougs)')], 
    'test30': [120], 
    'test31': [720], 
    'test32': [StringValue('(WSU)')]}

"""
parse output = {
    'test1': [Literal(10), Literal(-2), PSName(add), Literal(5), PSName(sub), Literal(2), PSName(mul), Literal(20), Literal(3), PSName(mod)], 
    'test2': [Literal(10), Literal(20), PSName(lt), Literal(20), Literal(15), PSName(gt), PSString((WSU)), PSString((WSU)), PSName(eq), PSString((Go)), PSName(dup), PSName(eq), PSString((Cougs)), PSString((cougs)), PSName(eq)], 
    'test3': [PSName(/x), Literal(1), PSName(def), PSName(x), PSName(/x), Literal(10), PSName(def), PSName(x)], 
    'test4': [PSName(/x), Literal(1), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(10), PSName(def), PSName(x), PSName(end), PSName(x)], 
    'test5': [PSName(/x), Literal(1), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(10), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(100), PSName(def), PSName(x), PSName(end), PSName(x), PSName(end), PSName(x)], 
    'test6': [PSName(/x), Literal(1), PSName(def), PSName(/y), Literal(2), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(10), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(100), PSName(def), PSName(y), PSName(end), PSName(y), PSName(end)], 
    'test7': [Literal(3), PSName(string), PSName(dup), Literal(0), Literal(80), PSName(put)], 
    'test8': [Literal(3), PSName(string), PSName(dup), PSName(dup), PSName(dup), Literal(0), Literal(80), PSName(put), Literal(1), Literal(81), PSName(put), Literal(2), Literal(83), PSName(put)], 
    'test9': [PSName(/s), PSString((WSU Cougs)), PSName(def), PSName(s), PSName(length), PSName(s), Literal(0), Literal(3), PSName(getinterval), PSName(length)], 
    'test10': [PSString((CptS 355)), PSName(dup), Literal(5), PSString((451)), PSName(putinterval), PSName(dup), Literal(5), PSName(get)], 
    'test11': [PSName(/myd), Literal(1), PSName(dict), PSName(def), PSName(myd)], 
    'test12': [PSName(/myd), Literal(1), PSName(dict), PSName(def), PSName(myd), PSName(myd), Literal(1), PSString((one)), PSName(put), PSName(myd), Literal(2), PSString((two)), PSName(put)], 
    'test13': [PSName(/myd), Literal(1), PSName(dict), PSName(def), PSName(myd), PSName(/x), Literal(1), PSName(put), PSName(myd), PSName(/y), Literal(2), PSName(put), PSName(myd), PSName(/x), Literal(10), PSName(put), PSName(myd), PSName(/y), PSName(get), PSName(myd), PSName(/x), PSName(get), PSName(myd)], 
    'test14': [PSName(/myd), Literal(1), PSName(dict), PSName(def), PSName(myd), PSName(/x), Literal(10), PSName(put), PSName(myd), PSName(/y), Literal(20), PSName(put), PSName(myd), PSName(begin), PSName(x), PSName(y), PSName(myd)], 
    'test15': [PSString((355 ,322,451)), PSString((,)), PSName(search)], 
    'test16': [PSString((355 ,322,451)), PSString((0)), PSName(search)], 
    'test17': [PSString((WSU)), PSName(dup), PSName(/str), PSName(exch), PSName(def), PSString((WSU)), PSName(str), PSName(eq)], 
    'test18': [Literal(1), Literal(2), Literal(3), Literal(4), Literal(5), Literal(3), PSName(copy), PSName(count)], 
    'test19': [PSName(/isNeg), PSCodeArray([Literal(0), PSName(lt)]), PSName(def), Literal(-5), PSName(dup), PSName(isNeg), PSCodeArray([Literal(-1), PSName(mul)]), PSName(if)], 
    'test20': [PSName(/isNeg), PSCodeArray([Literal(0), PSName(lt)]), PSName(def), Literal(-1), PSName(dup), PSName(isNeg), PSCodeArray([Literal(-2), PSName(mul)]), PSCodeArray([Literal(3), PSName(mul)]), PSName(ifelse)], 
    'test21': [Literal(1), Literal(1), Literal(5), PSCodeArray([]), PSName(for)], 
    'test22': [Literal(2), Literal(2), Literal(8), PSCodeArray([Literal(2), PSName(mul)]), PSName(for)], 
    'test23': [PSName(/square), PSCodeArray([PSName(dup), PSName(mul)]), PSName(def), PSName(/mydict), Literal(1), PSName(dict), PSName(def), PSName(mydict), PSName(/in), Literal(1), PSName(put), PSName(mydict), PSName(/out), Literal(100), PSName(put), PSName(mydict), PSName(/in), Literal(10), PSName(put), PSName(mydict), PSName(/in), PSName(get), PSName(square), PSName(mydict), PSName(/out), PSName(get), PSName(eq), PSCodeArray([PSString((equal))]), PSCodeArray([PSString((different))]), PSName(ifelse)], 
    'test24': [PSName(/x), Literal(1), PSName(def), PSName(/y), Literal(2), PSName(def), PSName(/x), Literal(10), PSName(def), PSName(/y), Literal(20), PSName(def), Literal(0), PSName(x), Literal(1), PSName(y), PSCodeArray([PSName(add)]), PSName(for)], 
    'test25': [PSName(/x), Literal(1), PSName(def), PSName(/y), Literal(2), PSName(def), PSName(/myd), Literal(1), PSName(dict), PSName(def), PSName(myd), PSName(/x), Literal(10), PSName(put), PSName(myd), PSName(/y), Literal(20), PSName(put), PSName(myd), PSName(begin), PSName(x), PSName(y), PSName(mul), PSName(end), PSName(x), PSName(y), PSName(mul)], 
    'test26': [PSName(/x), Literal(1), PSName(def), PSName(/y), Literal(2), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/x), Literal(10), PSName(def), Literal(1), PSName(dict), PSName(begin), PSName(/y), Literal(3), PSName(def), PSName(x), PSName(y), PSName(end), PSName(/y), Literal(20), PSName(def), PSName(x), PSName(y), PSName(end), PSName(x), PSName(y)], 
    'test27': [Literal(1), Literal(2), Literal(3), Literal(4), Literal(5), PSName(count), PSName(copy), Literal(15), Literal(1), Literal(1), Literal(5), PSCodeArray([PSName(pop), PSName(exch), PSName(sub)]), PSName(for), Literal(0), PSName(eq)], 
    'test28': [PSName(/first), PSString((CptS355 and CptS451)), PSName(def), PSName(/second), PSString((CptS321 and CptS322)), PSName(def), PSName(/cpy), PSCodeArray([Literal(4), Literal(3), PSName(getinterval), PSName(/str), PSName(exch), PSName(def), Literal(16), PSName(str), PSName(putinterval)]), PSName(def), PSName(first), PSName(second), PSName(cpy), PSName(second), PSName(first), PSName(cpy), PSName(first), PSName(second)], 
    'test29': [PSString((WSU)), PSName(dup), PSName(dup), PSName(dup), Literal(0), PSName(get), Literal(87), PSName(eq), PSCodeArray([Literal(1), PSName(get), Literal(83), PSName(eq), PSCodeArray([Literal(2), PSName(get), Literal(85), PSName(eq), PSCodeArray([PSString((Go Cougs))]), PSName(if)]), PSName(if)]), PSName(if)], 
    'test30': [PSName(/n), Literal(5), PSName(def), PSName(/fact), PSCodeArray([Literal(0), PSName(dict), PSName(begin), PSName(/n), PSName(exch), PSName(def), PSName(n), Literal(2), PSName(lt), PSCodeArray([Literal(1)]), PSCodeArray([PSName(n), Literal(1), PSName(sub), PSName(fact), PSName(n), PSName(mul)]), PSName(ifelse), PSName(end)]), PSName(def), PSName(n), PSName(fact)], 
    'test31': [PSName(/fact), PSCodeArray([Literal(0), PSName(dict), PSName(begin), PSName(/n), PSName(exch), PSName(def), Literal(1), PSName(n), Literal(-1), Literal(1), PSCodeArray([PSName(mul), PSName(/n), PSName(n), Literal(1), PSName(sub), PSName(def)]), PSName(for), PSName(end)]), PSName(def), Literal(6), PSName(fact)], 
    'test32': [Literal(3), PSName(string), PSName(dup), Literal(0), Literal(87), PSName(put), PSName(dup), Literal(1), Literal(83), PSName(put), PSName(dup), Literal(2), Literal(85), PSName(put)]}
"""

from copy import deepcopy
# program start
if __name__ == '__main__':

    ps_env = PSOperators()  
    testnum = 1
    for testcase in tests:
        print("--------------------------------------------------------")
        try:
            expr_list = read(testcase)
            for expr in expr_list:
                expr.eval(ps_env)
            print("--test {}--".format(testnum))
            testnum += 1
            print(CYAN+'opstack '+CEND, ps_env.opstack)
            print('dictstack ' , ps_env.dictstack)
            ps_env.clearBoth()
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
            ps_env.clearBoth()
    