import multiprocessing

from ..utils import interface


class ExampleCrawler(multiprocessing.Process):
    """An example crawler as a process
    """

    name = "ExampleCrawler" # Process name
    daemon = True # Daemon process flag

    def __init__(self, queue: multiprocessing.Queue, **kwargs):
        super().__init__()
        self.queue = queue

    def run(self):
        # Here we write some crawler code.
        # It should be in an infinite loop.
        while True:
            # request
            res = "some data"
            # parse
            results = ["newsdata1", "newsdata2"]
            # send
            for v in results:
                self.queue.put(interface.News(message="DFP just released another assignment.", title=v, url="https://www.cmu.edu", timestamp=1569046230))


if __name__ == "__main__":
    q = multiprocessing.Queue()
    p = ExampleCrawler(q)
    p.start()
    print(q.get())
    print(q.get())
