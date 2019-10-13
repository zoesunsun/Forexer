import socketio
import multiprocessing
import time

from .utils import interface


class FxRateCrawler(multiprocessing.Process):
    """An crawler to get real-time forex rate
    """

    name = "FxRateCrawler" # Process name
    daemon = True # Daemon process flag

    URI = "wss://fx.now.sh"

    def __init__(self, queue: multiprocessing.Queue, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue

    def run(self):
        sio = socketio.Client()
        
        @sio.event
        def data(d):
            for record in d:
                self.queue.put(interface.FxRate(
                    currencyPair=record["currencyPair"],
                    timestamp=int(record["timestamp"])//1000,
                    bidBig=float(record["bidBig"]),
                    bidPips=float(record["bidPips"]),
                    offerBig=record["offerBig"],
                    offerPips=record["offerPips"],
                    high=float(record["high"]),
                    low=float(record["low"]),
                    Open=float(record["open"])
                ))
        
        sio.connect(self.URI)
