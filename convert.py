import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FEED_URL = os.environ["SOURCE_FEED_URL"]
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "docs/mono.json"))
LIMIT = int(os.getenv("LIMIT", "0"))
MAX_PAY_IN_PARTS = int(os.getenv("MAX_PAY_IN_PARTS", "6"))
DAYS_TO_DISPATCH = int(os.getenv("DAYS_TO_DISPATCH", "2"))
WAREHOUSE_ID = os.getenv("WAREHOUSE_ID", "BLOKKY-MAIN")

def money(value):
    if value is None or value == "":
        return None
    number = float(value.replace(",", "."))
    return int(number) if number.is_integer() else int(round(number))

request = urllib.request.Request(
    SOURCE_FEED_URL,
    headers={"User-Agent": "BLOKKY-MonoMarket-Feed/1.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
offers = root.findall(".//offer")

filtered_offers = []

for offer in offers:
    stock = int(float((offer.findtext("stock_quantity") or "0").replace(",", ".")))
    available = offer.attrib.get("available", "false").lower() == "true"

    if not available or stock <= 0:
        continue

    filtered_offers.append(offer)

if LIMIT > 0:
    filtered_offers = filtered_offers[:LIMIT]

items = []

for offer in filtered_offers:
    stock = int(float((offer.findtext("stock_quantity") or "0").replace(",", ".")))

    items.append({
        "code": offer.attrib["id"],
        "price": money(offer.findtext("price")),
        "old_price": money(offer.findtext("price_old")),
        "availability": offer.attrib.get("available", "false").lower() == "true",
        "stock": stock,
        "warehouses": [
            {
                "id": WAREHOUSE_ID,
                "stock": stock
            }
        ],
        "warranty_type": "no",
        "warranty_period": 0,
        "max_pay_in_parts": MAX_PAY_IN_PARTS,
        "days_to_dispatch": DAYS_TO_DISPATCH,
        "manufacture": None
    })

payload = {
    "updatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "total": len(items),
    "data": items
}

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)
