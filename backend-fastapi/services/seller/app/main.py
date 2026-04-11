from fastapi import FastAPI
app = FastAPI()

@app.get("/insights")
def insights():
    return {"top_category": "mobiles", "demand": 100}
