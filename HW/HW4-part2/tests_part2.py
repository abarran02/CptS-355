import unittest
from psparser import read
from psexpressions import  Literal, PSName, PSString, PSCodeArray, StringValue, DictionaryValue, CodeArrayValue
from psoperators import PSOperators

class HW4Part2Tests(unittest.TestCase):

    def setUp(self):
        #create the Stack object
        self.ps_env = PSOperators()
        #clear the opstack and the dictstack
        self.ps_env.clearBoth() 
        self.ps_env.dictstack.append({})
        self.opstack_output= {
            'test1': [6, 2], 
            'test2': [True, True, True, True, False], 
            'test3': [1, 10], 
            'test4': [10, 1], 
            'test5': [100, 10, 1], 
            'test6': [2, 2], 
            'test7': [StringValue('(P\x00\x00)')], 
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
            'test32': [StringValue('(WSU)')],
            'test33': [8, 243],
            'test34': [True, False],
            'test35': [35, 5],
            'test36': [True],
            'test37': [StringValue('(wsu)')]}

    def compareObjectData(self,obj1,obj2):
        if type(obj1) != type(obj2):
            return False
        if isinstance(obj1,Literal):
            return obj1.value == obj2.value
        elif  isinstance(obj1,PSString):
            return obj1.value == obj2.value
        elif isinstance(obj1,PSCodeArray):
            for i in range(0,len(obj1.value)):
                if self.compareObjectData(obj1.value[i],obj2.value[i])== False:
                    return False
            return True
        elif isinstance(obj1,PSName):
            return obj1.var_name == obj2.var_name
        elif isinstance(obj1,StringValue):
            return obj1.value == obj2.value
        elif isinstance(obj1,DictionaryValue):
            for key in obj1.value.keys():
                if self.compareObjectData(obj1.value[key],obj2.value[key])== False:
                    return False
            return True
        elif isinstance(obj1,CodeArrayValue) :
            for i in range(0,len(obj1.value)):
                if self.compareObjectData(obj1.value[i],obj2.value[i])== False:
                    return False
            return True
        else:
            return obj1 == obj2

    def test_input1(self):
        testinput1 = """
            10 -2 add
            5 sub
            2 mul 
            20 3 mod
        """ 
        test_case = 'test{}'.format(1)
        expr_list = read(testinput1)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input2(self):
        testinput2 = """
            10 20 lt
            20 15 gt
            (WSU) (WSU) eq
            (Go) dup eq 
            (Cougs) (cougs) eq
        """
        test_case = 'test{}'.format(2)
        expr_list = read(testinput2)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input3(self):
            testinput3 = """
                /x 1 def
                x
                /x 10 def
                x
            """
            test_case = 'test{}'.format(3)
            expr_list = read(testinput3)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input4(self):
            testinput4 = """
                /x 1 def
                1 dict begin /x 10 def x end
                x
            """
            test_case = 'test{}'.format(4)
            expr_list = read(testinput4)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input5(self):
            testinput5 = """
                /x 1 def
                1 dict begin /x 10 def  
                    1 dict begin /x 100 def x end 
                    x 
                end
                x
            """
            test_case = 'test{}'.format(5)
            expr_list = read(testinput5)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input6(self):
            testinput6 = """
                /x 1 def
                /y 2 def
                1 dict begin /x 10 def  
                    1 dict begin /x 100 def y end 
                    y
                end
            """
            test_case = 'test{}'.format(6)
            expr_list = read(testinput6)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input7(self):
            testinput7 = """
                3 string dup 
                0 80 put
            """
            test_case = 'test{}'.format(7)
            expr_list = read(testinput7)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input8(self):
            testinput8 = """
                3 string dup dup dup
                0 80 put
                1 81 put
                2 83 put
            """
            test_case = 'test{}'.format(8)
            expr_list = read(testinput8)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input9(self):
            testinput9 = """
                /s (WSU Cougs) def
                s length
                s 0 3 getinterval
                length
            """
            test_case = 'test{}'.format(9)
            expr_list = read(testinput9)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input10(self):
            testinput10 = """
                (CptS 355) dup 5 (451) putinterval
                dup 5 get
            """
            test_case = 'test{}'.format(10)
            expr_list = read(testinput10)
            for expr in expr_list:
                expr.eval(self.ps_env)
            self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input11(self):
        testinput11 = """
            /myd 1 dict def
            myd
        """
        test_case = 'test{}'.format(11)
        expr_list = read(testinput11)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input12(self):
        testinput12 = """
            /myd 1 dict def
            myd
            myd 1 (one) put
            myd 2 (two) put
        """
        test_case = 'test{}'.format(12)
        expr_list = read(testinput12)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input13(self):
        testinput13 = """
            /myd 1 dict def
            myd /x 1 put
            myd /y 2 put
            myd /x 10 put 
            myd /y get 
            myd /x get 
            myd
        """
        test_case = 'test{}'.format(13)
        expr_list = read(testinput13)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input14(self):
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
        test_case = 'test{}'.format(14)
        expr_list = read(testinput14)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input15(self):
        testinput15 = """
            (355,322,451) (,) search 
        """
        test_case = 'test{}'.format(15)
        expr_list = read(testinput15)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input16(self):
        testinput16 = """
           (355,322,451) (0) search
        """ 
        test_case = 'test{}'.format(16)
        expr_list = read(testinput16)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input17(self):
        testinput17 = """
            (WSU) dup /str exch def 
            (WSU) str eq
        """ 
        test_case = 'test{}'.format(17)
        expr_list = read(testinput17)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input18(self):
        testinput18 = """
             1 2 3 4 5 3 copy count 
        """ 
        test_case = 'test{}'.format(18)
        expr_list = read(testinput18)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input19(self):
        testinput19 = """
            /isNeg { 0 lt } def  -5 dup isNeg { -1 mul } if
        """ 
        test_case = 'test{}'.format(19)
        expr_list = read(testinput19)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input20(self):
        testinput20 = """
            /isNeg { 0 lt } def  -1 dup isNeg { -2 mul } { 3 mul} ifelse
        """ 
        test_case = 'test{}'.format(20)
        expr_list = read(testinput20)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input21(self):
        testinput21 = """
            1 1 5 {  } for 
        """ 
        test_case = 'test{}'.format(21)
        expr_list = read(testinput21)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input22(self):
        testinput22 = """
            2 2 8 {2 mul } for 
        """ 
        test_case = 'test{}'.format(22)
        expr_list = read(testinput22)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input23(self):
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
        test_case = 'test{}'.format(23)
        expr_list = read(testinput23)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input24(self):
        testinput24 = """
            /x 1 def
            /y 2 def
            /x 10 def
            /y 20 def
            0 x 1 y {add} for
        """ 
        test_case = 'test{}'.format(24)
        expr_list = read(testinput24)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input25(self):
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
        test_case = 'test{}'.format(25)
        expr_list = read(testinput25)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input26(self):
        testinput26 = """
            /x 1 def
            /y 2 def
            1 dict begin
                /x 10 def
                1 dict 
                    begin /y 3 def x y end
                /y 20 def
                x y
            end
            x y
        """ 
        test_case = 'test{}'.format(26)
        expr_list = read(testinput26)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input27(self):
        testinput27 = """
            1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
        """ 
        test_case = 'test{}'.format(27)
        expr_list = read(testinput27)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input28(self):
        testinput28 = """
            /first (CptS355 and CptS451) def
            /second (CptS321 and CptS322) def
            /cpy {  4 3 getinterval /str exch def 
                    16 str putinterval } def
            first second cpy
            second first cpy
            first second
        """ 
        test_case = 'test{}'.format(28)
        expr_list = read(testinput28)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input29(self):
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
        test_case = 'test{}'.format(29)
        expr_list = read(testinput29)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input30(self):
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
        test_case = 'test{}'.format(30)
        expr_list = read(testinput30)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input31(self):
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
        test_case = 'test{}'.format(31)
        expr_list = read(testinput31)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_input32(self):
        testinput32 = """
            3 string 
            dup
            0 87 put
            dup
            1 83 put
            dup 
            2 85 put
        """ 
        test_case = 'test{}'.format(32)
        expr_list = read(testinput32)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_myinput1(self):
        my_input1 = """
            /exp {
                0 dict
                begin
                    /base exch def
                    /n exch def
                    1
                    n -1 1 { pop base mul } for
                end
            } def
            3 2 exp
            5 3 exp
        """
        test_case = 'test{}'.format(33)
        expr_list = read(my_input1)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))
    
    def test_myinput2(self):
        my_input2 = """
            /even {
                2 mod 0 eq
            } def
            16 even
            3 even
        """
        test_case = 'test{}'.format(34)
        expr_list = read(my_input2)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))
    
    def test_myinput3(self):
        my_input3 = """
            /abs {
                0 dict begin
                /n exch def
                n 0 gt
                { n }
                { n -1 mul }
                ifelse
                end
            } def
            -35 abs
            5 abs
        """
        test_case = 'test{}'.format(35)
        expr_list = read(my_input3)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))
    
    def test_myinput4(self):
        my_input4 = """
            /and {
                {
                    { 1 0 gt }
                    { pop -1 0 gt }
                    ifelse
                }
                { pop -1 0 gt }
                ifelse
            } def
            1 0 gt
            1 0 gt
            and
        """
        test_case = 'test{}'.format(36)
        expr_list = read(my_input4)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

    def test_myinput5(self):
        my_input4 = """
            3 string dup 
            0 119 put dup
            1 115 put dup
            2 117 put
        """
        test_case = 'test{}'.format(37)
        expr_list = read(my_input4)
        for expr in expr_list:
            expr.eval(self.ps_env)
        self.assertEqual(len(self.ps_env.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.ps_env.opstack[i], self.opstack_output[test_case][i]))

if __name__ == '__main__':
    unittest.main()

