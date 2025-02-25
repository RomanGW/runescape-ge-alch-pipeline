# Overview
`runescape-ge-alch-pipeline`, a lovably marketable repository written to show off some fluency in data pipeline construction, data conversion, and SQL. This repo is one part custom written pipeline to convert JSON from API GET requests to .csv for use in SQL database engines. Besides showing off skills, the main point of this codebase is to keep track of GE prices for the purpose of maximizing high alchemy profits (iykyk). 

# Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x: [Download](https://www.python.org/downloads/)
- PostgreSQL: [Download](https://www.postgresql.org/download/)
- Required Python packages:
  ```bash
  pip install requests pandas
(As well as just enough knowledge to compile Python and SQL code.)

# Getting Started

## Pulling the Data
Clone the repository to your local machine. Run `data_pipeline.py` in your IDE or from the command line to generate `ge.csv`, which contains data pulled from GE-based APIs on the RuneScape wiki. If you encounter an error, check the terminal for error messages and troubleshoot accordingly.

## Creating the Database
If you plan to utilize the SQL features, create a database in PostgreSQL and run the `init.sql` script. Note that functionality on other database services like SQL Server or MariaDB has not been tested.

Open `init.sql` and locate the line with the path to `ge.csv` inside the `create procedure update_ge_values()` block. Update this path to point to where `ge.csv` is stored within the data folder of the repository. Run `init.sql` to compile the tables, stored procedures, and included functions:
- `get_highest_alch_ratio()`: Returns the most profitable items based on the high alchemy to price ratio.
- `get_most_coins_on_alch()`: Returns items yielding the most coins when alched.
- `get_alch_value(item_look text)`: Returns the item price, alchemy return, and the net amount gained from alching a specific item.
