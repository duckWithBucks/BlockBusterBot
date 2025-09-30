from pycoingecko import CoinGeckoAPI

    # Instantiate the CoinGeckoAPI client
cg = CoinGeckoAPI()

    # Get the current price of Bitcoin in USD
try:
    price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')

        # Extract and print the Bitcoin price
    bitcoin_price = price_data['bitcoin']['usd']
    print(f"The current price of Bitcoin is ${bitcoin_price}")

except Exception as e:
    print(f"An error occurred: {e}")