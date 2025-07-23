# School Management System Backend

This project is a backend application built with FastAPI and MySQL.

## Project Structure

```
root
├── app
│   ├── main.py              # Entry point of the application
│   ├── models
│   │   └── user_model.py          # User model definition
│   ├── schemas
│   │   └── user_schema.py          # Pydantic schemas for user data validation
│   ├── services
│   │   └── user_service.py          # CRUD operations for users
│   ├── database.py          # Database connection setup
│   └── routers
│       └── user_route.py          # API routes for user operations
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
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_NAME=your_dbname
    ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage Examples
Access Swagger dashboard for testing APIS.

http://127.0.0.1:8000/docs

- **Create a User:**
  ```
  POST /users
  {
      "username": "example_user",
      "email": "user@example.com",
      "full_name": "Example User",
      "password": "securepassword"
  }
  ```

- **Get a User:**
  ```
  GET /users/{user_id}
  ```

- **Update a User:**
  ```
  PUT /users/{user_id}
  {
      "username": "updated_user",
      "email": "updated@example.com",
      "full_name": "Updated User"
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
