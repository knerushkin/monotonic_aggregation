import matplotlib.pyplot as plt
from pandas_datareader import data as web
import datetime
from shapely.geometry import LineString


def get_max_run(time_series):
    run = [time_series[0]]
    i = 1
    while i < len(time_series) - 1:
        prev = time_series[i - 1]
        current = time_series[i]
        next = time_series[i + 1]
        if prev[1] < current[1] and current[1] > next[1]:
            run.append(time_series[i])
        i += 1
    else:
        run.append(time_series[i])
    return run


def get_min_run(time_series):
    run = [time_series[0]]
    i = 1
    while i < len(time_series) - 1:
        prev = time_series[i - 1]
        current = time_series[i]
        next = time_series[i + 1]
        if prev[1] > current[1] and current[1] < next[1]:
            run.append(time_series[i])
        i += 1
    else:
        run.append(time_series[i])
    return run


def hull_intersection(h1, h2):
    line1 = LineString(h1)
    line2 = LineString(h2)
    return [(point.x, point.y) for point in list(line1.intersection(line2))]


def mark_hull(hull, label):
    return [point for point in [(list(sample))+ [label] for sample in hull]]

if __name__ == "__main__":
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2016, 1, 27)
    df = web.DataReader("GOOGL", 'yahoo', start, end)
    print(df)
    google_high_bid = list(df["High"])
    ts = sorted({i: google_high_bid[i] for i in range(len(google_high_bid[400:893]))}.items())

    #Calculation
    maximal_run = get_max_run(ts)
    minimal_run = get_min_run(ts)

    second_order_maximal_run = get_max_run(maximal_run)
    second_order_minimal_run = get_min_run(minimal_run)

    third_order_maximal_run = get_max_run(second_order_maximal_run)
    third_order_minimal_run = get_min_run(second_order_minimal_run)

    fourth_order_maximal_run = get_max_run(third_order_maximal_run)
    fourth_order_minimal_run = get_min_run(third_order_minimal_run)

    fifth_order_maximal_run = get_max_run(fourth_order_maximal_run)
    fifth_order_minimal_run = get_min_run(fourth_order_minimal_run)

    intersection1 = hull_intersection(maximal_run, third_order_minimal_run)
    print(intersection1)

    intersection2 = hull_intersection(minimal_run, third_order_minimal_run)
    print(intersection2)

    #Plotting
    plt.plot(list([k[0] for k in ts]), list([k[1] for k in ts]), "black", linewidth=1.5)

    plt.plot(list([k[0] for k in maximal_run]), list([k[1] for k in maximal_run]), "g--")
    plt.plot(list([k[0] for k in minimal_run]), list([k[1] for k in minimal_run]), "g--")
    #
    plt.plot(list([k[0] for k in second_order_maximal_run]), list([k[1] for k in second_order_maximal_run]), "r--")
    plt.plot(list([k[0] for k in second_order_minimal_run]), list([k[1] for k in second_order_minimal_run]), "r--")

    plt.plot(list([k[0] for k in third_order_maximal_run]), list([k[1] for k in third_order_maximal_run]), "y--")
    plt.plot(list([k[0] for k in third_order_minimal_run]), list([k[1] for k in third_order_minimal_run]), "y--")

    plt.plot(list([k[0] for k in fourth_order_maximal_run]), list([k[1] for k in fourth_order_maximal_run]), "m--")
    plt.plot(list([k[0] for k in fourth_order_minimal_run]), list([k[1] for k in fourth_order_minimal_run]), "m--")

    plt.plot(list([k[0] for k in fifth_order_maximal_run]), list([k[1] for k in fifth_order_maximal_run]), "b--")
    plt.plot(list([k[0] for k in fifth_order_minimal_run]), list([k[1] for k in fifth_order_minimal_run]), "b--")

    plt.plot(list([k[0] for k in intersection1]), list([k[1] for k in intersection1]), "ro", linewidth=5)
    plt.plot(list([k[0] for k in intersection2]), list([k[1] for k in intersection2]), "yo", linewidth=5)

    plt.show()