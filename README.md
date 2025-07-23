# Backend-Development-and-API-Design

This project provides a simple RESTful API for managing video information, built with Flask, Flask-RESTful, and Flask-SQLAlchemy. It allows you to perform standard CRUD (Create, Read, Update, Delete) operations on video entries, each identified by a unique ID and containing a name, view count, and like count.

## Features
 - RESTful Endpoints: Exposes clear API endpoints for video management.
 - Database Integration: Uses SQLAlchemy for easy interaction with an SQLite database.
 - Request Parsing & Validation: Utilizes reqparse to validate incoming request data for POST and PUT requests.
 - Data Serialization: Employs marshal_with to define and format API responses consistently.
 - Basic Authentication: Secures API endpoints using HTTP Basic Authentication.

## Setup and Installation
**Prerequisites**
 - Python 3.x
 - pip (Python package installer)

**Installation Steps**

**1. Clone the Repository (or save the code):**

If this code is part of a larger repository, clone it. Otherwise, save the provided code as a Python file (e.g., app.py).

**2. Create a Virtual Environment (Recommended):**

```Bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies:**

```Bash
pip install Flask Flask-RESTful Flask-SQLAlchemy Flask-HTTPAuth
```

**4. Set Environment Variables:**

The application uses environment variables for basic authentication credentials. Set USER and PASSWORD before running the app.

On Linux/macOS:

```Bash
export USER="your_username"
export PASSWORD="your_password"
```

On Windows (Command Prompt):

```DOS
set USER="your_username"
set PASSWORD="your_password"
On Windows (PowerShell):
```

On Windows (PowerShell)

```PowerShell
$env:USER="your_username"
$env:PASSWORD="your_password"
```

Replace "your_username" and "your_password" with your desired credentials.

**5. Run the Application:**

```Bash
python app.py
```

The API will be accessible at http://127.0.0.1:5000/.

## API Endpoints

All endpoints require HTTP Basic Authentication. Use the USER and PASSWORD environment variables you set up.

**1. Get a Video**
 - URL: /video/<int:video_id>
 - Method: GET
 - Description: Retrieves details of a specific video by its ID.
 - Example Request:
   ``` Bash
   curl -u your_username:your_password http://127.0.0.1:5000/video/1
   ```
 - Success Response:
```JSON
{
"id": 1,
"name": "My Awesome Video",
"views": 1000,
"likes": 50
}
```

 - Error Response:
   - 404 Not Found: If video_id does not exist.
   - 401 Unauthorized: If authentication fails.

**2. Create a Video**
 - URL: /video/<int:video_id>
 - Method: POST
 - Description: Creates a new video entry.
 - Request Body (JSON):
```JSON
{
"name": "New Video Title",
"views": 2500,
"likes": 120
}
```
 - Example Request:
```Bash
curl -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{"name": "New Video Title", "views": 2500, "likes": 120}' http://127.0.0.1:5000/video/2
```

 - Success Response:
   - 201 Created
   - JSON
    {
        "id": 2,
        "name": "New Video Title",
        "views": 2500,
        "likes": 120
    }

- Error Response:
   - 409 Conflict: If video_id already exists.
   - 400 Bad Request: If required arguments (name, views, likes) are missing or have invalid types.
   - 401 Unauthorized: If authentication fails.

**3. Update a Video**
 - URL: /video/<int:video_id>
 - Method: PUT
 - Description: Updates an existing video entry. Supports partial updates.
 - Request Body (JSON):
     ```JSON
    {
        "name": "Updated Video Name",
        "views": 3000
    }
     ```
 - Example Request:
   ``` Bash
   curl -u your_username:your_password -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Video Name", "views": 3000}' http://127.0.0.1:5000/video/1
   ```
   
 - Success Response:
    - 200 OK

   ```JSON
   {
   "id": 1,
   "name": "Updated Video Name",
   "views": 3000,
   "likes": 50
   }
   ```

 - Error Response:
    - 404 Not Found: If video_id does not exist.
    - 400 Bad Request: If provided arguments have invalid types.
    - 401 Unauthorized: If authentication fails.

**4. Delete a Video**
 - URL: /video/<int:video_id>
 - Method: DELETE
 - Description: Deletes a video entry by its ID.
 - Example Request:
   ```Bash
   curl -u your_username:your_password -X DELETE http://127.0.0.1:5000/video/1
   ```

 - Success Response:
    - 201 Created (empty response body, typically 204 No Content is used for successful deletions, but this API returns 201).

 - Error Response:
    - 404 Not Found: If video_id does not exist.
    - 401 Unauthorized: If authentication fails.

## Database

The application uses an SQLite database named database.db, which will be created in the same directory as app.py when the application is run for the first time. The VideoModel defines the schema for the video_model table.
