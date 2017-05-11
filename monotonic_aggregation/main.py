from utils import data_read
import matplotlib.pyplot as plt
import dateutil.parser
from shapely.geometry import LineString
import json


def hull_intersection(h1, h2):
    """ Get all intersection points
        :parameter h1 Hull path
        :parameter h2 Hull path
        :returns [(x0,y0), ..., (xn, yn)] Array of intersection points
    """
    line1 = LineString(h1)
    line2 = LineString(h2)
    intersection = line1.intersection(line2)
    # Considerate only point of intersection, in case of identical paths - ignore it.
    if intersection.__class__.__name__ == "MultiPoint":
        intersection = list(intersection)
    else:
        return []
    # Normalize result value to return array of tuples.
    return [(point.x, point.y) for point in intersection]


def get_hull(series, key, name, depth=1):
    """ Build hulls structure for given series
        :parameter series Series to build hull structure on
        :parameter key  Key to create runs on
        :parameter depth Indicate depth of recursion
        :returns [
                    {
                        "name": "min",
                        "depth": n,
                        "value": [(x0, y0), ..., (xn, yn)]
                        "next": [
                                    {
                                        "name": "min",
                                        "depth": n+1,
                                        "value": [(x0, y0), ..., (xn, yn)]
                                        "next": ...
                                    },
                                    {
                                        "name": "max",
                                        "depth": n+1,
                                        "value": [(x0, y0), ..., (xn, yn)]
                                        "next": ...
                                    }
                                ]
                    },
                    {
                        "name": "max",
                        "depth": n,
                        "value": [(x0, y0), ..., (xn, yn)]
                        "next": ...
                    }
                ]
    """
    if len(series) > 3:
        minh = min_band(series, key)
        maxh = max_band(series, key)
        nameComposition = {
            "min": name + "-min",
            "max": name + "-max"
        }
        return [
            {"name": nameComposition["min"], "children": get_hull(minh, key, nameComposition["min"], depth+1), "value": minh, "depth": depth},
            {"name": nameComposition["max"], "children": get_hull(maxh, key, nameComposition["max"], depth+1), "value": maxh, "depth": depth},
        ]
    else:
        return None

#TODO: After tree has been flatted, structure of tree has been lost(depth: {min, max})
def flat_tree(tree):
    """ To change hull tree structure on flatten one
        :parameter tree Tree to be flatten
        :return [
                    {
                        "name": "max",
                        "value": [
                            {
                                "openBid": "1.05991",
                                "id": 0,
                                "time": "2017-01-16T20:40:50.000000Z"
                            },
                            {
                                "openBid": "1.06029",
                                "id": 93,
                                "time": "2017-01-16T21:02:30.000000Z"
                            },
                            {
                                "openBid": "1.05999",
                                "id": 99,
                                "time": "2017-01-16T21:03:05.000000Z"
                            }
                        ],
                        "depth": 4
                    },
                    {},
                    ...
                ]
    """
    flat = []
    if tree:
        for branch in tree:
            flat.append({"depth": branch["depth"], "value": branch["value"], "name": branch["name"]})
            if branch["children"]:
                flat.extend(flat_tree(branch["next"]))
    return flat


def max_band(series, key):
    run = [series[0]]
    i = 1
    while i < len(series) - 1:
        prev = series[i - 1]
        current = series[i]
        next = series[i + 1]
        if prev[key] < current[key] and current[key] >= next[key]:
            run.append(series[i])
        i += 1
    else:
        run.append(series[i])
    return run


def min_band(series, key):
    run = [series[0]]
    i = 1
    while i < len(series) - 1:
        prev = series[i - 1]
        current = series[i]
        next = series[i + 1]
        if prev[key] > current[key] and current[key] <= next[key]:
            run.append(series[i])
        i += 1
    else:
        run.append(series[i])
    return run


if __name__ == "__main__":
    colors = {
        1: "g",
        2: "r",
        3: "c",
        4: "m",
        5: "b",
        6: "y",
        7: "k",
    }
    include = ["time", "openBid"]
    dd = data_read.DataDistributor("../utils/data-set-EUR_USD-365-days.csv", ["time", "openBid"], 5)
    dd.connect()
    data = dd.data[900:1000]

    hull = get_hull(data, include[1])
    flat_hull = flat_tree(hull)
    flat_hull_remain = flat_hull[:]

    max_run = max_band(data, include[1])
    min_run = min_band(data, include[1])
    #
    plt.xticks([k["id"] for k in data], [dateutil.parser.parse(k[include[0]]) for k in data], rotation='vertical')
    plt.locator_params(axis='x',nbins=25)
    #
    plt.plot([k["id"] for k in data], [k[include[1]] for k in data], "black", linewidth=1.5)

    for component in flat_hull:
        flat_hull_remain.remove(component)
        current = component["value"]
        color = colors[component["depth"]] + "--"
        plt.plot([k["id"] for k in current], [k[include[1]] for k in current], color)
        for component_remain in flat_hull_remain:
            current_remain = component_remain["value"]
            intersection1 = hull_intersection([(record["id"], float(record[include[1]])) for record in current], [(record["id"], float(record[include[1]])) for record in current_remain])
            color_point = colors[component["depth"]] + "o"
            plt.plot([k[0] for k in intersection1], [k[1] for k in intersection1], color_point, linewidth=5)

    plt.show()