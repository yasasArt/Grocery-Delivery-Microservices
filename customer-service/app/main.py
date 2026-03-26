from fastapi import FastAPI

app = FastAPI(title="Customer Service")

@app.get("/")
def root():
    return {"message": "Customer Service is running"}