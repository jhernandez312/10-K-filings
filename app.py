from flask import Flask, render_template, request, redirect, url_for, flash
from sec_edgar_downloader import Downloader
import os
from project.llm import get_summary
from project.data_processing import run

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a real secret key in production

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None  # Initialize summary as None at every request
    if request.method == 'POST':
        ticker = request.form['ticker']
        email = request.form['email']
        action = request.form.get('action', 'download')  # Default to 'download' if not specified

        if action == 'download':
            try:
                download_10k_filings(ticker, 1995, 2023, email)
                flash(f'Successfully downloaded 10-K filings for {ticker} from 1995 to 2023.')
            except Exception as e:
                flash(str(e))
        elif action == 'analyze':
            try:
                run(ticker)  # Assuming you process and save data first
                print(ticker)
                summary = get_summary()  # Ensure get_summary is defined to handle analysis properly
                #flash(summary)
                print(summary)
            except Exception as e:
                flash(str(e))
 # Render the same page, which will now include any messages or summaries in the context
    return render_template('index.html', summary=summary)

def download_10k_filings(ticker, start_year, end_year, email):
    dl = Downloader(os.path.join(os.getcwd(), "sec_filings"), email)
    for year in range(start_year, end_year + 1):
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")

if __name__ == '__main__':
    app.run(debug=True)
