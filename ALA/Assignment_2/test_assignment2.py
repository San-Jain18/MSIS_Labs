import numpy as np

from main import (
    TAGS,
    Vector,
    preprocess_text,
    build_tag_matrix,
    build_text_matrix,
    similarity_matrix_vector_class,
    similarity_matrix_numpy,
    rank_tags
)


# Sample embedding model for testing
class SampleModel:

    def __init__(self):
        self.key_to_index = {}
        self.word_vectors = {}

        words = set()

        for tag in TAGS:
            for word in tag.lower().split():
                words.add(word)

        words.update(["manipal", "learning", "digital"])

        for i, word in enumerate(sorted(words)):
            vector = np.zeros(50)
            vector[i % 50] = 1.0
            vector[(i + 1) % 50] = 0.5

            self.key_to_index[word] = i
            self.word_vectors[word] = vector

    def __getitem__(self, word):
        return self.word_vectors[word]


# Function to display test results
def check(condition, message):

    if condition:
        print("PASS:", message)
    else:
        print("FAIL:", message)
        raise AssertionError(message)


# Create sample model
model = SampleModel()


# TEST 1: Check tag matrix dimensions
tag_names, T = build_tag_matrix(model, TAGS)

check(
    T.shape == (20, 50),
    "Tag matrix shape is (20, 50)"
)


# TEST 2: Check text matrix dimensions
sample_text = [
    "manipal",
    "research",
    "learning",
    "unknownword"
]

in_vocab, oov, W = build_text_matrix(
    model, sample_text
)

check(
    W.shape == (len(in_vocab), 50),
    "Text matrix shape is (n, 50)"
)


# TEST 3: Check similarity matrix dimensions
S_vector = similarity_matrix_vector_class(W, T)

S_numpy = similarity_matrix_numpy(W, T)

check(
    S_numpy.shape == (len(in_vocab), 20),
    "Similarity matrix shape is (n, 20)"
)


# TEST 4: Compare one cosine similarity
word_index = in_vocab.index("research")

tag_index = tag_names.index("research")

value_vector = Vector(
    W[word_index]
).cosine_similarity(
    Vector(T[tag_index])
)

value_numpy = S_numpy[word_index, tag_index]

check(
    abs(value_vector - value_numpy) < 1e-8,
    "Vector cosine similarity matches NumPy"
)


# TEST 5: Compare complete similarity matrices
check(
    np.allclose(
        S_vector,
        S_numpy,
        rtol=1e-5,
        atol=1e-8
    ),
    "Vector and NumPy similarity matrices are equal"
)

print(
    "Maximum difference:",
    np.max(np.abs(S_vector - S_numpy))
)


# TEST 6: Check out-of-vocabulary words
check(
    "unknownword" in oov,
    "Out-of-vocabulary word is reported"
)

check(
    "unknownword" not in in_vocab,
    "Out-of-vocabulary word is excluded from W"
)


# TEST 7: Check invalid tag vocabulary
invalid_tags = list(TAGS)

invalid_tags[0] = "notaword"

try:
    build_tag_matrix(model, invalid_tags)

    check(
        False,
        "Invalid tag vocabulary raises an error"
    )

except ValueError:
    check(
        True,
        "Invalid tag vocabulary raises an error"
    )


# TEST 8: Check repeated words
repeated_tokens, repeated_oov, repeated_W = build_text_matrix(
    model,
    ["research", "research", "manipal"]
)

check(
    repeated_tokens == [
        "research", "research", "manipal"
    ] and repeated_W.shape == (3, 50),
    "Repeated words are retained"
)


# TEST 9: Check text preprocessing
before, after = preprocess_text(
    "The research is in AI and learning."
)

check(
    after == ["research", "learning"],
    "Preprocessing removes stopwords and short words"
)


# EXTRA TEST 10: Check tag ranking
ranking = rank_tags(
    tag_names,
    S_numpy,
    in_vocab
)

scores = [item[1] for item in ranking]

check(
    len(ranking) == 20
    and scores == sorted(scores, reverse=True),
    "Tag ranking returns 20 tags in descending order"
)


print("All testing checks passed successfully!")