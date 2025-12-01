def validate_dataframe(df):
    assert "league_id" in df.columns, "Falta 'league_id'"
    assert df["season"].notna().all(), "Existen temporadas vacías"
    assert df["league_id"].dtype in ["int64", "int32"], "Tipo incorrecto en league_id"

    df = df.drop_duplicates()
    return df
