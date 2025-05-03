import streamlit as st  # Importing Streamlit library
import io  # Importing io for handling string I/O
import contextlib  # Importing contextlib for redirecting stdout


# Setting the page configuration
st.set_page_config(page_title="21 OOP Concepts in Python", layout="wide")

# Title of the Application
st.title("🧠 Python OOP Concepts Explorer")

# Description of the Application
st.write("This application provides an overview of various Object-Oriented Programming (OOP) concepts in Python.")

# Sidebar for selecting OOP concept
concepts = {
    # 1. "Using `self`":
    "Using `self`": (
        "### Definition of `self`:\n\n`self` is a reference to the current instance of the class. It is used to access the instance's attributes and methods from within the class.\n\n"
        "### Question: \n\nCreate a class `Student` with attributes `name` and `marks`. Use the `self` keyword to initialize these values via a constructor. Add a method `display()` that prints student details.",
        '''class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def display(self):
        print(f"Name: {self.name}, Marks: {self.marks}")

s = Student("Alice", 95)
s.display()''',
        "The `self` keyword is used to bind the instance attributes `name` and `marks` to each object. It ensures that each instance has its own unique set of attributes."
    ),

    # 2. "Using `cls`":
    "Using `cls`": (
        "### Definition of `cls`:\n\n`cls` refers to the class itself, not the instance. It is used in class methods to access class-level variables and methods.\n\n"
        "### Question: \n\nCreate a class `Counter` that keeps track of how many objects have been created. Use a class variable and a class method with `cls` to manage and display the count.",
        '''class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

    @classmethod
    def show_count(cls):
        print(f"Total objects created: {cls.count}")

c1 = Counter()
c2 = Counter()
Counter.show_count()''',
        "The `cls` keyword accesses the class variable `count` to track how many objects are created. This method allows modifying class variables from within the class."
    ),

    # 3.Public Variables and Methods:
    "Public Variables and Methods": (
        "### Definition of Public Variables and Methods:\n\nPublic variables and methods are accessible from outside the class. They are used to define properties and behaviors that are meant to be used by any object of the class.\n\n"
        "### Question: \n\nCreate a class `Car` with a public variable `brand` and a public method `start()`. Instantiate the class and access both from outside the class.",
        '''class Car:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} car has started.")

my_car = Car("Toyota")
print(my_car.brand)
my_car.start()''',
        "Public members like `brand` and `start()` can be accessed directly outside the class, making it easy to interact with objects."
    ),

    # 4.Class Variables and Class Methods:
    "Class Variables and Class Methods": (
        "### Definition of Class Variables and Methods:\n\nClass variables are shared across all instances of a class. Class methods are bound to the class rather than any specific instance, and they use `cls` to access class variables.\n\n"
        "### Question: \n\nCreate a class `Bank` with a class variable `bank_name`. Add a class method `change_bank_name(cls, name)` that allows changing the bank name. Show that it affects all instances.",
        '''class Bank:
    bank_name = "Default Bank"

    @classmethod
    def change_bank_name(cls, name):
        cls.bank_name = name

b1 = Bank()
b2 = Bank()
Bank.change_bank_name("SuperBank")
print(b1.bank_name)
print(b2.bank_name)''',
        "Changing `bank_name` using a class method reflects in all instances because class variables are shared among all instances."
    ),

    # 5.Static Variables and Static Methods:
    "Static Variables and Static Methods": (
        "### Definition of Static Variables and Methods:\n\nStatic methods don't access or modify the state of the class or instance. They are bound to the class and can be called without creating an instance of the class.\n\n"
        "### Question: \n\nCreate a class `MathUtils` with a static method `add(a, b)` that returns the sum. No class or instance variables should be used.",
        '''class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

print(MathUtils.add(5, 3))''',
        "Static methods, defined with `@staticmethod`, don't rely on instance or class-specific data and are useful for utility functions that don't need to change state."
    ),

    # 6. "Constructors and Destructors":
    "Constructors and Destructors": (
        "### Definition of Constructors and Destructors:\n\nA constructor is a special method that is automatically called when an object is created. A destructor is called when an object is about to be destroyed.\n\n"
        "### Question: \n\nCreate a class `Logger` that prints a message when an object is created (constructor) and another message when it is destroyed (destructor).",
        '''class Logger:
    def __init__(self):
        print("Logger started")

    def __del__(self):
        print("Logger destroyed")

l = Logger()
del l''',
        "`__init__()` is the constructor and `__del__()` is the destructor. These methods help manage object lifecycle events such as initialization and cleanup."
    ),

    # 7. "Access Modifiers: Public, Private, and Protected":
    "Access Modifiers: Public, Private, and Protected": (
        "### Definition of Access Modifiers:\n\nPublic members are accessible from anywhere. Protected members are meant to be used within the class and its subclasses. Private members are inaccessible from outside the class and are name-mangled.\n\n"
        "### Question: \n\nCreate a class `Employee` with a public variable `name`, a protected variable `_salary`, and a private variable `__ssn`. Try accessing all three variables from an object of the class and document what happens.",
        '''class Employee:
    def __init__(self):
        self.name = "John"  # public
        self._salary = 50000  # protected
        self.__ssn = "123-45-6789"  # private

emp = Employee()
print(emp.name)        # accessible
print(emp._salary)     # accessible (by convention, not recommended)
# print(emp.__ssn)     # AttributeError''',
        "Private variables (with `__`) are name-mangled and not accessible directly, enforcing encapsulation."
    ),

    # 8. "The `super()` Function":
    "The `super()` Function": (
        "### Definition of `super()`:\n\n`super()` is used to call methods from a parent class. It's useful when you want to extend or modify the behavior of inherited methods.\n\n"
        "### Question: \n\nCreate a class `Person` with a constructor that sets the name. Inherit a class `Teacher` from it, add a subject field, and use `super()` to call the base class constructor.",
        '''class Person:
    def __init__(self, name):
        self.name = name

class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

t = Teacher("Mr. Smith", "Math")
print(t.name, t.subject)''',
        "`super()` allows the child class to call the constructor of the parent class, enabling inheritance of its properties."
    ),

    # 9. "Abstract Classes and Methods":
    "Abstract Classes and Methods": (
        "### Definition of Abstract Classes and Methods:\n\nAbstract classes define a blueprint for other classes. They can have abstract methods, which must be implemented in derived classes.\n\n"
        "### Question: \n\nCreate an abstract class `Shape` with an abstract method `area()`. Inherit a class `Rectangle` that implements `area()`.",
        '''from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

r = Rectangle(4, 5)
print(r.area())''',
        "Abstract classes define common methods for their subclasses, and `abstractmethod` forces subclasses to implement those methods."
    ),

    # 10. "Instance Methods":
    "Instance Methods": (
        "### Definition of Instance Methods:\n\nInstance methods operate on an instance of the class and can access instance attributes.\n\n"
        "### Question: \n\nCreate a class `Dog` with instance variables `name` and `breed`. Add an instance method `bark()` that prints a message including the dog's name.",
        '''class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} the {self.breed} says woof!")

dog = Dog("Max", "Beagle")
dog.bark()''',
        "Instance methods operate on specific objects and can modify or interact with their state."
    ),

    # 11. "Class Methods":
    "Class Methods": (
        "### Definition of Class Methods:\n\nClass methods work on the class level rather than the instance level. They are defined using `@classmethod`.\n\n"
        "### Question: \n\nCreate a class `Book` with a class variable `total_books`. Add a class method `increment_book_count()` to increase the count when a new book is added.",
        '''class Book:
    total_books = 0

    def __init__(self, title):
        self.title = title
        Book.total_books += 1

    @classmethod
    def increment_book_count(cls):
        cls.total_books += 1

b1 = Book("1984")
b2 = Book("Brave New World")
print(Book.total_books)''',
        "Class methods are bound to the class, not instances, and are useful for modifying class-level state."
    ),

    # 12. "Static Methods":
    "Static Methods": (
        "### Definition of Static Methods:\n\nStatic methods do not access or modify class or instance variables. They behave like regular functions but are grouped inside the class.\n\n"
        "### Question: \n\nCreate a class `TemperatureConverter` with a static method `celsius_to_fahrenheit(c)` that returns the Fahrenheit value.",
        '''class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return (c * 9/5) + 32

print(TemperatureConverter.celsius_to_fahrenheit(30))''',
        "Static methods are independent of the instance and class, and they're often used for utility or helper functions."
    ),

    # 13. "Inheritance":
    "Composition": (
        "### Definition of Composition:\n\nComposition is a design principle where one class is made up of objects of other classes. It represents a 'has-a' relationship.\n\n"
        "### Question: \n\nCreate a class `Engine` and a class `Car`. Use composition by passing an `Engine` object to the `Car` class during initialization. Access a method of the `Engine` class via the `Car` class.",
        '''class Engine:
    def start(self):
        print("Engine starting...")

class Car:
    def __init__(self, engine):
        self.engine = engine

    def start_car(self):
        self.engine.start()

car_engine = Engine()
my_car = Car(car_engine)
my_car.start_car()''',
        "Composition allows objects to be built from other objects, enabling modular and reusable code."
    ),

    # 14. "Aggregation":
    "Aggregation": (
        "### Definition of Aggregation:\n\nAggregation is a type of association where one class can contain objects of another class, but the contained object can exist independently.\n\n"
        "### Question: \n\nCreate a class `Department` and a class `Employee`. Use aggregation by having a `Department` object store a reference to an `Employee` object that exists independently of it.",
        '''class Employee:
    def __init__(self, name):
        self.name = name

class Department:
    def __init__(self, department_name, employee):
        self.department_name = department_name
        self.employee = employee

emp = Employee("John")
dept = Department("HR", emp)
print(dept.employee.name)''',
        "Aggregation represents a 'has-a' relationship but with less dependence between the classes compared to composition."
    ),

    # 15. "MRO & Inheritance":
    "Method Resolution Order (MRO) and Diamond Inheritance": (
        "### Definition of MRO and Diamond Inheritance:\n\nMRO determines the order in which classes are inherited. The diamond problem arises when two parent classes share a common ancestor, causing ambiguity in method resolution.\n\n"
        "### Question: \n\nCreate four classes: `A`, `B`, and `C` inherit from `A`, and `D` inherits from both `B` and `C`. Call `show()` to observe MRO.",
        '''class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        print("Class B")

class C(A):
    def show(self):
        print("Class C")

class D(B, C):
    pass

obj = D()
obj.show()''',
        "In Python, MRO resolves which method to use in case of diamond inheritance, and it ensures a clear inheritance chain."
    ),

    # 16. "Function Decorators":
    "Function Decorators": (
        "### Definition of Function Decorators:\n\nDecorators are functions that modify the behavior of other functions or methods. They are used to add functionality in a reusable way.\n\n"
        "### Question: \n\nWrite a decorator function `log_function_call` that prints 'Function is being called' before a function executes. Apply it to a function `say_hello()`.",
        '''def log_function_call(func):
    def wrapper():
        print("Function is being called")
        func()
    return wrapper

@log_function_call
def say_hello():
    print("Hello!")

say_hello()''',
        "Decorators allow you to add extra functionality to functions or methods in a clean, reusable way."
    ),

    # 17. "Class Decorators":
    "Class Decorators": (
        "### Definition of Class Decorators:\n\nClass decorators modify the behavior of a class. They can add or modify methods or properties in a class.\n\n"
        "### Question: \n\nCreate a class decorator `add_greeting` that modifies a class to add a `greet()` method returning 'Hello from Decorator!'. Apply it to a class `Person`.",
        '''def add_greeting(cls):
    cls.greet = lambda self: "Hello from Decorator!"
    return cls

@add_greeting
class Person:
    pass

p = Person()
print(p.greet())''',
        "Class decorators modify classes at the time of definition, adding functionality or changing behavior."
    ),

    # 18. "Property Decorators":
    "Property Decorators: `@property`, `@setter`, and `@deleter`": (
        "### Definition of Property Decorators:\n\n`@property` allows you to define methods that can be accessed like attributes. `@setter` and `@deleter` allow modifying and deleting properties.\n\n"
        "### Question: \n\nCreate a class `Product` with a private attribute `_price`. Use `@property` to get the price, `@price.setter` to update it, and `@price.deleter` to delete it.",
        '''class Product:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @price.deleter
    def price(self):
        del self._price

p = Product(100)
print(p.price)
p.price = 200
print(p.price)
del p.price''',
        "Property decorators allow you to control access to attributes while keeping the interface clean."
    ),

    # 19. "Callable Objects":
    "callable() and `__call__()`": (
        "### Definition of `__call__()`:\n\n`__call__()` allows an instance of a class to be called as a function. This enables objects to behave like functions.\n\n"
        "### Question: \n\nCreate a class `Multiplier` with an `__init__()` to set a factor. Define a `__call__()` method that multiplies an input by the factor.",
        '''class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, num):
        return num * self.factor

multiply_by_2 = Multiplier(2)
print(multiply_by_2(5))''',
        "`__call__()` makes an object callable like a regular function, enhancing flexibility."
    ),

    # 20. "Method Overloading":
    "Method Overloading": (
        "### Definition of Method Overloading:\n\nMethod overloading allows a method to behave differently based on the number or type of arguments passed.\n\n"
        "### Question: \n\n Define a class `Calculator` with an `add()` method that can add two or three numbers, demonstrating overloading using default arguments.",
        '''class Calculator:
    def add(self, a, b, c=0):
        return a + b + c

calc = Calculator()
print(calc.add(2, 3))
print(calc.add(2, 3, 4))''',
        "Method overloading can be simulated by using default arguments, allowing a method to handle different numbers or types of inputs."
    ),
 
    # 21. "Method Overriding":
    "Method Overriding": (
        "### Definition of Method Overriding:\n\nMethod overriding allows a subclass to provide a specific implementation of a method that is already defined in the parent class.\n\n"
        "### Question: \n\n Create a class `Animal` with a method `sound()`, then override it in a subclass `Dog` to provide a custom implementation.",
        '''class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

d = Dog()
d.sound()''',
        "Method overriding allows subclasses to redefine parent class methods to provide specific functionality."
    )
}
# Sidebar for concept selection
selected_concept = st.sidebar.selectbox("📚 Choose a Concept", list(concepts.keys()))

# Display selected concept content
if selected_concept:
    description, code, explanation = concepts[selected_concept]
    st.subheader(f"📘 {selected_concept}")
    st.markdown(f"{description}")
    st.code(code, language="python")
    st.markdown(f"**Explanation:**\n\n{explanation}")

# Footer
st.write("---")
st.write("© 2023 OOP Concepts in Python")
