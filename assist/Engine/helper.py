import re



def extract_yt_term(command):
    #Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to to find the match in the command
    match = re.search(pattern,command,re.IGNORECASE)
    #if the is found return the extracted song name; otherwise return None
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

import re

def extract_location(query):
    # Updated regex pattern to include "shortest distance" variations
    pattern_with_source = r"(find me the (shortest )?distance|get me the (shortest )?distance|find me (shortest )?distance|get me (shortest )?distance|show me the (shortest )?route|find the (shortest )?distance) (?:from|between) (.*?) (?:to|and) (.*)"
    pattern_destination_only = r"(find|get|show) the (shortest )?(distance|route) (?:to|for) (.*)"

    # Check for source and destination in the query
    match_with_source = re.search(pattern_with_source, query, re.IGNORECASE)
    match_destination_only = re.search(pattern_destination_only, query, re.IGNORECASE)

    if match_with_source:
        # Debugging print to check what groups are captured
        print(f"DEBUG: Matched source and destination: {match_with_source.groups()}")
        # Extract source and destination from the query
        source = match_with_source.group(8).strip()
        destination = match_with_source.group(9).strip()
    elif match_destination_only:
        # Debugging print to check what groups are captured
        print(f"DEBUG: Matched destination only: {match_destination_only.groups()}")
        # Extract only the destination, and use 'Your location' as source
        source = "Your location"
        destination = match_destination_only.group(4).strip()
    else:
        # Debugging print to check if no match is found
        print(f"DEBUG: No match found for query: {query}")
        # If no valid pattern is found
        source = None
        destination = None

    return source, destination



