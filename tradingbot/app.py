from flask import Flask, render_template, request
from stock_analysis import fetch_and_analyze, get_news

app = Flask(__name__)

def is_valid_symbol(symbol):
    return symbol.isalpha() and symbol.isalnum()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    symbol = request.form.get('symbol')

    if not is_valid_symbol(symbol):
        return render_template('error.html', message="Invalid stock symbol")

    try:
        results = fetch_and_analyze(symbol)
        news = get_news(symbol)

        if results is None:
            return render_template('error.html', message="Error during analysis")

        return render_template('results.html', symbol=symbol, results=results, news=news)
    except Exception as e:
        return render_template('error.html', message=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
