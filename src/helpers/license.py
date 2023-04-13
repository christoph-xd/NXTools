import base64
import codecs
import datetime
import json
from pathlib import Path


def create_lic(days: int = 14):
    date = datetime.datetime.date(datetime.datetime.now()) + datetime.timedelta(
        days=days
    )
    config = Path(__file__).parent.parent
    with open(f"{config}/config.json") as f:
        data = json.load(f)
    license = str(date).encode("ascii")
    license = base64.b64encode(license)
    license = license.decode("ascii")
    data["license"] = license
    with codecs.open(f"{config}/config.json", "w", "utf8") as f:
        f.write(json.dumps(data, sort_keys=True, ensure_ascii=False))
    return license


def check_lic(lic: str):
    license = lic.encode("ascii")
    license = base64.b64decode(license)
    license = license.decode("ascii")
    print(type(license))
    print(license)
    return datetime.datetime.strptime(license, "%Y-%m-%d")


lic = create_lic(180)
