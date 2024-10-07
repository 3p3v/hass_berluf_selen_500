from typing import Callable


class Timer:
    def start(self) -> None:
        raise NotImplementedError()

    def cancel(self) -> None:
        raise NotImplementedError()


class Timer_factory:
    def create_timer(self, timeout: int, callb: Callable[[], None]) -> Timer:
        raise NotImplementedError()
