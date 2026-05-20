import boto3
import json
import time
import yfinance as yf

# AWS Kinesis Configuration
kinesis_client = boto3.client(
    'kinesis',
    region_name='ap-south-1'
)

STREAM_NAME = "stock-market-stream"

# Indian NSE Stocks
STOCK_SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "SBIN.NS"
]

# Company Names
COMPANY_NAMES = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "SBIN.NS": "State Bank of India"
}

# Delay Between Streaming Cycles
DELAY_TIME = 30


def get_stock_data(symbol):

    try:

        stock = yf.Ticker(symbol)

        # Fetch last 2 days data
        data = stock.history(period="2d")

        if len(data) < 2:
            raise ValueError(
                f"Insufficient data for {symbol}"
            )

        # Latest Day Values
        latest = data.iloc[-1]

        # Previous Day Values
        previous = data.iloc[-2]

        stock_data = {

            "symbol": symbol,

            "company_name": COMPANY_NAMES.get(
                symbol,
                "Unknown"
            ),

            "market": "NSE",

            "open": float(round(latest["Open"], 2)),

            "high": float(round(latest["High"], 2)),

            "low": float(round(latest["Low"], 2)),

            "price": float(round(latest["Close"], 2)),

            "previous_close": float(
                round(previous["Close"], 2)
            ),

            "change": float(
                round(
                    latest["Close"] - previous["Close"],
                    2
                )
            ),

            "change_percent": float(
                round(
                    (
                        (
                            latest["Close"]
                            - previous["Close"]
                        )
                        / previous["Close"]
                    ) * 100,
                    2
                )
            ),

            "volume": int(latest["Volume"]),

            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime()
            )
        }

        return stock_data

    except Exception as e:

        print(f"Error fetching stock data for {symbol}: {e}")

        return None


def send_to_kinesis():

    while True:

        try:

            print("\nStarting stock streaming cycle...\n")

            for symbol in STOCK_SYMBOLS:

                stock_data = get_stock_data(symbol)

                if stock_data is None:

                    print(
                        f"Skipping {symbol} due to API issue."
                    )

                    continue

                print(f"Sending: {stock_data}")

                # Send Record to Kinesis
                response = kinesis_client.put_record(

                    StreamName=STREAM_NAME,

                    Data=json.dumps(stock_data),

                    PartitionKey=symbol
                )

                # Verify Response
                if (
                    response["ResponseMetadata"][
                        "HTTPStatusCode"
                    ] == 200
                ):

                    print(
                        f"Kinesis success for {symbol}"
                    )

                else:

                    print(
                        f"Kinesis failed for {symbol}: "
                        f"{response}"
                    )

            print(
                f"\nWaiting {DELAY_TIME} seconds...\n"
            )

            time.sleep(DELAY_TIME)

        except Exception as e:

            print(f"Streaming Error: {e}")

            time.sleep(DELAY_TIME)


# Run Producer
send_to_kinesis()