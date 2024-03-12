# from xml.sax.saxutils import quoteattr
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

xml_folder = Path("originaux")
xml_output = Path("output")
csv = "metadata-result.csv"

xmls = list(xml_folder.glob("*.xml"))
xml_output.mkdir(exist_ok=True)
df = pd.read_csv(csv, delimiter=";").fillna("")

for xml in tqdm(xmls):
    with open(xml, "r") as file:
        soup = BeautifulSoup(file, "xml")

    text = soup.find('TEI').find('text')

    row = df.loc[df["file"] == xml.name]

    for col in row.columns:
        if col in ["file", "PDF"]:
            continue

        val = row[col].values[0]

        if col == "date":
            val = int(val.split("-")[0])
            val = int(val / 10) * 10

        if not val:
            continue
        text[col] = val

    with open(xml_output / xml.name, "w") as file:
        file.write(str(soup))
