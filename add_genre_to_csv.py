from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

csv = "metadata-V01_14022024.csv"
xml_folder = Path("originaux")

xmls = list(xml_folder.glob("*.xml"))
df = pd.read_csv(csv, delimiter=";")

for xml in tqdm(xmls):
    with open(xml, "r") as file:
        soup = BeautifulSoup(file, "xml")

    genre = soup.find('TEI').find('teiHeader').find('profileDesc').find("textDesc").find("authorGender")["key"]

    df.loc[df["file"] == xml.name, "genre"] = genre

df.to_csv("metadata-result.csv", index=False, sep=";")
