import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=1234, reload=True)
    print("FastAPI server running on http://localhost:1234")

