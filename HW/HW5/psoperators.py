from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue

class PSOperators:
    def __init__(self, scoperule):
        self.scope = scoperule
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        # The environment that the REPL evaluates expressions in.
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }

    #------- Operand Stack Helper Functions --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if not self.opstack:
            print("Error: opPop - Operand stack is empty")
        else:
            return self.opstack.pop()

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        # check if dictstack is empty
        if not self.dictstack:
            print("Error: dictPop - dictionary stack is empty")
        else:
            return self.dictstack.pop()

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self, name, value):
        # check if dictstack is empty
        if not self.dictstack:
            self.dictstack.append({name:value})
        else:
            self.dictstack[-1][name] = value

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self, name):
        # check if dictstack is empty
        if not self.dictstack:
            print("Error: lookup failed - dictionary stack is empty")
            return None

        # using the end of dictstack as top of stack, search for matching name
        for d in reversed(self.dictstack):
            # attempt to return matching value, otherwise iterate
            try:
                return d['/' + name]
            except KeyError:
                pass

        print(f"Error: lookup failed - /{name} not found in dictionary stack")
        
    #------- Arithmetic Operators --------------
    def __bothnum(self, op1, op2) -> bool:
        """ Checks that both op1 and op2 are numerical (int) """
        return (isinstance(op1,int) or isinstance(op1,float)) and (isinstance(op2,int) or isinstance(op2,float))

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if not len(self.opstack) > 1:
            print("Error: add expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__bothnum(op1, op2):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number")
                self.opPush(op1)
                self.opPush(op2)

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if not len(self.opstack) > 1:
            print("Error: sub expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__bothnum(op1, op2):
                self.opPush(op1 - op2)
            else:
                print("Error: sub - one of the operands is not a number")
                self.opPush(op1)
                self.opPush(op2)

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if not len(self.opstack) > 1:
            print("Error: mul expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__bothnum(op1, op2):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number")
                self.opPush(op1)
                self.opPush(op2)

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if not len(self.opstack) > 1:
            print("Error: mod expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__bothnum(op1, op2):
                self.opPush(op1 % op2)
            else:
                print("Error: mod - one of the operands is not a number")
                self.opPush(op1)
                self.opPush(op2)   

    def __samevalidtype(self, op1, op2) -> bool:
        """ Check that op1 and op2 are int, float, bool, StringValue, or DictionaryValue, and are the same type """
        valid_types = [int, float, bool, StringValue, DictionaryValue]
        return type(op1) in valid_types and type(op1) == type(op2)
        
    
    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of the StringValue objects;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """
    def eq(self):
        if not len(self.opstack) > 1:
            print("Error: eq expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__samevalidtype(op1, op2):
                self.opPush(op1 == op2)
            else:
                print(f"Error: eq - operands are different or invalid types, {type(op1)} and {type(op2)} given")
                self.opPush(op1)
                self.opPush(op2)

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if not len(self.opstack) > 1:
            print("Error: lt expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__samevalidtype(op1, op2):
                self.opPush(op1 < op2)
            else:
                print(f"Error: lt - operands are different or invalid types, {type(op1)} and {type(op2)} given")
                self.opPush(op1)
                self.opPush(op2)

    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if not len(self.opstack) > 1:
            print("Error: gt expects 2 operands")
        else: 
            op2 = self.opPop()
            op1 = self.opPop()
            if self.__samevalidtype(op1, op2):
                self.opPush(op1 > op2)
            else:
                print(f"Error: gt - operands are different or invalid types, {type(op1)} and {type(op2)} given")
                self.opPush(op1)
                self.opPush(op2)  

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop(self):
        if not self.opstack:
            print("Error: pop - not enough arguments")
        else:
            self.opPop()

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print(OKGREEN+"**opstack**")
        for item in reversed(self.opstack):
            print(item)
        print("-----------------------"+CEND)
        print(RED+"**dictstack**")
        for item in reversed(self.dictstack):
            print(item)
        print("-----------------------"+ CEND)

    """
       Copies the top element in opstack.
    """
    def dup(self):
        if not self.opstack:
            print("Error: dup - not enough arguments")
        else:
            # get reference to top of stack, and push to stack twice
            last = self.opPop()
            self.opPush(last)
            self.opPush(last)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if not self.opstack:
            print("Error: copy - not enough arguments")
        else:
            num = self.opPop()
            if not isinstance(num, int):
                print(f"Error: copy - operand is not a number, {type(num)} given")
            elif num > len(self.opstack):
                print(f"Error: copy - not enough operands in opstack, {num} required, {len(self.opstack)} given")
            else:
                for cp in self.opstack[-num:]:
                    self.opPush(cp)

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        ct = len(self.opstack)
        self.opPush(ct)

    """
       Clears the opstack.
    """
    def clear(self):
        self.opstack.clear()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if not len(self.opstack) > 1:
            print("Error: exch expects 2 operands")
        else:
            op1 = self.opPop()
            op2 = self.opPop()
            
            self.opPush(op1)
            self.opPush(op2) 

    # ------- String and Dictionary creator operators --------------
    def __pack(self, instr: str) -> StringValue:
        """ Packs an input string into a StringValue container with parenthesis delimiters """
        return StringValue(f"({instr})")

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        if not self.opstack:
            print("Error: string - not enough arguments")
        else:
            num = self.opPop()
            if not isinstance(num, int):
                print(f"Error: string - int argument expected, {type(num)} given")
                self.opPush(num)
            else:
                self.opPush(self.__pack("\0" * num))
    
    """Creates a new empty dictionary, pushes it on the opstack """
    def psDict(self):
        if not self.opstack:
            print(f"Error: dict - int argument expected, {type(num)} given")
        else:
            num = self.opPop()
            if not isinstance(num, int):
                print("Error: dict - int argument expected")
                self.opPush(num)
            else:
                self.opPush(DictionaryValue({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictionaryValue and StringValue values.
    """
    def length(self):
        if not self.opstack:
            print("Error: length - not enough arguments")
        else:
            op = self.opPop()
            if isinstance(op, StringValue):
                self.opPush(op.length() - 2)
            elif isinstance(op, DictionaryValue):
                self.opPush(op.length())
            else:
                print(f"Error: length - StringValue or DictionaryValue argument expected, {type(op)} given")

    """ Pops either:
         -  "A (zero-based) index and an StringValue value" from opstack OR 
         -  "A `name` (i.e., a key) and DictionaryValue value" from opstack.  
        If the argument is a StringValue, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictionaryValue, gets the value for the given `name` from DictionaryValue's dictionary value and pushes it onto the opstack
    """
    def get(self):
        if not len(self.opstack) > 1:
            print("Error: get expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()

            if isinstance(op1, StringValue) and isinstance(op2, int):
                # convert character to ascii value
                ascii = ord(op1.value[op2+1])
                self.opPush(ascii)
            elif isinstance(op1, DictionaryValue):
                try:
                    self.opPush(op1.value[op2])
                except KeyError:
                    # key not found in given dictionary
                    self.opPush = op1
                    self.opPush = op2
            else:
                print(f"Error: get - expected StringValue and int, or DictionaryValue and name, given {type(op1)} and {type(op2)}")
   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StringValue value from  opstack", OR
    - "An `item`, a `name`, and a DictionaryValue value from  opstack". 
    If the argument is a StringValue, replaces the character at `index` of the StringValue's string with the character having the ASCII value of `item`.
    If the argument is an DictionaryValue, adds (or updates) "name:item" in DictionaryValue's dictionary `value`.
    """
    def put(self):
        if not len(self.opstack) > 2:
            print("Error: put expects 3 operands")
        else:
            item = self.opPop()
            index = self.opPop()
            op1 = self.opPop()

            if isinstance(op1, StringValue) and isinstance(index, int):
                # convert string to list, which is mutable
                mutable = list(op1.value)
                # convert ascii int to char
                mutable[index+1] = chr(item)
                # convert list to string
                op1.value = "".join(mutable)
            elif isinstance(op1, DictionaryValue):
                op1.value[index] = item
            else:
                print(f"Error: put - expected StringValue and int, or DictionaryValue and name, with item, given {type(op1)} and {type(index)}")

    """
    getinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a `count`, a (zero-based) `index`, and an StringValue value from opstack, and 
    extracts a substring of length count from the `value` of StringValue starting from `index`,
    pushes the substring back to opstack as a StringValue value. 
    """ 
    def getinterval(self):
        if not len(self.opstack) > 2:
            print("Error: getinterval expects 3 operands")
        else:
            count = self.opPop()
            index = self.opPop() + 1 # increment substring for parenthesis delimiters
            strval = self.opPop()

            if not (isinstance(strval, StringValue) and isinstance(index, int) and isinstance(count, int)):
                print(f"Error: getinterval - expected StringValue and two int, given {type(strval)}, {type(index)}, and {type(count)}")
            else:
                # slice string for new substring
                substr = strval.value[index:index+count]
                self.opPush(self.__pack(substr))

    """
    putinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a StringValue value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StringValue's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        if not len(self.opstack) > 2:
            print("Error: putinterval expects 3 operands")
        else:
            substr = self.opPop()
            index = self.opPop() + 1
            strval = self.opPop()

            if not (isinstance(strval, StringValue) and isinstance(index, int) and isinstance(substr, StringValue)):
                print(f"Error: putinterval - expected StringValue, int, and substring, given {type(strval)}, {type(index)}, and {type(substr)}")
            else:
                # convert string to list, which is mutable
                mutable = list(strval.value)
                # remove delimiters
                raw = substr.value.strip("()")
                mutable[index:index+substr.length()-2] = raw
                # convert list to string
                strval.value = "".join(mutable)

    """
    search is a string only operator, i.e., works only with StringValue values. 
    Pops two StringValue values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StringValue values;
       - pushes True 
    else,
        - pushes the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        if not len(self.opstack) > 1:
            print("Error: search expects 2 operands")
        else:
            op2 = self.opPop()
            op1 = self.opPop()
            
            if not (isinstance(op1, StringValue) and isinstance(op2, StringValue)):
                print("Error: search - one or both operands is not StringValue")
                self.opPush(op1)
                self.opPush(op2)
            else:
                # remove delimiters
                raw1 = op1.value.strip('()')
                raw2 = op2.value.strip('()')
                # check op2 is substring of op2
                if raw2 not in raw1:
                    print("Error: search - operand 2 must exist in string 1")
                    self.opPush(op1)
                    self.opPush(False)
                else:
                    # split by delimiter for first instance
                    spl = raw1.split(raw2, 1)
                    self.opPush(self.__pack(spl[1]))
                    # push delimiter to stack
                    self.opPush(op2)
                    self.opPush(self.__pack(spl[0]))
                    
                    self.opPush(True)
            
    # ------- Operators that manipulate the dictstact --------------
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):            
        if not len(self.opstack) > 1:
            print("Error: psDef expects 2 operands")
        else:
            # ensure at least one dictionary is in stack
            if not self.dictstack:
                self.dictstack.append({})

            value = self.opPop()
            name = self.opPop()

            self.dictstack[-1][name] = value

    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a CodeArrayValue object and a boolean value, if the value is True, executes (applies) the code array by calling apply.
    """
    def psIf(self):
        if not len(self.opstack) > 1:
            print("Error: if expects 2 operands")
        else:
            codearray = self.opPop()
            check = self.opPop()

            if not (isinstance(check, bool) and isinstance(codearray, CodeArrayValue)):
                print(f"Error: if - expected CodeArrayValue and boolean, given {type(codearray)} and {type(check)}")
            else:
                if check:
                    codearray.apply(self)

    """ ifelse operator
        Pops two CodeArrayValue objects and a boolean value, if the value is True, executes (applies) the bottom CodeArrayValue otherwise executes the top CodeArrayValue.
    """
    def psIfelse(self):
        if not len(self.opstack) > 2:
            print("Error: ifelse expects 3 operands")
        else:
            codearray_else = self.opPop()
            codearray_if = self.opPop()
            check = self.opPop()

            if not (isinstance(check, bool) and isinstance(codearray_if, CodeArrayValue)
                     and isinstance(codearray_else, CodeArrayValue)):
                print(f"Error: ifelse - expected two CodeArrayValue and boolean, given {type(codearray_if)}, {type(codearray_else)} and {type(check)}")
            else:
                if check:
                    codearray_if.apply(self)
                else:
                    codearray_else.apply(self)


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
    """ 
    def psFor(self):
        if not len(self.opstack) > 3:
            print("Error: for expects 4 operands")
        else:
            code_array = self.opPop()
            end = self.opPop()
            inc = self.opPop()
            begin = self.opPop()

            if not (isinstance(code_array, CodeArrayValue) and isinstance(end, int) 
                    and isinstance(inc, int) and isinstance(begin, int)):
                print("Error: for - expected CodeArrayValue and three int")
            else:
                # meets termination condition
                if begin == end:
                    pass
                # increment is positive, terminates when i is greater than end
                elif inc > 0:
                    for i in range(begin, end + 1, inc):
                        self.opPush(i)
                        code_array.apply(self)
                # increment is negative, terminates when i is less than end
                elif inc < 0:
                    for i in range(begin, end - 1, inc):
                        self.opPush(i)
                        code_array.apply(self)
                else:
                    print("Error: for - increment is zero, infinite loop")

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()
