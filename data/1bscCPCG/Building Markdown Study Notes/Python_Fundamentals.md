# Python Fundamentals: A Comprehensive Guide

## Table of Contents
1. [Introduction to Python](#introduction-to-python)
2. [Variables and Data Types](#variables-and-data-types)
3. [Control Flow](#control-flow)
4. [Functions](#functions)
5. [Data Structures](#data-structures)
6. [String Operations](#string-operations)
7. [File Handling](#file-handling)
8. [Error Handling](#error-handling)
9. [Object-Oriented Programming](#object-oriented-programming)
10. [Modules and Packages](#modules-and-packages)
11. [Advanced Concepts](#advanced-concepts)

---

## Introduction to Python

Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, Python emphasizes code readability and allows programmers to express concepts in fewer lines of code than other languages.

### Why Python?
- **Easy to Learn**: Simple syntax similar to natural English
- **Versatile**: Used in web development, data science, AI, automation, and more
- **Large Community**: Extensive libraries and frameworks available
- **Interpreted**: No compilation needed; code runs directly
- **Cross-Platform**: Works on Windows, macOS, and Linux

---

## Variables and Data Types

### Variables
Variables are containers for storing data values. Python doesn't require explicit type declaration.

```python
# Variable assignment
name = "Alice"
age = 25
height = 5.7
is_student = True

# Dynamic typing - variables can change type
value = 10        # integer
value = "Hello"   # now a string
value = 3.14      # now a float
```

### Primitive Data Types

#### 1. **Integer (int)**
Whole numbers without decimal points.
```python
x = 10
y = -5
z = 0

# Integer operations
print(10 + 5)      # 15
print(10 - 3)      # 7
print(10 * 2)      # 20
print(10 / 3)      # 3.333... (float division)
print(10 // 3)     # 3 (floor division)
print(10 % 3)      # 1 (modulo - remainder)
print(2 ** 3)      # 8 (exponentiation)
```

#### 2. **Float (float)**
Numbers with decimal points.
```python
pi = 3.14159
temperature = -10.5
price = 19.99

# Float operations
print(10.5 + 5.3)  # 15.8
print(10.0 / 3)    # 3.333...
```

#### 3. **String (str)**
Sequences of characters enclosed in quotes.
```python
name = "John"
sentence = 'Python is great'
multiline = """This is a
multiline string"""

# String operations
print("Hello" + " " + "World")  # Concatenation
print("Python" * 3)              # "PythonPythonPython"
```

#### 4. **Boolean (bool)**
Logical values: `True` or `False`.
```python
is_adult = True
is_raining = False

# Boolean operations
print(True and False)   # False
print(True or False)    # True
print(not True)         # False
```

#### 5. **None**
Represents absence of value.
```python
result = None
print(result)  # None
```

### Type Checking and Conversion

```python
# Check type
x = 10
print(type(x))  # <class 'int'>

# Type conversion
string_num = "42"
number = int(string_num)      # 42
float_num = float("3.14")     # 3.14
string = str(100)             # "100"
bool_val = bool(1)            # True
```

---

## Control Flow

### Conditional Statements (if-elif-else)

```python
# Basic if statement
age = 18
if age >= 18:
    print("You are an adult")

# if-else statement
score = 75
if score >= 80:
    print("Grade: A")
else:
    print("Grade: B or below")

# if-elif-else statement
temperature = 20
if temperature > 30:
    print("It's hot")
elif temperature > 15:
    print("It's warm")
elif temperature > 0:
    print("It's cold")
else:
    print("It's freezing")

# Nested conditions
age = 25
income = 50000
if age >= 18:
    if income > 40000:
        print("Eligible for loan")
    else:
        print("Income too low")
else:
    print("Too young for loan")
```

### Comparison Operators

```python
x = 10
y = 20

print(x == y)   # False (equal to)
print(x != y)   # True (not equal to)
print(x < y)    # True (less than)
print(x > y)    # False (greater than)
print(x <= y)   # True (less than or equal)
print(x >= y)   # False (greater than or equal)
```

### Logical Operators

```python
# and - both conditions must be True
print(True and True)    # True
print(True and False)   # False

# or - at least one condition must be True
print(True or False)    # True
print(False or False)   # False

# not - reverses the boolean value
print(not True)         # False
print(not False)        # True
```

### Loops

#### While Loop
```python
# While loop - continues while condition is True
count = 0
while count < 5:
    print(count)
    count += 1

# Infinite loop example (use break to exit)
while True:
    user_input = input("Enter 'exit' to quit: ")
    if user_input == "exit":
        break
    print(f"You entered: {user_input}")
```

#### For Loop
```python
# For loop - iterates over a sequence
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

# For loop with step
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)

# For loop over list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# For loop with enumerate (get index and value)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

#### Break and Continue

```python
# Break - exits the loop
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0, 1, 2, 3, 4

# Continue - skips current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)  # Prints 0, 1, 3, 4
```

---

## Functions

### Function Definition and Calling

```python
# Basic function
def greet():
    print("Hello, World!")

greet()  # Call the function

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")

# Function with return value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8

# Function with multiple parameters
def describe_person(name, age, city):
    return f"{name} is {age} years old and lives in {city}"

info = describe_person("Bob", 30, "New York")
print(info)
```

### Default Parameters

```python
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()           # Hello, Guest!
greet("Alice")    # Hello, Alice!
```

### Keyword Arguments

```python
def order_pizza(size, topping, extra_cheese=False):
    print(f"Pizza size: {size}, Topping: {topping}, Extra cheese: {extra_cheese}")

order_pizza(size="large", topping="pepperoni")
order_pizza(topping="mushroom", size="medium", extra_cheese=True)
```

### Variable-Length Arguments

```python
# *args - allows multiple positional arguments
def sum_numbers(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_numbers(1, 2, 3, 4, 5))  # 15

# **kwargs - allows multiple keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="NYC")
# Output:
# name: Alice
# age: 25
# city: NYC
```

### Docstrings

```python
def calculate_area(radius):
    """
    Calculate the area of a circle.
    
    Args:
        radius (float): The radius of the circle
    
    Returns:
        float: The area of the circle
    """
    return 3.14159 * radius ** 2

print(calculate_area(5))
```

---

## Data Structures

### Lists

Lists are ordered, mutable collections that can contain different data types.

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

# Accessing elements (0-indexed)
print(numbers[0])   # 1
print(numbers[-1])  # 5 (last element)

# Slicing
print(numbers[1:4])   # [2, 3, 4]
print(numbers[:3])    # [1, 2, 3]
print(numbers[2:])    # [3, 4, 5]
print(numbers[::2])   # [1, 3, 5] (every 2nd element)

# List methods
numbers.append(6)           # Add element at end
numbers.insert(0, 0)        # Insert at specific position
numbers.remove(3)           # Remove specific element
popped = numbers.pop()      # Remove and return last element
numbers.extend([7, 8, 9])   # Add multiple elements
numbers.sort()              # Sort in-place
sorted_nums = sorted(numbers)  # Return sorted copy
numbers.reverse()           # Reverse in-place
count = numbers.count(1)    # Count occurrences

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

### Tuples

Tuples are ordered, immutable collections.

```python
# Creating tuples
coordinates = (10, 20)
colors = ("red", "green", "blue")
single_item = (42,)  # Must have comma for single item

# Accessing elements (same as lists)
print(coordinates[0])   # 10
print(colors[1:3])      # ("green", "blue")

# Tuples are immutable
# coordinates[0] = 15  # This would raise an error

# Unpacking
x, y = coordinates
print(x, y)  # 10 20

# Tuple operations
combined = (1, 2) + (3, 4)  # (1, 2, 3, 4)
repeated = (1, 2) * 3       # (1, 2, 1, 2, 1, 2)
```

### Dictionaries

Dictionaries store key-value pairs.

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Accessing values
print(person["name"])    # Alice
print(person.get("age"))  # 25
print(person.get("email", "Not found"))  # Not found

# Adding/modifying
person["email"] = "alice@example.com"
person["age"] = 26

# Dictionary methods
print(person.keys())      # dict_keys(['name', 'age', 'city', 'email'])
print(person.values())    # dict_values(['Alice', 26, 'New York', 'alice@example.com'])
print(person.items())     # Key-value pairs

# Iterating
for key, value in person.items():
    print(f"{key}: {value}")

# Removing items
del person["email"]
removed_value = person.pop("city")  # Remove and return value

# Checking keys
if "name" in person:
    print("Name exists")

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Sets

Sets are unordered collections of unique items.

```python
# Creating sets
numbers = {1, 2, 3, 4, 5}
colors = {"red", "green", "blue"}
empty_set = set()  # Not {} which creates an empty dict

# Set operations
numbers.add(6)              # Add element
numbers.remove(3)           # Remove element (raises error if not found)
numbers.discard(3)          # Remove if exists (no error)
popped = numbers.pop()      # Remove arbitrary element

# Set mathematical operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2         # {1, 2, 3, 4, 5, 6}
intersection = set1 & set2  # {3, 4}
difference = set1 - set2    # {1, 2}
symmetric_diff = set1 ^ set2  # {1, 2, 5, 6}

# Membership testing
print(2 in set1)            # True
print(10 in set1)           # False

# Remove duplicates from list
numbers_with_duplicates = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(numbers_with_duplicates))
```

---

## String Operations

### String Basics

```python
# Creating strings
text = "Hello, World!"
single_quote = 'Python'
multiline = """This is
a multiline
string"""

# String indexing and slicing
print(text[0])      # H
print(text[7:12])   # World
print(text[-1])     # !
print(text[:5])     # Hello
print(text[::2])    # Hlo ol!
```

### String Methods

```python
text = "hello world"

# Case conversion
print(text.upper())        # HELLO WORLD
print(text.capitalize())   # Hello world
print(text.title())        # Hello World

# String searching
print(text.find("world"))  # 6 (index of substring)
print(text.find("xyz"))    # -1 (not found)
print(text.count("l"))     # 3

# String manipulation
print(text.replace("world", "Python"))  # hello Python
print(text.split())        # ['hello', 'world']
print(text.split("o"))     # ['hell', ' w', 'rld']

# Stripping whitespace
padded = "  hello  "
print(padded.strip())      # "hello"
print(padded.lstrip())     # "hello  "
print(padded.rstrip())     # "  hello"

# String checking
print(text.startswith("hello"))  # True
print(text.endswith("world"))    # True
print(text.isalpha())      # False (contains space)
print("123".isdigit())     # True
print("abc".islower())     # True
```

### String Formatting

```python
name = "Alice"
age = 25
height = 5.7

# f-string (Python 3.6+)
print(f"Name: {name}, Age: {age}")  # Name: Alice, Age: 25

# format() method
print("Name: {}, Age: {}".format(name, age))
print("Name: {0}, Age: {1}".format(name, age))
print("Name: {name}, Age: {age}".format(name=name, age=age))

# String formatting with specifiers
print(f"{height:.2f}")      # 5.70 (2 decimal places)
print(f"{age:05d}")         # 00025 (zero-padded)
print(f"{name:>10}")        # "     Alice" (right-aligned)
print(f"{name:<10}")        # "Alice     " (left-aligned)
print(f"{name:^10}")        # "  Alice   " (centered)
```

---

## File Handling

### Reading Files

```python
# Reading entire file
with open("file.txt", "r") as file:
    content = file.read()
    print(content)

# Reading line by line
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())

# Reading all lines as list
with open("file.txt", "r") as file:
    lines = file.readlines()
    print(lines)
```

### Writing to Files

```python
# Write mode (overwrites existing content)
with open("file.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("Python is great!")

# Append mode (adds to existing content)
with open("file.txt", "a") as file:
    file.write("\nNew line added")

# Writing multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("file.txt", "w") as file:
    file.writelines(lines)
```

### File Operations

```python
import os

# Check if file exists
if os.path.exists("file.txt"):
    print("File exists")

# Get file size
size = os.path.getsize("file.txt")
print(f"File size: {size} bytes")

# Remove file
os.remove("file.txt")

# Rename file
os.rename("old_name.txt", "new_name.txt")
```

---

## Error Handling

### Try-Except-Finally

```python
# Basic try-except
try:
    x = 10 / 0  # This will raise an error
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Multiple except blocks
try:
    data = {"name": "Alice"}
    print(data["age"])  # KeyError
except KeyError:
    print("Key not found")
except TypeError:
    print("Type error occurred")
except Exception as e:
    print(f"An error occurred: {e}")

# Try-except-finally
try:
    file = open("file.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("Cleanup code")
    # This runs regardless of whether an exception occurred

# Try-except-else
try:
    x = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print(f"Result: {x}")  # Runs if no exception
```

### Raising Exceptions

```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return age

try:
    validate_age(-5)
except ValueError as e:
    print(f"Error: {e}")
```

---

## Object-Oriented Programming

### Classes and Objects

```python
# Class definition
class Person:
    # Class variable
    species = "Homo sapiens"
    
    # Constructor (initializer)
    def __init__(self, name, age):
        # Instance variables
        self.name = name
        self.age = age
    
    # Methods
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old"
    
    def celebrate_birthday(self):
        self.age += 1
        return f"{self.name} is now {self.age} years old"

# Creating objects
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# Accessing attributes
print(person1.name)        # Alice
print(person2.age)         # 30
print(Person.species)      # Homo sapiens

# Calling methods
print(person1.introduce())        # Hi, I'm Alice and I'm 25 years old
print(person1.celebrate_birthday())  # Alice is now 26 years old
```

### Inheritance

```python
# Parent class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Some sound"

# Child class
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# Using inheritance
dog = Dog("Rex")
cat = Cat("Whiskers")

print(dog.speak())  # Rex says Woof!
print(cat.speak())  # Whiskers says Meow!
```

### Encapsulation

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private variable (name mangling)
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited {amount}. New balance: {self.__balance}"
        return "Invalid amount"
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew {amount}. New balance: {self.__balance}"
        return "Invalid amount or insufficient funds"
    
    def get_balance(self):
        return self.__balance

# Using encapsulation
account = BankAccount("Alice", 1000)
print(account.deposit(500))      # Deposited 500. New balance: 1500
print(account.withdraw(200))     # Withdrew 200. New balance: 1300
print(account.get_balance())     # 1300
# print(account.__balance)       # This would raise an error
```

### Polymorphism

```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

# Polymorphism in action
shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(shape.area())
```

---

## Modules and Packages

### Importing Modules

```python
# Import entire module
import math
print(math.pi)           # 3.14159...
print(math.sqrt(16))     # 4.0

# Import specific functions
from math import pi, sqrt
print(pi)
print(sqrt(25))

# Import with alias
import numpy as np
from collections import defaultdict as dd

# Import all (not recommended)
from math import *
print(sin(0))
```

### Common Built-in Modules

```python
# os - Operating system operations
import os
print(os.getcwd())          # Current directory
os.chdir("path/to/dir")     # Change directory
files = os.listdir(".")     # List files

# sys - System-specific operations
import sys
print(sys.version)          # Python version
print(sys.argv)             # Command-line arguments

# datetime - Date and time
from datetime import datetime, timedelta
now = datetime.now()
print(now)
tomorrow = now + timedelta(days=1)

# random - Random number generation
import random
print(random.randint(1, 10))       # Random int
print(random.choice([1, 2, 3]))    # Random choice
random.shuffle([1, 2, 3])          # Shuffle

# json - JSON handling
import json
data = {"name": "Alice", "age": 25}
json_string = json.dumps(data)     # Convert to JSON
parsed = json.loads(json_string)   # Parse JSON

# re - Regular expressions
import re
pattern = r"[0-9]+"
text = "I have 123 apples"
matches = re.findall(pattern, text)  # ['123']
```

---

## Advanced Concepts

### List Comprehensions

```python
# Basic list comprehension
numbers = [x for x in range(10)]  # [0, 1, 2, ..., 9]

# With condition
even_numbers = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# With transformation
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# Nested list comprehension
matrix = [[x for x in range(3)] for _ in range(3)]
# [[0, 1, 2], [0, 1, 2], [0, 1, 2]]

# Dictionary comprehension
word_lengths = {word: len(word) for word in ["apple", "banana", "cherry"]}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# Set comprehension
unique_lengths = {len(word) for word in ["apple", "apple", "banana"]}
# {5, 6}
```

### Lambda Functions

```python
# Basic lambda
square = lambda x: x**2
print(square(5))  # 25

# Lambda with multiple arguments
add = lambda x, y: x + y
print(add(3, 5))  # 8

# Using lambda with map()
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]

# Using lambda with filter()
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6]

# Using lambda with sorted()
students = [("Alice", 85), ("Bob", 75), ("Charlie", 90)]
sorted_students = sorted(students, key=lambda x: x[1])
# [("Bob", 75), ("Alice", 85), ("Charlie", 90)]
```

### Decorators

```python
# Simple decorator
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before function call
# Hello!
# After function call

# Decorator with arguments
def my_decorator_with_args(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator_with_args
def add(a, b):
    return a + b

result = add(3, 5)  # Calling add
print(result)       # 8

# Timing decorator (practical example)
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)

slow_function()
```

### Generators

```python
# Generator function
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
    i += 1

for number in count_up_to(3):
    print(number)  # 1, 2, 3

# Generator expression
numbers = (x**2 for x in range(5))  # Generator object
print(list(numbers))  # [0, 1, 4, 9, 16]

# Benefits: Memory efficient for large datasets
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

gen = infinite_sequence()
print(next(gen))  # 0
print(next(gen))  # 1
```

### Context Managers

```python
# Using context managers (with statement)
with open("file.txt", "r") as file:
    content = file.read()
# File is automatically closed

# Creating custom context manager
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")

with MyContextManager():
    print("Inside context")

# Output:
# Entering context
# Inside context
# Exiting context
```

---

## Best Practices

1. **Use Meaningful Names**: Choose descriptive variable and function names
2. **Keep Functions Small**: Each function should do one thing well
3. **Use Comments**: Explain complex logic and important decisions
4. **Follow PEP 8**: Python Enhancement Proposal 8 - Python style guide
5. **Error Handling**: Always handle potential errors appropriately
6. **Code Reusability**: Write functions and classes for common tasks
7. **Testing**: Write tests to verify your code works correctly
8. **Virtual Environments**: Use virtual environments for project isolation
9. **Documentation**: Write docstrings for functions and classes
10. **Avoid Global Variables**: Use functions and classes to encapsulate state

---

## Conclusion

Python fundamentals form the foundation for writing clean, efficient, and maintainable code. Mastering these concepts will enable you to tackle complex programming challenges and build robust applications. Continue practicing and exploring more advanced topics to further enhance your Python skills.

### Recommended Resources
- [Python Official Documentation](https://docs.python.org/3/)
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Real Python](https://realpython.com/)
- [Codecademy Python Course](https://www.codecademy.com/learn/learn-python)
