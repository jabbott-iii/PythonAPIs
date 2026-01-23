from fastapi import FastAPI
from . import data

app = FastAPI()

@app.get('/dataframe')
def get_dataframe():
    return data.hourly_dataframe.to_dict(orient='records')