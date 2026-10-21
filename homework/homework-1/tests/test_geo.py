import requests


def test_search_paris():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": "Paris",
            "countryCode": "FR",
            "count": 1,
            "language": "en",
        },
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    results = data["results"]

    assert len(results) == 1
    assert results[0]["name"] == "Paris"
    assert results[0]["country_code"] == "FR"
def test_unknown_city_returns_no_results():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "zzzznonexistentcity987654321"},
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("results", []) == []


def test_count_zero_returns_validation_error():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Paris", "count": 0},
        timeout=15,
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] is True
    assert isinstance(data["reason"], str)
    assert len(data["reason"]) > 0
def test_count_maximum_is_allowed():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Paris", "count": 100},
        timeout=15,
    )

    assert response.status_code == 200

    results = response.json()["results"]

    assert 1 <= len(results) <= 100


def test_count_above_maximum_returns_validation_error():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Paris", "count": 101},
        timeout=15,
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] is True
    assert isinstance(data["reason"], str)
    assert len(data["reason"]) > 0


def test_missing_name_returns_validation_error():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"count": 1},
        timeout=15,
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] is True
    assert isinstance(data["reason"], str)
    assert len(data["reason"]) > 0


def test_location_fields_have_valid_types_and_values():
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": "Paris",
            "countryCode": "FR",
            "count": 1,
        },
        timeout=15,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")

    data = response.json()

    assert isinstance(data, dict)
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 1

    city = data["results"][0]

    assert isinstance(city, dict)
    assert type(city["id"]) is int
    assert isinstance(city["name"], str)
    assert len(city["name"]) > 0

    assert type(city["latitude"]) in (int, float)
    assert type(city["longitude"]) in (int, float)
    assert -90 <= city["latitude"] <= 90
    assert -180 <= city["longitude"] <= 180

    assert isinstance(city["country_code"], str)
    assert len(city["country_code"]) == 2