import rank_bm25


class BM25(rank_bm25.BM25Okapi):
    """BM25Okapi modified to maintain a corpus pool
    """

    RELATIVE_THRESHOLD = 0.8  # A relative duplication threshold compared in the pool
    ABSOLUTE_THRESHOLD = 1.5

    def __init__(
        self,
        pool_size=50,
        corpus=["This is only intended for initialization.".split(" ")],
        tokenizer=None,
        k1=1.5,
        b=0.75,
        epsilon=0.25,
    ):
        self.pool_size = pool_size
        self.is_full = pool_size <= len(corpus)
        self.pool_ptr = 0
        super().__init__(corpus, tokenizer=tokenizer, k1=k1, b=b, epsilon=epsilon)
        # self.corpus = corpus

    def _initialize(self, corpus):
        self.nd = super()._initialize(corpus)
        return self.nd

    def update(self, new_corpus):
        """
        Add an new corpus to the documents pool.
        If it has been full, the oldest one will be replaced.
        """
        num_doc = int(self.avgdl * self.corpus_size)
        if self.is_full:
            # Clean legacy influences
            # old = self.corpus[self.pool_ptr]
            num_doc += len(new_corpus) - self.doc_len[self.pool_ptr]
            self.doc_len[self.pool_ptr] = len(new_corpus)

            frequencies = {}
            for word in new_corpus:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1

            # Clean legacy freqs
            for word, freq in self.doc_freqs[self.pool_ptr].items():
                self.nd[word] -= 1
                if self.nd[word] == 0:
                    del self.nd[word]
            # Update new one
            self.doc_freqs[self.pool_ptr] = frequencies
            for word, freq in frequencies.items():
                if word not in self.nd:
                    self.nd[word] = 0
                self.nd[word] += 1

            self.pool_ptr = (self.pool_ptr + 1) % self.pool_size
        else:
            self.doc_len.append(len(new_corpus))
            num_doc += len(new_corpus)

            frequencies = {}
            for word in new_corpus:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                if word not in self.nd:
                    self.nd[word] = 0
                self.nd[word] += 1

            self.corpus_size += 1
            if self.corpus_size >= self.pool_size:
                self.is_full = True

        self.avgdl = num_doc / self.corpus_size

        self._calc_idf(self.nd)

    def __contains__(self, new_doc: str):
        score = self.get_scores(new_doc.split())
        # print("score:", score.max())
        _sum = max(score.sum(), 0.001)
        normalized_score = score / _sum
        return ((normalized_score.max() >= self.RELATIVE_THRESHOLD).any()) and (score.max() > self.ABSOLUTE_THRESHOLD)


if __name__ == "__main__":
    bm = BM25()
    print(bm.get_scores("workers of the world, rise up!".split(" ")))
    bm.update("Workers of the world, unite!".split(" "))
    bm.update("Hello there good man!".split())
    bm.update("It is quite windy in London".split())
    bm.update("How is the weather today?".split())
    print(bm.get_scores("This is a test".split(" ")))
    print(bm.get_scores("workers of the world, rise up!".split(" ")))
    print(bm.get_scores("windy London".split()))
    print("workers of the world, rise up!" in bm)
