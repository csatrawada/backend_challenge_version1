# Cube Python Code Challenge

In this repository, there's a directory called `project`. It contains a standalone Django application. The
application has one app called `dimensions`. In addition, there's a SQLite database with tables and rows
already prepopulated.

## Get Started

1. Clone this repository `git clone https://github.com/cube-planning/backend-challenge.git`
2. `cd backend-challenge/`
3. Start a virtual environment (if desired)
4. `cd project/`
5. Install requirements `pip install -r requirements.txt`
6. Try `python manage.py check_answers` to see there are failing tests!

Read on to find out how to make the tests pass...

## Models

You are given the models `Company` and `Dimension` in `dimensions/models.py`.  A `Company` has a hierarchy of
`Dimension` objects as defined by this schema.

A `parent` value of `None` means that `Dimension` instance is a top-level `Dimension` with no
parents of its own. The hierarchy can be nested up to 10 levels deep.

## Challenges

You'll find the challenge assignments in `dimensions/challenge.py`

### Assignment 1: `list_children(dimension_id)`

Given a dimension ID, write a function that iterates through all its children and returns a list of strings
representing the nested hierarchy of its children.

#### Example:

```python
>>> from dimensions.challenge import list_children
>>> balance_sheet_id = 8
>>> [print(row) for row in list_children(balance_sheet_id)]
Balance Sheet
	Assets
	Equity
	Liabilities

>>> list_children(balance_sheet_id)
[
    'Balance Sheet',
    '\tAssets',
    '\tEquity',
    '\tLiabilities',
]
```

### Assignment 2: `list_hierarchy(company_id)`

Given a company ID, write a function that iterates through all of that company's dimensions and returns a list
of strings representing the nested hierarchy.

Bonus points: Also include a version of this that only makes one query against the database. For this bonus solution do not use a `RECURSIVE` SQL query.

#### Example:

```python
>>> from dimensions.challenge import list_hierarchy
>>> company_id = 1
>>> [print(row) for row in list_hierarchy(company_id)]
Account
	Balance Sheet
		Assets
		Equity
		Liabilities
	Income Statement
		Expense
		Net Income
		Revenue
			Product Revenue
			Services Revenue
Department
	All Departments
		General & Administrative
			Finance & Accounting
			Human Resources
			Operations
		Marketing
		Product
			Design
			Engineering
Scenario
	Actuals
	Budget

>>> list_hierarchy(company_id)
[
    'Account',
    '\tBalance Sheet',
    '\t\tAssets',
    '\t\tEquity',
    '\t\tLiabilities',
    '\tIncome Statement',
    '\t\tExpense',
    '\t\tNet Income',
    '\t\tRevenue',
    '\t\t\tProduct Revenue',
    '\t\t\tServices Revenue',
    'Department',
    '\tAll Departments',
    '\t\tGeneral & Administrative',
    '\t\t\tFinance & Accounting',
    '\t\t\tHuman Resources',
    '\t\t\tOperations',
    '\t\tMarketing',
    '\t\tProduct',
    '\t\t\tDesign',
    '\t\t\tEngineering',
    'Scenario',
    '\tActuals',
    '\tBudget'
]	
```

### Check Your Answers

You can check your answers using `python manage.py check_answers`

### Hint

`db.sqlite3` has data in it! You can use the Django shell to explore the models and run your code.

## Submit Your Answers

When you're done, push your code to a private GitHub repository under your username
(e.g. github.com/your-username/backend-challenge). Give access permission the repo to @joshholat, @jeremylancaster, @lschachter, @acdameli, and @bennett39.

### Extra Questions

When you push up your copy of the repo, answer these questions in your copy of README.md

1. Explain what SQL queries your solution is making and why.
    For questions there were 2 options I considered. 
	Version -1 : 
		Assignment 1. list_children()_
		Query 1 - Get dimension name for the given id
			dimension_name = list(Dimension.objects.filter(id=dimension_id).values('name'))
		list_hierarchy
		Assignment 2 - Query to get the list of child dimensions for a given parent
			childDimensionNames = Dimension.objects.filter(parent__name=name).values('name'):
			
			This gives the list of children for the given parent.
			This query is the called recursively (dfs). Basically, after adding the parent’s name to the result, the same query is called for each of the children recursively.
			The recursion ends for the dimension if the dimension has no children which is the base case.
	
	Version -2 :
		In this version took an approach where create in-
		
		Query 1 : Get the company for the dimension id.
		Query 2 : Get all the dimensions for the given dimension id 
				The result is used to create a in-memory tree that will used to finally create the result.
			
			
2. Assume there are hundreds of dimensions, and the hierarchy is loaded on every page load. What caching strategies
would you suggest?
    - Hint: The answer here is not a SQL query using `RECURSIVE`.
	Enabling Server side caching will be a good choice to improve performance and latecy when the hierarchy is loaded for every user. In this case the data to be loaded is stored on the site's server. 
	Few Types of server caching strategies
		Object caching, store database queries in server side cache for quick retrieval 
		CDN caching, a cluster of servers that are geographically located all around the world. They cache content that’s loaded using the server that’s closest to the end user for much faster loading times are good choices.
	In-Memory based system like Redis to be keep most recently used hierarchies.


Please note that I have provided 2 versions,

Version 1 : The functions directly get the information’s from database.

Version 2: The functions get the information’s from memory which is preloaded when requested for the first time.

Based on the requirement and the size data need to consider a combination of the 2 approaches.
	

	
	
	
	
	
	
	
	
	
	
	
