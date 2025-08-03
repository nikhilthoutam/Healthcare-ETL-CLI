import pandas as pd

class DataTransformer:
    """
    Cleans/transforms API JSON into dictionary-list for DB loading.
    """

    def clean_cases(self, raw_json, start_date, end_date):
        timeline = raw_json.get("timeline", {})
        country = raw_json.get("country", "Unknown")

        df = pd.DataFrame({
            'report_date': pd.to_datetime(list(timeline.get('cases', {}).keys()), format="%m/%d/%y"),
            'total_cases': list(timeline.get('cases', {}).values()),
            'total_deaths': list(timeline.get('deaths', {}).values())
        })

        df["country_name"] = country
        df["new_cases"] = df["total_cases"].diff().fillna(0).astype(int)
        df["new_deaths"] = df["total_deaths"].diff().fillna(0).astype(int)

        df = df[(df["report_date"] >= start_date) & (df["report_date"] <= end_date)]
        df = df[['report_date','country_name','total_cases','new_cases','total_deaths','new_deaths']]
        df = df.drop_duplicates(subset=["report_date","country_name"])
        return df.to_dict(orient="records")

    def clean_vaccinations(self, raw_json, start_date, end_date):
        timeline = raw_json.get("timeline", {})
        country = raw_json.get("country", "Unknown")

        df = pd.DataFrame({
            'report_date': pd.to_datetime(list(timeline.keys()), format="%m/%d/%y"),
            'total_vaccinations': list(timeline.values())
        })

        df["country_name"] = country
        df = df[(df["report_date"] >= start_date) & (df["report_date"] <= end_date)]
        df = df[['report_date','country_name','total_vaccinations']].drop_duplicates(subset=['report_date','country_name'])
        return df.to_dict(orient="records")
