import numpy as np
import pytest

from lab2 import (TAGS, Vector, build_tag_matrix, build_text_matrix,
                  preprocess, rank_tags, similarity_matrix_numpy,
                  similarity_matrix_vector_class)


class FakeModel:
    def __init__(self, words, seed=0):
        rng = np.random.default_rng(seed)
        self.key_to_index = {w: i for i, w in enumerate(words)}
        self.vecs = rng.normal(size=(len(words), 50))

    def __getitem__(self, w):
        return self.vecs[self.key_to_index[w]]


WORDS = TAGS + ["manipal", "students", "labs", "digital", "learning"]
TEXT = "Manipal students love research, research labs and zzzqx digital learning!"


@pytest.fixture
def setup():
    model = FakeModel(WORDS)
    names, T = build_tag_matrix(model, TAGS)
    _, tokens = preprocess(TEXT)
    in_vocab, oov, W = build_text_matrix(model, tokens)
    return model, names, T, in_vocab, oov, W


def test_tag_shape(setup):
    assert setup[2].shape == (20, 50)


def test_text_shape(setup):
    _, _, _, in_vocab, _, W = setup
    assert W.shape == (len(in_vocab), 50)


def test_similarity_shape(setup):
    _, _, T, in_vocab, _, W = setup
    assert similarity_matrix_numpy(W, T).shape == (len(in_vocab), 20)
    assert similarity_matrix_vector_class(W, T).shape == (len(in_vocab), 20)


def test_pair_agreement(setup):
    _, _, T, _, _, W = setup
    S = similarity_matrix_numpy(W, T)
    assert Vector(W[0]).cosine_similarity(Vector(T[3])) == pytest.approx(S[0, 3])


def test_allclose(setup):
    _, _, T, _, _, W = setup
    assert np.allclose(similarity_matrix_vector_class(W, T), similarity_matrix_numpy(W, T))


def test_oov_excluded(setup):
    _, _, _, in_vocab, oov, W = setup
    assert "zzzqx" in oov
    assert "zzzqx" not in in_vocab
    assert W.shape[0] == len(in_vocab)


def test_repetitions_preserved(setup):
    _, _, _, in_vocab, _, _ = setup
    assert in_vocab.count("research") == 2


def test_tag_oov_raises():
    model = FakeModel(WORDS)
    with pytest.raises(ValueError):
        build_tag_matrix(model, TAGS[:-1] + ["notinvocab"])


def test_multiword_tag_mean():
    model = FakeModel(WORDS)
    _, T = build_tag_matrix(model, ["research campus"])
    assert np.allclose(T[0], (model["research"] + model["campus"]) / 2)


def test_rank_tags(setup):
    _, names, T, in_vocab, _, W = setup
    S = similarity_matrix_numpy(W, T)
    ranked = rank_tags(names, S, in_vocab)
    assert len(ranked) == 20
    assert ranked[0][1] >= ranked[-1][1]
    assert ranked[0][1] == pytest.approx(1.0)
