# Database Management with Python: A Comprehensive Guide

## Table of Contents
1. [Introduction to Databases](#introduction-to-databases)
2. [SQL Basics](#sql-basics)
3. [SQLite](#sqlite)
4. [MySQL/MariaDB](#mysqlmariadb)
5. [PostgreSQL](#postgresql)
6. [MongoDB (NoSQL)](#mongodb-nosql)
7. [SQLAlchemy ORM](#sqlalchemy-orm)
8. [Connection Pooling](#connection-pooling)
9. [Transactions](#transactions)
10. [Data Validation](#data-validation)
11. [Best Practices](#best-practices)

---

## Introduction to Databases

### What is a Database?

A database is an organized collection of structured data stored electronically in a computer system. It allows efficient storage, retrieval, and manipulation of data.

### Types of Databases

#### 1. **Relational Databases (SQL)**
- Organize data in tables (rows and columns)
- Use SQL (Structured Query Language) for queries
- Examples: SQLite, MySQL, PostgreSQL, SQL Server
- Best for: Structured data with defined relationships

#### 2. **NoSQL Databases**
- Store data in flexible formats (documents, key-value, etc.)
- No fixed schema required
- Examples: MongoDB, Cassandra, Redis, DynamoDB
- Best for: Unstructured or semi-structured data

### Database Operations (CRUD)
- **Create** - INSERT new data
- **Read** - SELECT and retrieve data
- **Update** - UPDATE existing data
- **Delete** - DELETE data

---

## SQL Basics

### DDL (Data Definition Language)

#### CREATE TABLE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### ALTER TABLE

```sql
-- Add column
ALTER TABLE users ADD COLUMN phone TEXT;

-- Rename table
ALTER TABLE users RENAME TO customers;

-- Drop column (not supported in SQLite)
ALTER TABLE users DROP COLUMN phone;
```

#### DROP TABLE

```sql
DROP TABLE posts;
DROP TABLE IF EXISTS posts;  -- Safe drop
```

### DML (Data Manipulation Language)

#### INSERT

```sql
INSERT INTO users (name, email, age)
VALUES ('Alice', 'alice@example.com', 25);

INSERT INTO users (name, email, age)
VALUES 
    ('Bob', 'bob@example.com', 30),
    ('Charlie', 'charlie@example.com', 28);
```

#### SELECT

```sql
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- With WHERE clause
SELECT * FROM users WHERE age > 25;

-- With ORDER BY
SELECT * FROM users ORDER BY age DESC;

-- With LIMIT
SELECT * FROM users LIMIT 10;

-- With OFFSET
SELECT * FROM users LIMIT 10 OFFSET 20;

-- Aggregation functions
SELECT COUNT(*) FROM users;
SELECT AVG(age) FROM users;
SELECT MAX(age), MIN(age) FROM users;

-- GROUP BY
SELECT age, COUNT(*) as count FROM users GROUP BY age;

-- HAVING (filtering groups)
SELECT age, COUNT(*) as count FROM users 
GROUP BY age HAVING COUNT(*) > 2;

-- JOIN operations
SELECT users.name, posts.title 
FROM users 
INNER JOIN posts ON users.id = posts.user_id;
```

#### UPDATE

```sql
UPDATE users SET age = 26 WHERE name = 'Alice';

UPDATE users 
SET age = age + 1, modified_at = CURRENT_TIMESTAMP 
WHERE age > 30;
```

#### DELETE

```sql
DELETE FROM users WHERE id = 1;

DELETE FROM users WHERE age < 18;
```

### Constraints

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,              -- NOT NULL
    email TEXT UNIQUE,               -- UNIQUE
    price DECIMAL(10, 2) CHECK (price > 0),  -- CHECK
    category TEXT DEFAULT 'General', -- DEFAULT
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(name, category)           -- Composite unique
);
```

---

## SQLite

SQLite is a lightweight, serverless SQL database that's perfect for beginners and small projects. It's built into Python!

### Installation

```bash
# SQLite is built into Python, no installation needed
# For Python SQLite wrapper:
pip install sqlite3  # Already included in Python
```

### Basic Operations

#### Connect to Database

```python
import sqlite3

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect('database.db')

# In-memory database
conn = sqlite3.connect(':memory:')

# Get cursor
cursor = conn.cursor()
```

#### Create Table

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
cursor.close()
conn.close()
```

#### Insert Data

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert single row
cursor.execute('''
    INSERT INTO users (name, email, age)
    VALUES (?, ?, ?)
''', ('Alice', 'alice@example.com', 25))

# Insert multiple rows
data = [
    ('Bob', 'bob@example.com', 30),
    ('Charlie', 'charlie@example.com', 28),
    ('Diana', 'diana@example.com', 26)
]
cursor.executemany('''
    INSERT INTO users (name, email, age)
    VALUES (?, ?, ?)
''', data)

conn.commit()
print(f"Inserted {cursor.rowcount} rows")
cursor.close()
conn.close()
```

#### Fetch Data

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all rows
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fetch one row
cursor.execute('SELECT * FROM users WHERE id = ?', (1,))
row = cursor.fetchone()
print(row)

# Fetch multiple rows
cursor.execute('SELECT * FROM users')
rows = cursor.fetchmany(5)  # Fetch first 5

# Get column names
cursor.execute('SELECT * FROM users LIMIT 0')
column_names = [description[0] for description in cursor.description]
print(column_names)

cursor.close()
conn.close()
```

#### Update Data

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    UPDATE users 
    SET age = ? 
    WHERE name = ?
''', (26, 'Alice'))

conn.commit()
print(f"Updated {cursor.rowcount} rows")

cursor.close()
conn.close()
```

#### Delete Data

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM users WHERE id = ?', (1,))

conn.commit()
print(f"Deleted {cursor.rowcount} rows")

cursor.close()
conn.close()
```

#### Row Factory (Dictionary Results)

```python
import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row  # Returns rows as dictionaries

cursor = conn.cursor()
cursor.execute('SELECT * FROM users')

for row in cursor.fetchall():
    print(f"Name: {row['name']}, Email: {row['email']}")

cursor.close()
conn.close()
```

### Context Manager Pattern

```python
import sqlite3

# Automatic connection handling
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Automatically commits and closes
```

---

## MySQL/MariaDB

### Installation

```bash
# Install MySQL connector
pip install mysql-connector-python

# Or using PyMySQL
pip install PyMySQL
```

### Connection

```python
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()
```

### CRUD Operations

#### Create Table

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
cursor.close()
conn.close()
```

#### Insert Data

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# Insert single record
sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
values = ("Alice", "alice@example.com", 25)
cursor.execute(sql, values)

conn.commit()
print(f"Last inserted ID: {cursor.lastrowid}")

cursor.close()
conn.close()
```

#### Fetch Data

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# Fetch all
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
for row in results:
    print(row)

# Fetch with dictionary cursor
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
for row in results:
    print(row['name'], row['email'])

cursor.close()
conn.close()
```

#### Update Data

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

sql = "UPDATE users SET age = %s WHERE name = %s"
values = (26, "Alice")
cursor.execute(sql, values)

conn.commit()
print(f"Rows updated: {cursor.rowcount}")

cursor.close()
conn.close()
```

#### Delete Data

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

sql = "DELETE FROM users WHERE id = %s"
value = (1,)
cursor.execute(sql, value)

conn.commit()
print(f"Rows deleted: {cursor.rowcount}")

cursor.close()
conn.close()
```

---

## PostgreSQL

### Installation

```bash
# Install psycopg2 (PostgreSQL adapter)
pip install psycopg2-binary

# Or psycopg3
pip install psycopg[binary]
```

### Connection

```python
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()
```

### CRUD Operations

#### Create Table

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
cursor.close()
conn.close()
```

#### Insert Data

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# Using %s placeholder
sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
values = ("Alice", "alice@example.com", 25)
cursor.execute(sql, values)

conn.commit()
print(f"Row inserted successfully")

cursor.close()
conn.close()
```

#### Fetch Data

```python
import psycopg2
import json

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# Fetch with RealDictCursor (returns dictionaries)
from psycopg2.extras import RealDictCursor
cursor = conn.cursor(cursor_factory=RealDictCursor)

cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
for row in results:
    print(json.dumps(row))

cursor.close()
conn.close()
```

#### Update Data

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

sql = "UPDATE users SET age = %s WHERE name = %s"
values = (26, "Alice")
cursor.execute(sql, values)

conn.commit()
print(f"Rows updated: {cursor.rowcount}")

cursor.close()
conn.close()
```

#### Delete Data

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

sql = "DELETE FROM users WHERE id = %s"
cursor.execute(sql, (1,))

conn.commit()
print(f"Rows deleted: {cursor.rowcount}")

cursor.close()
conn.close()
```

---

## MongoDB (NoSQL)

### Installation

```bash
# Install PyMongo
pip install pymongo
```

### Connection

```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']
```

### CRUD Operations

#### Create (Insert)

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# Insert one document
user = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
}
result = users.insert_one(user)
print(f"Inserted ID: {result.inserted_id}")

# Insert multiple documents
users_list = [
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 28}
]
result = users.insert_many(users_list)
print(f"Inserted IDs: {result.inserted_ids}")

client.close()
```

#### Read (Query)

```python
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# Find one document
user = users.find_one({"name": "Alice"})
print(user)

# Find by ID
user = users.find_one({"_id": ObjectId("...")})

# Find all documents
all_users = users.find()
for user in all_users:
    print(user)

# Find with filter
adults = users.find({"age": {"$gte": 18}})
for user in adults:
    print(user)

# Find with projection (select fields)
users_names = users.find({}, {"name": 1, "email": 1, "_id": 0})
for user in users_names:
    print(user)

# Count documents
count = users.count_documents({"age": {"$gte": 25}})
print(f"Adults: {count}")

# Sort
users_sorted = users.find().sort("age", -1)  # -1 for descending

# Limit and skip
page_size = 10
page = 1
skip = (page - 1) * page_size
users_page = users.find().skip(skip).limit(page_size)

client.close()
```

#### Update

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# Update one document
result = users.update_one(
    {"name": "Alice"},
    {"$set": {"age": 26}}
)
print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# Update multiple documents
result = users.update_many(
    {"age": {"$lt": 25}},
    {"$set": {"status": "young"}}
)

# Replace document
users.replace_one(
    {"name": "Bob"},
    {"name": "Bob", "email": "newbob@example.com", "age": 31}
)

client.close()
```

#### Delete

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# Delete one document
result = users.delete_one({"name": "Alice"})
print(f"Deleted: {result.deleted_count}")

# Delete multiple documents
result = users.delete_many({"age": {"$lt": 18}})

# Delete all
users.delete_many({})

client.close()
```

### Aggregation Pipeline

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# Aggregation pipeline
pipeline = [
    {"$match": {"age": {"$gte": 25}}},  # Filter
    {"$group": {"_id": None, "avg_age": {"$avg": "$age"}}},  # Aggregate
    {"$sort": {"avg_age": -1}}  # Sort
]

result = users.aggregate(pipeline)
for doc in result:
    print(doc)

client.close()
```

---

## SQLAlchemy ORM

SQLAlchemy is a powerful ORM (Object-Relational Mapping) library that abstracts database operations.

### Installation

```bash
pip install sqlalchemy
```

### Basic Setup

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create engine
engine = create_engine('sqlite:///database.db', echo=True)

# Base class for models
Base = declarative_base()

# Define model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, age={self.age})>"

# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()
```

### Create (Insert)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create single user
user = User(name="Alice", email="alice@example.com", age=25)
session.add(user)
session.commit()

# Create multiple users
users = [
    User(name="Bob", email="bob@example.com", age=30),
    User(name="Charlie", email="charlie@example.com", age=28)
]
session.add_all(users)
session.commit()

session.close()
```

### Read (Query)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Query all
all_users = session.query(User).all()

# Query with filter
user = session.query(User).filter(User.name == "Alice").first()

# Query with multiple conditions
young_adults = session.query(User).filter(
    User.age >= 18,
    User.age <= 30
).all()

# Query with OR
from sqlalchemy import or_
users = session.query(User).filter(
    or_(User.age < 20, User.age > 60)
).all()

# Order by
sorted_users = session.query(User).order_by(User.age.desc()).all()

# Limit
limited = session.query(User).limit(5).all()

# Count
user_count = session.query(User).count()

# Distinct
distinct_ages = session.query(User.age).distinct().all()

session.close()
```

### Update

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Update single record
user = session.query(User).filter(User.name == "Alice").first()
if user:
    user.age = 26
    session.commit()

# Update multiple records
session.query(User).filter(User.age < 25).update({"age": 25})
session.commit()

session.close()
```

### Delete

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Delete single record
user = session.query(User).filter(User.name == "Alice").first()
if user:
    session.delete(user)
    session.commit()

# Delete multiple records
session.query(User).filter(User.age < 18).delete()
session.commit()

session.close()
```

### Relationships

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///database.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    
    # One-to-many relationship
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    # Back reference
    author = relationship("User", back_populates="posts")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create user with posts
user = User(name="Alice", email="alice@example.com")
post1 = Post(title="First Post", content="Content here", author=user)
post2 = Post(title="Second Post", content="More content", author=user)

session.add(user)
session.commit()

# Query with relationship
user = session.query(User).filter(User.name == "Alice").first()
print(user.posts)  # Access related posts

session.close()
```

---

## Connection Pooling

Connection pooling manages database connections efficiently.

### SQLAlchemy Connection Pooling

```python
from sqlalchemy import create_engine

# Default pool (QueuePool)
engine = create_engine(
    'postgresql://user:password@localhost/dbname',
    poolclass=QueuePool,
    pool_size=10,           # Number of connections to keep
    max_overflow=20,        # Additional connections allowed
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True      # Test connections before using
)

# NullPool - no pooling (create new connection each time)
from sqlalchemy.pool import NullPool
engine = create_engine(
    'sqlite:///database.db',
    poolclass=NullPool
)

# SingletonPool - single connection
from sqlalchemy.pool import SingletonPool
engine = create_engine(
    'sqlite:///database.db',
    poolclass=SingletonPool
)
```

### MySQL Connection Pooling

```python
from mysql.connector import pooling

# Create connection pool
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "mydb"
}

pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,
    pool_reset_session=True,
    **dbconfig
)

# Get connection from pool
conn = pool.get_connection()
cursor = conn.cursor()

# Use connection
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

# Return connection to pool
cursor.close()
conn.close()
```

---

## Transactions

Transactions ensure data consistency and integrity.

### SQLite Transactions

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # Start transaction (implicit in SQLite)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
    cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (1, 1, "Post Title"))
    
    # Commit if successful
    conn.commit()
    print("Transaction committed")
    
except Exception as e:
    # Rollback on error
    conn.rollback()
    print(f"Transaction rolled back: {e}")

finally:
    cursor.close()
    conn.close()
```

### MySQL Transactions

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

try:
    # Disable autocommit
    conn.autocommit = False
    
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", 
                   ("Bob", "bob@example.com"))
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", 
                   (cursor.lastrowid, 1000))
    
    # Commit transaction
    conn.commit()
    print("Transaction committed")
    
except Exception as e:
    # Rollback on error
    conn.rollback()
    print(f"Transaction rolled back: {e}")

finally:
    cursor.close()
    conn.close()
```

### PostgreSQL Transactions

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", 
                   ("Charlie", "charlie@example.com"))
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", 
                   (1, 5000))
    
    conn.commit()
    print("Transaction committed")
    
except Exception as e:
    conn.rollback()
    print(f"Transaction rolled back: {e}")

finally:
    cursor.close()
    conn.close()
```

### Savepoints

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
    
    # Create savepoint
    cursor.execute("SAVEPOINT sp1")
    
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Duplicate", "dup@example.com"))
    except Exception:
        # Rollback to savepoint
        cursor.execute("ROLLBACK TO SAVEPOINT sp1")
    
    conn.commit()
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()
```

---

## Data Validation

### Input Validation

```python
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_age(age):
    """Validate age range"""
    try:
        age = int(age)
        return 0 < age < 150
    except ValueError:
        return False

def validate_phone(phone):
    """Validate phone number"""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

# Using validation
user_data = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "phone": "+1234567890"
}

if not validate_email(user_data["email"]):
    print("Invalid email")
if not validate_age(user_data["age"]):
    print("Invalid age")
if not validate_phone(user_data["phone"]):
    print("Invalid phone")
```

### SQLAlchemy Validation

```python
from sqlalchemy import Column, Integer, String, CheckConstraint, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 150'))
    
    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError("Invalid email")
        return value
    
    @validates('age')
    def validate_age(self, key, value):
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        return value
```

---

## Best Practices

### 1. Use Connection Context Managers

```python
import sqlite3

# Good
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # Auto-closes and commits

# Avoid
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Might forget to close
```

### 2. Use Parameterized Queries (Prevent SQL Injection)

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Good - prevents SQL injection
user_input = "Alice'; DROP TABLE users; --"
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# Avoid - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE name = '{user_input}'"
cursor.execute(query)

conn.close()
```

### 3. Use Connection Pooling

```python
from sqlalchemy import create_engine

# Good - reuses connections
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=10,
    max_overflow=20
)

# Avoid - creates new connection each time
engine = create_engine('postgresql://user:pass@localhost/db')
```

### 4. Handle Exceptions Properly

```python
import sqlite3

try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
    conn.commit()
except sqlite3.IntegrityError:
    print("Duplicate entry")
    conn.rollback()
except sqlite3.OperationalError as e:
    print(f"Database error: {e}")
    conn.rollback()
except Exception as e:
    print(f"Unexpected error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
```

### 5. Use Transactions for Related Operations

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # All-or-nothing operation
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
    cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)", (1, 1000))
    conn.commit()
except Exception:
    conn.rollback()
finally:
    cursor.close()
    conn.close()
```

### 6. Validate Input Data

```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value.strip()
```

### 7. Use Prepared Statements

```python
import mysql.connector

conn = mysql.connector.connect(...)
cursor = conn.cursor(prepared=True)

# Prepared statement
query = "SELECT * FROM users WHERE age > %s AND city = %s"
cursor.execute(query, (25, "New York"))

results = cursor.fetchall()
```

### 8. Index Important Columns

```python
from sqlalchemy import Column, String, Integer, Index

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, index=True)
    name = Column(String(100), index=True)
    age = Column(Integer)
    
    __table_args__ = (
        Index('idx_age_name', 'age', 'name'),
    )
```

### 9. Log Database Operations

```python
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')

# Enable SQL query logging
engine = create_engine(
    'sqlite:///database.db',
    echo=True  # Logs all SQL queries
)
```

### 10. Use ORM for Complex Operations

```python
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

# Use ORM instead of raw SQL for maintainability
Session = sessionmaker(bind=engine)
session = Session()

# Clear ORM approach
user = User(name="Alice", email="alice@example.com", age=25)
session.add(user)
session.commit()

# Query with ORM
adult_users = session.query(User).filter(User.age >= 18).all()

session.close()
```

---

## Comparison: Which Database to Use?

| Database | Use Case | Pros | Cons |
|----------|----------|------|------|
| **SQLite** | Small projects, testing | Easy setup, no server | Limited concurrency |
| **MySQL** | Web applications, general use | Fast, reliable, popular | Limited scaling |
| **PostgreSQL** | Enterprise, complex queries | Advanced features, ACID | Heavier setup |
| **MongoDB** | Document storage, flexible schema | Flexible, scalable | Higher memory usage |

---

## Conclusion

Database management is a critical skill for developers. Understanding how to:
- Connect to databases
- Perform CRUD operations
- Use transactions for data consistency
- Handle errors gracefully
- Use ORMs for clean code

These skills will help you build robust, scalable applications. Choose the appropriate database for your use case and follow best practices to ensure data integrity and performance.

### Quick Reference

- **SQLite**: Best for learning and small projects
- **MySQL**: Popular for web applications
- **PostgreSQL**: For advanced features and reliability
- **MongoDB**: For flexible, document-based data
- **SQLAlchemy**: Recommended ORM for Python

---

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Python Database API Specification](https://www.python.org/dev/peps/pep-0249/)
