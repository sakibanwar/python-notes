# Getting Started with Python

In this chapter, we'll write our first Python programs. We'll learn about printing output, working with different types of values, creating variables, and even building our own functions. By the end, you'll have a solid foundation for everything that follows.

## Your First Python Program

Let's start with the classic "Hello World" program. This is traditionally the first program anyone writes when learning a new language.

```python
print("Hello World")
```

```
Hello World
```

You'll notice we used a Python built-in function called `print()`. This function takes whatever you give it (we call this the *argument* or *input*) and displays it on the screen. Our argument was `"Hello World"`.

We could have done the same thing with a slight variation:

```python
print('Hello World')
```

```
Hello World
```

Notice here that we got the same result — it printed `Hello World`. But do you see the difference? We used single quotes `' '` instead of double quotes `" "`. In Python, both work exactly the same for strings. You can use whichever you prefer, but try to be consistent throughout your code.

```{tip}
**Which quotes should I use?** Most Python programmers use double quotes `"` by default. However, single quotes `'` are useful when your text contains double quotes, like `'She said "Hello"'`.
```

We can also print numbers:

```python
print(2)
```

```
2
```

```python
print(100)
```

```
100
```

## Values and Types

A **value** is one of the basic things a program works with, like a letter or a number. Notice that we printed `Hello World`, `2`, and `100`. These values belong to different **types**:

| Value | Type | Description |
|-------|------|-------------|
| `"Hello World"` | `str` (string) | Text enclosed in quotes |
| `2` | `int` (integer) | Whole numbers |
| `2.0` | `float` | Decimal numbers |

Strings are called "strings" because they contain a "string" of characters (letters, numbers, symbols). You can identify strings because they are enclosed in quotation marks.

Python can tell you the type of any value using the `type()` function:

```python
type('Hello World')
```

```
str
```

```python
type(2)
```

```
int
```

```python
type(2.0)
```

```
float
```

```python
type(2.2)
```

```
float
```

Now here's something important — what type is `'2'`?

```python
type('2')
```

```
str
```

Notice that `'2'` is a **string**, not an integer! The quotation marks make all the difference. Python sees the quotes and treats it as text, not a number. This distinction will become very important later when we start doing calculations with user input.

```{warning}
`2` and `'2'` are completely different things in Python! The first is a number you can do maths with. The second is text — you cannot add `'2' + '2'` and get `4` (you'd get `'22'`).
```

## Variables

One of the most powerful features of a programming language is the ability to manipulate **variables**. A variable is a name that refers to a value. Think of it like a labelled box where you can store things.

An **assignment statement** creates a new variable and gives it a value:

```python
message = 'And now for something completely different'
some_number = 2
```

The example above makes two assignments:
- The first assigns a string to a new variable named `message`
- The second assigns the integer `2` to `some_number`

The `=` sign here doesn't mean "equals" in the mathematical sense. It means "assign the value on the right to the variable on the left." Think of it as an arrow pointing left: `message ← 'And now for something...'`

To display the value of a variable, you can use a print statement:

```python
print(message)
```

```
And now for something completely different
```

```python
print(some_number)
```

```
2
```

The type of a variable is simply the type of the value it refers to:

```python
type(message)
```

```
str
```

```python
type(some_number)
```

```
int
```

### Variable Naming Rules

When naming variables, there are some rules you must follow:

1. Variable names can contain letters, numbers, and underscores `_`
2. They cannot start with a number
3. They cannot contain spaces (use underscores instead)
4. They are case-sensitive (`Name` and `name` are different variables)
5. They cannot be Python keywords (like `print`, `if`, `for`, etc.)

```python
# Good variable names
student_name = "Alice"
age = 25
total_score_2024 = 95

# Bad variable names (these will cause errors)
# 2nd_place = "Bob"      # Cannot start with number
# student name = "Carol" # Cannot contain spaces
```

## Print Function and Variables

In the `print()` function, we can include variables. Let's say we create a variable called `name`:

```python
name = "Nasreen"
```

```python
print("Hello", name)
```

```
Hello Nasreen
```

In the code above, we used two inputs to the print function: the string `"Hello"` and the variable `name`. The print function automatically adds a space between multiple arguments.

We could have gotten a similar result by **concatenating** (joining) strings:

```python
print("Hello" + name)
```

```
HelloNasreen
```

But the output is not quite right — there's no space between "Hello" and "Nasreen". We can fix that by adding a space inside the first string:

```python
print("Hello " + name)
```

```
Hello Nasreen
```

### The Input Function

Now let's make our program interactive by getting input from the user:

```python
name_input = input("What is your name? ")
print("Hello", name_input)
```

```
What is your name? Sakib
Hello Sakib
```

We successfully said hello to the user! Here's what happened:

1. We created a variable `name_input`
2. We used the built-in function `input()` to get the user's name
3. When `input()` is called, the program **stops and waits** for the user to type something
4. When the user presses Enter, the program resumes and `input()` returns what the user typed as a **string**

```{important}
The `input()` function **always returns a string**, even if the user types a number. This will matter when we start doing calculations!
```

### Formatting Strings (f-strings)

Probably the most elegant way to combine strings and variables is using **f-strings**:

```python
name_input = input("What is your name? ")
print(f"Hello {name_input}")
```

```
What is your name? Sakib
Hello Sakib
```

Notice the `f` before the opening quote in `print(f"Hello {name_input}")`. This `f` is a special indicator that tells Python to treat this string in a special way. Inside the string, anything in curly brackets `{}` will be replaced with the value of that variable.

F-strings are incredibly useful because they make your code more readable. Compare these two approaches:

```python
# Without f-strings (harder to read)
print("Hello " + name + ", you scored " + str(score) + " points!")

# With f-strings (much cleaner)
print(f"Hello {name}, you scored {score} points!")
```

You'll be using f-strings frequently throughout this course.

### Cleaning Up User Input

Look at the following program and its output:

```python
name_input = input("What is your name? ")
print("Hello", name_input)
```

```
What is your name?    Sakib   
Hello    Sakib   
```

We see that the user pressed the spacebar too many times! This messes up our output. You should never expect your users to cooperate perfectly. Therefore, you need to ensure that user input is cleaned up.

Python strings have a built-in method called `.strip()` that removes whitespace from both ends of a string:

```python
name_input = input("What is your name? ")
name_clean = name_input.strip()
print("Hello", name_clean)
```

```
What is your name?    Sakib   
Hello Sakib
```

Much better! The `.strip()` method removed all the extra spaces.

### The Title Method

What if the user types their name in all lowercase? We can use the `.title()` method to capitalise the first letter of each word:

```python
name = input("What's your name? ")
name = name.strip()       # Remove whitespace
name = name.title()       # Capitalise first letters
print(f"Hello, {name}")
```

```
What's your name? sakib
Hello, Sakib
```

Notice that we can modify our code to be more efficient by **chaining** methods together:

```python
name = input("What's your name? ")
name = name.strip().title()
print(f"Hello, {name}")
```

We could even go further and do it all in one line:

```python
name = input("What's your name? ").strip().title()
print(f"Hello, {name}")
```

```
What's your name? sakib
Hello, Sakib
```

This technique of chaining methods is very common in Python. Each method returns a new string, which the next method then operates on.

### Comments

Comments are a way for programmers to leave notes in their code. They're notes for yourself and others who will read your code! We write comments by putting a hash sign `#` at the start of a line:

```python
# Ask the user for their name
name = input("What's your name? ")

# Clean up the input and capitalise
name = name.strip().title()

# Print the greeting
print(f"Hello, {name}")
```

When Python sees a `#`, it ignores everything after it on that line. Comments don't affect how your program runs — they're purely for human readers.

```{tip}
Write comments to explain **why** you're doing something, not **what** the code does. The code itself shows what it does; comments should explain the reasoning behind it.
```

## Integers and Arithmetic

In Python, an integer is referred to as an `int`. Let's do some calculations:

```python
2 + 3
```

```
5
```

```python
a = 2
b = 3
print(a + b)
```

```
5
```

```python
print(a / b)
```

```
0.6666666666666666
```

```python
print(a * b)
```

```
6
```

Python supports all the basic arithmetic operators:

| Operator | Operation | Example | Result |
|----------|-----------|---------|--------|
| `+` | Addition | `2 + 3` | `5` |
| `-` | Subtraction | `5 - 2` | `3` |
| `*` | Multiplication | `4 * 3` | `12` |
| `/` | Division | `7 / 2` | `3.5` |
| `**` | Exponentiation | `2 ** 3` | `8` |
| `//` | Floor division | `7 // 2` | `3` |
| `%` | Modulo (remainder) | `7 % 2` | `1` |

For exponents (powers), we use `**`. So to calculate $2^3$ (2 × 2 × 2):

```python
2 ** 3
```

```
8
```

```python
print(a ** b)  # 2 to the power of 3
```

```
8
```

### Converting Types

Sometimes you need to convert between types. What if you want to convert a string to an integer?

```python
c = '2'
d = '3'
c1 = int(c)
d1 = int(d)
print(c1 * d1)
```

```
6
```

The `int()` function converts a value to an integer. Similarly, `float()` converts to a decimal number, and `str()` converts to a string.

```python
z = 3.2
z1 = int(z)
print(z1)
```

```
3
```

Notice that converting a float to an integer **truncates** (cuts off) the decimal part — it doesn't round!

### A Common Pitfall with Input

Let's make an interactive calculator:

```python
x = input("What's x? ")
y = input("What's y? ")
z = x + y
print(z)
```

```
What's x? 1
What's y? 2
12
```

Wait, what? We expected `3`, not `12`! Why did this happen?

Remember that `input()` always returns a **string**. So `x` is the string `'1'` and `y` is the string `'2'`. When you use `+` with strings, Python **concatenates** them (joins them together), giving us `'12'`.

To fix this, we need to convert the inputs to integers:

```python
x = input("What's x? ")
y = input("What's y? ")
z = int(x) + int(y)
print(z)
```

```
What's x? 1
What's y? 2
3
```

We can make this even cleaner:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))
print(x + y)
```

```
What's x? 1
What's y? 2
3
```

## Creating Your Own Functions

So far, we've used functions that come with Python (`print()`, `input()`, `type()`, `int()`). But you can also create your own functions! A function is a reusable block of code that performs a specific task.

We use the `def` keyword to **define** a function:

```python
def print_lyrics():
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")
```

Let's break this down:

- `def` is a keyword that tells Python we're defining a function
- `print_lyrics` is the name of our function
- `()` contains the parameters (inputs) — empty here because this function takes no inputs
- `:` marks the end of the function header
- The indented lines below are the function **body** — the code that runs when you call the function

```{note}
In Python, indentation matters! The function body must be indented (typically 4 spaces). This is how Python knows which code belongs to the function.
```

Let's check what type `print_lyrics` is:

```python
type(print_lyrics)
```

```
function
```

No surprise — it's a function! Now let's **call** the function:

```python
print_lyrics()
```

```
I'm a lumberjack, and I'm okay.
I sleep all night and I work all day.
```

### Functions with Parameters

Let's create a function that takes inputs (called **parameters**):

```python
def add_two_things(a, b):
    addition = a + b
    print(addition)
```

Now let's call it:

```python
add_two_things(3, 2)
```

```
5
```

We get the desired result. But what if we want to use this function's result somewhere else? Let's try:

```python
add_two_things(3, 2) * 3
```

```
5
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

We get an error! The problem is that our function **prints** the result but doesn't **return** it. When a function doesn't explicitly return a value, it returns `None` — and you can't multiply `None` by 3.

### The Return Statement

To fix this, we use `return` instead of `print()`:

```python
def add_two_things(a, b):
    addition = a + b
    return addition
```

Now the function **gives back** a value that we can use:

```python
add_two_things(3, 2) * 3
```

```
15
```

The difference between `print` and `return`:
- `print()` displays something on the screen (for humans to see)
- `return` gives a value back to the code that called the function (for the program to use)

Let's make our calculator interactive:

```python
def add_two_things(a, b):
    addition = a + b
    return addition

a = int(input('What is the number a? '))
b = int(input('What is the number b? '))
result = add_two_things(a, b)
print(f"The sum is {result}")
```

```
What is the number a? 5
What is the number b? 7
The sum is 12
```

---

## Exercises

Test your understanding with these exercises. Write your code and check your answers!

````{exercise}
:label: ex1-hello

**Exercise 1: Personalised Greeting**

Write a program that:
1. Asks the user for their name
2. Asks the user for their favourite colour
3. Prints a message like: "Hello Alice, your favourite colour is blue!"

Use f-strings for the output.
````

````{solution} ex1-hello
:class: dropdown

```python
name = input("What is your name? ")
colour = input("What is your favourite colour? ")
print(f"Hello {name}, your favourite colour is {colour}!")
```
````

````{exercise}
:label: ex1-calculator

**Exercise 2: Simple Calculator**

Write a program that:
1. Asks the user for two numbers
2. Prints their sum, difference, product, and quotient

Remember to convert the inputs to numbers!
````

````{solution} ex1-calculator
:class: dropdown

```python
x = float(input("Enter first number: "))
y = float(input("Enter second number: "))

print(f"Sum: {x + y}")
print(f"Difference: {x - y}")
print(f"Product: {x * y}")
print(f"Quotient: {x / y}")
```
````

````{exercise}
:label: ex1-function

**Exercise 3: Create a Function**

Write a function called `square` that takes a number and returns its square (the number multiplied by itself).

Then use the function to print the square of 7.
````

````{solution} ex1-function
:class: dropdown

```python
def square(n):
    return n * n

print(square(7))  # Should print 49
```
````
