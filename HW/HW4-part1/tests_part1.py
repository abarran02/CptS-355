from psoperators import PSOperators
from psexpressions import StringValue, DictionaryValue
import unittest

class HW4Part1Tests(unittest.TestCase):
    def setUp(self):
        #create the Stack object
        self.ps_env = PSOperators()
        #clear the opstack and the dictstack
        self.ps_env.clearBoth() 

    # Tests for helper functions : define, lookup   
    def test_lookup1(self):
        self.ps_env.dictPush({'/v':3, '/x': 20})
        self.ps_env.dictPush({'/v':4, '/x': 10})
        self.ps_env.dictPush({'/v':5})
        self.assertEqual(self.ps_env.lookup('x'),10)
        self.assertEqual(self.ps_env.lookup('v'),5)

    def testLookup2(self):
        self.ps_env.dictPush({'/a':'(355)'})
        s = StringValue('(355)')
        self.ps_env.dictPush({'/a':s})
        self.assertTrue(self.ps_env.lookup("a") is s)
        self.assertEqual(self.ps_env.lookup("a").value,s.value)

    def test_define1(self):
        self.ps_env.dictPush({})
        self.ps_env.define("/n1", 4)
        self.assertEqual(self.ps_env.lookup("n1"),4)

    def test_define2(self):
        self.ps_env.dictPush({})
        self.ps_env.define("/n1", 4)
        self.ps_env.define("/n1", 5)
        self.ps_env.define("/n2", 6)
        self.assertEqual(self.ps_env.lookup("n1"),5)
        self.assertEqual(self.ps_env.lookup("n2"),6)        

    def test_define3(self):
        self.ps_env.dictPush({})
        self.ps_env.define("/n1", 4)
        self.ps_env.dictPush({})
        self.ps_env.define("/n2", 6)
        self.ps_env.define("/n2", 7)
        self.ps_env.dictPush({})
        self.ps_env.define("/n1", 6)
        self.assertEqual(self.ps_env.lookup("n1"),6)
        self.assertEqual(self.ps_env.lookup("n2"),7)    
    #-----------------------------------------------------
    #Arithmatic operator tests
    def test_add(self):
        #9 3 add
        self.ps_env.opPush(9)
        self.ps_env.opPush(3)
        self.ps_env.add()
        self.assertEqual(self.ps_env.opPop(),12)

    def test_sub(self):
        #10 2 sub
        self.ps_env.opPush(10)
        self.ps_env.opPush(2)
        self.ps_env.sub()
        self.assertEqual(self.ps_env.opPop(),8)

    def test_mul(self):
        #2 40 mul
        self.ps_env.opPush(2)
        self.ps_env.opPush(40)
        self.ps_env.mul()
        self.assertEqual(self.ps_env.opPop(),80)

    def test_mod(self):
        #20 3 mod
        self.ps_env.opPush(20)
        self.ps_env.opPush(3)
        self.ps_env.mod()
        self.assertEqual(self.ps_env.opPop(),2)

    #-----------------------------------------------------
    #Comparison operators tests
    def test_eq1(self):
        #6 6 eq
        self.ps_env.opPush(6)
        self.ps_env.opPush(6)
        self.ps_env.eq()
        self.assertEqual(self.ps_env.opPop(),True)

    def test_eq2(self):
        # (WSU) (WSU) eq
        #compare values
        self.ps_env.opPush(StringValue('(WSU)'))
        self.ps_env.opPush(StringValue('(WSU)'))
        self.ps_env.eq()
        self.assertEqual(self.ps_env.opPop(),True)
        #compare objects
        s = StringValue('(WSU)')
        self.ps_env.opPush(s)
        self.ps_env.opPush(s)
        self.ps_env.eq()
        self.assertEqual(self.ps_env.opPop(),True)

    def test_eq3(self):
        # 1 dict  2 dict 
        #compare objects
        d1 = DictionaryValue({})
        self.ps_env.opPush(d1)
        d2 = DictionaryValue({})
        self.ps_env.opPush(d2)
        self.ps_env.eq()
        self.assertEqual(self.ps_env.opPop(),False)
        self.ps_env.opPush(d1)
        #duplicate the object
        self.ps_env.dup()
        self.ps_env.eq()
        self.assertEqual(self.ps_env.opPop(),True)
    
    def test_lt(self):
        #3 6 lt
        self.ps_env.opPush(3)
        self.ps_env.opPush(6)
        self.ps_env.lt()
        self.assertEqual(self.ps_env.opPop(),True)

    def test_gt(self):
        #4 5 gt
        self.ps_env.opPush(4)
        self.ps_env.opPush(5)
        self.ps_env.gt()
        self.assertEqual(self.ps_env.opPop(),False)

    #-----------------------------------------------------
    #String operator tests
    def test_string(self):
        # 3 string 
        self.ps_env.opPush(3)
        self.ps_env.string()
        d = self.ps_env.opPop() # pop the StringValue value
        self.assertEqual(d.value,'(\x00\x00\x00)')  #the characters in the StringValue's value should be initialized to '\0' , ascii NUL
        self.assertTrue(len(self.ps_env.opstack)==0)  

    def test_length_StrConstant(self):
        #(CptS355) length
        self.ps_env.opPush(StringValue('(CptS355)'))
        self.ps_env.length()
        self.assertEqual(self.ps_env.opPop(),7)      
        self.assertTrue(len(self.ps_env.opstack)==0) 
        #length will not push back the StringValue onto the opstack      

    def test_get_StrConstant(self):
        #(CptS355) 3 get
        self.ps_env.opPush(StringValue('(CptS355)'))
        self.ps_env.opPush(3)
        self.ps_env.get()
        self.assertEqual(self.ps_env.opPop(),83)
        self.assertTrue(len(self.ps_env.opstack)==0)
        #get will not push back the StringValue onto the opstack   

    def test_put_StrConstant1(self):
        #(CptS451) dup 4 51 put 
        str1 = StringValue('(CptS451)')
        self.ps_env.opPush(str1)
        self.ps_env.dup()  #duplicating the StringValue reference
        self.ps_env.opPush(4)
        self.ps_env.opPush(51)  # ascii value for '3'
        self.ps_env.put()  #put will not push back the changed StringValue onto the opstack 
        str2 = self.ps_env.opPop()
        self.assertTrue(str2 is str1)  #we pop the StringValue reference we copied with "dup"; check if it the same object
        self.assertEqual(str2.value,'(CptS351)')  #we check if the StringValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #put will not push back the original StringValue onto the opstack 

    def test_put_StrConstant2(self):
        #/x (CptS321) def x 6 50 put x
        str1 = StringValue('(CptS321)')
        self.ps_env.opPush('/x')
        self.ps_env.opPush(str1)
        self.ps_env.psDef()  #defines x; x holds the StringValue reference
        self.ps_env.opPush(self.ps_env.lookup('x'))
        self.ps_env.opPush(6)
        self.ps_env.opPush(50)  # ascii value for '1'
        self.ps_env.put()  #put will not push back the changed StringValue onto the opstack 
        self.ps_env.opPush(self.ps_env.lookup('x'))
        str2 = self.ps_env.opPop()
        self.assertTrue(str2 is str1)  #we pop the StringValue reference we saved in x; check if it the same object
        self.assertEqual(str2.value,'(CptS322)')  #we check if the StringValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #put will not push back the original StringValue onto the opstack 

    def test_getinterval(self):
        #(WSU Pullman Campus) 4 7 getinterval
        self.ps_env.opPush(StringValue('(WSU Pullman Campus)'))
        self.ps_env.opPush(4)
        self.ps_env.opPush(7)
        self.ps_env.getinterval()
        s =  self.ps_env.opPop() #pop the StringValue slice
        self.assertEqual(s.value, '(Pullman)')
        self.assertTrue(len(self.ps_env.opstack)==0)
        #getinterval will not push back the original StringValue onto the opstack 

    def test_putinterval1(self):
        #(WSU Pullman Campus) dup dup dup (Everett) putinterval
        s1 = StringValue('(WSU Pullman Campus)')
        self.ps_env.opPush(s1)
        self.ps_env.dup()  # duplicating the StringValue reference
        self.ps_env.dup()  # duplicating the StringValue reference
        self.ps_env.opPush(4)
        self.ps_env.opPush(StringValue('(Everett)'))  # the slice that starts at index 4 will be replaced by (Everett)
        self.ps_env.putinterval()  # putinterval will not push back the changed StringValue onto the opstack 
        s2 = self.ps_env.opPop()  # we pop the StringValue reference we copied with "dup"; 
        self.assertTrue(s2 is s1)  # check if it the same object
        self.assertEqual(s2.value,'(WSU Everett Campus)')  # we check if the StringValue object value is updated
        s3 = self.ps_env.opPop()  # we pop the string reference we copied with "dup";
        self.assertTrue(s3 is s1)  # check if it the same object
        self.assertEqual(s3.value,'(WSU Everett Campus)')  # we check if the StringValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #putinterval will not push back the original StringValue onto the opstack 

    def test_putinterval2(self):
        # /str1 (WSU Pullman Campus) def s1  (Everett) putinterval
        s1 = StringValue('(WSU Pullman Campus)')
        self.ps_env.opPush('/str1')
        self.ps_env.opPush(s1)
        self.ps_env.psDef()  # defines /str1 ; /str1 holds the StringValue reference
        self.ps_env.opPush(self.ps_env.lookup('str1'))  # pushes the StringValue reference str1 holds onto the stack
        self.ps_env.opPush(4)
        self.ps_env.opPush(StringValue('(Everett)'))  # the slice that starts at index 4 will be replaced by (Everett)
        self.ps_env.putinterval()  # putinterval will not push back the changed StringValue onto the opstack 
        
        self.ps_env.opPush(self.ps_env.lookup('str1'))  # pushes the StringValue reference str1 holds onto the stack
        s2 = self.ps_env.opPop()  # we pop the StringValue reference ; 
        self.assertTrue(s2 is s1)  # check if it the same object
        self.assertEqual(s2.value,'(WSU Everett Campus)')  # we check if the StringValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #putinterval will not push back the original StringValue onto the opstack 

    def test_search1(self):
        # (WSU,Go,Cougs) (,) search 
        self.ps_env.opPush(StringValue('(WSU,Go,Cougs)'))
        self.ps_env.opPush(StringValue('(,)'))
        self.ps_env.search()
        self.assertTrue(self.ps_env.opPop())  # the substring exists
        self.assertEqual(self.ps_env.opPop().value,'(WSU)') 
        self.assertEqual(self.ps_env.opPop().value,'(,)') 
        self.assertEqual(self.ps_env.opPop().value,'(Go,Cougs)')       
        self.assertTrue(len(self.ps_env.opstack)==0)

    def test_search2(self):
        # (WSU Go Cougs) (,) search 
        self.ps_env.opPush(StringValue('(WSU Go Cougs)'))
        self.ps_env.opPush(StringValue('(,)'))
        self.ps_env.search()
        self.assertFalse(self.ps_env.opPop())  # the substring doesn't exist
        self.assertEqual(self.ps_env.opPop().value,'(WSU Go Cougs)')       
        self.assertTrue(len(self.ps_env.opstack)==0)

    #-----------------------------------------------------
    #Dictionary operator tests

    def test_dict(self):
        # 10 dict 
        self.ps_env.opPush(10)
        self.ps_env.psDict()
        d = self.ps_env.opPop() # pop the DictionaryValue value
        self.assertEqual(d.value,{}) 
        self.assertTrue(len(self.ps_env.opstack)==0)  # dict should pop the size argument

    def test_get_put_DictConstant1(self):
        # 1 dict dup dup 1 10 put 1 get
        self.ps_env.opPush(1)
        self.ps_env.psDict()
        self.ps_env.dup()  #duplicating the DictionaryValue reference
        self.ps_env.dup()  #duplicating the DictionaryValue reference

        self.ps_env.opPush(1)
        self.ps_env.opPush(10)  
        self.ps_env.put()  #put will not push back the changed string onto the opstack 
        self.ps_env.opPush(1)
        self.ps_env.get() 
        self.assertEqual(self.ps_env.opPop(),10)  #we pop the value get pushed onto the opstack
        d2 = self.ps_env.opPop()  # pop the updated DictStack value
        self.assertDictEqual(d2.value,{1:10})  #we check if the DictionaryValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #put will not push back the original DictionaryValue onto the opstack 

    def test_get_put_DictConstant2(self):
        # /myd 1 dict def myd 2 10 put myd 2 22 put  myd 2 get myd
        self.ps_env.opPush('/myd')
        self.ps_env.opPush(1)
        self.ps_env.psDict()
        self.ps_env.psDef()
        self.ps_env.opPush(self.ps_env.lookup('myd'))
        self.ps_env.opPush(2)
        self.ps_env.opPush(10)
        self.ps_env.put() 
        self.ps_env.opPush(self.ps_env.lookup('myd'))
        self.ps_env.opPush(2)
        self.ps_env.opPush(22)
        self.ps_env.put() # overwrite the previous value for key (x)
        self.ps_env.opPush(self.ps_env.lookup('myd'))
        self.ps_env.opPush(2)        
        self.ps_env.get() 
        self.assertEqual(self.ps_env.opPop(),22)  #we pop the value get pushed onto the opstack
        self.ps_env.opPush(self.ps_env.lookup('myd'))        
        d2 = self.ps_env.opPop()  # pop the updated DictStack value
        self.assertDictEqual(d2.value,{2:22})  #we check if the DictionaryValue object value is updated
        self.assertTrue(len(self.ps_env.opstack)==0)
        #put will not push back the original DictionaryValue onto the opstack 

    def test_length_DictConstant(self):
        #1 dict 1 dup 11 put length
        self.ps_env.opPush(1)
        self.ps_env.psDict()
        self.ps_env.dup()
        self.ps_env.opPush(1)
        self.ps_env.opPush(11)
        self.ps_env.put()
        self.ps_env.length()
        self.assertEqual(self.ps_env.opPop(),1)      
        self.assertTrue(len(self.ps_env.opstack)==0) 
        #length will not push back the DictionaryValue onto the opstack  

    #-----------------------------------------------------
    #stack manipulation operator tests
    def test_dup(self):
        #(CptS355)  dup
        self.ps_env.opPush(StringValue('(CptS355)'))
        self.ps_env.dup()
        isSame = self.ps_env.opPop() is self.ps_env.opPop()
        self.assertTrue(isSame)

    def test_exch(self):
        # /x 10 exch
        self.ps_env.opPush('/x')
        self.ps_env.opPush(10)
        self.ps_env.exch()
        self.assertEqual(self.ps_env.opPop(),'/x')
        self.assertEqual(self.ps_env.opPop(),10)

    def test_pop(self):
        l1 = len(self.ps_env.opstack)
        self.ps_env.opPush(10)
        self.ps_env.pop()
        l2 = len(self.ps_env.opstack)
        self.assertEqual(l1,l2)

    def test_copy(self):
        #true 1 3 4 3 copy
        self.ps_env.opPush(True)
        self.ps_env.opPush(1)
        self.ps_env.opPush(3)
        self.ps_env.opPush(4)
        self.ps_env.opPush(3)
        self.ps_env.copy()
        self.assertTrue(self.ps_env.opPop()==4 and self.ps_env.opPop()==3 and self.ps_env.opPop()==1 and self.ps_env.opPop()==4 and self.ps_env.opPop()==3 and self.ps_env.opPop()==1 and self.ps_env.opPop()==True)
        
    def test_clear(self):
        #10 /x clear
        self.ps_env.opPush(10)
        self.ps_env.opPush("/x")
        self.ps_env.clear()
        self.assertEqual(len(self.ps_env.opstack),0)


    #-----------------------------------------------------
    #dictionary stack operators

    def test_psDef(self):
        #/x 10 def /x 20 def x
        self.ps_env.dictPush({})
        self.ps_env.opPush("/x")
        self.ps_env.opPush(10)
        self.ps_env.psDef()
        self.ps_env.opPush("/x")
        self.ps_env.opPush(20)
        self.ps_env.psDef()
        self.assertEqual(self.ps_env.lookup('x'),20)

    def test_psDef2(self):
        #/x 10 def 1 dict begin /y 20 def x
        self.ps_env.dictPush({})
        self.ps_env.opPush("/x")
        self.ps_env.opPush(10)
        self.ps_env.psDef()
        self.ps_env.dictPush({})
        self.ps_env.opPush("/y")
        self.ps_env.opPush(20)
        self.ps_env.psDef()
        self.assertEqual(self.ps_env.lookup('x'),10)

    def test_begin_end(self):
        #/x 3 def 1 dict begin /x 4 def end x
        self.ps_env.opPush("/x")
        self.ps_env.opPush(3)
        self.ps_env.psDef()
        self.ps_env.opPush(1)
        self.ps_env.psDict()
        self.ps_env.begin()
        self.ps_env.opPush("/x")
        self.ps_env.opPush(4)
        self.ps_env.psDef()
        self.ps_env.end() 
        self.assertEqual(self.ps_env.lookup('x'),3)

    def test_dict_put_begin_end(self):
        #1 dict /x 3 def /myd 2 dict def myd /x 4 put myd begin x end x
        self.ps_env.opPush(1)
        self.ps_env.psDict()
        self.ps_env.opPush("/x")
        self.ps_env.opPush(3)
        self.ps_env.psDef()
        self.ps_env.opPush("/myd")
        self.ps_env.opPush(2)
        self.ps_env.psDict()
        self.ps_env.psDef()
        self.ps_env.opPush(self.ps_env.lookup('myd'))
        self.ps_env.opPush("/x")
        self.ps_env.opPush(4)
        self.ps_env.put()
        self.ps_env.opPush(self.ps_env.lookup('myd'))
        self.ps_env.begin()
        self.ps_env.opPush(self.ps_env.lookup('x'))        
        self.ps_env.end() 
        self.ps_env.opPush(self.ps_env.lookup('x'))                
        self.assertEqual(self.ps_env.opPop(),3)
        self.assertEqual(self.ps_env.opPop(),4)
        self.assertEqual(self.ps_env.opPop().value,{})
        self.assertTrue(len(self.ps_env.opstack)==0) 

    def test_psDef3(self):
        #/x 3 def 1 dict begin /x 30 def 1 dict begin /x 300 def end x
        # define x in the bottom dictionary
        self.ps_env.dictPush({})
        self.ps_env.opPush("/x")
        self.ps_env.opPush(3)
        self.ps_env.psDef()
        # define x in the second dictionary
        self.ps_env.dictPush({})
        self.ps_env.opPush("/x")
        self.ps_env.opPush(30)
        self.ps_env.psDef()
        # define x in the third dictionary
        self.ps_env.dictPush({})
        self.ps_env.opPush("/x")
        self.ps_env.opPush(300)
        self.ps_env.psDef()
        self.ps_env.dictPop()
        self.assertEqual(self.ps_env.lookup('x'),30)

#-----------------------------------------------------

if __name__ == '__main__':
    unittest.main()
