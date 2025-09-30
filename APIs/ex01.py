import requests

def get_random_zenquote():
    """Fetches and returns a random quote from ZenQuotes.io."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data and len(data) > 0:
            quote = data[0]['q']
            author = data[0]['a']
            return f'"{quote}" - {author}'
        else:
            return "Could not retrieve a quote."

    except requests.exceptions.RequestException as e:
        return f"Error fetching quote: {e}"

if __name__ == "__main__":
    random_quote = get_random_zenquote()
    print(random_quote)