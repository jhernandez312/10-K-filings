from sec_edgar_downloader import Downloader
import os

# Function to download 10-K filings
def download_10k_filings(ticker, start_year, end_year, email):
    # Create an instance of the downloader, passing in the email address
    dl = Downloader(os.path.join(os.getcwd(), "sec_filings"), email)

    # Loop through each year and download the 10-K filing
    for year in range(start_year, end_year + 1):
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")

if __name__ == "__main__":
    # Ask the user for a ticker symbol
    ticker = input("Enter the ticker symbol of the company: ")

    # Request an email address for SEC EDGAR access
    email = input("Enter your email address (required for SEC EDGAR access): ")

    # Define the range of years
    start_year = 1995
    current_year = 2023  # Adjust based on current year or end year of interest

    # Call the function to download filings
    download_10k_filings(ticker, start_year, current_year, email)

    print(f"Completed downloading 10-K filings for {ticker} from {start_year} to {current_year}.")
