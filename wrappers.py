import numpy as np
from collections import deque

# taken from https://github.com/openai/baselines/blob/master/baselines/common/atari_wrappers.py
class LazyFrames(object):
    def __init__(self, frames):
        """This object ensures that common frames between the observations are only stored once.
        It exists purely to optimize memory usage which can be huge for DQN's 1M frames replay
        buffers.
        This object should only be converted to numpy array before being passed to the model.
        You'd not believe how complex the previous solution was."""
        self._frames = frames
        self._out = None

    def _force(self):
        if self._out is None:
            self._out = np.stack(self._frames, axis=-1)
            self._frames = None
        return self._out

    def __array__(self, dtype=None):
        out = self._force()
        if dtype is not None:
            out = out.astype(dtype)
        return out

    def __len__(self):
        return len(self._force())

    def __getitem__(self, i):
        return self._force()[i]

    def count(self):
        frames = self._force()
        return frames.shape[frames.ndim - 1]

    def frame(self, i):
        return self._force()[..., i]

# taken from https://github.com/openai/baselines/blob/master/baselines/common/atari_wrappers.py
class FrameStack():
    def __init__(self, env, k):
        """Stack k last frames.
        Returns lazy array, which is much more memory efficient.
        See Also
        --------
        baselines.common.atari_wrappers.LazyFrames
        """
        self.k = k
        self.frames = deque([], maxlen=k)
        self.env = env

    def restart(self):
        ob = self.env.restart()
        for _ in range(self.k):
            self.frames.append(ob)
        return self._get_ob()

    def step(self, action):
        ob, reward, done = self.env.step(action)
        self.frames.append(ob)
        return self._get_ob(), reward, done

    def _get_ob(self):
        assert len(self.frames) == self.k
        return LazyFrames(list(self.frames))