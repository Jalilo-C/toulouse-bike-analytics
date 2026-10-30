from datetime import datetime, timezone
import logging

from src.extract import extract
from src.validate import validate_station_infos, validate_station_status
from src.transform import transform_station_infos, transform_station_status
from src.load import load_station_infos, load_station_status
from src.database import get_connection

def run_pipeline(collected_at=None):
    logging.info("Pipeline started")
    INFO_URL = "https://api.cyclocity.fr/contracts/toulouse/gbfs/v3/station_information.json"
    STATUS_URL = "https://api.cyclocity.fr/contracts/toulouse/gbfs/v3/station_status.json"

    if collected_at is None:
        collected_at = datetime.now(timezone.utc)

    _, station_infos = extract(INFO_URL)
    last_updated_status, station_status = extract(STATUS_URL)

    station_infos = validate_station_infos(station_infos)
    station_status = validate_station_status(station_status)

    station_infos_transformed = transform_station_infos(station_infos)
    logging.info("Station infos: %s rows", len(station_infos_transformed))
    
    station_status_transformed = transform_station_status(last_updated_status, station_status, collected_at)
    logging.info("Station status: %s rows", len(station_status_transformed))

    with get_connection() as conn:

        try:
            load_station_infos(conn, station_infos_transformed)
            load_station_status(conn, station_status_transformed)
        
        except Exception as e:
            logging.error(f"Loading failed: {e}")
            raise

    logging.info("Loading complete: stations loaded successfully")


if __name__ == "__main__":
    run_pipeline()