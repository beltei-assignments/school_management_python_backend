# School Management System Backend

This project is a backend application built with FastAPI and MySQL.

## Project Structure

```
root
├── app
│   ├── main.py              # Entry point of the application
│   ├── db
│   │   └── seeders          # Add seeders for data testing
│   ├── models
│   │   └── user_model.py          # User model definition
│   ├── schemas
│   │   └── user_schema.py          # Pydantic schemas for user data validation
│   ├── services
│   │   └── user_service.py          # CRUD operations for users
│   ├── database.py          # Database connection setup
│   └── routers
│       └── user_route.py          # API routes for user operations
│   └── utils
│       └── paginate.py          # App utilities and helpers function
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Create a virtual environment:**
   ```
   python -m venv venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure the database:**
   Update the database connection properties in `.env` to match your MySQL configuration.

   Copy from `.env.example` to `.env`

   ```
   #  Database Configuration
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_NAME=your_dbname
   DB_CREATE_ALL_TABLE=true
   
   # JWT Configuration
   JWT_SECRET_KEY="your_secret_key"
   JWT_ALGORITHM="HS256"
   JWT_ACCESS_TOKEN_EXPIRE_DAYS=1
    ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```
5. **Run seed data to tables:**
   ```
   python -m app.db.seed
   ```

## Usage Examples
Access Swagger dashboard for testing APIs.

http://127.0.0.1:8000/docs

- **Login:**
  ```
  POST /auth/login
  {
     "email": "admin@example.com",
     "password": "123"
   }
  ```

- **Get all users:**
  ```
  GET /users/?page=1&limit=10
  ```

- **Get user by ID:**
  ```
  GET /users/{user_id}
  ```

- **Create a User:**
  ```
  POST /users
  {
     "email": "string",
     "first_name": "string",
     "last_name": "string",
     "password": "string",
     "phone_number": "string",
     "roles_ids": [
       1
     ]
   }
  ```

- **Update a User:**
  ```
  PUT /users/{user_id}
   {
     "email": "string",
     "first_name": "string",
     "last_name": "string",
     "password": "string",
     "phone_number": "string",
     "disabled": false
   }
  ```

- **Delete a User:**
  ```
  DELETE /users/{user_id}
  ```

## Code Formatting

This project uses [Black](https://black.readthedocs.io/en/stable/) for Python code formatting.

### Usage

1. **Format all Python files in the project**
   ```
   black .
   ```

2. **Format a specific file**
   ```
   black path/to/your_file.py
   ```

Black will use the configuration in `pyproject.toml`.
