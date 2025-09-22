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


### tasks:
[x] connect data to the app
[x] create a df from it
[x] process the df in various ways
[] construct a query for
    - all service numbers by customer, pivoted by service type (i imagine)
[] visualize the above query
[] connect hauler time to labor time
    - that is, connect DS Hauler time from rbr.regular_hours to rbr.stops
