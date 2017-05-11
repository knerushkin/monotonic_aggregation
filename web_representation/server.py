import flask
from monotonic_aggregation.main import *

APP = {"data": None}

app = flask.Flask(__name__)


@app.route('/aggregation/monotonic')
def selection():
    return flask.render_template('monotonic_aggregation.html')


@app.route('/data/forex/eur_usd/')
def data():
    d = data_read.DataDistributor("../utils/data-set-EUR_USD-365-days.csv", ["time", "openBid"], 5)
    d.connect()
    APP["data"] = d.data[0:10000]
    # reversing data order
    for sample in APP['data']:
        sample['id'] = len(APP['data']) - sample['id'] - 1
    APP['data'] = sorted(APP['data'], key=lambda el: el['id'])

    print(APP["data"])
    return json.dumps(APP["data"])

@app.route('/data/forex/eur_usd/<chunk>')
def get_chunked_data(chunk):
    start, end = chunk.split('-')
    return json.dumps(get_hull(APP["data"][int(start): int(end)], "openBid", "root"))

@app.route('/data/forex/eur_usd/instersection/<chunk>')
def get_hull_intersection(chunk):
    # start1, end1 = chunk1.split('-')
    # start2, end2 = chunk2.split('-')
    # hull1 = get_hull(APP["data"][int(start1): int(end1)], "openBid", "root")
    # hull2 = get_hull(APP["data"][int(start2): int(end2)], "openBid", "root")
    print(chunk)
    print(json.loads(chunk))
    chunk = json.loads(chunk)
    print(len(chunk))
    intersection = hull_intersection(chunk[0], chunk[1])
    print(intersection)
    return json.dumps(intersection)


if __name__ == '__main__':
    app.run(debug=True)
