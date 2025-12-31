from fastapi import FastAPI, UploadFile, File
import pandas as pd
from core.visualizacao import generate_plot
from core.analises import basic_statistics

app = FastAPI(title="Axioma ERP - Analytics")

@app.post("/stats")
async def get_stats(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return basic_statistics(df)
