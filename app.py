# app.py

from flask import Flask, render_template, request, Response
from stock_data_fetcher import get_stock_data
from io import BytesIO
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/stockdata', methods=['GET'])
def fetch_stock_data():
    tickerSymbol = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not all([tickerSymbol, start_date, end_date]):
        return "Missing parameters", 400

    try:
        data = get_stock_data(tickerSymbol, start_date, end_date)
        
        # Save DataFrame to in-memory Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Stock Data', index=False)
        
        output.seek(0)
        
        return Response(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment;filename={tickerSymbol}_stock_data.xlsx"}
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
