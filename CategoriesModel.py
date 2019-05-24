categories = [
    {
        "category": "Datatypes",
        "clues": [
            {
                "points": "200",
                "clue": "Data type that holds positive and negative whole numbers",
                "question": "What is an Int?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "A linear sequence of characters, words, or other data.",
                "question": "What is a String?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "These are numbers stored internally in two parts: a base and an exponent. When printed they look like decimal numbers",
                "question": "What is a Float?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "This data type can be a variable, a data structure, a function, or a method",
                "question": "What is an Object?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "These are the three basic sequence types",
                "question": "What is a list, tuple, and range?",
                "answered": False,
            },
        ],
    },
    {
        "category": "Debugging",
        "clues": [
            {
                "points": "200",
                "clue": "This number is spaces is best practive for indentation, as opposed to using Tab.",
                "question": "What is 4?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "This type of error will occur when forgetting a colon at the end of a statement where one is required.",
                "question": "What is a Syntax Error?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "This function can be used to output the object, which can be extremely helpfull durring the debugging process",
                "question": "What is print()?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "This website often found after an internet search of your error or bug can help you make a breakthrough.",
                "question": "What is Stack Overflow?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "This type of development is used to avoid long debugging sessions by adding and testing small amounts of code at a time.",
                "question": "What is incremental debugging?",
                "answered": False,
            },
      ],
    },
    {
        "category": "Modules, Function",
        "clues": [
               {
                "points": "200",
                "clue": "This is the keyword used to begin writing a function.",
                "question": "What is def?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "The process in which a function calls itself.",
                "question": "What is recursion?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "The line of code to have access to a class name Database in a module named storage.",
                "question": "What is `from storage import Database``?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "This is a python file containing variables, functions, and/or classes.",
                "question": "What is a module?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "This type of function does not mutate (change) any of the data passed to it.",
                "question": "What is a pure function?",
                "answered": False,
            },
       ],
    },
    {
        "category": "Selection",
        "clues": [
              {
                "points": "200",
                "clue": "This is the simplest form of selection/conditional statements.",
                "question": "What is the `if` statement?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "This is an expression that is either true or false.",
                "question": "What is boolean expression?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "These are all logical operators that work on boolean expressions.",
                "question": "What is `and`, `or`, and `not`?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "A conditional branch with more than two possible flows of execution.",
                "question": "What are chained conditionals?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "These are all of the operators that compare two values.",
                "question": "What is `==`, `!=`, `>`, `<`, `>=`, `<=`?",
                "answered": False,
            },
      ],
    },
    {
        "category": "Iteration",
        "clues": [
             {
                "points": "200",
                "clue": "In python this allows us to write programs that iterate over types like lists.",
                "question": "What is a for loop?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "This function allows you to iterate over a list's index and it's contents simultaneously",
                "question": "What is the enumerate function?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "These are the three parameters that can passed into a range type inside a for loop.",
                "question": "What is start, stop, and  step?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "This function can be used to iterate through multiple lists simultaneously.",
                "question": "What is `zip()`?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "This time complexity can be achieved by putting a for loop inside of an original for loop.",
                "question": "What is quadratic time complexity or O(n^2)?",
                "answered": False,
            },
       ],
    },
    {
        "category": "Classes",
        "clues": [
            {
                "points": "200",
                "clue": "This strangely-spelled method defines what should happen when an instance of a class is first created",
                "question": "What is __init__?",
                "answered": False,
            },
            {
                "points": "400",
                "clue": "This Object Oriented Programming mechanisim allows code reuse by including all methods of a \"parent\" class.",
                "question": "What is inheritance or sub-classing?",
                "answered": False,
            },
            {
                "points": "600",
                "clue": "This magic method allows you to print your class instance in a manner of your choosing.",
                "question": "What is __repr__ or __str__?",
                "answered": False,
            },
            {
                "points": "800",
                "clue": "The collection of attribute values that a specific data object maintains.",
                "question": "What is state?",
                "answered": False,
            },
            {
                "points": "1000",
                "clue": "This concept allows you to rewrite existing methods of a parent class.",
                "question": "What is override?",
                "answered": False,
            },
        ],
    }
]

class Categories():
    @staticmethod
    def getClueField(column, row, field):
        return categories[column]['clues'][row][field]

    @staticmethod
    def markAnswered(column, row):
        categories[column]['clues'][row]['answered'] = True
