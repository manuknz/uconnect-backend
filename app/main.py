import uvicorn

from app import app

# Run Server
if __name__ == "main":
    uvicorn.run(app)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
