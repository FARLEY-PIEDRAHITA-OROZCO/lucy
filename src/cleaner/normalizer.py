import pandas as pd

def normalize_leagues(raw_data):
    records = []

    for entry in raw_data.get("response", []):
        league = entry.get("league", {})
        country = entry.get("country", {})
        season_list = entry.get("seasons", [])

        for season in season_list:
            records.append({
                "league_id": league.get("id"),
                "league_name": league.get("name"),
                "type": league.get("type"),
                "country": country.get("name"),
                "season": season.get("year"),
                "start": season.get("start"),
                "end": season.get("end"),
                "current": season.get("current"),
            })

    return pd.DataFrame(records)
