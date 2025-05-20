import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

VALID_USERNAME = "vebbox"
VALID_PASSWORD = "12345"

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital",
        port="3306"
    )

class Item (BaseModel) :
    name:str
    age:str
    phoneNo:str
    P_Type:str

@app.get("/PatientDetail")
def get_details():
    try:
         mydb = get_db_connection()
         cursor = mydb.cursor(dictionary=True)  # Get results as dictionary

         cursor.execute("SELECT * FROM patient")
         students = cursor.fetchall()

         cursor.close()
         mydb.close()

         return students

    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/insertDetail")
def post_details(obj : Item):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()

        query="""Insert into patient (name,age,phoneNo,P_Type) values (%s,%s,%s,%s)"""
        values=(obj.name,obj.age,obj.phoneNo,obj.P_Type)

        cursor.execute(query, values)
        mydb.commit()

        cursor.close()
        mydb.close()

        return {"message": "Patient added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class DeleteRequest(BaseModel):
    id : int
@app.post("/deleteRequest")
def post_delete(d : DeleteRequest ):


    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()

        cursor.execute("DELETE FROM patient WHERE S_NO = %s", (d.id,))
        mydb.commit()

        cursor.close()
        mydb.close()

        return {"message": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class UpdateRequest(BaseModel):
    id : int
    name: str
    age: int
    phoneNo: str
    P_Type: str
@app.post("/Update")
def post_delete(u : UpdateRequest ):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()

        query = """
            UPDATE patient
            SET name = %s, age = %s, phoneNo = %s, P_Type = %s
            WHERE S_NO = %s
        """
        values = (u.name, u.age, u.phoneNo, u.P_Type, u.id)

        cursor.execute(query, values)
        mydb.commit()

        cursor.close()
        mydb.close()

        return {"message": "Patient updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")





