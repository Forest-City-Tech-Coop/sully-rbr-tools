# Dash app

This app connects to a supabase db to get operational info and uses a Dash webapp to process and visualize the data.

## Project outcomes
ultimately, this app would be most useful if it could:
- visualize data
- process the data to do useful things
    - generate KPIs
    - create bulk invoices that could be imported as csv
        - ultimately connecting to QB via the api
    - easily create payroll allocation
- replace the soil sheets network. This would make the network:
    - more reliable
    - easily maintainable
    - easily interactive (webforms rather than manual sheet entry)

## Project strucutre
This app uses a basic multipage Dashapp structure. Check out the [Dash docs](https://dash.plotly.com/installation) for more info. 
there is a main app (`app.py`). the Dash server is instantiated with this code `app = Dash(__name__, use_pages=True)`. the `use_pages=True` bit allows the main app to read the `pages/` directory. Currently (9/24/25) the `app.py` layout has some filler in it. This helps to show where the page is being rendered from `pages`. It's slightly messy because I'm learning while I'm doing. It's quite simple. Here some packages installed in the venv:
- Dash: this is the main dash module. hit the [link](https://dash.plotly.com/installation) to see details. My understanding is that it uses Flask as it's web framwork
- Supabase: we are using a supabase project at work to house the data.
- plotly.express: Dash is developed by Plotly, and this module helps make dat visualizations easy to have in the webpage format
The rest of the libraries/modules are straighforward.

## Startup
1. Make sure you have python installed. One of these should work. If they don't you might not have python installed
    - `python3 --version`
    - `python --version`
    - `python`
    - install python if you keep coming up with errors
2. activate the virtual environment
    - `source venv/bin/activate`
3. start the app
    - `python3 app.py`

