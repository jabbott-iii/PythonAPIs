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
            'hourly_temperature_2m': data.response.current_weather().Temperature2m(),
            'hourly_relative_humidity_2m': data.response.current_weather().RelativeHumidity2m(),
            'hourly_precipitation': data.response.current_weather().Precipitation(),
            'hourly_precipitation_probability': data.response.current_weather().PrecipitationProbability()
        }

      # figure out how to apply only current weather attribute to each city