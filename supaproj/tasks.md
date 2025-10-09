### tasks:
[x] connect data to the app
[x] create a df from it
[x] process the df in various ways
[] construct a query for
    - all service numbers by customer, pivoted by service type (i imagine)
[] visualize the above query
[] connect hauler time to labor time
    - that is, connect DS Hauler time from rbr.regular_hours to rbr.stops


### Phx page
[] set up dataframes
    [x] sum total products
    [] map to QB products
[x] actually the filename can just be the id
[x] generate consignment info
    - 85% expected check amount
    - % to each class
[] generate csv to create invoice for phx
    - product lines
    - amt totals
    - classes
    - date
    - due date
    - vendor (phx)
    - inv #
[] download csv
[] create tables in supabase
    - checks table
        - check num
        - check amt
        - expected amt
        - id (the filename)
    - actual phx info
        - main df loaded into the csv
[] load finished data into supabase
