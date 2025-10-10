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


## Set up local instance

1. run docker daemon
in your terminal run:
2. `docker build -t supaproj .`
3. `docker run -p 8080:8080 supaproj`

the local instance will be up and running at `localhost:8080`