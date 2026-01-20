import uvicorn

if __name__ == "__main__":
    uvicorn.run("ministral3_3b_API.app:app", host="0.0.0.0", port=8000, reload=True)