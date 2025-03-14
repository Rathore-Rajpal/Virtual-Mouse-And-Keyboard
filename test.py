import webbrowser

from assist.Engine.commands import speak

def SearchYoutube(query):
    
    search_term = query.lower().replace("search", "").replace("on youtube", "").strip()
    search_url = f"https://www.youtube.com/results?search_query={search_term}"
    webbrowser.open(search_url)


