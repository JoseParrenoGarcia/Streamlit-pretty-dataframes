from st_aggrid import AgGrid, GridOptionsBuilder


def _get_numeric_style_with_precision(column_name: str) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"],
            "valueGetter": f"data.{column_name}.toLocaleString('en-US', {{style: 'currency', currency: 'USD', maximumFractionDigits:1}})"
    }


column_formatting = {
        'Country': ('Country', {'width': 100}),
        'Period_1': ('Period 1', {**{'width': 100}, **_get_numeric_style_with_precision('Period_1')}),
        'Period_2': ('Period 2', {'width': 100}),
        'Difference': ('Difference', {'width': 120}),
        'Percentage Change': ('Percentage Change', {'width': 180}),
        'Percentage Change rank': ('Percentage Change rank', {'width': 200}),
    }


def aggrid_cells_formatting(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    # https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html#st_aggrid.grid_options_builder.GridOptionsBuilder.configure_column
    # https://www.ag-grid.com/javascript-data-grid/column-properties/
    for input_column_name, (clean_name, style_dict) in column_formatting.items():
        grid_builder.configure_column(input_column_name, header_name=clean_name, **style_dict)

    return AgGrid(df, gridOptions=grid_builder.build(), allow_unsafe_jscode=True,)
