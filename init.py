import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

api_url_trelle = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/23/station/53230/period/corrected-archive/data.csv"
api_url_arvids = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/23/station/167710/period/corrected-archive/data.csv"
api_url_sanda = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/23/station/78140/period/corrected-archive/data.csv"
api_url_hemse = "https://resource.sgu.se/oppnadata/grundvatten/api/grundvattennivaer/nivaer/station/8_5?format=csv"

trelle = "trelleborg.csv"
arvids = "arvidsjour.csv"
sanda = "sanda.csv"
hemse_grundvatten = "hemsegv.csv"


def read_file(api, file_name):
    req = requests.get(api)

    url_content = req.content

    csv_file = open(file_name, "wb")

    csv_file.write(url_content)

    csv_file.close()


read_file(api_url_trelle, trelle)
read_file(api_url_arvids, arvids)
read_file(api_url_sanda, sanda)
read_file(api_url_hemse, hemse_grundvatten)

data_t = pd.read_csv(trelle, delimiter=";", skiprows=10)
data_a = pd.read_csv(arvids, delimiter=";", skiprows=12)
data_s = pd.read_csv(sanda, delimiter=";", skiprows=10)
data_h_gv = pd.read_csv(hemse_grundvatten, delimiter=";", encoding="latin1")


def clear_smhi_data_pandas(df):
    # Remove unused data columns
    df.drop(
        [
            "Från Datum Tid (UTC)",
            "Unnamed: 5",
            "Tidsutsnitt:",
            "Kvalitet",
            "Till Datum Tid (UTC)",
        ],
        inplace=True,
        axis=1,
    )

    prefixes = ("1986", "1989", "2000")
    df_may = df[df["Representativ månad"].str.endswith("05")]

    df_may40 = df_may[~df_may["Representativ månad"].str.startswith(prefixes)]
    df_may_40 = df_may40.iloc[-30:]

    return df_may_40


def clear_other_data_pandas(df):
    # Remove unused data columns
    df.drop(
        [
            "Område- och stationsnummer",
            "Stationens namn",
            "Startdatum för mätning",
            "Slutdatum för mätning",
            "Jordart",
            "Akvifertyp",
            "Topografiskt läge",
            "Referensnivå för röröverkant (m ö.h.)",
            "Rörhöjd ovan mark (m)",
            "Total rörlängd (m)",
            "Metod för mätning",
            "Kommunkod",
            "EUCD för grundvattenförekomst",
            "N",
            "E",
            "Nivåmätningskvalitet",
            "Nivåanmärkning",
            "Stationsanmärkning",
        ],
        inplace=True,
        axis=1,
    )

    # df_may = df[df["Datum för mätning"].str.replace(" 00:00:00", "")]
    df["Datum för mätning"] = df["Datum för mätning"].str[:-12]

    df_may = df[df["Datum för mätning"].str.endswith("05")]

    # df_may["Datum för mätning"] = df_may["Datum för mätning"].astype("string")

    df_may.drop_duplicates(subset=["Datum för mätning"], inplace=True)

    prefixes = ("2000", "2023")

    df_may40 = df_may[~df_may["Datum för mätning"].str.startswith(prefixes)]
    df_may_40 = df_may40.iloc[-30:]

    return df_may_40


df_t = clear_smhi_data_pandas(data_t)
df_a = clear_smhi_data_pandas(data_a)
df_s = clear_smhi_data_pandas(data_s)
df_h_gv = clear_other_data_pandas(data_h_gv)

print(df_h_gv)
print(df_s)
df_t["Representativ månad"] = df_t["Representativ månad"].astype("string")
df_a["Representativ månad"] = df_a["Representativ månad"].astype("string")
df_s["Representativ månad"] = df_s["Representativ månad"].astype("string")


df_temp_jan_visby = clear_smhi_data_pandas(data_temp_jan_visby, "visby", "01")
df_temp_feb_visby = clear_smhi_data_pandas(data_temp_feb_visby, "visby", "02")
df_temp_march_visby = clear_smhi_data_pandas(data_temp_march_visby, "visby", "03")
df_temp_april_visby = clear_smhi_data_pandas(data_temp_april_visby, "visby", "04")
df_temp_may_visby = clear_smhi_data_pandas(data_temp_may_visby, "visby", "05")
df_temp_june_visby = clear_smhi_data_pandas(data_temp_june_visby, "visby", "06")
df_temp_july_visby = clear_smhi_data_pandas(data_temp_july_visby, "visby", "07")
df_temp_aug_visby = clear_smhi_data_pandas(data_temp_aug_visby, "visby", "08")
df_temp_sep_visby = clear_smhi_data_pandas(data_temp_sep_visby, "visby", "09")
df_temp_okt_visby = clear_smhi_data_pandas(data_temp_okt_visby, "visby", "10")
df_temp_nov_visby = clear_smhi_data_pandas(data_temp_nov_visby, "visby", "11")
df_temp_dec_visby = clear_smhi_data_pandas(data_temp_dec_visby, "visby", "12")


df_temp_jan_visby = df_temp_jan_visby.rename(columns={"Lufttemperatur": "Temp jan"})
df_temp_feb_visby = df_temp_feb_visby.rename(columns={"Lufttemperatur": "Temp feb"})
df_temp_march_visby = df_temp_march_visby.rename(
    columns={"Lufttemperatur": "Temp march"}
)
df_temp_april_visby = df_temp_april_visby.rename(
    columns={"Lufttemperatur": "Temp april"}
)
df_temp_may_visby = df_temp_may_visby.rename(columns={"Lufttemperatur": "Temp may"})
df_temp_june_visby = df_temp_june_visby.rename(columns={"Lufttemperatur": "Temp june"})
df_temp_july_visby = df_temp_july_visby.rename(columns={"Lufttemperatur": "Temp july"})
df_temp_aug_visby = df_temp_aug_visby.rename(columns={"Lufttemperatur": "Temp aug"})
df_temp_sep_visby = df_temp_sep_visby.rename(columns={"Lufttemperatur": "Temp sep"})
df_temp_okt_visby = df_temp_okt_visby.rename(columns={"Lufttemperatur": "Temp okt"})
df_temp_nov_visby = df_temp_nov_visby.rename(columns={"Lufttemperatur": "Temp nov"})
df_temp_dec_visby = df_temp_dec_visby.rename(columns={"Lufttemperatur": "Temp dec"})


df_temp_jan_visby["Representativ månad"] = df_temp_jan_visby[
    "Representativ månad"
].dt.year
df_temp_feb_visby["Representativ månad"] = df_temp_feb_visby[
    "Representativ månad"
].dt.year
df_temp_march_visby["Representativ månad"] = df_temp_march_visby[
    "Representativ månad"
].dt.year
df_temp_april_visby["Representativ månad"] = df_temp_april_visby[
    "Representativ månad"
].dt.year
df_temp_may_visby["Representativ månad"] = df_temp_may_visby[
    "Representativ månad"
].dt.year
df_temp_june_visby["Representativ månad"] = df_temp_june_visby[
    "Representativ månad"
].dt.year
df_temp_july_visby["Representativ månad"] = df_temp_july_visby[
    "Representativ månad"
].dt.year
df_temp_aug_visby["Representativ månad"] = df_temp_aug_visby[
    "Representativ månad"
].dt.year
df_temp_sep_visby["Representativ månad"] = df_temp_sep_visby[
    "Representativ månad"
].dt.year
df_temp_okt_visby["Representativ månad"] = df_temp_okt_visby[
    "Representativ månad"
].dt.year
df_temp_nov_visby["Representativ månad"] = df_temp_nov_visby[
    "Representativ månad"
].dt.year
df_temp_dec_visby["Representativ månad"] = df_temp_dec_visby[
    "Representativ månad"
].dt.year

# Visby


# make year index for sorting
# Lund
df_temp_jan_visby = df_temp_jan_visby.set_index("Representativ månad")
df_temp_feb_visby = df_temp_feb_visby.set_index("Representativ månad")
df_temp_march_visby = df_temp_march_visby.set_index("Representativ månad")
df_temp_april_visby = df_temp_april_visby.set_index("Representativ månad")
df_temp_may_visby = df_temp_may_visby.set_index("Representativ månad")
df_temp_june_visby = df_temp_june_visby.set_index("Representativ månad")
df_temp_july_visby = df_temp_july_visby.set_index("Representativ månad")
df_temp_aug_visby = df_temp_aug_visby.set_index("Representativ månad")
df_temp_sep_visby = df_temp_sep_visby.set_index("Representativ månad")
df_temp_okt_visby = df_temp_okt_visby.set_index("Representativ månad")
df_temp_nov_visby = df_temp_nov_visby.set_index("Representativ månad")
df_temp_dec_visby = df_temp_dec_visby.set_index("Representativ månad")


data_temp_jan_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_feb_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_march_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_april_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_may_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_june_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_july_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_aug_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_sep_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_okt_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_nov_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)
data_temp_dec_lule = pd.read_csv(lule_temp, delimiter=";", skiprows=9)


df_temp_jan_lule = clear_smhi_data_pandas(data_temp_jan_lule, "lule", "01")
df_temp_feb_lule = clear_smhi_data_pandas(data_temp_feb_lule, "lule", "02")
df_temp_march_lule = clear_smhi_data_pandas(data_temp_march_lule, "lule", "03")
df_temp_april_lule = clear_smhi_data_pandas(data_temp_april_lule, "lule", "04")
df_temp_may_lule = clear_smhi_data_pandas(data_temp_may_lule, "lule", "05")
df_temp_june_lule = clear_smhi_data_pandas(data_temp_june_lule, "lule", "06")
df_temp_july_lule = clear_smhi_data_pandas(data_temp_july_lule, "lule", "07")
df_temp_aug_lule = clear_smhi_data_pandas(data_temp_aug_lule, "lule", "08")
df_temp_sep_lule = clear_smhi_data_pandas(data_temp_sep_lule, "lule", "09")
df_temp_okt_lule = clear_smhi_data_pandas(data_temp_okt_lule, "lule", "10")
df_temp_nov_lule = clear_smhi_data_pandas(data_temp_nov_lule, "lule", "11")
df_temp_dec_lule = clear_smhi_data_pandas(data_temp_dec_lule, "lule", "12")


df_temp_jan_lule = df_temp_jan_lule.rename(columns={"Lufttemperatur": "Temp jan"})
df_temp_feb_lule = df_temp_feb_lule.rename(columns={"Lufttemperatur": "Temp feb"})
df_temp_march_lule = df_temp_march_lule.rename(columns={"Lufttemperatur": "Temp march"})
df_temp_april_lule = df_temp_april_lule.rename(columns={"Lufttemperatur": "Temp april"})
df_temp_may_lule = df_temp_may_lule.rename(columns={"Lufttemperatur": "Temp may"})
df_temp_june_lule = df_temp_june_lule.rename(columns={"Lufttemperatur": "Temp june"})
df_temp_july_lule = df_temp_july_lule.rename(columns={"Lufttemperatur": "Temp july"})
df_temp_aug_lule = df_temp_aug_lule.rename(columns={"Lufttemperatur": "Temp aug"})
df_temp_sep_lule = df_temp_sep_lule.rename(columns={"Lufttemperatur": "Temp sep"})
df_temp_okt_lule = df_temp_okt_lule.rename(columns={"Lufttemperatur": "Temp okt"})
df_temp_nov_lule = df_temp_nov_lule.rename(columns={"Lufttemperatur": "Temp nov"})
df_temp_dec_lule = df_temp_dec_lule.rename(columns={"Lufttemperatur": "Temp dec"})


df_temp_jan_lule["Representativ månad"] = pd.to_datetime(
    df_temp_jan_lule["Representativ månad"].astype(str)
)
df_temp_feb_lule["Representativ månad"] = pd.to_datetime(
    df_temp_feb_lule["Representativ månad"].astype(str)
)
df_temp_march_lule["Representativ månad"] = pd.to_datetime(
    df_temp_march_lule["Representativ månad"].astype(str)
)
df_temp_april_lule["Representativ månad"] = pd.to_datetime(
    df_temp_april_lule["Representativ månad"].astype(str)
)
df_temp_may_lule["Representativ månad"] = pd.to_datetime(
    df_temp_may_lule["Representativ månad"].astype(str)
)
df_temp_june_lule["Representativ månad"] = pd.to_datetime(
    df_temp_june_lule["Representativ månad"].astype(str)
)
df_temp_july_lule["Representativ månad"] = pd.to_datetime(
    df_temp_july_lule["Representativ månad"].astype(str)
)
df_temp_aug_lule["Representativ månad"] = pd.to_datetime(
    df_temp_aug_lule["Representativ månad"].astype(str)
)
df_temp_sep_lule["Representativ månad"] = pd.to_datetime(
    df_temp_sep_lule["Representativ månad"].astype(str)
)
df_temp_okt_lule["Representativ månad"] = pd.to_datetime(
    df_temp_okt_lule["Representativ månad"].astype(str)
)
df_temp_nov_lule["Representativ månad"] = pd.to_datetime(
    df_temp_nov_lule["Representativ månad"].astype(str)
)
df_temp_dec_lule["Representativ månad"] = pd.to_datetime(
    df_temp_dec_lule["Representativ månad"].astype(str)
)


df_temp_jan_lule["Representativ månad"] = df_temp_jan_lule[
    "Representativ månad"
].dt.year
df_temp_feb_lule["Representativ månad"] = df_temp_feb_lule[
    "Representativ månad"
].dt.year
df_temp_march_lule["Representativ månad"] = df_temp_march_lule[
    "Representativ månad"
].dt.year
df_temp_april_lule["Representativ månad"] = df_temp_april_lule[
    "Representativ månad"
].dt.year
df_temp_may_lule["Representativ månad"] = df_temp_may_lule[
    "Representativ månad"
].dt.year
df_temp_june_lule["Representativ månad"] = df_temp_june_lule[
    "Representativ månad"
].dt.year
df_temp_july_lule["Representativ månad"] = df_temp_july_lule[
    "Representativ månad"
].dt.year
df_temp_aug_lule["Representativ månad"] = df_temp_aug_lule[
    "Representativ månad"
].dt.year
df_temp_sep_lule["Representativ månad"] = df_temp_sep_lule[
    "Representativ månad"
].dt.year
df_temp_okt_lule["Representativ månad"] = df_temp_okt_lule[
    "Representativ månad"
].dt.year
df_temp_nov_lule["Representativ månad"] = df_temp_nov_lule[
    "Representativ månad"
].dt.year
df_temp_dec_lule["Representativ månad"] = df_temp_dec_lule[
    "Representativ månad"
].dt.year


df_temp_jan_lule = df_temp_jan_lule.set_index("Representativ månad")
df_temp_feb_lule = df_temp_feb_lule.set_index("Representativ månad")
df_temp_march_lule = df_temp_march_lule.set_index("Representativ månad")
df_temp_april_lule = df_temp_april_lule.set_index("Representativ månad")
df_temp_may_lule = df_temp_may_lule.set_index("Representativ månad")
df_temp_june_lule = df_temp_june_lule.set_index("Representativ månad")
df_temp_july_lule = df_temp_july_lule.set_index("Representativ månad")
df_temp_aug_lule = df_temp_aug_lule.set_index("Representativ månad")
df_temp_sep_lule = df_temp_sep_lule.set_index("Representativ månad")
df_temp_okt_lule = df_temp_okt_lule.set_index("Representativ månad")
df_temp_nov_lule = df_temp_nov_lule.set_index("Representativ månad")
df_temp_dec_lule = df_temp_dec_lule.set_index("Representativ månad")


df_lule = pd.concat(
    [
        df_temp_jan_lule,
        df_temp_feb_lule,
        df_temp_march_lule,
        df_temp_april_lule,
        df_temp_may_lule,
        df_temp_june_lule,
        df_temp_july_lule,
        df_temp_aug_lule,
        df_temp_sep_lule,
        df_temp_okt_lule,
        df_temp_nov_lule,
        df_temp_dec_lule,
    ],
    join="inner",
    axis=1,
)
df_lule["total"] = df_lule.sum(axis=1) / 12
