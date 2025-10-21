from semantic_router.encoders import HuggingFaceEncoder
from semantic_chunkers import StatisticalChunker, CumulativeChunker

encoder = HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2")
stat_chunker = StatisticalChunker(encoder=encoder)

cum_chunker = CumulativeChunker(
    encoder=encoder,
    score_threshold=0.3
)

class TextChunker:
    def __init__(self, method='statistical'):
        if method == 'statistical':
            self.chunker = stat_chunker
        elif method == 'cumulative':
            self.chunker = cum_chunker
        else:
            raise ValueError("Unsupported chunking method. Use 'statistical' or 'cumulative'.")

    def chunk_text(self, text):
        result = self.chunker(docs=[text])
        return [''.join(chunk.splits) for chunk in result[0]]
    