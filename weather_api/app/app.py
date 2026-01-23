from fastapi import FastAPI
from . import data

app = FastAPI()

@app.get('/dataframe')
def get_dataframe():
    return data.hourly_dataframe.to_dict(orient='records')

@app.get('/cities')
def get_cities():
    for response in data.responses:
        yield {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "elevation": response.Elevation(),
            'hourly_temperature_2m': data.hourly_dataframe['temperature_2m'].tolist(),
            'hourly_relative_humidity_2m': data.hourly_dataframe['relative_humidity_2m'].tolist(),
            'hourly_precipitation': data.hourly_dataframe['precipitation'].tolist(),
            'hourly_precipitation_probability': data.hourly_dataframe['precipitation_probability'].tolist()
        }