import requests

BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

def get_ut_stream_sites(limit=1000):
    url = f"{BASE}/collections/monitoring-locations/items"
    params = {
        "f": "json",
        "state_code": "49",      # Utah
        "site_type": "Stream",   # from your earlier sample
        "limit": limit,
    }
    # NOTE: you may need pagination via links["next"]
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def get_daily_discharge(monitoring_location_ids, start_date, end_date):
    url = f"{BASE}/collections/daily/items"
    params = {
        "f": "json",
        "parameter_code": "00060",
        "statistic_id": "00003",
        "time": f"{start_date}/{end_date}",
        "limit": 1000,
    }

    # depending on server support, you may:
    # 1) pass monitoring_location_id multiple times, or
    # 2) chunk IDs and make multiple requests
    # safest approach: chunk
    out = []
    for chunk in chunked(monitoring_location_ids, 50):
        # many APIs accept repeated query params:
        # monitoring_location_id=USGS-...&monitoring_location_id=USGS-...
        params_chunk = params.copy()
        # requests supports list values -> repeated params
        params_chunk["monitoring_location_id"] = chunk

        r = requests.get(url, params=params_chunk, timeout=30)
        r.raise_for_status()
        out.append(r.json())
    return out
