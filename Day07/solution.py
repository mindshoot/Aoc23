import os
from collections import Counter


CARD_RANK = "AKQJT98765432"
CARD_RANK_PART_2 = "AKQT98765432J"


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def get_values(hand, ranking):
    return [ranking.index(card) for card in hand]


def eval_cards(cards):
    counted = Counter(cards)
    summary = sorted(counted.items(), key=lambda i: i[1], reverse=True)
    num, best = len(summary), summary[0][1]
    if num == 1:
        return "1. Five of a kind"
    if num == 2 and best == 4:
        return "2. Four of a kind"
    if num == 2 and best == 3:
        return "3. Full house"
    if num == 3 and best == 3:
        return "4. Three of a kind"
    if num == 3 and best == 2:
        return "5. Two pair"
    if num == 4 and best == 2:
        return "6. One pair"
    if num == 5:
        return "7. High card"
    raise Exception("Oh no")


def calculate_part_1(test=False):
    lines = read(1, test=test)
    input = map(str.split, lines)

    def eval_hand(hand):
        scores = get_values(hand, CARD_RANK)
        card_type = eval_cards(scores)
        return (card_type, *scores)

    sortable = ((eval_hand(hand), int(bid)) for hand, bid in input)
    total = sum(
        (i + 1) * bid
        for i, (_, bid) in enumerate(sorted(sortable, key=lambda i: i[0], reverse=True))
    )
    return total


def calculate_part_2(test=False):
    lines = read(1, test=test)
    input = map(str.split, lines)
    joker = get_values("J", CARD_RANK_PART_2)[0]

    def tweak(scores):
        num_jokers = len([j for j in scores if j == joker])
        if num_jokers == 5:
            return ["A"] * 5
        if num_jokers > 0:
            without_joker = [s for s in scores if s != joker]
            best = Counter(without_joker).most_common()[0][0]
            return without_joker + [best] * num_jokers
        return scores

    def eval_hand(hand):
        scores = get_values(hand, CARD_RANK_PART_2)
        tweaked_scores = tweak(scores)
        card_type = eval_cards(tweaked_scores)
        return (card_type, *scores)

    sortable = [(eval_hand(hand), int(bid)) for hand, bid in input]
    total = sum(
        (i + 1) * bid
        for i, (_, bid) in enumerate(sorted(sortable, key=lambda i: i[0], reverse=True))
    )
    return total


for part, function, test_result in [
    (1, calculate_part_1, 6440),
    (2, calculate_part_2, 5905),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
