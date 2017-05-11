import csv

class DataDistributor(object):

    def __init__(self, csv, include, step=1):
        self.csv = csv
        self.include = include
        self.data = []
        self.step = step
        self.i = 0

    def connect(self):
        with open(self.csv, "r") as data:
            reader = csv.reader(data)
            header = next(reader)
            for field in self.include:
                if field not in header:
                    raise ValueError
            id = 0
            for row in reader:
                record = {field: row[header.index(field)] for field in self.include}
                record.update({"id": id})
                self.data.append(record)
                id += 1

    def step(self, step):
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.data) - self.step + 1:
            i = self.i
            self.i += 1
            return self.data[i:i+self.step]
        else:
            raise StopIteration()

if __name__ == "__main__":
    dd = DataDistributor("data-set-EUR_USD-365-days.csv", ["time", "openBid"], 5)
    dd.connect()
    print(dd.data)


    # for chunk in dd:
    #     print(chunk)
