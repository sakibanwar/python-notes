# Creating Dashboards with Streamlit

So far in this course, you've been writing Python code in Jupyter notebooks. Notebooks are great for exploration and analysis, but what if you want to share your work with someone who doesn't know Python? What if you want to create an interactive tool that lets users filter data, change parameters, and see results update instantly?

This is where **Streamlit** comes in. Streamlit lets you turn your Python scripts into interactive web applications — without needing to know HTML, CSS, or JavaScript.

---

## What is Streamlit?

Streamlit is a Python library that makes it incredibly easy to create data-driven web apps. You write a Python script, and Streamlit automatically converts it into an interactive dashboard that runs in a web browser.

Here's why Streamlit is perfect for data analysts:

| Feature | Benefit |
|---------|---------|
| Pure Python | No web development knowledge needed |
| Reactive | Changes update automatically |
| Interactive widgets | Sliders, dropdowns, buttons built-in |
| Data-friendly | Works seamlessly with pandas and plotting libraries |
| Free deployment | Host your apps on Streamlit Cloud |

Think of Streamlit as the bridge between your analysis and your audience. Your manager doesn't need to run Python code — they can just interact with your dashboard.

---

## Installing Streamlit

Before we begin, you'll need to install Streamlit. Open your terminal (or Anaconda Prompt on Windows) and run:

```bash
pip install streamlit
```

You'll also want Plotly for interactive charts:

```bash
pip install plotly
```

To verify the installation worked:

```bash
streamlit --version
```

```
Streamlit, version 1.28.0
```

```{note}
Streamlit apps are **not** run in Jupyter notebooks. You write them as `.py` files and run them from the command line. This is a key difference from everything else we've done in this course.
```

---

## Your First Streamlit App

Let's create a simple app to understand how Streamlit works.

Create a new file called `hello_app.py` with the following code:

```python
import streamlit as st

st.title("Hello, Streamlit!")
st.write("This is my first Streamlit app.")
```

Now, open your terminal, navigate to the folder containing this file, and run:

```bash
streamlit run hello_app.py
```

Your web browser will open automatically, showing your app:

```
Hello, Streamlit!

This is my first Streamlit app.
```

Notice how simple that was — just two lines of Python, and you have a web app!

---

## Basic Streamlit Elements

Streamlit provides many functions for displaying content. Let's explore the most common ones.

### Text Elements

```python
import streamlit as st

# Large title
st.title("Main Title")

# Section header
st.header("This is a Header")

# Smaller subheader
st.subheader("This is a Subheader")

# Regular text
st.write("This is regular text using st.write()")

# Markdown formatting
st.markdown("You can use **bold**, *italics*, and even `code` formatting.")

# Display code
st.code("print('Hello, World!')", language="python")
```

The `st.write()` function is particularly versatile — it automatically detects what you pass to it and displays it appropriately. Pass it a string, it shows text. Pass it a DataFrame, it shows a table. Pass it a chart, it displays the chart.

### Displaying Data

When working with pandas DataFrames, you have two main options:

```python
import streamlit as st
import pandas as pd

# Create sample data
data = {
    'Name': ['Harry', 'Hermione', 'Ron', 'Draco'],
    'House': ['Gryffindor', 'Gryffindor', 'Gryffindor', 'Slytherin'],
    'Score': [85, 95, 78, 82]
}
df = pd.DataFrame(data)

# Option 1: Static table
st.write("### Student Scores")
st.write(df)

# Option 2: Interactive table (sortable, searchable)
st.dataframe(df)

# Option 3: Display metrics
st.metric(label="Average Score", value=df['Score'].mean(), delta="+5 from last term")
```

The `st.dataframe()` function creates an interactive table that users can sort by clicking column headers. The `st.metric()` function is perfect for displaying KPIs (Key Performance Indicators) with optional change indicators.

---

## Interactive Widgets

This is where Streamlit really shines. Widgets let users interact with your app — filtering data, adjusting parameters, and making selections.

### Text Input

```python
import streamlit as st

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}!")
```

Notice the pattern here: the widget returns the user's input, which you store in a variable. Then you can use that variable in your code.

### Select Box (Dropdown)

```python
import streamlit as st

house = st.selectbox(
    "Choose a Hogwarts house:",
    options=["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
)

st.write(f"You selected: {house}")
```

### Multi-Select

When you want users to select multiple options:

```python
import streamlit as st

houses = st.multiselect(
    "Select houses to include:",
    options=["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"],
    default=["Gryffindor", "Slytherin"]  # Pre-selected options
)

st.write(f"You selected: {houses}")
```

### Slider

Perfect for numeric ranges:

```python
import streamlit as st

# Single value slider
age = st.slider("Select age:", min_value=11, max_value=18, value=15)
st.write(f"Age: {age}")

# Range slider (two handles)
score_range = st.slider(
    "Select score range:",
    min_value=0,
    max_value=100,
    value=(60, 90)  # Tuple creates range slider
)
st.write(f"Score range: {score_range[0]} to {score_range[1]}")
```

### Checkbox

```python
import streamlit as st

show_data = st.checkbox("Show raw data")

if show_data:
    st.write("Here's the raw data...")
```

### Button

```python
import streamlit as st

if st.button("Click me!"):
    st.write("Button was clicked!")
    st.balloons()  # Fun celebration animation!
```

---

## The Sidebar

For more complex apps, you don't want all your controls cluttering the main area. Streamlit provides a sidebar for filters and settings.

Simply prefix any widget with `st.sidebar`:

```python
import streamlit as st
import pandas as pd

# Main content
st.title("Sales Dashboard")

# Sidebar controls
st.sidebar.header("Filters")

city = st.sidebar.selectbox(
    "Select city:",
    options=["London", "Manchester", "Birmingham"]
)

date_range = st.sidebar.slider(
    "Select date range:",
    min_value=1,
    max_value=31,
    value=(1, 31)
)

# Use the filter values
st.write(f"Showing data for {city}, days {date_range[0]}-{date_range[1]}")
```

The sidebar appears on the left side of your app and can be collapsed by the user. This keeps your main area clean while still providing powerful filtering options.

---

## Layout with Columns

You can create multi-column layouts to display content side-by-side:

```python
import streamlit as st

# Create two columns
left_column, right_column = st.columns(2)

# Add content to left column
with left_column:
    st.header("Left Side")
    st.write("This appears on the left")

# Add content to right column
with right_column:
    st.header("Right Side")
    st.write("This appears on the right")
```

You can also create unequal columns:

```python
import streamlit as st

# 70-30 split
col1, col2 = st.columns([7, 3])

with col1:
    st.write("This column is wider (70%)")

with col2:
    st.write("Narrower (30%)")
```

This is especially useful for dashboards where you want to display multiple charts or KPIs side-by-side.

---

## Data Caching

When your app loads data from a file or database, you don't want to reload it every time the user interacts with a widget. Streamlit provides caching to solve this.

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """Load data from CSV - this only runs once!"""
    df = pd.read_csv('sales_data.csv')
    return df

# This function is cached - data loads once, then reuses
df = load_data()

st.write(f"Loaded {len(df)} rows")
```

The `@st.cache_data` decorator tells Streamlit to store the result of this function. The first time your app runs, it loads the data. After that, it uses the cached version — making your app much faster!

```{warning}
Without caching, your app would reload the entire dataset every time a user moves a slider or changes a selection. For large datasets, this makes the app painfully slow. Always cache your data loading functions!
```

---

## Interactive Charts with Plotly

While Streamlit works with matplotlib and seaborn, **Plotly Express** creates truly interactive charts that users can hover over, zoom, and pan.

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
df = pd.DataFrame({
    'City': ['London', 'London', 'Manchester', 'Manchester', 'Birmingham', 'Birmingham'],
    'Month': ['Jan', 'Feb', 'Jan', 'Feb', 'Jan', 'Feb'],
    'Sales': [1200, 1350, 890, 920, 670, 710]
})

# Create a bar chart
fig = px.bar(
    df,
    x='City',
    y='Sales',
    color='Month',
    title='Sales by City and Month',
    barmode='group'
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
```

The `use_container_width=True` parameter makes the chart fill the available width, which looks better on different screen sizes.

### Other Plotly Chart Types

```python
import plotly.express as px

# Scatter plot
fig = px.scatter(df, x='total_bill', y='tip', color='day',
                 title='Tips vs Total Bill')

# Line chart
fig = px.line(df, x='date', y='sales', color='category',
              title='Sales Over Time')

# Pie chart
fig = px.pie(df, values='sales', names='region',
             title='Sales by Region')

# Histogram
fig = px.histogram(df, x='age', nbins=20,
                   title='Age Distribution')
```

---

## Building a Complete Dashboard

Now let's put everything together to build a real dashboard. We'll create a sales analysis tool.

Create a file called `sales_dashboard.py`:

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================
# DATA LOADING (with caching)
# ============================================
@st.cache_data
def load_data():
    """Load and prepare the sales data."""
    # For this example, we'll create sample data
    # In practice, you'd load from: pd.read_csv('your_file.csv')
    data = {
        'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'City': ['London', 'Manchester', 'Birmingham', 'Leeds'] * 25,
        'Product': ['Electronics', 'Clothing', 'Food', 'Books'] * 25,
        'Sales': [150, 200, 80, 120, 180, 220, 90, 140] * 12 + [160, 210, 85, 125],
        'Units': [10, 15, 20, 8, 12, 18, 25, 10] * 12 + [11, 16, 21, 9]
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.header("🔍 Filters")

# City filter
cities = st.sidebar.multiselect(
    "Select City:",
    options=df['City'].unique(),
    default=df['City'].unique()
)

# Product filter
products = st.sidebar.multiselect(
    "Select Product Category:",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

# Date range filter
date_range = st.sidebar.slider(
    "Select Date Range (Day of Year):",
    min_value=1,
    max_value=100,
    value=(1, 100)
)

# ============================================
# APPLY FILTERS
# ============================================
# Filter the dataframe based on user selections
df_filtered = df[
    (df['City'].isin(cities)) &
    (df['Product'].isin(products))
]

# Apply date filter (using row index as proxy for simplicity)
df_filtered = df_filtered.iloc[date_range[0]-1:date_range[1]]

# ============================================
# MAIN PAGE
# ============================================
st.title("📊 Sales Dashboard")
st.markdown("### Overview of Sales Performance")

# Check if we have data after filtering
if df_filtered.empty:
    st.warning("No data matches your filter criteria. Please adjust the filters.")
    st.stop()

# ============================================
# KPI METRICS (Top Row)
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = df_filtered['Sales'].sum()
    st.metric("Total Sales", f"£{total_sales:,.0f}")

with col2:
    total_units = df_filtered['Units'].sum()
    st.metric("Units Sold", f"{total_units:,}")

with col3:
    avg_sale = df_filtered['Sales'].mean()
    st.metric("Avg Sale Value", f"£{avg_sale:,.2f}")

with col4:
    num_transactions = len(df_filtered)
    st.metric("Transactions", f"{num_transactions}")

st.markdown("---")

# ============================================
# CHARTS (Two columns)
# ============================================
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Sales by City")
    sales_by_city = df_filtered.groupby('City')['Sales'].sum().reset_index()
    fig_city = px.bar(
        sales_by_city,
        x='City',
        y='Sales',
        color='City',
        title='Total Sales by City'
    )
    fig_city.update_layout(showlegend=False)
    st.plotly_chart(fig_city, use_container_width=True)

with right_col:
    st.subheader("Sales by Product")
    sales_by_product = df_filtered.groupby('Product')['Sales'].sum().reset_index()
    fig_product = px.pie(
        sales_by_product,
        values='Sales',
        names='Product',
        title='Sales Distribution by Product'
    )
    st.plotly_chart(fig_product, use_container_width=True)

st.markdown("---")

# ============================================
# DETAILED DATA TABLE
# ============================================
st.subheader("📋 Detailed Data")

show_data = st.checkbox("Show raw data table")

if show_data:
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True
    )

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("*Dashboard created with Streamlit • Data Analytics Course*")
```

To run this dashboard:

```bash
streamlit run sales_dashboard.py
```

Let's break down what this dashboard does:

1. **Page configuration** — Sets the browser tab title and icon, uses wide layout
2. **Data loading** — Uses caching so data only loads once
3. **Sidebar filters** — Users can filter by city, product, and date range
4. **Filtered data** — Applies all filters using boolean indexing
5. **KPI metrics** — Shows key numbers in a row at the top
6. **Charts** — Bar chart and pie chart side-by-side
7. **Data table** — Optional detailed view (hidden by default)

---

## A Tips Explorer Dashboard

Let's build another example — an interactive explorer for the tips dataset:

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

# Page config
st.set_page_config(page_title="Tips Explorer", page_icon="💰", layout="wide")

# Load the tips dataset
@st.cache_data
def load_tips():
    return sns.load_dataset('tips')

tips_df = load_tips()

# Title
st.title("💰 Tips Dataset Explorer")
st.write("Explore the relationship between bills, tips, and other factors")

# Sidebar filters
st.sidebar.header("Filters")

# Day filter
days = st.sidebar.multiselect(
    "Select Day(s):",
    options=tips_df['day'].unique(),
    default=tips_df['day'].unique()
)

# Time filter
time = st.sidebar.multiselect(
    "Select Time:",
    options=tips_df['time'].unique(),
    default=tips_df['time'].unique()
)

# Party size slider
size_range = st.sidebar.slider(
    "Party Size:",
    min_value=int(tips_df['size'].min()),
    max_value=int(tips_df['size'].max()),
    value=(int(tips_df['size'].min()), int(tips_df['size'].max()))
)

# Apply filters
filtered_df = tips_df[
    (tips_df['day'].isin(days)) &
    (tips_df['time'].isin(time)) &
    (tips_df['size'] >= size_range[0]) &
    (tips_df['size'] <= size_range[1])
]

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Records", len(filtered_df))

with col2:
    avg_tip = filtered_df['tip'].mean()
    st.metric("Avg Tip", f"${avg_tip:.2f}")

with col3:
    avg_pct = (filtered_df['tip'] / filtered_df['total_bill'] * 100).mean()
    st.metric("Avg Tip %", f"{avg_pct:.1f}%")

# Scatter plot
st.subheader("Tips vs Total Bill")
fig = px.scatter(
    filtered_df,
    x='total_bill',
    y='tip',
    color='smoker',
    size='size',
    hover_data=['day', 'time'],
    title='Relationship between Bill Amount and Tip'
)
st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
```

---

## Running and Sharing Your App

### Running Locally

1. Save your code as a `.py` file
2. Open terminal/command prompt
3. Navigate to the folder containing your file
4. Run: `streamlit run your_app.py`

The app opens in your default browser at `http://localhost:8501`

### Stopping the App

Press `Ctrl+C` in the terminal to stop the server.

### Deploying to Streamlit Cloud

Streamlit offers free hosting for your apps:

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and main file
6. Click "Deploy"

Your app will be live at a URL like: `https://yourname-yourapp.streamlit.app`

```{tip}
Make sure your repository includes a `requirements.txt` file listing all the packages your app needs:

```
streamlit
pandas
plotly
seaborn
```
```

---

## Common Patterns and Tips

### Handling Empty Filters

Always check if filtering leaves you with no data:

```python
if df_filtered.empty:
    st.warning("No data matches your selection. Please adjust filters.")
    st.stop()  # Stop execution here
```

### Formatting Numbers

```python
# Currency
st.metric("Revenue", f"£{value:,.2f}")

# Percentages
st.metric("Growth", f"{pct:.1f}%")

# Large numbers with commas
st.metric("Population", f"{count:,}")
```

### Adding Emojis

Emojis make dashboards more visually appealing:

```python
st.title("📊 Sales Dashboard")
st.header("🔍 Filter Options")
st.success("✅ Data loaded successfully!")
st.error("❌ Error loading data")
st.warning("⚠️ No data found")
st.info("ℹ️ Tip: Try adjusting the filters")
```

### Progress and Status

For long-running operations:

```python
import time

with st.spinner("Loading data..."):
    time.sleep(2)  # Simulating slow operation
    data = load_large_dataset()

st.success("Data loaded!")
```

---

## Summary

In this chapter, you've learned how to:

| Concept | Code |
|---------|------|
| Display text | `st.title()`, `st.write()`, `st.markdown()` |
| Show data | `st.dataframe()`, `st.metric()` |
| Create dropdowns | `st.selectbox()`, `st.multiselect()` |
| Add sliders | `st.slider()` |
| Use sidebar | `st.sidebar.widget_name()` |
| Create columns | `st.columns()` |
| Cache data | `@st.cache_data` |
| Show Plotly charts | `st.plotly_chart()` |
| Configure page | `st.set_page_config()` |

Streamlit transforms your Python analysis into interactive applications that anyone can use. You don't need to learn web development — just write Python, and Streamlit handles the rest.

---

## Exercises

````{exercise}
:label: ex12-basic

**Exercise 1: Hello Dashboard**

Create a simple Streamlit app that:
1. Displays your name as a title
2. Has a text input where users can enter their name
3. Shows a greeting message using the entered name
4. Includes a slider to select an age (1-100)
5. Displays a message based on the age (e.g., "You are young!" for under 30)

Save it as `hello_dashboard.py` and run it.
````

````{solution} ex12-basic
:class: dropdown

```python
import streamlit as st

# Title
st.title("My First Dashboard")

# Text input
name = st.text_input("What's your name?")

if name:
    st.write(f"Hello, {name}! Welcome to my dashboard.")

# Age slider
age = st.slider("How old are you?", min_value=1, max_value=100, value=25)

# Age-based message
if age < 18:
    st.write("You're still young - enjoy your school years!")
elif age < 30:
    st.write("You're in your prime - make the most of it!")
elif age < 50:
    st.write("Experience is your superpower!")
else:
    st.write("Wisdom comes with age - you have plenty!")

# Run with: streamlit run hello_dashboard.py
```
````

````{exercise}
:label: ex12-filters

**Exercise 2: Filtered Data Viewer**

Create a Streamlit app that:
1. Loads the `penguins` dataset from seaborn (`sns.load_dataset('penguins')`)
2. Has sidebar filters for:
   - Species (multiselect)
   - Island (multiselect)
   - Bill length range (slider)
3. Displays the number of penguins matching the filters
4. Shows the filtered data in a table

Use `@st.cache_data` to cache the data loading.
````

````{solution} ex12-filters
:class: dropdown

```python
import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="Penguin Explorer", page_icon="🐧")

# Cache data loading
@st.cache_data
def load_penguins():
    return sns.load_dataset('penguins').dropna()

df = load_penguins()

# Title
st.title("🐧 Penguin Data Explorer")

# Sidebar filters
st.sidebar.header("Filters")

species = st.sidebar.multiselect(
    "Select Species:",
    options=df['species'].unique(),
    default=df['species'].unique()
)

islands = st.sidebar.multiselect(
    "Select Island:",
    options=df['island'].unique(),
    default=df['island'].unique()
)

bill_range = st.sidebar.slider(
    "Bill Length (mm):",
    min_value=float(df['bill_length_mm'].min()),
    max_value=float(df['bill_length_mm'].max()),
    value=(float(df['bill_length_mm'].min()), float(df['bill_length_mm'].max()))
)

# Apply filters
filtered = df[
    (df['species'].isin(species)) &
    (df['island'].isin(islands)) &
    (df['bill_length_mm'] >= bill_range[0]) &
    (df['bill_length_mm'] <= bill_range[1])
]

# Display results
st.metric("Penguins Found", len(filtered))

st.subheader("Filtered Data")
st.dataframe(filtered, use_container_width=True, hide_index=True)
```
````

````{exercise}
:label: ex12-charts

**Exercise 3: Interactive Chart Dashboard**

Build a dashboard for the tips dataset that includes:
1. Sidebar filters for day and smoker status
2. Three KPI metrics: total tips, average bill, number of records
3. Two charts side-by-side:
   - A bar chart showing average tip by day
   - A scatter plot of total_bill vs tip (colored by time)
4. Use `st.columns()` for the layout
````

````{solution} ex12-charts
:class: dropdown

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Tips Dashboard", page_icon="💰", layout="wide")

@st.cache_data
def load_data():
    return sns.load_dataset('tips')

tips = load_data()

st.title("💰 Tips Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

days = st.sidebar.multiselect(
    "Day:",
    options=tips['day'].unique(),
    default=tips['day'].unique()
)

smoker = st.sidebar.multiselect(
    "Smoker:",
    options=tips['smoker'].unique(),
    default=tips['smoker'].unique()
)

# Filter data
filtered = tips[
    (tips['day'].isin(days)) &
    (tips['smoker'].isin(smoker))
]

# KPI metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tips", f"${filtered['tip'].sum():.2f}")

with col2:
    st.metric("Avg Bill", f"${filtered['total_bill'].mean():.2f}")

with col3:
    st.metric("Records", len(filtered))

st.markdown("---")

# Charts side by side
left, right = st.columns(2)

with left:
    avg_by_day = filtered.groupby('day')['tip'].mean().reset_index()
    fig_bar = px.bar(avg_by_day, x='day', y='tip',
                     title='Average Tip by Day',
                     color='day')
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    fig_scatter = px.scatter(filtered, x='total_bill', y='tip',
                             color='time',
                             title='Bill vs Tip by Time',
                             hover_data=['day', 'size'])
    st.plotly_chart(fig_scatter, use_container_width=True)
```
````

````{exercise}
:label: ex12-complete

**Exercise 4: Build Your Own Dashboard**

Create a complete dashboard for a dataset of your choice. Your dashboard must include:

1. Page configuration (title, icon, layout)
2. Data caching with `@st.cache_data`
3. At least 3 sidebar filters
4. At least 3 KPI metrics
5. At least 2 different chart types
6. Proper handling for empty filter results
7. An optional data table view (using checkbox)

You can use any dataset — the penguins dataset, a CSV file you have, or create sample data. Focus on making it useful and visually appealing.
````

````{solution} ex12-complete
:class: dropdown

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Penguin Research Dashboard",
    page_icon="🐧",
    layout="wide"
)

# Data loading with cache
@st.cache_data
def load_data():
    df = sns.load_dataset('penguins').dropna()
    return df

df = load_data()

# Title and description
st.title("🐧 Palmer Penguins Research Dashboard")
st.markdown("Explore the characteristics of penguins from the Palmer Archipelago")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Filter 1: Species
species = st.sidebar.multiselect(
    "Species:",
    options=df['species'].unique(),
    default=df['species'].unique()
)

# Filter 2: Island
islands = st.sidebar.multiselect(
    "Island:",
    options=df['island'].unique(),
    default=df['island'].unique()
)

# Filter 3: Sex
sex = st.sidebar.multiselect(
    "Sex:",
    options=df['sex'].unique(),
    default=df['sex'].unique()
)

# Filter 4: Body mass range
mass_range = st.sidebar.slider(
    "Body Mass (g):",
    min_value=int(df['body_mass_g'].min()),
    max_value=int(df['body_mass_g'].max()),
    value=(int(df['body_mass_g'].min()), int(df['body_mass_g'].max()))
)

# Apply filters
filtered = df[
    (df['species'].isin(species)) &
    (df['island'].isin(islands)) &
    (df['sex'].isin(sex)) &
    (df['body_mass_g'] >= mass_range[0]) &
    (df['body_mass_g'] <= mass_range[1])
]

# Handle empty results
if filtered.empty:
    st.warning("⚠️ No penguins match your criteria. Please adjust the filters.")
    st.stop()

# KPI Metrics Row
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🐧 Penguins", len(filtered))

with col2:
    avg_mass = filtered['body_mass_g'].mean()
    st.metric("⚖️ Avg Mass", f"{avg_mass:,.0f}g")

with col3:
    avg_bill = filtered['bill_length_mm'].mean()
    st.metric("📏 Avg Bill", f"{avg_bill:.1f}mm")

with col4:
    avg_flipper = filtered['flipper_length_mm'].mean()
    st.metric("🏊 Avg Flipper", f"{avg_flipper:.0f}mm")

st.markdown("---")

# Charts Row
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Species Distribution")
    species_counts = filtered['species'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']
    fig_pie = px.pie(species_counts, values='Count', names='Species',
                     color='Species',
                     color_discrete_map={'Adelie': '#636EFA',
                                        'Chinstrap': '#EF553B',
                                        'Gentoo': '#00CC96'})
    st.plotly_chart(fig_pie, use_container_width=True)

with right_col:
    st.subheader("Bill Length vs Flipper Length")
    fig_scatter = px.scatter(
        filtered,
        x='bill_length_mm',
        y='flipper_length_mm',
        color='species',
        size='body_mass_g',
        hover_data=['island', 'sex'],
        color_discrete_map={'Adelie': '#636EFA',
                           'Chinstrap': '#EF553B',
                           'Gentoo': '#00CC96'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Second row of charts
st.markdown("---")
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Body Mass by Species")
    fig_box = px.box(filtered, x='species', y='body_mass_g',
                     color='species',
                     color_discrete_map={'Adelie': '#636EFA',
                                        'Chinstrap': '#EF553B',
                                        'Gentoo': '#00CC96'})
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

with right_col2:
    st.subheader("Penguins per Island")
    island_counts = filtered.groupby('island').size().reset_index(name='count')
    fig_bar = px.bar(island_counts, x='island', y='count',
                     color='island', text='count')
    fig_bar.update_layout(showlegend=False)
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

# Optional data table
st.markdown("---")
show_data = st.checkbox("📋 Show Raw Data Table")

if show_data:
    st.subheader("Filtered Penguin Data")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("*Data source: Palmer Penguins dataset • Built with Streamlit*")
```
````

---

*Congratulations! You've completed the Python for Data Analytics course. You now have the skills to load, clean, analyse, visualise, and present data — from raw CSV files to interactive dashboards. Keep practising, and remember: the best way to learn is by building projects that interest you.*
