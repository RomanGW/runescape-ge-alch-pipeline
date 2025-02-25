import requests
import datetime
import pandas as pd

def get_data(source, attempts = 0):
    """
    Fetch data from the given API source.
    """

    # Runescape Wiki natively blocks default requests user-agent, so we set a custom one in headers to meet acceptable use policy!
    # See: https://runescape.wiki/w/Help:APIs for more info.
    headers = {'Accept': 'application/json', 'User-Agent' : 'ge-price-to-alc-ratio'}

    # Pull from API data.
    try:
        print(f"Accessed {source}!")
        response = requests.get(source, headers = headers)
        return response.json() # Return JSON from page. O:
    except Exception as e:
        if attempts < 3:
            get_data(source, attempts + 1)
            return
        print(f"Unable to access {source}! Error: {e}")

def main():
    start = datetime.datetime.now()
    
    # Initialize modular source list.
    sources = {
        'price' : 'https://oldschool.runescape.wiki/?title=Module:GEPrices/data.json&action=raw',
        'high_alch' : 'https://oldschool.runescape.wiki/?title=Module:GEHighAlchs/data.json&action=raw',
        'low_alch' : 'https://oldschool.runescape.wiki/?title=Module:GELowAlchs/data.json&action=raw'
    }

    # Initialize header and data.
    header = ['item'] + list(sources.keys())
    data_list = []

    # Iterate through sources (lmao)
    for source, url in sources.items():
        print(f"Attempting to access {url}...")
        # Pull response from sources.
        response = get_data(url)
        print(f"Pulling data from {url}...")

        # Iterate through all items in response.
        if response:
            for item, value in response.items():
                # Check if item exists in data_list.
                item_data = next((data for data in data_list if data['item'] == item), None)
                # Filter out characters that can affect the future data querying.
                if not '%' in item:
                    # If not, add a new dictionary item.
                    if item_data is None:
                        item_data = {'item': item}
                        data_list.append(item_data)
                
                    # Add values found from each source.
                    item_data[source] = value
        else:
            print("Error GETting API data! Please notify me on Github!")
            return
    
    # Create DataFrame and convert to CSV.
    print("Writing DataFrame...")
    df = pd.DataFrame(data_list)

    print("Converting DataFrame to csv...")
    df.to_csv('data\ge.csv', header = header, index = False)

    # Print time to run!
    print(f"Success! Ran in: {datetime.datetime.now() - start}")

if __name__ == "__main__":
    main()