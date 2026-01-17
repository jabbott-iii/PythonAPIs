import uvicorn # webserver for FastAPI

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True) # app.app:app referes to app folder, app.py file, and app variable