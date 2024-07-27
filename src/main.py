import os
import uvicorn
import src.database
import src.models


from fastapi import FastAPI


from src.users.router import user
from src.courses.router import course
from src.events.router import event


app = FastAPI()

app.title = "learning System API"

app.include_router(user)
app.include_router(course)
app.include_router(event)

if __name__ == "__main__":

    port = os.getenv("PORT")

    if not port:
        print("[INFO] Environment variable not found: Port")

        port = 8080

    uvicorn.run(app, host="0.0.0.0", port=int(port))
