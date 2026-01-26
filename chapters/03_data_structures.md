# Data Structures and Loops

So far, we've stored information in individual variables:

```python
a = 'Sakib'
b = 1
c = 2.0
```

Maybe we want to store the age of Sakib:

```python
sakib_age = 100
```

But this approach becomes impractical quickly. What if we need to store the age of everyone in a class of 50 students? We'd need 50 separate variables — a waste of memory and effort!

Instead, we can store multiple pieces of information using Python's built-in **data structures**. Here's a preview:

```python
age = [10, 20, 32, 35, 26]
```

We've just stored 5 ages in a single variable! Let's explore how this works.

## Python's Built-in Data Structures

Python has four main built-in data structures:

| Structure | Syntax | Description |
|-----------|--------|-------------|
| **List** | `[item1, item2, ...]` | Ordered, changeable collection |
| **Dictionary** | `{key1: value1, ...}` | Key-value pairs |
| **Tuple** | `(item1, item2, ...)` | Ordered, unchangeable collection |
| **Set** | `{item1, item2, ...}` | Unordered collection of unique items |

Let's see examples of each:

**List:**
```python
age = [10, 20, 32, 35, 26]
```

**Dictionary:**
```python
students = {
    'Hermoine': 'Gryffindor',
    'Harry': 'Gryffindor',
    'Ron': 'Gryffindor',
    'Draco': 'Slytherin'
}
```

**Tuple:**
```python
age_tuple = (10, 20, 30, 200)
```

We'll focus mainly on **lists** and **dictionaries** in this chapter, as they're the most commonly used.

## Lists

A **list** is an ordered collection of items. Think of it like a numbered container where you can store multiple values.

### Creating Lists

```python
list_of_students = ['Hermoine', 'Harry', 'Ron', 'Draco']
```

```python
animals = ['dog', 'cat', 'cow']
```

```python
ages = [10, 20, 32, 35, 26]
```

Lists can contain **any type** of value, and you can even mix types:

```python
anything = ['spam', 2.0, 5, [10, 20]]
```

Notice that last item — a list inside a list! This is called a **nested** list.

An empty list is created with empty brackets:

```python
empty = []
```

### Finding the Length of a List

The `len()` function tells you how many items are in a list:

```python
len(list_of_students)
```

```
4
```

### Accessing Items (Indexing)

Each item in a list has a position number called an **index**. Here's the crucial thing to remember: **indexing starts at 0, not 1!**

```python
list_of_students = ['Hermoine', 'Harry', 'Ron', 'Draco']
```

| Index | 0 | 1 | 2 | 3 |
|-------|---|---|---|---|
| Value | Hermoine | Harry | Ron | Draco |

To access the **first** item:

```python
list_of_students[0]
```

```
'Hermoine'
```

```python
print(list_of_students[0])
```

```
Hermoine
```

To access the **last** item (index 3):

```python
list_of_students[3]
```

```
'Draco'
```

What happens if you try to access an index that doesn't exist?

```python
list_of_students[4]
```

```
IndexError: list index out of range
```

You get an **IndexError** because our list only has 4 items (indices 0-3), so index 4 doesn't exist.

```{tip}
You can use negative indices to count from the end. `list_of_students[-1]` gives you the last item, `list_of_students[-2]` gives the second-to-last, and so on.
```

### Adding Items to a List

Use the `.append()` method to add an item to the end of a list:

```python
list_of_students.append('Sakib')
list_of_students
```

```
['Hermoine', 'Harry', 'Ron', 'Draco', 'Sakib']
```

### Changing Items (Lists are Mutable)

Lists are **mutable**, meaning you can change their contents after creation. Let's replace 'Sakib' with 'Joe':

```python
list_of_students[4] = 'Joe'
list_of_students
```

```
['Hermoine', 'Harry', 'Ron', 'Draco', 'Joe']
```

### Iterating Through a List

If we want to print all the student names one by one, we could do this:

```python
print(list_of_students[0])
print(list_of_students[1])
print(list_of_students[2])
print(list_of_students[3])
print(list_of_students[4])
```

```
Hermoine
Harry
Ron
Draco
Joe
```

But this is tedious! What if we had 1000 students? Instead, we use a **loop**:

```python
for student in list_of_students:
    print(student)
```

```
Hermoine
Harry
Ron
Draco
Joe
```

Much better! The `for` loop automatically goes through each item in the list, one at a time. In each iteration, the variable `student` holds the current item.

### Getting Position and Value Together

What if you want to print both the position and the name? You can combine `range()` with `len()`:

```python
for i in range(len(list_of_students)):
    print(i + 1, list_of_students[i])
```

```
1 Hermoine
2 Harry
3 Ron
4 Draco
5 Joe
```

Here's what's happening:
1. `len(list_of_students)` returns `5`
2. `range(5)` generates `0, 1, 2, 3, 4`
3. In each iteration, `i` is the index, and `list_of_students[i]` is the student at that index
4. We print `i + 1` to show human-friendly numbering (1, 2, 3... instead of 0, 1, 2...)

```{note}
Python also has a built-in function `enumerate()` that does this more elegantly. We'll cover that later!
```

## Dictionaries

A **dictionary** (or `dict`) is a data structure that associates **keys** with **values**. Unlike lists, which use numeric indices, dictionaries let you use meaningful labels.

### Why Dictionaries?

Imagine we want to associate students with their houses at Hogwarts:

| Hermoine | Harry | Ron | Draco |
|----------|-------|-----|-------|
| Gryffindor | Gryffindor | Gryffindor | Slytherin |

We could use two separate lists:

```python
students = ["Hermoine", "Harry", "Ron", "Draco"]
houses = ["Gryffindor", "Gryffindor", "Gryffindor", "Slytherin"]
```

The idea is that `students[0]` corresponds to `houses[0]`, `students[1]` to `houses[1]`, and so on. But this approach is fragile — if we accidentally reorder one list but not the other, everything breaks!

A dictionary makes this relationship explicit:

```python
students = {
    "Hermoine": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin"
}
```

### Accessing Values

To get a value from a dictionary, you use its key:

```python
print(students['Hermoine'])
```

```
Gryffindor
```

```python
print(students['Draco'])
```

```
Slytherin
```

Think of it like looking up a word in a real dictionary — you search for the word (key) and get its definition (value).

### Iterating Through a Dictionary

You can loop through a dictionary's keys:

```python
for name in students:
    print(name)
```

```
Hermoine
Harry
Ron
Draco
```

Notice this only prints the **keys**. To get the values too:

```python
for name in students:
    print(name, students[name])
```

```
Hermoine Gryffindor
Harry Gryffindor
Ron Gryffindor
Draco Slytherin
```

Let's make the output more readable:

```python
for name in students:
    print(name, "lives in", students[name])
```

```
Hermoine lives in Gryffindor
Harry lives in Gryffindor
Ron lives in Gryffindor
Draco lives in Slytherin
```

### Adding More Information

What if we want to store more data about each student — not just their house, but also their gender?

| Name | House | Gender |
|------|-------|--------|
| Hermoine | Gryffindor | Female |
| Harry | Gryffindor | Male |
| Draco | Slytherin | Male |

We can create a **list of dictionaries** — each dictionary represents one student with all their attributes:

```python
students_info = [
    {'name': 'Hermoine', 'house': 'Gryffindor', 'gender': 'female'},
    {'name': 'Harry', 'house': 'Gryffindor', 'gender': 'male'},
    {'name': 'Draco', 'house': 'Slytherin', 'gender': 'male'}
]
```

Now we have a list called `students_info` containing three dictionaries. Each dictionary has three key-value pairs.

```python
for student in students_info:
    print(
        student['name'], 
        'lives in', student['house'], 
        'and is', student['gender']
    )
```

```
Hermoine lives in Gryffindor and is female
Harry lives in Gryffindor and is male
Draco lives in Slytherin and is male
```

This structure — a list of dictionaries — is extremely common in data analysis. It's essentially a table where each dictionary is a row, and each key is a column.

### Adding Items to a Dictionary

To add a new key-value pair, simply assign to a new key:

```python
students['sakib'] = 'Winchester'
students
```

```
{'Hermoine': 'Gryffindor',
 'Harry': 'Gryffindor',
 'Ron': 'Gryffindor',
 'Draco': 'Slytherin',
 'sakib': 'Winchester'}
```

### Changing Values

You can update an existing value the same way:

```python
students['Draco'] = 'Winchester'
students
```

```
{'Hermoine': 'Gryffindor',
 'Harry': 'Gryffindor',
 'Ron': 'Gryffindor',
 'Draco': 'Winchester',
 'sakib': 'Winchester'}
```

Draco has transferred to Winchester!

## Tuples (Brief Overview)

A **tuple** is like a list, but **immutable** — once created, you cannot change it:

```python
coordinates = (10, 20)
```

Tuples are useful when you have data that shouldn't be modified. We'll see them more when we work with pandas.

## Summary: Lists vs Dictionaries

| Feature | List | Dictionary |
|---------|------|------------|
| Syntax | `[item1, item2, ...]` | `{key1: value1, ...}` |
| Access | By index number `list[0]` | By key `dict['key']` |
| Order | Ordered | Ordered (Python 3.7+) |
| Best for | Sequential data, collections | Named data, lookups |

---

## Exercises

````{exercise}
:label: ex3-list-ops

**Exercise 1: List Operations**

Create a list called `fruits` containing: apple, banana, cherry.

1. Add "orange" to the end of the list
2. Change "banana" to "blueberry"
3. Print the length of the list
4. Print each fruit on a separate line using a loop
````

````{solution} ex3-list-ops
:class: dropdown

```python
fruits = ['apple', 'banana', 'cherry']

# Add orange
fruits.append('orange')

# Change banana to blueberry
fruits[1] = 'blueberry'

# Print length
print(len(fruits))

# Print each fruit
for fruit in fruits:
    print(fruit)
```
````

````{exercise}
:label: ex3-dict-create

**Exercise 2: Create a Dictionary**

Create a dictionary called `prices` that maps the following items to their prices:
- milk: 1.50
- bread: 2.00
- eggs: 3.25

Then print each item and its price in the format: "milk costs £1.50"
````

````{solution} ex3-dict-create
:class: dropdown

```python
prices = {
    'milk': 1.50,
    'bread': 2.00,
    'eggs': 3.25
}

for item in prices:
    print(f"{item} costs £{prices[item]}")
```
````

````{exercise}
:label: ex3-students-table

**Exercise 3: Student Records**

Create a list of dictionaries representing 3 students. Each student should have:
- name
- age
- course

Then write a loop that prints each student's information in a nice format.
````

````{solution} ex3-students-table
:class: dropdown

```python
students = [
    {'name': 'Alice', 'age': 22, 'course': 'Economics'},
    {'name': 'Bob', 'age': 25, 'course': 'Data Science'},
    {'name': 'Carol', 'age': 23, 'course': 'Business'}
]

for student in students:
    print(f"{student['name']} is {student['age']} years old, studying {student['course']}")
```
````

````{exercise}
:label: ex3-list-sum

**Exercise 4: Sum and Average**

Given the list `scores = [85, 92, 78, 90, 88]`:

1. Calculate the sum of all scores
2. Calculate the average (mean) score
3. Find the highest score
4. Find the lowest score

Hint: You can use a loop, or Python has built-in functions `sum()`, `max()`, and `min()`.
````

````{solution} ex3-list-sum
:class: dropdown

```python
scores = [85, 92, 78, 90, 88]

# Method 1: Using built-in functions
total = sum(scores)
average = total / len(scores)
highest = max(scores)
lowest = min(scores)

print(f"Sum: {total}")
print(f"Average: {average}")
print(f"Highest: {highest}")
print(f"Lowest: {lowest}")

# Method 2: Using a loop (for sum)
total_loop = 0
for score in scores:
    total_loop = total_loop + score
print(f"Sum (loop): {total_loop}")
```
````
