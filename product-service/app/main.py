from fastapi import FastAPI

app = FastAPI(title="Product Service")

@app.get("/")
def root():
    return {"message": "Product Service is running"}