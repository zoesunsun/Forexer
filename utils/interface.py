import typing

class News(typing.NamedTuple):
    """News message format
    """

    title: str
    message: str
    url: str
    timestamp: int
    sentiment: float = 0

class FxRate(typing.NamedTuple):
    """Foreign exchange rate format
    """

    currencyPair: str
    timestamp: int
    bidBig: float
    bidPips: float
    offerBig: str
    offerPips: str
    high: float
    low: float
    Open: float

if __name__ == "__main__":
    t = News("For test", "test content", "http or something", 123456)
    print(t, t.message, t.timestamp)
