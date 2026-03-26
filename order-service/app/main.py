from fastapi import FastAPI

app = FastAPI(title="Oder Service")

@app.get("/")
def root():
    return {"message": "Order Service is running"}