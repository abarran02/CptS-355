"""Parts of this code was adopted from https://composingprograms.com/. 
The code has been changed according to Postscript syntax. 
https://creativecommons.org/licenses/by-sa/3.0/
"""

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
