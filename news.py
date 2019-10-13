import multiprocessing
import textblob
import sys

from .utils import interface
from .utils import bm25
from .crawlers import dailyfx, investing, Reuters


class NewsProcess(multiprocessing.Process):
    """News data processing process
    """

    DUPLICATION_THRESHOLD = 0.95

    SOURCES = [dailyfx.get_content, investing.get_content, Reuters.get_content]

    def __init__(self, queue: multiprocessing.Queue, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue
        self.news_pool = bm25.BM25(100)

    def run(self):
        while 1:
            for source in self.SOURCES:
                data = source()
                for news in data:
                    if news.title not in self.news_pool:
                        tb = textblob.TextBlob(news.title)

                        self.queue.put(interface.News(sentiment=tb.sentiment.polarity, title=news.title, message=news.message, url=news.url, timestamp=news.timestamp))
                        self.news_pool.update(news.title.split())

if __name__ == "__main__":
    q = multiprocessing.Queue()
    test = NewsProcess(q)
    test.start()
