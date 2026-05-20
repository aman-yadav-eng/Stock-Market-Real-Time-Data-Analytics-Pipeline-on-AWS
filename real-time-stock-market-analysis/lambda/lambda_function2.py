import boto3
import json
import decimal
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

# AWS Clients
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# DynamoDB Table Name and SNS ARN
TABLE_NAME = "stock-market-data"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:672726205278:Stock_Trend_Alerts"

# Company Name Mapping
COMPANY_NAMES = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "SBIN.NS": "State Bank of India"
}

# Multi-Stock Support
STOCK_SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "SBIN.NS"
]


def get_recent_stock_data(symbol, minutes=5):
    """
    Fetch recent stock data from DynamoDB
    """

    table = dynamodb.Table(TABLE_NAME)

    now = datetime.utcnow()
    past_time = now - timedelta(minutes=minutes)

    try:

        response = table.query(
            KeyConditionExpression=
                Key("symbol").eq(symbol) &
                Key("timestamp").gte(
                    past_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                ),

            ScanIndexForward=True
        )

        return sorted(
            response.get("Items", []),
            key=lambda x: x["timestamp"]
        )

    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return []


def calculate_moving_average(data, period):
    """
    Calculate moving average
    """

    if len(data) < period:
        return decimal.Decimal("0")

    return sum(
        decimal.Decimal(str(d["price"]))
        for d in data[-period:]
    ) / period


def lambda_handler(event, context):

    print("Starting trend analysis...")

    for symbol in STOCK_SYMBOLS:

        print(f"Checking stock: {symbol}")

        stock_data = get_recent_stock_data(symbol)

        # Reduce requirement for easier testing
        if len(stock_data) < 10:
            print(f"Not enough data for {symbol}")
            continue

        # Current Moving Averages
        sma_5 = calculate_moving_average(stock_data, 5)
        sma_20 = calculate_moving_average(stock_data, 10)

        # Previous Moving Averages
        sma_5_prev = calculate_moving_average(stock_data[:-1], 5)
        sma_20_prev = calculate_moving_average(stock_data[:-1], 10)

        message = None

        # Detect Uptrend
        if sma_5_prev < sma_20_prev and sma_5 > sma_20:

            message = (
                f"{COMPANY_NAMES.get(symbol, symbol)} "
                f"({symbol}) is in an UPTREND.\n\n"
                f"SMA 5 crossed above SMA 10.\n"
                f"Possible BUY signal."
            )

        # Detect Downtrend
        elif sma_5_prev > sma_20_prev and sma_5 < sma_20:

            message = (
                f"{COMPANY_NAMES.get(symbol, symbol)} "
                f"({symbol}) is in a DOWNTREND.\n\n"
                f"SMA 5 crossed below SMA 10.\n"
                f"Possible SELL signal."
            )

        # Publish SNS Alert
        if message:

            print(f"Publishing alert for {symbol}")

            try:

                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject=f"Stock Trend Alert - {symbol}"
                )

                print(f"SNS alert sent for {symbol}")

            except Exception as e:
                print(f"Failed to publish SNS message for {symbol}: {e}")

        else:
            print(f"No trend change detected for {symbol}")

    return {
        "statusCode": 200,
        "body": json.dumps("Trend analysis complete")
    }