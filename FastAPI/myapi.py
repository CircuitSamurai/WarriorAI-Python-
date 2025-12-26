from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

# Create the FastAPI application object
# This 'app' is what uvicorn runs.
app = FastAPI()

# In-memory "database" of students
# Key: student_id (int)
# Value: dict with name, age, year
students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "senior"
    }
}

# Pydantic model: defines the shape of a Student object
# This is used for request bodies (and can be used for responses too).
class Student(BaseModel):
    name: str      # required string
    age: int       # required integer
    year: str      # required string

# Pydantic model for partial updates
# All fields are Optional and default to None.
# This allows you to send only the fields you want to update.
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


# Basic root endpoint — just returns some test data.
@app.get("/")
def index():
    return {"name": "First Data"}


# ========= PATH PARAMETER EXAMPLE =========
# /get-student/1  → student_id = 1
@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(
        ...,  # "..." means required
        description="Enter the ID of the student you want to view",
        gt=0,  # greater than 0
        lt=3   # less than 3
    )
):
    # If the ID doesn't exist in the dictionary, raise a 404 error
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    # Return that student's data
    return students[student_id]


# ========= QUERY PARAMETER EXAMPLE =========
# /get-by-name?name=john
@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None):
    # Loop over all students and check their "name" field
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    # If no student matched, we return a simple "not found" message
    return {"data": "Not found"}


# ========= COMBINED PATH + QUERY PARAMETER EXAMPLE =========
# (commented out in your code, but this is another pattern)
"""
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return ["data: Not found"]
"""


# ========= CREATE (POST) =========
# Request Body + Path parameter
# Example: POST /create-student/2  with a JSON body like:
# { "name": "mary", "age": 18, "year": "junior" }
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    # If the student already exists, return an error
    if student_id in students:
        return {"Error": "Student exists"}
    
    # IMPORTANT:
    # student is a Pydantic model; to store it in your dict,
    # convert it to a plain dict first with .dict()
    students[student_id] = student.dict()  # <-- small fix

    return students[student_id]


# ========= UPDATE (PUT) =========
# Partial update using UpdateStudent model
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    # Here, students[student_id] is a dict, not a model,
    # so we should access fields like ["name"], not .name
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.year is not None:
        students[student_id]["year"] = student.year

    return students[student_id]


# ========= DELETE (DELETE) =========
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    # Remove the student from the dictionary
    del students[student_id]
    return {"Message": "Student deleted successfully"}


"""
Notes on Path validation:
- gt: greater than
- lt: less than
- ge: greater than or equal to
- le: less than or equal to
"""