"""Additional varied-payload and duplicate/loss checks; official tests unchanged."""
import json
import random
from pathlib import Path

from task1_rdt import Sender, Receiver, UnreliableChannel
from task3_congestion import YourControl, FixedWindow
from bench import simulate


def transfer(seed, size, loss=.10, dup=.03, reorder=.10):
    rng = random.Random(seed)
    original = bytes(rng.getrandbits(8) for _ in range(size))
    up = UnreliableChannel(seed, loss=loss, dup=dup, reorder=reorder)
    down = UnreliableChannel(seed + 1, loss=loss, dup=dup, reorder=reorder)
    sender, receiver = Sender(up, down, original), Receiver(up, down)
    for steps in range(200000):
        alive = sender.step()
        receiver.step()
        if not alive:
            assert receiver.data() == original, (seed, size)
            return dict(seed=seed, size=size, steps=steps+1,
                        data_channel=up.stats, ack_channel=down.stats)
    raise AssertionError(('did not terminate', seed, size))


def main():
    rows = [transfer(seed, size) for seed in range(30)
            for size in (0, 1, 7, 8, 9, 31, 2000, 2049)]
    rows += [transfer(seed, 2000, .30, .50, .80) for seed in range(20)]
    examples = [transfer(seed, 2000) for seed in (246, 999)]
    comparisons = {}
    for beta in (.5, .6, .7, .75, .8):
        class Variant(YourControl):
            def __init__(self):
                super().__init__()
                self.backoff = beta
        comparisons[str(beta)] = simulate(Variant)
    class Observed(YourControl):
        latest = None
        def __init__(self):
            super().__init__()
            type(self).latest = self
            self.ack_windows = []
        def on_ack(self):
            super().on_ack()
            self.ack_windows.append(self.window)
    simulate(Observed)
    tail = Observed.latest.ack_windows[-1000:]
    result = dict(reliable_delivery_cases=len(rows), examples=examples,
                  baseline=simulate(FixedWindow), backoff_comparison=comparisons,
                  last_1000_ack_windows=dict(min=min(tail), max=max(tail)))
    Path('out').mkdir(exist_ok=True)
    Path('out/extra-validation.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
