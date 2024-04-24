import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from endpoints import insert_data, user, login, patients

app = FastAPI()

frontend_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../front-end/public"))

app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="static")

app.include_router(insert_data.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(patients.router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def test_html():
    return FileResponse(os.path.join(frontend_dist_path, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
