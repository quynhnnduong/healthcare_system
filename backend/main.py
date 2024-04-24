from fastapi import FastAPI
import uvicorn

# from endpoints import insert_data, user, login
# from endpoints import patients
from endpoints import insert_data, user, login, patients

app = FastAPI()
app.include_router(insert_data.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(patients.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
