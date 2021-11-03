from icecream import ic


config = dict(
    url_seeds=dict(
        ted='https://www.ted.com/talks',
        ted_summary='https://tedsummaries.com'
    )
)

if __name__ == "__main__":
    import json

    fl_nm = 'config.json'
    ic(config)
    with open(fl_nm, 'w') as f:
        json.dump(config, f, indent=4)
