from fastapi import FastAPI
from . import data

app = FastAPI()

@app.get('/dataframe')
def get_dataframe():
    return data.hourly_dataframe.to_dict(orient='records')

@app.get('/cities')
def get_cities():
    
    cities = {
        "New York": {"latitude": 40.71, "longitude": -74.01},
        "Los Angeles": {"latitude": 34.05, "longitude": -118.24},
        "Chicago": {"latitude": 41.88, "longitude": -87.63},
        "Houston": {"latitude": 29.76, "longitude": -95.37},
        "Phoenix": {"latitude": 33.45, "longitude": -112.07},
        "Philadelphia": {"latitude": 39.95, "longitude": -75.17},
        "San Antonio": {"latitude": 29.43, "longitude": -98.49},
        "San Diego": {"latitude": 32.72, "longitude": -117.16},
        "Dallas": {"latitude": 32.47, "longitude": -96.48},
        "San Jose": {"latitude": 37.34, "longitude": -121.89},
    }
    
    for response in data.responses:
        yield {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "elevation": response.Elevation(),
            'hourly_temperature_2m': data.hourly_temperature_2m,
            'hourly_relative_humidity_2m': data.hourly_relative_humidity_2m,
            'hourly_precipitation': data.hourly_precipitation,
            'hourly_precipitation_probability': data.hourly_precipitation_probability
        }

        # for this get, instead buuild a while new SQL database for the hourly inputs and have it auto delete old entries everytime a new one is entered?