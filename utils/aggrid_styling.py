from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


def get_numeric_style_with_precision(column_name: str,
                                     decimal_points: int = None,
                                     currency: bool = False,
                                     percentage: bool = False,
                                     ) -> dict:
    if currency:
        return {"type": ["numericColumn", "customNumericFormat"],
                "valueGetter": f"data.{column_name}.toLocaleString('en-US', {{style: 'currency', currency: 'USD', maximumFractionDigits: {decimal_points}}})",
                }


    elif percentage:
        PERCENTAGE_FORMATTER = JsCode(
            f"""
            function(params) {{
                            if (params.value === null || params.value === undefined) {{
                                return '';
                            }}
                            return (params.value * 100).toLocaleString('en-US', {{minimumFractionDigits: {decimal_points}, maximumFractionDigits: {decimal_points}}}) + '%';
                        }}
            """
        )

        return {"type": ["numericColumn", "customNumericFormat"],
                "valueFormatter": PERCENTAGE_FORMATTER,
                }

    else:
        THOUSAND_COMMA_SEPARATOR = JsCode(
            f"""
            function(params) {{
                            if (params.value === null || params.value === undefined) {{
                                return '';
                            }}
                            return Number(params.value).toLocaleString('en-US');
                            }}
            """
        )

        return {"type": ["numericColumn", "customNumericFormat"],
                "valueFormatter": THOUSAND_COMMA_SEPARATOR,
                }


# Define serializable column formatting
column_formatting = {
        'Country': ('Country', {}),
        'Period_1': ('Period 1', {**get_numeric_style_with_precision(column_name='Period_1', decimal_points=0, currency=True)}),
        'Period_2': ('Period 2', {**get_numeric_style_with_precision(column_name='Period_2', decimal_points=0, currency=True)}),
        'Difference': ('Difference', {**get_numeric_style_with_precision(column_name='Difference', decimal_points=0, currency=True)}),
        'Percentage Change': ('Percentage', {**get_numeric_style_with_precision(column_name='Percentage', decimal_points=0, percentage=True)}),
        'Percentage Change rank': ('Percentage Change rank', {}),
    }


grid_options = {
    'autoSizeStrategy':
        {'type': 'fitCellContents',}
}


# Wrapping up function
def aggrid_cells_formatting(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_grid_options(**grid_options)

    # https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html#st_aggrid.grid_options_builder.GridOptionsBuilder.configure_column
    # https://www.ag-grid.com/javascript-data-grid/column-properties/
    for input_column_name, (clean_name, style_dict) in column_formatting.items():
        grid_builder.configure_column(input_column_name, header_name=clean_name, **style_dict)

    # Build grid options
    gridOptions = grid_builder.build()

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return AgGrid(df,
                  gridOptions=gridOptions,
                  allow_unsafe_jscode=True,
                  height=min(500, (len(df))*38),  # 38px per row or 500px
                  fit_columns_on_grid_load=False,
                  theme='balham',  # 'streamlit', 'balham', 'alpine', 'material'
                  )
