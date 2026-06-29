import requests
import time
import random
import pandas as pd

SEARCH_URL = "https://api.divar.ir/v8/postlist/w/search"
DETAIL_URL = "https://api.divar.ir/v8/posts-v2/web/{}"

session = requests.Session()
headers = {"Content-Type": "application/json"}

def get_tokens(limit=40):
    tokens = []
    pagination_data = None  

    while len(tokens) < limit:
        payload = {
            "city_ids": ["1"],
            "disable_recommendation": False,
            "map_state": {"camera_info": {"bbox": {}}},
            "search_data": {
                "form_data": {"data": {"category": {"str": {"value": "light"}}}},
                "query": "ماشین",
                "server_payload": {
                    "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                    "additional_form_data": {
                        "data": {"sort": {"str": {"value": "sort_date"}}}
                    }
                }
            },
            "source_view": "SEARCH_BAR_QUERY_SUGGESTION"
        }

        if pagination_data:
            payload["pagination_data"] = pagination_data

        r = session.post(SEARCH_URL, json=payload, headers=headers)
        try:
            data = r.json()
        except Exception as e:
            print("JSON decode error:", e)
            break

        new_count = 0
        for w in data.get("list_widgets", []):
            try:
                t = w["data"]["token"]
                if t not in tokens:
                    tokens.append(t)
                    new_count += 1
            except Exception:
                pass

        print(f"TOKENS: {len(tokens)} (+{new_count} new)")

        if not data.get("pagination", {}).get("has_next_page"):
            print("STOP: has_next_page = False")
            break

        next_pagination = data.get("pagination", {}).get("data")
        if not next_pagination:
            print("STOP: pagination.data خالیه")
            break

        if new_count == 0:
            print("WARNING: این صفحه چیزی جدید نداشت")

        pagination_data = next_pagination
        time.sleep(random.uniform(1, 2))

    return tokens


def parse_detail(data):
    out: dict = {
        "token": None, "url": None, "title": None, "price": None,
        "mileage": None, "year": None, "color": None, "brand_model": None,
        "gearbox": None, "fuel": None, "insurance": None,
        "score_engine": None, "score_chassis": None,
        "score_body": None, "score_gearbox": None,
        "desc": None
    }

    def extract_field(label, value):
        if not label or value is None:
            return
        if "برند و مدل" in label:
            out["brand_model"] = value
        elif "مدل (سال تولید)" in label:
            out["year"] = value
        elif "کارکرد" in label:
            out["mileage"] = value
        elif "رنگ" in label:
            out["color"] = value
        elif "گیربکس" in label:
            out["gearbox"] = value
        elif "نوع سوخت" in label:
            out["fuel"] = value
        elif "قیمت" in label:
            out["price"] = value
        elif "بیمه" in label:
            out["insurance"] = value

    def extract_score(label, value):
        if not label or value is None:
            return
        if "موتور" in label:
            out["score_engine"] = value
        elif "شاسی" in label:
            out["score_chassis"] = value
        elif "بدنه" in label:
            out["score_body"] = value
        elif "گیربکس" in label:
            out["score_gearbox"] = value

    for sec in data.get("sections", []):
        name = sec.get("section_name")
        widgets = sec.get("widgets", [])

        if name == "TITLE":
            for w in widgets:
                d = w.get("data", {})
                out["title"] = d.get("title", out["title"])

        if name == "DESCRIPTION":
            for w in widgets:
                d = w.get("data", {})
                if "text" in d:
                    out["desc"] = d["text"]

        if name == "LIST_DATA":
            for w in widgets:
                wtype = w.get("widget_type")
                d = w.get("data", {})

                if wtype == "GROUP_INFO_ROW":
                    for it in d.get("items", []):
                        extract_field((it.get("title") or "").strip(), it.get("value"))

                elif wtype == "UNEXPANDABLE_ROW":
                    extract_field((d.get("title") or "").strip(), d.get("value"))

                elif wtype == "SCORE_ROW":
                    label = (d.get("title") or "").strip()
                    value = d.get("descriptive_score")
                    extract_score(label, value)

    return out


def get_detail(token):
    url = DETAIL_URL.format(token)
    try:
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


if __name__ == "__main__":
    tokens = get_tokens(100)
    print("TOTAL TOKENS:", len(tokens))

    results = []

    for i, t in enumerate(tokens):
        data = get_detail(t)
        if not data:
            continue
        parsed = parse_detail(data)
        parsed["token"] = t
        parsed["url"] = f"https://divar.ir/v/{t}"
        results.append(parsed)
        print(f"PARSED {i+1}/{len(tokens)}")
        time.sleep(random.uniform(1.2, 2.5))

  
    df = pd.DataFrame(results)
    df.to_csv(
        "D:/Web Scaping/divardata.csv",
        index=False,
        encoding="utf-8"
    )
    print("DONE -> divardata.csv")