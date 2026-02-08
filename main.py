from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from backend import analyze_loan, generate_explanation


app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    income: int
    loan: int
    tenure: int
    cibil: int


@app.post("/chat")
def chat(data: LoanRequest):

    result = analyze_loan(
        data.income,
        data.loan,
        data.tenure,
        data.cibil
    )

    explanation = generate_explanation({
        "income": data.income,
        "loan": data.loan,
        "cibil": data.cibil,
        **result
    })

    return {
        **result,
        "reply": explanation
    }

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

