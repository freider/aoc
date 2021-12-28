import numbers
import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""

    src = aoc_input()
    expr = pp.Forward()

    num = pp.Word(pp.nums).set_parse_action(lambda s: int(s[0]))
    ops = pp.one_of("+ *")

    subexpr = pp.Literal("(") + expr + pp.Literal(")")
    term = subexpr | num
    expr << term + pp.ZeroOrMore(ops + term)


    def apply(op, a, b):
        if op == '+':
            return a + b
        else:
            return a * b
    s = 0
    for l in lines(src):
        result = expr.parseString(l)
        stack = [0, '+']
        for term in result:
            if isinstance(term, numbers.Number):
                *stack, a, op = stack
                stack.append(apply(op, a, term))
            elif term == '(':
                stack += [0, '+']
            elif term == ')':
                *stack, a, op, b = stack
                stack.append(apply(op, a, b))
            elif term in "+*":
                stack.append(term)
            else:
                assert False

        assert len(stack) == 1
        s += stack[0]

    print(s)

def part2():
    src = """1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

    src = aoc_input()
    expr = pp.Forward()
    base_expr = pp.Word(pp.nums).set_parse_action(lambda s: int(s[0]))
    lpar = pp.Literal("(").suppress()
    rpar = pp.Literal(")").suppress()

    term = base_expr | pp.Group(lpar + expr + rpar).set_results_name('pargroup').set_parse_action(lambda x: x[0])
    addition = pp.Group(term + pp.ZeroOrMore(pp.Literal('+').suppress() + term)).set_results_name("add")
    multiplication = pp.Group(addition + pp.ZeroOrMore(pp.Literal('*').suppress() + addition)).set_results_name("mul")
    expr <<= multiplication

    def eval(toks):
        if isinstance(toks, numbers.Number):
            return toks

        n = toks.get_name()
        if n == "add":
            return sum(eval(x) for x in toks)
        elif n == "mul":
            return np.product([eval(x) for x in toks])

    s = 0
    for l in lines(src):
        result = expr.parseString(l)
        s += eval(result[0])
    print(s)


if __name__ == "__main__":
    part1()
    part2()
