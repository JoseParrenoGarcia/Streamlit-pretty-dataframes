import pandas as pd
import numpy as np


def create_synthetic_data():
    mock_data = {
        "Country": ["US", "IN", "BR", "ES", "AR", "IT", "EG"],
        "Period_1": [50_000, 30_000, 17_000, 14_000, 22_000, 16_000, 1_000],
        "Period_2": [52_000, 37_000, 16_000, 12_000, 21_000, 19_000, 2_100],
    }

    df = pd.DataFrame(mock_data)
    df['Difference'] = df['Period_2'] - df['Period_1']
    df['Percentage Change'] = np.round(((df['Period_2'] - df['Period_1']) / df['Period_1']), 2)
    df['Percentage Change rank'] = df['Percentage Change'].rank(method='dense', ascending=False).astype(int)

    return df
