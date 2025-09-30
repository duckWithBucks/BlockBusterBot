from pycoingecko import CoinGeckoAPI

    # Instantiate the CoinGeckoAPI client
cg = CoinGeckoAPI()

print("Enter the cryptocurrency in small letters (bitocin/litecoin/ethereum):")
crypto = input()

if (crypto == "bitcoin"):
    try:
        price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')

        # Extract and print the Bitcoin price
        bitcoin_price = price_data['bitcoin']['usd']
        print(f"The current price of Bitcoin is ${bitcoin_price}")

    except Exception as e:
        print(f"An error occurred: {e}")
        
elif (crypto == "litecoin"):
    try:
        price_data = cg.get_price(ids='litecoin', vs_currencies='usd')

        # Extract and print the Litecoin price
        bitcoin_price = price_data['litecoin']['usd']
        print(f"The current price of Litecoin is ${bitcoin_price}")

    except Exception as e:
        print(f"An error occurred: {e}")

elif (crypto == "ethereum"):
    try:
        price_data = cg.get_price(ids='ethereum', vs_currencies='usd')

        # Extract and print the Ethereum price
        bitcoin_price = price_data['ethereum']['usd']
        print(f"The current price of Ethereum is ${bitcoin_price}")

    except Exception as e:
        print(f"An error occurred: {e}")

else:
    print("Sorry, an error occurred. Please try again.")