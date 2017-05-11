from pyoanda import Client, PRACTICE
from pyoanda.exceptions import BadRequest
from datetime import datetime, timedelta

client = Client(
    PRACTICE,
    account_id="2015316",
    access_token="d2165c62b827b4ecc7c8d6e902cffc00-b65a089471813642049226e1ec9fc935"
)

INSTRUMENT = "EUR_USD"
DAYS = 365
end = datetime.now()
import csv
with open('data-set-{}-{}-days.csv'.format(INSTRUMENT, DAYS),'w') as f:
    fields = ['time', 'lowBid', 'closeBid', 'openAsk', 'closeAsk', 'complete', 'openBid', 'highAsk', 'lowAsk','highBid', 'volume']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for _ in range(DAYS):
        f.flush()
        for _ in range(2):  # 24/12 hours
            start = end - timedelta(hours=12)
            kwargs = dict(
                instrument=INSTRUMENT,
                candle_format="bidask",
                granularity="S5",
                count=None,
                start=start.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                end=end.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            )
            try:
                rows = client.get_instrument_history(**kwargs)["candles"]
                writer.writerows(rows)
            except BadRequest:
                pass
            end = start
