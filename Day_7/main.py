# SECTION 1: DECORATORS

from os import name


print("=" * 60)
print("SECTION 1: DECORATORS")
print("=" * 60)

def decorator(func):

    def wrapper():
        print("Wrapper function executed.")
        func()
        print("Wrapper function executed.")

    return wrapper

@decorator
def hello_world():
    print("Hello, World!")

hello_world()

# SECTION 2: PROPERTY DECORATORS

print("=" * 60)
print("SECTION 2: PROPERTY DECORATORS")
print("=" * 60)

# data validation, private/public (encapsulation)

class Person:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    # This is actually a getter, we can call 'name' but cannot change 'name'
    @property
    def name(self):
        return self.__name

    # This is a setter, we can change 'name', but its advantage is we can set some rules
    @name.setter
    def name(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("Name must be a string.")
            if len(value) < 2:
                raise ValueError("Name must be at least 2 characters long.")
        except Exception as error:
            print(f"Input: {value}, Error Message: {error}")
        else:
            self.__name = value

    @name.deleter
    def name(self):
        self.__name = None

    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, value):
        try:
            if not isinstance(value, int):
                raise ValueError("Age must be an integer.")
            if value < 0:
                raise ValueError("Age cannot be negative.")
        except Exception as error:
            print(f"Input: {value}, Error Message: {error}")
        else:
            self.__age = value

# Getter
ilker = Person("Ilker", 20)
print("Getter Methods")
print(ilker.name)
# Setter
print("\nSetter Methods")
ilker.name = "ilker"
print(ilker.name)

print("\nExceptions")
ilker.name = 20
ilker.name = "a"
ilker.age = "20"
ilker.age = -5

# Deleter
print("\nDeleter Methods")
del ilker.name
print(ilker.name)

# SECTION 3: STATIC METHODS

print("=" * 60)
print("SECTION 3: STATIC METHODS")
print("=" * 60)

class MathOperations:

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

a = 5
b = 3

print("Static Methods")    
print(f"{a} + {b} = {MathOperations.add(a, b)}")
print(f"{a} - {b} = {MathOperations.subtract(a, b)}")

# SECTION 4: CLASS METHODS

print("=" * 60)
print("SECTION 4: CLASS METHODS")
print("=" * 60)

class Pizza:

    total_pizzas = 0

    def __init__(self, ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    # The constructor for creating pre-set pizzas.
    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomatoes"])
    
    @classmethod
    def pepperoni(cls):
        return cls(["mozzarella", "tomatoes", "pepperoni"])
    
    @classmethod
    def vegetarian(cls):
        return cls(["mozzarella", "tomatoes", "bell peppers", "olives"])
    
    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas

print("Class Methods")    
margherita_pizza = Pizza.margherita()
print(f"Margherita Pizza Ingredients: {margherita_pizza.ingredients}")
pepperoni_pizza = Pizza.pepperoni()
print(f"Pepperoni Pizza Ingredients: {pepperoni_pizza.ingredients}")
vegetarian_pizza = Pizza.vegetarian()
print(f"Vegetarian Pizza Ingredients: {vegetarian_pizza.ingredients}")

print(f"Total pizzas: {Pizza.get_total_pizzas()}")

# SECTION 5: ABSTRACT METHODS

print("=" * 60)
print("SECTION 5: ABSTRACT METHODS")
print("=" * 60)

from abc import ABC, abstractmethod

class Animal(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def sleep(self):
        pass


class Dog(Animal):

    def make_sound(self):
        return "Woof!"

    def move(self):
        return "The dog runs."

    def sleep(self):
        return "The dog sleeps in its bed."
    

dog = Dog("Buddy")
print(f"{dog.name} says: {dog.make_sound()}")

# overloading, overriding, final

# SECTION 6: OVERLOADING

print("=" * 60)
print("SECTION 6: OVERLOADING")
print("=" * 60)

from typing import overload, Union

class Calculator:

    @overload
    def add(self, a: int, b: int, c:int) -> int: ...
    @overload
    def add(self, a:int, b:int) -> int: ...

    def add(self, a:int, b:int, c: int | None = None):
        if c is not None:
            return a + b + c
        return a + b

    @overload
    def process(self, value: int) -> int: ...

    @overload
    def process(self, value:str) -> str: ...

    def process(self, value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
        else:
            raise TypeError("Unsupported type")

calculator = Calculator()

print(calculator.add(5, 3))
print(calculator.add(5, 3, 2))

print(calculator.process(5))
print(calculator.process("hello"))

# SECTION 7: FINAL
print("=" * 60)
print("SECTION 7: FINAL")
print("=" * 60)

from typing import final

class BaseGame():

    def start(self):
        print("Game started!")

# It should not be overridden
    @final
    def calculate_score(self, points: int) -> int:
        return points * 10

    def end(self):
        print("Game ended!")

class MyGame(BaseGame):

    def start(self):
        print("MyGame started!")

    def calculate_score(self, points):
        return points * 2

#It should not used as base class
@final
class SecretAlgorithm:

    def process(self):
        print("Processing with secret algorithm...")

game = MyGame()
game.start()
secret_algorithm = SecretAlgorithm()
secret_algorithm.process()


# SECTION 8: OVERRIDE
print("=" * 60)
print("SECTION 8: OVERRIDE")
print("=" * 60)

from typing import override

class Shape:

    def area(self):
        return 0.0
    
    def perimeter(self):
        return 0.0

class Rectangle(Shape):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @override
    def area(self):
        return self.width * self.height
    
    @override
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):

    def __init__(self, radius):
        self.radius = radius

    @override
    def area(self):
        return 3.14 * self.radius ** 2
    
    @override
    def perimeter(self):
        return 2 * 3.14 * self.radius
    
rectangle = Rectangle(4, 5)
print(f"Rectangle Area: {rectangle.area()}")
print(f"Rectangle Perimeter: {rectangle.perimeter()}")
circle = Circle(3)
print(f"Circle Area: {circle.area()}")
print(f"Circle Perimeter: {circle.perimeter()}")

# SECTION 9: COMBINING DECORATORS

print("=" * 60)
print("SECTION 9: COMBINING DECORATORS")
print("=" * 60)

def multiply_decorator(func):
    
    def wrapper(x: int):
        return func(x) * 2

    return wrapper

def other_decorator(func):
    
    def wrapper(x: int):
        return func(x) * 4

    return wrapper

@multiply_decorator
@other_decorator
def calculate(x:int):
    return x * 2

print(calculate(5))