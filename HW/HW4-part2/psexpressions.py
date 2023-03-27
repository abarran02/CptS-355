"""Parts of this code was adopted from https://composingprograms.com/. 
The code has been changed according to Postscript syntax. 
https://creativecommons.org/licenses/by-sa/3.0/
"""
class Expr:
    """
    When you type input into this interpreter, it is parsed (read) into an expression. 
    This expression is represented in our code as an instance of this `Expr` class.
    In our interpreter, there are four types of expressions:
        1.	Literal:  represents primitive constants : integers or booleans . The `value` attribute contains the fixed value the `Literal` refers to. 
        2.	PSName: represents names of variables, functions, or operators .  The `var_name` attribute contains the name of the variable as a Python string, e.g., '/sq','sq','add','def'. If the `var_name` starts with a `/` character, PSName represents a name constant, otherwise it represents a variable reference ,  function call, or a built-in operator call. 
        3.	PSString: represents strings. The `value` attribute contains the string value the `PSString` refers to e.g., '(CptS355)'.
        4.	PSCodeArray: represents body of a function or if, ifelse, or for expressions. The `value` attribute is a Python list that includes the tokens of the PostScript code-array (block) it represents [Literal(10), Literal(5),PSName(mul)]
    In our code, the four types of expressions are subclasses of the `Expr`
    class: `Literal`, `PSName`, `PSString`, and `PSCodeArray`.
    """

    def __init__(self, value):
        self.value = value

    def eval(self, ps_env):
        """
        Each subclass of Expr implements its own eval method.
        `ps_env` is the PSOperators object that include the `opstack` and `dictstack`. 
        Subclasses of `Expr` should implement this method. (i.e., `Literal`, `PSName`, `PSString`, and `PSCodeArray`  )
        This method should return a `Value` instance, the result of  evaluating the expression.
        """
        raise NotImplementedError

    def __str__(self):
        """ Returns a parsable and human-readable string of this expression (i.e.    what you would type into the interpreter).  """
        raise NotImplementedError
    
    def __repr__(self):
        """  Returns how this expression is written in our Python representation.   """
        return "{}({})".format(type(self).__name__, self.value)

class Literal(Expr):
    """A literal is notation for representing a primitive constant value in code. 
    In our interpreter, a `Literal` evaluates to a number (int)  or a boolen. The evaluated value is pushed onto the stack. 
    The `value` attribute contains the fixed value the `Literal` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        """`ps_env` is the PSOperators object that include the `opstack` and `dictstack`. """
        """TO-DO (part2)"""
        pass

    def __str__(self):
        return str(self.value)

class PSString(Expr):
    """A PSString is notation for representing a string constant in code. `
    In our interpreter, a `PSString` evaluates to a `StringValue` object. The evaluated StringValue value is pushed onto the stack. 
    The `value` attribute contains the string value the `PSString` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        """`ps_env` is the PSOperators object that include the `opstack` and `dictstack`. """
        """TO-DO (part2)"""
        pass 

    def __str__(self):
        return str(self.value)

class PSName(Expr):
    """A `PSName` is a variable , a built-in operator, or a function. 
        a.	If the `PSName` represents a name constant (i.e., its `var_name` attribute starts with a `/`), it will be evaluated to a Python string having value `var_name` . The evaluated value will be pushed onto the opstack.
        b.	If the `PSName` represents a built-in operator (i.e., its `var_name` attribute is one of the built-in operator names),  then we will evaluate it by executing the operator function defined in psoperators.py in the current environment (opstack). 
        c.	If the `PSName` represents a variable or function, interpreter looks up the value of the variable in the current environment (dictstack).
            i.	If the variable value is a code-array (`CodeArrayValue`), it should be applied (i.e., executed) by calling its `apply` method.  
            ii.	Otherwise, the variable value is a constant and it should be pushed onto the opstack. 

       The `var_name` attribute contains the name of the variable (as a Python string).
    """
    def __init__(self, var_name):
        Expr.__init__(self, var_name)
        self.var_name = var_name

    def eval(self,ps_env):
        """`ps_env` is the PSOperators object that include the `opstack` and `dictstack`. """
        """TO-DO (part2)"""
        pass       

    def __str__(self):
        return str(self.var_name)

class PSCodeArray(Expr):
    """A `PSCodeArray` is a notation for representing a code block in PostScript, i.e., a function body, `if` block, `ifelse` block, or `for` loop block. 
    In our interpreter, a `PSCodeArray` evaluates to a `CodeArrayValue` object. The `CodeArrayValue` value is pushed onto the stack.   
    The `value` attribute contains the list of tokens in the code array.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        """`ps_env` is the PSOperators object that include the `opstack` and `dictstack`. """
        """TO-DO (part2)"""
        pass

    def __str__(self):
        return str(self.value)

## -----------------------------------------------------------------------------------
## -----------------------------------------------------------------------------------

class Value:
    """
    "Value" objects represent the string , dictionary, and code-array constants that are pushed onto the stack.  
    
    In our interpreter,
        -  For simplicity, the integers and boolean values are pushed onto the opstack as integers and booleans, respectively. 
        -  Similarly, name constants (e.g. '/x') are pushed to the opstack as strings. 
        -  The string, dictionary, and code array constants are represented as StringValue, DictionaryValue, and CodeArrayValue objects, 
           which are subclasses of the `Value`. 
        -  StringValue, DictionaryValue, and CodeArrayValue implement the following methods in the `Value` interface:
            * apply : Evaluates the value. `apply` is only applicable to CodeArrayValue objects (applies the function, evaluates all the tokens in the function's code-array, i.e., CodeArrayValue )  
            * __str__: Conversts the value to  a human-readable version (i.e., string) for printing.
    """
    def __init__(self, value):
        self.value = value

    def apply(self, ps_env):
        """
        Each subclass of Value implements its own `apply` method.
        Note that only `CodeArrayValue`s can be "applied"; attempting to apply a StringValue or DictionaryValue will give an error. 
        """
        raise NotImplementedError

    def __str__(self):
        """ Returns a parsable and human-readable version of this value (i.e. the string to be displayed in the interpreter). """
        raise NotImplementedError

    def __repr__(self):
        """ Returns how this value is printed in our Python representation.   """
        return "{}({})".format(type(self).__name__, self.value)

class StringValue(Value):
    """A  string constant delimited in paranthesis. Attempting to apply a `string constant` will give an error.
      The `value` attribute is the Python string that this value represents.

      You may add additional methods to this class as needed and use them in your operator implementations. 
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, ps_env):
        raise TypeError("Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}('{}')".format(type(self).__name__, self.value)
    
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.value)
    
    def __eq__(self, other):
        # with help from https://stackoverflow.com/questions/390250/
        if isinstance(other, StringValue):
            return self.value == other.value
        else:
            return False
        
    def __lt__(self, other):
        if isinstance(other, StringValue):
            return self.value < other.value
        else:
            return False
        
    def __gt__(self, other):
        if isinstance(other, StringValue):
            return self.value > other.value
        else:
            return False

    # returns length of the string value
    def length(self):
        return len(self.value)

class DictionaryValue(Value):
    """A dictionary contant. Attempting to apply an `dictionary constant` will give an error.
      The `value` attribute is the Python dictionary that this value represents.
      You may add additional methods to this class as needed and use them in your operator implementations. 
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, ps_env):
        raise TypeError("Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.value)

    def __eq__(self, other):
        if isinstance(other, DictionaryValue):
            return id(self) == id(other)
        else:
            return False
        
    def __lt__(self, other):
        if isinstance(other, DictionaryValue):
            return id(self) < id(other)
        else:
            return False
        
    def __gt__(self, other):
        if isinstance(other, DictionaryValue):
            return id(self) > id(other)
        else:
            return False

    # returns length of the array value
    def length(self):
        return len(list(self.value.keys()))    

class CodeArrayValue(Value):
    """The constant-array that represents the body of a (user-defined) function, or if, ifelse, for operators. 
    The `body` attribute is a nested list of expressions.
    The `apply` method will evaluate each expression in the `body` by calling token's `eval` method. 
    Expressions will be evaluated in the current referencing environment (ps_env).  
    """
    def __init__(self, body):
        Value.__init__(self, body)
        self.body = body

    def apply(self, ps_env):
        pass
        # TO-DO in milestone2

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.body)
