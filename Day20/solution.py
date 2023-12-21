import os
from collections import Counter


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


"""
Flip-flop (%): 
- has state (initially off). 
- Ignores high, flips on low, and sends state.
Conjunction (&): 
- remembers last puse per input (initially low). 
- Stores input, then sends low if all inputs high, otherwise high.
broadcaster: no state, passes on input to all outputs.

- button sends a low pulse to the broadcaster
- works in generations: resultant pulses not processed until all priors done
- the press is resolved once no further pulses happen
"""

LOW, HIGH, NONE = "low", "high", "none"


class NodeState:
    def __init__(self, key):
        self.key = key
        self.output_callback = None
        self.received = Counter()
        self.sent = Counter()
        self._init_state()

    def set_output_callback(self, output_callback):
        self.output_callback = output_callback

    def _init_state(self):
        ...

    def send(self, src, signal):
        self.received.update((signal))
        result = self._process(src, signal)
        self.sent.update((result))
        if self.output_callback:
            self.output_callback(self.key, result)
        return result

    def _process(self, src, signal):
        return NONE

    def set_sources(self, sources):
        ...

    def set_sources(self, sources):
        ...


class DoesNothing(NodeState):
    ...


class FlipFlop(NodeState):
    def _init_state(self):
        self.state = LOW

    def _process(self, src, signal):
        if signal == HIGH:
            return NONE
        self.state = HIGH if self.state == LOW else LOW
        return self.state


class Conjunction(NodeState):
    def _init_state(self):
        self.inputs = dict()

    def set_sources(self, sources):
        self.inputs = {s: LOW for s in sources}

    def _process(self, src, signal):
        self.inputs[src] = signal
        return LOW if all(v == HIGH for v in self.inputs.values()) else HIGH


class Broadcaster(NodeState):
    def _process(self, src, signal):
        return signal


def parse_line(line):
    start, dests = line.split(" -> ")
    cls = {"%": FlipFlop, "&": Conjunction}.get(start[0], Broadcaster)
    ntype, key = (cls, start[1:] if start[0] in "%&" else start)
    return key, ntype, [d.strip() for d in dests.split(",")]


class Network:
    def __init__(self):
        self.queue = []
        self.state = {}
        self.links = {}
        self.counter = Counter()

    def add(self, key, node_cls, dests):
        self.state[key] = node_cls(key)
        self.links[key] = dests

    def prepare(self):
        for key, node in self.state.items():
            linked_to_node = {k for k, l in self.links.items() if key in l}
            node.set_sources(linked_to_node)
        missing_keys = {n for l in self.links.values() for n in l} - self.state.keys()
        for key in missing_keys:
            self.state[key] = DoesNothing(key)
            self.links[key] = []

    def _enqueue(self, seq, src_key, dest_key, signal):
        self.counter.update([signal])
        self.queue.append((seq, src_key, dest_key, signal))

    def press_button(self):
        self._enqueue(1, "button", "broadcaster", LOW)
        while len(self.queue) > 0:
            (seq, src_key, dest_key, signal), self.queue = self.queue[0], self.queue[1:]
            output = self.state[dest_key].send(src_key, signal)
            if output != NONE:
                for out_key in self.links[dest_key]:
                    self._enqueue(seq + 1, dest_key, out_key, output)


def calculate_part_1(test=False):
    lines = read(1, test=test)
    n = Network()
    for key, ntype, dests in map(parse_line, lines):
        n.add(key, ntype, dests)
    n.prepare()

    for _ in range(1000):
        n.press_button()

    return n.counter[LOW] * n.counter[HIGH]


def calculate_part_2(test=False):
    lines = read(1, test=test)
    n = Network()
    for key, ntype, dests in map(parse_line, lines):
        n.add(key, ntype, dests)
    n.prepare()

    output = []
    press_number = 0

    presses_to_high = {}

    def capture_press_count(key, output):
        if output == HIGH:
            presses_to_high[key] = presses_to_high.get(key, []) + [press_number]

    # Set some callbacks on interesting nodes (ie the ones controlling dh, and thus rx)
    for key in ("tr", "xm", "dr", "nh"):
        n.state[key].set_output_callback(capture_press_count)

    for _ in range(9999):
        press_number += 1
        n.press_button()

    # Confirm fixed periodicities, and get product - this will be when they are all high,
    # which will trigger the desired output
    product = 1
    for key, values in presses_to_high.items():
        diffs = [v2 - v1 for v1, v2 in zip(values, values[1:])]
        assert len(set(diffs)) == 1
        product *= diffs[0]

    return product


for part, function, test_result in [
    (1, calculate_part_1, 11687500),
    (2, calculate_part_2, None),
]:
    if test_result is not None:
        test_answer = function(test=True)
        print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
        assert True or (
            test_answer == test_result
        ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
