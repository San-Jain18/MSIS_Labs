import math
import re
import string
import sys

import numpy as np

TAGS = [
    "research", "innovation", "education", "university", "students",
    "faculty", "campus", "engineering", "medicine", "technology",
    "curriculum", "collaboration", "publication", "laboratory", "scholarship",
    "mentorship", "internship", "entrepreneurship", "accreditation", "alumni",
]

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are",
    "was", "were", "with", "at", "by", "from",
    "it", "its", "this", "that", "these", "those", "our", "we", "us", "you",
    "your", "they", "their", "them", "he", "she", "his", "her", "i", "my",
    "be", "been", "has", "have", "had", "will", "can", "as", "but", "not",
    "all", "also", "who", "which", "what", "more", "than", "into", "about",
}


class Vector:
    def __init__(self, data):
        self.data = tuple(float(x) for x in data)

    def dot(self, other):
        return sum(a * b for a, b in zip(self.data, other.data))

    def norm(self):
        return math.sqrt(self.dot(self))

    def cosine_similarity(self, other):
        n1, n2 = self.norm(), other.norm()
        if n1 == 0 or n2 == 0:
            raise ValueError("Cosine similarity undefined for zero vector")
        return self.dot(other) / (n1 * n2)


def build_tag_matrix(model, tags):
    rows = []
    for tag in tags:
        words = tag.split()
        for w in words:
            if w not in model.key_to_index:
                raise ValueError(f"Tag word not in vocabulary: {w!r} (tag {tag!r})")
        rows.append(np.mean([model[w] for w in words], axis=0))
    return list(tags), np.array(rows)


def preprocess(text):
    raw_count = len(text.split())
    text = text.lower()
    text = re.sub("[" + re.escape(string.punctuation) + "]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [t for t in tokens if len(t) > 2]
    return raw_count, tokens


def build_text_matrix(model, tokens):
    in_vocab, oov = [], []
    for t in tokens:
        (in_vocab if t in model.key_to_index else oov).append(t)
    W = np.array([model[t] for t in in_vocab]) if in_vocab else np.empty((0, 50))
    return in_vocab, oov, W


def similarity_matrix_vector_class(W, T):
    return np.array([
        [Vector(w).cosine_similarity(Vector(t)) for t in T] for w in W
    ])


def similarity_matrix_numpy(W, T):
    W_norm = np.linalg.norm(W, axis=1, keepdims=True)
    T_norm = np.linalg.norm(T, axis=1, keepdims=True)
    if np.any(W_norm == 0) or np.any(T_norm == 0):
        raise ValueError("Zero-norm row encountered")
    return (W / W_norm) @ (T / T_norm).T


def rank_tags(tag_names, S, in_vocab_tokens):
    best_idx = S.argmax(axis=0)
    scores = S.max(axis=0)
    order = np.argsort(-scores)
    return [(tag_names[j], float(scores[j]), in_vocab_tokens[best_idx[j]]) for j in order]


def main(path, model=None):
    if model is None:
        import gensim.downloader as api
        model = api.load("glove-wiki-gigaword-50")

    with open(path, encoding="utf-8") as f:
        text = f.read()

    raw_count, tokens = preprocess(text)
    tag_names, T = build_tag_matrix(model, TAGS)
    in_vocab, oov, W = build_text_matrix(model, tokens)

    print(f"Tokens before preprocessing : {raw_count}")
    print(f"Tokens after preprocessing  : {len(tokens)}")
    print(f"In-vocabulary tokens        : {len(in_vocab)}")
    print(f"Out-of-vocabulary tokens    : {len(oov)}")
    print(f"Distinct OOV tokens         : {sorted(set(oov))}")

    if len(in_vocab) == 0:
        sys.exit("Error: no in-vocabulary tokens; cannot compute similarities.")

    print("T.shape:", T.shape)
    print("W.shape:", W.shape)

    S_vector = similarity_matrix_vector_class(W, T)
    S_numpy = similarity_matrix_numpy(W, T)

    print("np.allclose:", np.allclose(S_vector, S_numpy, atol=1e-8))
    print("Max abs difference:", np.max(np.abs(S_vector - S_numpy)))

    ranked = rank_tags(tag_names, S_numpy, in_vocab)[:8]
    print(f"\n{'Rank':<6}{'Tag':<20}{'Score':<9}{'Best-matching word':<22}Match")
    print("-" * 70)
    for r, (tag, score, word) in enumerate(ranked, 1):
        kind = "identical" if word == tag else "different"
        print(f"{r:<6}{tag:<20}{score:<9.4f}{word:<22}{kind}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "manipal_linkedin.txt")
