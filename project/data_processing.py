from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import json



#filepath = "sec-edgar-filings\\GE\\10-K\\0001193125-11-047479\\full-submission.txt"  # Ensure this path is correct


def read_file(filepath):
    """ Reads the entire file content, handling files with null bytes. """
    if not os.path.exists(filepath):
        print("File does not exist:", filepath)
        return None
    try:
        with open(filepath, 'rb') as file:  # Open as binary to handle potential null bytes.
            content = file.read()
            content = content.replace(b'\x00', b'')  # Remove null bytes.
        return content.decode('utf-8', errors='ignore')  # Decode ignoring errors after cleaning.
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


def process(filepath):
    raw_10k = read_file(filepath)
    if raw_10k is None:
        print(f"No data to process in {filepath}")
        return None

    # Initialize regular expressions
    doc_start_pattern = re.compile(r'<DOCUMENT>')
    doc_end_pattern = re.compile(r'</DOCUMENT>')
    type_pattern = re.compile(r'<TYPE>[^\n]+')

    # Find document sections
    starts = [match.end() for match in doc_start_pattern.finditer(raw_10k)]
    ends = [match.start() for match in doc_end_pattern.finditer(raw_10k)]
    types = [match.group()[len('<TYPE>'):] for match in type_pattern.finditer(raw_10k)]

    document = {}
    for dtype, start, end in zip(types, starts, ends):
        if '10-K' in dtype:
            document[dtype] = raw_10k[start:end]

    if '10-K' not in document:
        print("No 10-K document found in file.")
        return None

    # Extract items using regex
    regex = re.compile(r'(>Item\s*(?:<[^>]+>)*\s*(1A|1B|7A|7|8)\.{0,1})|(ITEM\s*(?:<[^>]+>)*\s*(1A|1B|7A|7|8))', re.IGNORECASE)
    matches = regex.finditer(document['10-K'])
    #if not matches:
    #    print("No matches found for specified items.")
    #    return None

    # Create DataFrame from matches
    for match in matches:
        print(match)
    matches = regex.finditer(document['10-K'])


    match_list = [(match.group(), match.start(), match.end()) for match in matches]
    if match_list:
        test_df = pd.DataFrame(match_list, columns=['item', 'start', 'end'])
    else:
        print("No data to populate DataFrame.")
        return None

    test_df.columns = ['item', 'start', 'end']
    test_df['item'] = test_df.item.str.lower()
    test_df.replace({'&#160;': ' ', '&nbsp;': ' ', ' ': '', '\\.': '', '>': ''}, regex=True, inplace=True)

    # Drop duplicates and set DataFrame index
    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
    pos_dat.set_index('item', inplace=True)

    if not 'item7a' in pos_dat.index:
        print(f"'Item 7a' not found in {filepath}")
        return None


    if 'item7' in pos_dat.index:
            item_1a_raw = document['10-K'][pos_dat.loc['item7', 'start']:pos_dat.loc['item7a', 'end']]
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml').get_text("\n\n", strip=True)

            words_to_skip = 430  # Number of words to skip
            item_1a_content = ' '.join(item_1a_content.split()[words_to_skip:])  # Skip first 'n' words
            return item_1a_content

    else:
            print(f"'Item 7' not found in {filepath}")
            return None

    # Extract and return content for a specific item, checking for existence
    # Get Item 1a
    item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]

    # Get Item 7
    item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

    # Get Item 7a
    item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]




# Assuming 'item_1a_raw', 'item_7_raw', and 'item_7a_raw' contain the raw HTML contents of the respective sections
def get_text_content(html_content, limit=1000):
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text("\n\n", strip=True)
    return text[:limit] if limit else text

# Let's assume you want to limit the text to the first 1000 characters per item
"""
sec_data = {
    'Item 1A': process("sec-edgar-filings\\AMZN\\10-K\\0000891020-00-000622\\full-submission.txt")
}


# Save to JSON
json_filepath = 'sec_data.json'
with open(json_filepath, 'w', encoding='utf-8') as f:
    json.dump(sec_data, f, ensure_ascii=False, indent=4)

print(f"Data truncated and saved to {json_filepath}")

"""
results = {}
def process_directory(root_directory, results):
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            if filename == 'full-submission.txt':  # Match the target file name
                filepath = os.path.join(root, filename)
                print(f"Processing file: {filepath}")  # Debug: Which file is being processed
                processed = process(filepath)
                if processed is not None:
                    next_p = get_text_content(processed)
                    results[f'{filepath}'] = next_p
                else:
                    print(f"No valid data to process for file: {filepath}")

    return results
"""
# Define the root directory of your 10-K filings
root_directory = 'sec-edgar-filings\\0000320193\\10-K'
results = process_directory(root_directory, results)
json_filepath = 'sec_data.json'
with open(json_filepath, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"Data truncated and saved to {json_filepath}")

"""
def run(ticker):

    first = "sec-edgar-filings/"
    last = "/10-K"
    root_directory = first + ticker + last
    print(root_directory)
    results = {}
    #root_directory = 'sec-edgar-filings\\0000320193\\10-K'
    resultss = process_directory(root_directory, results)
    json_filepath = 'sec_data.json'
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(resultss, f, ensure_ascii=False, indent=4)

    print(f"Data truncated and saved to {json_filepath}")

