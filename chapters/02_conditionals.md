---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Conditionals and Loops

In this chapter, we're diving into **conditionals** and **loops** in Python. Conditionals are a fundamental concept in programming, allowing your code to make decisions based on certain criteria. Loops let you repeat actions multiple times. Together, these enable your programs to respond differently to different inputs or situations, making your code more dynamic and versatile.

## Understanding Comparison Operators

Before we can make decisions, we need to be able to compare values. Python provides several **comparison operators** for this purpose:

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal to | `5 >= 5` | `True` |
| `<=` | Less than or equal to | `5 <= 3` | `False` |
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |

```{warning}
Notice that we use **double equals** `==` for comparison. A single `=` is for **assignment** (storing a value in a variable). This is a very common source of bugs for beginners!
```

These operators allow you to ask questions about the relationship between values. Each comparison returns either `True` or `False` — these are called **boolean** values.

```{code-cell} ipython3
print(5 > 3)
```

```{code-cell} ipython3
print(5 < 3)
```

```{code-cell} ipython3
x = 10
print(x == 10)
```

## The `if` Statement

The `if` statement is the simplest form of a conditional. It checks a condition: if the condition is `True`, it executes a block of code. If the condition is `False`, it skips that code.

```python
x = int(input('Enter a number: '))

if x > 0:
    print('x is positive')
```

```
Enter a number: 2
x is positive
```

Let's break down what's happening:

1. We ask the user for a number and store it in `x`
2. The `if` statement checks whether `x > 0` is `True`
3. If it is, Python executes the indented code below (`print('x is positive')`)
4. If `x > 0` is `False`, Python skips the indented code entirely

```{note}
Notice the colon `:` after the condition, and the indentation of the code block. Both are required in Python!
```

### Multiple `if` Statements

We can check multiple conditions by using multiple `if` statements:

```python
x = int(input('What is x? '))
y = int(input('What is y? '))

if x < y:
    print('x is less than y')

if x > y:
    print('x is greater than y')

if x == y:
    print('x equals y')
```

```
What is x? 2
What is y? 2
x equals y
```

Notice how this works:
1. First, the condition `x < y` is evaluated — if `True`, it prints the message
2. Then, `x > y` is evaluated — if `True`, it prints the message
3. Finally, `x == y` is evaluated — if `True`, it prints the message

Each `if` statement is checked **independently**. This flow of decisions is called **control flow**.

## The `elif` Statement

The code above works, but it's inefficient. If `x` is less than `y`, we already know it can't be greater than or equal to `y`. Why check those conditions at all?

This is where `elif` (short for "else if") comes in:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
elif x == y:
    print("x is equal to y")
```

```
What's x? 2
What's y? 2
x is equal to y
```

Now the program is smarter:
1. First, it checks `x < y`
2. If that's `True`, it prints the message **and skips all remaining conditions**
3. If that's `False`, it moves to the first `elif` and checks `x > y`
4. And so on...

This is more efficient because once a condition is `True`, Python doesn't bother checking the rest.

## The `else` Statement

There's one more improvement we can make. Think about it logically: if `x` is not less than `y`, and `x` is not greater than `y`, then `x` **must** equal `y`. We don't need to check!

The `else` statement acts as a "catch-all" for when none of the previous conditions were `True`:

```python
x = int(input('What is x? '))
y = int(input('What is y? '))

if x < y:
    print('x is less than y')
elif x > y:
    print('x is greater than y')
else:
    print('x equals y')
```

```
What is x? 2
What is y? 2
x equals y
```

The `else` block runs when all previous conditions are `False`. It doesn't have a condition of its own — it's simply "everything else."

```{tip}
Use `else` when you have a clear "default" case. It makes your code cleaner and ensures you always handle every possibility.
```

## The `or` Operator

Sometimes you want to check if **at least one** of multiple conditions is true. The `or` operator does exactly this:

```python
x = int(input('What is x? '))
y = int(input('What is y? '))

if x < y or x > y:
    print('x is not equal to y')
else:
    print('x equals y')
```

```
What is x? 2
What is y? 5
x is not equal to y
```

The condition `x < y or x > y` is `True` if **either** `x < y` is true **or** `x > y` is true (or both).

But wait — there's a simpler way to check if two values are not equal. The `!=` operator does this directly:

```python
x = int(input('What is x? '))
y = int(input('What is y? '))

if x != y:
    print('x is not equal to y')
else:
    print('x equals y')
```

```
What is x? 2
What is y? 5
x is not equal to y
```

Much cleaner! The `!=` operator returns `True` if the values are different.

## The `and` Operator

The `and` operator checks if **both** conditions are true:

```python
score = int(input("Give me your score: "))

if score >= 90 and score <= 100:
    print('Grade A')
elif score >= 80 and score < 90:
    print('Grade B')
elif score >= 70 and score < 80:
    print('Grade C')
elif score >= 60 and score < 70:
    print('Grade D')
else:
    print('Fail')
```

```
Give me your score: 90
Grade A
```

The condition `score >= 90 and score <= 100` is `True` only if **both** parts are true — the score must be at least 90 **and** at most 100.

### Chained Comparisons

Python has a nice shortcut for range checks. Instead of `score >= 90 and score <= 100`, you can write:

```python
if 90 <= score <= 100:
    print('Grade A')
```

This reads almost like mathematical notation: "if 90 ≤ score ≤ 100".

### Further Simplification

We can simplify the grading program even more. Since we use `elif`, once we've determined the score isn't an A, we know it's below 90. So we don't need to check the upper bound:

```python
score = int(input("Give me your score: "))

if score >= 90:
    print('Grade A')
elif score >= 80:
    print('Grade B')
elif score >= 70:
    print('Grade C')
elif score >= 60:
    print('Grade D')
else:
    print('Fail')
```

```
Give me your score: 85
Grade B
```

This works because:
1. If score is 85, the first check `score >= 90` is `False`
2. Python moves to the next check: `score >= 80` is `True`
3. Python prints "Grade B" and skips all remaining conditions

## Loops and Iteration

Loops are powerful constructs that allow you to repeat a block of code multiple times. Python offers two types of loops:

- **`for` loops**: iterate over a sequence (like a list or range)
- **`while` loops**: continue as long as a condition remains `True`

### The Problem: Repetition

Imagine you want to print "meow" three times:

```{code-cell} ipython3
print('meow')
print('meow')
print('meow')
```

This works, but what if you wanted to print it 500 times? Typing `print('meow')` 500 times would be tedious and error-prone. This is exactly what loops are for — automating repetition.

### The `while` Loop

A `while` loop repeats as long as a condition is `True`:

```{code-cell} ipython3
i = 3

while i != 0:
    print('meow')
    i = i - 1
```

Let's trace through this step by step:

| Iteration | `i` at start | `i != 0`? | Action | `i` at end |
|-----------|--------------|-----------|--------|------------|
| 1 | 3 | `True` | Print "meow" | 2 |
| 2 | 2 | `True` | Print "meow" | 1 |
| 3 | 1 | `True` | Print "meow" | 0 |
| 4 | 0 | `False` | Exit loop | — |

The formal flow of a `while` loop:

1. Evaluate the condition
2. If `False`, exit the loop and continue with the next statement
3. If `True`, execute the body, then go back to step 1

```{warning}
The loop body must eventually make the condition `False`, otherwise you get an **infinite loop** — your program will run forever! The variable that controls when the loop ends is called the **iteration variable**.
```

Here's another example — a countdown:

```{code-cell} ipython3
n = 5

while n > 0:
    print(n)
    n = n - 1

print('Blastoff!')
```

You can almost read this as English: "While n is greater than 0, print n and reduce n by 1. When n reaches 0, print Blastoff!"

### The `for` Loop

A `for` loop iterates through a sequence of items. To understand `for` loops, let's first introduce **lists** — a way to store multiple values:

```{code-cell} ipython3
for i in [0, 1, 2]:
    print('meow')
```

Here, `[0, 1, 2]` is a list containing three items. The `for` loop goes through each item:
1. `i` is set to `0`, and "meow" is printed
2. `i` is set to `1`, and "meow" is printed
3. `i` is set to `2`, and "meow" is printed
4. No more items, so the loop ends

Notice how clean this is compared to the `while` loop! We don't need to manage a counter variable ourselves.

### The `range()` Function

What if you wanted to iterate 1000 times? Typing out `[0, 1, 2, ..., 999]` would be impractical. The `range()` function generates a sequence of numbers for you:

```{code-cell} ipython3
for i in range(3):
    print('meow')
```

`range(3)` generates the numbers 0, 1, and 2 (three numbers total, starting from 0). This is equivalent to `[0, 1, 2]` but much more convenient for large ranges.

```{note}
`range(n)` produces numbers from 0 to n-1 (not including n). So `range(5)` gives you 0, 1, 2, 3, 4.
```

You can also specify a starting point:

```{code-cell} ipython3
for i in range(1, 6):  # 1 to 5
    print(i)
```

Or even a step size:

```{code-cell} ipython3
for i in range(0, 10, 2):  # 0 to 9, stepping by 2
    print(i)
```

## When to Use `for` vs `while`

- Use a **`for` loop** when you know in advance how many times you want to iterate, or when you're going through a collection of items
- Use a **`while` loop** when you want to repeat until some condition changes, especially when you don't know in advance how many iterations you'll need

---

## Exercises

````{exercise}
:label: ex2-even-odd

**Exercise 1: Even or Odd**

Write a program that asks the user for a number and prints whether it's even or odd.

Hint: A number is even if dividing it by 2 leaves no remainder. Use the modulo operator `%`.
````

````{solution} ex2-even-odd
:class: dropdown

```python
n = int(input("Enter a number: "))

if n % 2 == 0:
    print("Even")
else:
    print("Odd")
```
````

````{exercise}
:label: ex2-age-category

**Exercise 2: Age Category**

Write a program that asks for a person's age and prints their life stage:
- 0-12: Child
- 13-19: Teenager
- 20-64: Adult
- 65+: Senior
````

````{solution} ex2-age-category
:class: dropdown

```python
age = int(input("Enter your age: "))

if age <= 12:
    print("Child")
elif age <= 19:
    print("Teenager")
elif age <= 64:
    print("Adult")
else:
    print("Senior")
```
````

````{exercise}
:label: ex2-countdown

**Exercise 3: Countdown**

Write a program using a `while` loop that counts down from a number entered by the user to 1, then prints "Blast off!".

For example, if the user enters 5, it should print:
```
5
4
3
2
1
Blast off!
```
````

````{solution} ex2-countdown
:class: dropdown

```python
n = int(input("Start countdown from: "))

while n > 0:
    print(n)
    n = n - 1

print("Blast off!")
```
````

````{exercise}
:label: ex2-sum

**Exercise 4: Sum of Numbers**

Write a program using a `for` loop that calculates the sum of all numbers from 1 to n, where n is entered by the user.

For example, if the user enters 5, the sum is 1+2+3+4+5 = 15.
````

````{solution} ex2-sum
:class: dropdown

```python
n = int(input("Enter n: "))
total = 0

for i in range(1, n + 1):
    total = total + i

print(f"The sum from 1 to {n} is {total}")
```
````
