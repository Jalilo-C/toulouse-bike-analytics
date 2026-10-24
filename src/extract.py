import requests
import logging
import time
from datetime import datetime
logging.basicConfig(level=logging.INFO)

def extract(api_url, max_retries=3):
    logging.info("Extraction started :")
    for attempt in range(1, max_retries+1):
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, dict):
                raise ValueError(
                    "Data Error : data must be a dict"
                )

            if not isinstance(data["data"], dict):
                raise ValueError(
                    "Data Error : data[\"data\"] must be a dict"
                )
            
            stations = data["data"]["stations"]
            if not isinstance(stations, list):
                raise ValueError(
                    "Data Error : stations must be a list"
                )
            
            for station in stations:
                if not isinstance(station, dict):
                    raise ValueError(
                        "Data Error : each station must be a dict"
                    )
                  
            last_updated = data["last_updated"]
            if not isinstance(last_updated, str) or not last_updated.strip():
                raise ValueError(
                    "Data Error : last_updated must be a non-empty string"
                )

            try:
                parsed_date = datetime.fromisoformat(
                    last_updated.replace("Z", "+00:00")
                )
            except ValueError:
                raise ValueError(
                    f"Invalid ISO 8601 timestamp: {last_updated}"
                )

            if parsed_date.tzinfo is None:
                raise ValueError(
                    "Invalid timestamp: timezone information is missing"
                )

            break

        except requests.RequestException as e:
            logging.error(f"Error of extraction for attempt {attempt}: {e}")
            if attempt==max_retries:
                logging.error("All the attempts failed")
                raise
            else:
                time.sleep(2)

    logging.info("Extraction successful: %s stations", len(stations))
    return last_updated, stations