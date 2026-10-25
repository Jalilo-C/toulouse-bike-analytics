from unittest.mock import patch, Mock
from src.extract import extract
import requests
import pytest

def test_extract_success():
    fake_data = {
        "last_updated": "2026-10-25T10:00:00Z",
        "data": {
            "stations": [
                {"station_id": "1"},
                {"station_id": "2"}
            ]
        }
    }

    fake_response = Mock()
    fake_response.json.return_value = fake_data
    fake_response.raise_for_status.return_value = None

    with patch("src.extract.requests.get", return_value=fake_response) as mock_get:
        last_updated, stations = extract("https://example.com/gbfs")
        assert last_updated == fake_data["last_updated"]
        assert len(stations)==2
        assert stations == fake_data["data"]["stations"]
        mock_get.assert_called_once_with(
            "https://example.com/gbfs",
            timeout=5
        )

def test_extract_invalid_json_structure():
    fake_data = {
        "last_updated": "2026-10-25T10:00:00Z",
        "data": {
            "stations": "invalid"
        }
    }

    fake_response = Mock()
    fake_response.json.return_value = fake_data
    fake_response.raise_for_status.return_value = None

    with patch("src.extract.requests.get", return_value=fake_response) as mock_get:
        with pytest.raises(ValueError, match="stations must be a list"):
            extract("https://example.com/gbfs")
        assert mock_get.call_count == 1

def test_extract_network_error():
    with patch(
        "src.extract.requests.get",
        side_effect=requests.ConnectionError("Network unavailable")
    ) as mock_get, patch("src.extract.time.sleep") as mock_sleep:

        with pytest.raises(requests.ConnectionError):
            extract("https://example.com/gbfs")

        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2