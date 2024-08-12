# Streamlit Pretty DataFrames

## Introduction

**Streamlit Pretty DataFrames** is a Python project that enhances the display of dataframes within Streamlit applications. The utility allows for more visually appealing data presentation, making it easier to analyze and understand data directly within a Streamlit app.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
````

## Usage
To use this tool, include the following in your Streamlit application:

```from utils import prettify_dataframe
# Example usage

df = load_your_dataframe()  # Replace with your dataframe loading logic

st.dataframe(prettify_dataframe(df))
```

## Features
* Custom Styling: Apply custom styles to your dataframes for enhanced readability.
* Streamlit Integration: Seamless integration with Streamlit's st.dataframe.

## Dependencies
For a complete list, see the requirements.txt file.

## Configuration
You can configure the appearance and behavior of your dataframes by modifying the prettify_dataframe function in the utils directory.

## Examples
You can find example usage in the streamlit_app.py file, which demonstrates how to integrate the pretty dataframe utility within a Streamlit app.

## Contributing
Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.