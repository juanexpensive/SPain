from pathlib import Path

import pandas as pd

SAMPLE_DATA_PATH = Path("data") / "housing_sample.csv"
MIVAU_PROVINCIAL_URL = "https://apps.fomento.gob.es/BoletinOnline2/sedal/35101000.XLS"

SOURCE_PROVINCE_NAMES = {
    "Almería": "Almería",
    "Cádiz": "Cádiz",
    "Córdoba": "Córdoba",
    "Granada": "Granada",
    "Huelva": "Huelva",
    "Jaén": "Jaén",
    "Málaga": "Málaga",
    "Sevilla": "Sevilla",
    "Huesca": "Huesca",
    "Teruel": "Teruel",
    "Zaragoza": "Zaragoza",
    "Asturias (Principado de )": "Asturias",
    "Balears (Illes)": "Illes Balears",
    "Palmas (Las)": "Las Palmas",
    "Santa Cruz de Tenerife": "Santa Cruz de Tenerife",
    "Cantabria": "Cantabria",
    "Ávila": "Ávila",
    "Burgos": "Burgos",
    "León": "León",
    "Palencia": "Palencia",
    "Salamanca": "Salamanca",
    "Segovia": "Segovia",
    "Soria": "Soria",
    "Valladolid": "Valladolid",
    "Zamora": "Zamora",
    "Albacete": "Albacete",
    "Ciudad Real": "Ciudad Real",
    "Cuenca": "Cuenca",
    "Guadalajara": "Guadalajara",
    "Toledo": "Toledo",
    "Barcelona": "Barcelona",
    "Girona": "Girona",
    "Lleida": "Lleida",
    "Tarragona": "Tarragona",
    "Alicante/Alacant": "Alicante/Alacant",
    "Castellón/Castelló": "Castellón/Castelló",
    "Valencia/València": "Valencia/València",
    "Badajoz": "Badajoz",
    "Cáceres": "Cáceres",
    "Coruña (A)": "A Coruña",
    "Lugo": "Lugo",
    "Ourense": "Ourense",
    "Pontevedra": "Pontevedra",
    "Madrid (Comunidad de)": "Madrid",
    "Murcia (Región de)": "Murcia",
    "Navarra (Comunidad Foral de)": "Navarra",
    "Araba/Alava": "Araba/Álava",
    "Gipuzkoa": "Gipuzkoa",
    "Bizkaia": "Bizkaia",
    "Rioja (La)": "La Rioja",
    "Ceuta": "Ceuta",
    "Melilla": "Melilla",
}
VALID_QUARTERS = {"1º": "Q1", "2º": "Q2", "3º": "Q3", "4º": "Q4"}


def load_sample_housing_data() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_PATH)


def load_mivau_workbook() -> dict[str, pd.DataFrame]:
    return pd.read_excel(MIVAU_PROVINCIAL_URL, sheet_name=None, header=None)


def extract_period_columns(sheet: pd.DataFrame) -> list[tuple[int, str]]:
    period_columns: list[tuple[int, str]] = []
    current_year: str | None = None

    for column_index in range(2, sheet.shape[1]):
        year_cell = sheet.iloc[11, column_index]
        quarter_cell = sheet.iloc[13, column_index]

        if isinstance(year_cell, str) and year_cell.startswith("Año "):
            current_year = year_cell.replace("Año ", "").strip()

        quarter_text = str(quarter_cell).strip()
        quarter_suffix = VALID_QUARTERS.get(quarter_text)

        if current_year and quarter_suffix:
            period_columns.append((column_index, f"{current_year}-{quarter_suffix}"))

    return period_columns


def normalize_mivau_housing_data(workbook: dict[str, pd.DataFrame]) -> pd.DataFrame:
    normalized_rows: list[dict] = []

    for sheet in workbook.values():
        period_columns = extract_period_columns(sheet)

        for row_index in range(14, sheet.shape[0]):
            territory_cell = sheet.iloc[row_index, 1]

            if not isinstance(territory_cell, str):
                continue

            source_name = territory_cell.strip()
            province_name = SOURCE_PROVINCE_NAMES.get(source_name)

            if province_name is None:
                continue

            for column_index, period in period_columns:
                value = sheet.iloc[row_index, column_index]

                if pd.isna(value):
                    continue

                if isinstance(value, str):
                    normalized_value = value.strip().lower()

                    if normalized_value == "n.r":
                        continue

                    value = normalized_value

                normalized_rows.append(
                    {
                        "province": province_name,
                        "period": period,
                        "value": float(value),
                    }
                )

    if not normalized_rows:
        raise ValueError("MIVAU workbook returned no provincial housing price rows.")

    housing_data = pd.DataFrame(normalized_rows)
    return housing_data.sort_values(["province", "period"]).reset_index(drop=True)


def load_housing_data() -> pd.DataFrame:
    workbook = load_mivau_workbook()
    return normalize_mivau_housing_data(workbook)
