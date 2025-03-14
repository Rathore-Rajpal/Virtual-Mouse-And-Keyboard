import webbrowser
import urllib.parse # For URL encoding
from assist.Engine.commands import speak

def search_product(query):
    # Convert query to lowercase and strip extra spaces
    query = query.lower().strip()

    # List of websites we support
    supported_websites = [
        "amazon", "myntra", "flipkart", "ebay", "snapdeal", "walmart",
        "alibaba", "aliexpress", "bestbuy", "shopclues", "etsy", "homedepot",
        "target", "wayfair", "zappos", "ikea", "olx", "makemytrip", "expedia", "booking"
    ]

    # Find the website name by matching from the end
    for website in supported_websites:
        if website in query:
            # Extract the product name by splitting before the website name
            product_name = query.split("search for")[1].split(f"on {website}")[0].strip()
            website_name = website
            break
    else:
        speak("No supported website found in query.")
        print("No supported website found in query.")
        return

    # Dictionary to store base URLs for different websites
    search_urls = {
        "amazon": "https://www.amazon.in/s?k=",
        "myntra": "https://www.myntra.com/",
        "flipkart": "https://www.flipkart.com/search?q=",
        "ebay": "https://www.ebay.com/sch/i.html?_nkw=",
        "snapdeal": "https://www.snapdeal.com/search?keyword=",
        "walmart": "https://www.walmart.com/search/?query=",
        "alibaba": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=",
        "aliexpress": "https://www.aliexpress.com/wholesale?SearchText=",
        "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=",
        "shopclues": "https://www.shopclues.com/search?q=",
        "etsy": "https://www.etsy.com/search?q=",
        "homedepot": "https://www.homedepot.com/s/",
        "target": "https://www.target.com/s?searchTerm=",
        "wayfair": "https://www.wayfair.com/keyword.php?keyword=",
        "zappos": "https://www.zappos.com/search?term=",
        "ikea": "https://www.ikea.com/us/en/search/?q=",
        "olx": "https://www.olx.in/items/q-",
        "makemytrip": "https://www.makemytrip.com/flights/search?itinerary=",
        "expedia": "https://www.expedia.com/Hotel-Search?destination=",
        "booking": "https://www.booking.com/searchresults.html?ss=",
    }

    # Encode the product name for URL compatibility
    product_search_query = urllib.parse.quote(product_name)
    search_url = search_urls[website_name] + product_search_query
    speak(f"Searching for '{product_name}' on {website_name}...")
    print(f"Searching for '{product_name}' on {website_name}...")

    # Open the search URL in the web browser
    webbrowser.open(search_url)

