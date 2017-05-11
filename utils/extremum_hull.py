class ExtremumHull(object):

    def __init__(self, series, order=0):
        self.series = series
        self.decompose()
        self.order = order

    def decompose(self):
        pass

    def get_band(self):
        band = self.series
        i = 1
        while i < len(self.series) - 1:
            prev = self.series[i - 1]
            current = self.series[i]
            next = self.series[i + 1]
            if prev[1] < current[1] and current[1] > next[1]:
                band.concat(self.series[i])
            i += 1
        else:
            band.concat(self.series[i])
        return {"order": self.order, "band": band}
