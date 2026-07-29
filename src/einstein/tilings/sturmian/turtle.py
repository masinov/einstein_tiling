"""Exact combinatorial controls from Akiyama--Araki's Turtle proof.

The paper's Golden Sturmian Patches use the characteristic Sturmian word of
slope ``(5-sqrt(5))/10 = [3,1,1,...]``.  This module reproduces the standard
words, their central palindromes, the two decomposition identities used by
the Golden Hex construction, and the exact density algebra used by the
Golden Ammann-bar proof.

It deliberately does *not* claim to reconstruct the geometric Golden Hex
patches or to prove that Ammann bars are forced by every Turtle tiling.  Those
are separate geometric obligations in the published proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


SOURCE_ID = "akiyama-araki-turtle-2025"


@dataclass(frozen=True)
class WordStats:
    """Exact length and letter counts of one standard word."""

    index: int
    length: int
    zeros: int
    ones: int

    @property
    def one_frequency(self) -> Fraction:
        return Fraction(self.ones, self.length)


def standard_word(index: int) -> str:
    """Return the paper's standard word ``s_index`` for index >= -1.

    ``s_-1=1``, ``s_0=0``, ``s_1=001`` and
    ``s_(n+1)=s_n s_(n-1)`` for ``n>=1``.
    """

    if index < -1:
        raise ValueError("standard-word index must be at least -1")
    if index == -1:
        return "1"
    words = ["0", "001"]
    if index < len(words):
        return words[index]
    for _ in range(1, index):
        words.append(words[-1] + words[-2])
    return words[index]


def standard_word_stats(index: int) -> WordStats:
    """Return counts without constructing an exponentially growing word."""

    if index < -1:
        raise ValueError("standard-word index must be at least -1")
    if index == -1:
        return WordStats(-1, 1, 0, 1)
    stats = [WordStats(0, 1, 1, 0), WordStats(1, 3, 2, 1)]
    if index < len(stats):
        return stats[index]
    for n in range(1, index):
        a, b = stats[-1], stats[-2]
        stats.append(WordStats(
            n + 1,
            a.length + b.length,
            a.zeros + b.zeros,
            a.ones + b.ones,
        ))
    return stats[index]


def central_word(index: int) -> str:
    """Return the central palindrome ``p_index``.

    For positive odd indices ``s_n=p_n 01``; for positive even indices
    ``s_n=p_n 10``.  The paper defines ``p_0`` as the empty word.
    """

    if index < 0:
        raise ValueError("central-word index must be nonnegative")
    if index == 0:
        return ""
    word = standard_word(index)
    suffix = "01" if index % 2 else "10"
    if not word.endswith(suffix):
        raise AssertionError(f"s_{index} lacks expected suffix {suffix}")
    return word[:-2]


def verify_central_identities(max_index: int) -> dict[str, int]:
    """Verify the paper's palindrome and equations (1)--(2) through a level.

    Equation (1) starts at ``p_3`` (n=1); equation (2) starts at ``p_4``
    (n=2), because the exceptional seed ``s_0`` does not have the generic
    two-letter suffix.
    """

    if max_index < 0:
        raise ValueError("max_index must be nonnegative")
    words = [central_word(n) for n in range(max_index + 1)]
    for n, word in enumerate(words):
        if word != word[::-1]:
            raise AssertionError(f"p_{n} is not a palindrome")

    equation_1 = 0
    for n in range(1, (max_index - 1) // 2 + 1):
        target = words[2 * n + 1]
        if target != words[2 * n] + "10" + words[2 * n - 1]:
            raise AssertionError(f"first form of equation (1) fails at n={n}")
        if target != words[2 * n - 1] + "01" + words[2 * n]:
            raise AssertionError(f"second form of equation (1) fails at n={n}")
        equation_1 += 1

    equation_2 = 0
    for n in range(2, max_index // 2 + 1):
        target = words[2 * n]
        if target != words[2 * n - 1] + "01" + words[2 * n - 2]:
            raise AssertionError(f"first form of equation (2) fails at n={n}")
        if target != words[2 * n - 2] + "10" + words[2 * n - 1]:
            raise AssertionError(f"second form of equation (2) fails at n={n}")
        equation_2 += 1

    return {
        "palindromes": len(words),
        "equation_1_instances": equation_1,
        "equation_2_instances": equation_2,
    }


def lower_density_side(value: Fraction) -> int:
    """Compare a rational in (0,1/2) with ``(5-sqrt(5))/10`` exactly.

    Returns -1 below the irrational root and +1 above it.  The comparison
    uses the sign of ``x^2-x+1/5`` between zero and one half.
    """

    if not 0 < value < Fraction(1, 2):
        raise ValueError("comparison value must lie strictly between 0 and 1/2")
    polynomial = value * value - value + Fraction(1, 5)
    if polynomial == 0:
        raise AssertionError("a rational cannot equal the irrational root")
    return -1 if polynomial > 0 else 1


def golden_density_root_residual(sign: int) -> tuple[Fraction, Fraction]:
    """Evaluate ``q^2-q+1/5`` at ``q=(5+sign*sqrt(5))/10`` exactly.

    The return value is the pair (rational coefficient, sqrt(5)
    coefficient).  Both must vanish.
    """

    if sign not in (-1, 1):
        raise ValueError("sign must be -1 or +1")
    a, b, d = Fraction(5), Fraction(sign), Fraction(10)
    rational = (a * a + 5 * b * b) / (d * d) - a / d + Fraction(1, 5)
    radical = 2 * a * b / (d * d) - b / d
    return rational, radical


def minority_chirality_residual() -> tuple[Fraction, Fraction]:
    """Evaluate ``9f^2-9f+1`` at ``f=(3-sqrt(5))/6`` exactly."""

    a, b, d = Fraction(3), Fraction(-1), Fraction(6)
    rational = 9 * (a * a + 5 * b * b) / (d * d) - 9 * a / d + 1
    radical = 18 * a * b / (d * d) - 9 * b / d
    return rational, radical


def minority_chirality_side(value: Fraction) -> int:
    """Compare a rational in (0,1/2) with ``(3-sqrt(5))/6`` exactly."""

    if not 0 < value < Fraction(1, 2):
        raise ValueError("comparison value must lie strictly between 0 and 1/2")
    polynomial = 9 * value * value - 9 * value + 1
    if polynomial == 0:
        raise AssertionError("a rational cannot equal the irrational root")
    return -1 if polynomial > 0 else 1


def standard_word_table(max_index: int) -> list[dict]:
    """JSON-ready exact frequency table for ``s_0`` through ``s_max``."""

    if max_index < 0:
        raise ValueError("max_index must be nonnegative")
    table = []
    for index in range(max_index + 1):
        stats = standard_word_stats(index)
        frequency = stats.one_frequency
        table.append({
            "index": index,
            "length": stats.length,
            "zeros": stats.zeros,
            "ones": stats.ones,
            "one_frequency": [frequency.numerator, frequency.denominator],
            "side_of_q_minus": (
                None if index == 0 else lower_density_side(frequency)
            ),
        })
    return table
