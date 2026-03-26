from fastapi import FastAPI

app = FastAPI(title="Delivery Service")

@app.get("/")
def root():
    return {"message": "Delivery Service is running"}