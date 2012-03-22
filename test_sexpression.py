from sexpression import (
    parse, tosexp, Symbol, String, Quoted, ParenMismatched, LookAheadIterator)
from nose.tools import eq_, raises

data_identity = [
    Symbol('a'),
    String('a'),
    [Symbol('a')],
    [String('a')],
    Quoted(Symbol('a')),
    Quoted(String('a')),
    Quoted([Symbol('a')]),
    Quoted([String('a')]),
    [Symbol('a'), Symbol('b')],
    [Symbol('a'), [Symbol('b')]],
    [Symbol('a'), Quoted([Symbol('b')])],
]


def check_identity(obj):
    eq_(parse(tosexp(obj))[0], obj)


def test_identity():
    for data in data_identity:
        yield (check_identity, data)


@raises(ParenMismatched)
def test_too_many_parentheses():
    parse("(a b))")


@raises(ParenMismatched)
def test_not_enough_parentheses():
    parse("(a (b)")


def test_lookaheaditerator_as_normal():
    for length in [0, 1, 2, 3, 5]:
        lst = range(length)
        yield (eq_, list(iter(lst)), list(LookAheadIterator(lst)))


def test_lookaheaditerator_lookahead():
    laiter = LookAheadIterator(range(3))
    eq_(laiter.lookahead(), 0)
    eq_(laiter.lookahead(), 0)
    eq_(laiter.next(), 0)
    eq_(laiter.lookahead(), 1)
    eq_(laiter.lookahead(), 1)
    eq_(laiter.next(), 1)
    eq_(laiter.lookahead(), 2)
    eq_(laiter.lookahead(), 2)
    eq_(laiter.next(), 2)
    try:
        laiter.next()
        assert False
    except StopIteration:
        assert True
    try:
        laiter.lookahead()
        assert False
    except StopIteration:
        assert True


def test_lookaheaditerator_has_next():
    laiter = LookAheadIterator(range(3))
    assert laiter.has_next() is True
    list(laiter)
    assert laiter.has_next() is False