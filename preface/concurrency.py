import concurrent.futures
import typing

from tqdm.auto import tqdm

T = typing.TypeVar("T")


class BoundedExecutor(typing.Generic[T]):
    def __init__(
        self,
        pool_cls: typing.Type[
            concurrent.futures.Executor
        ] = concurrent.futures.ThreadPoolExecutor,
    ):
        self._pool = pool_cls()
        self._futures: list[concurrent.futures.Future[T]] = []

    def submit(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._futures.append(self._pool.submit(*args, **kwargs))

    def shutdown(self, **kwargs: typing.Any) -> None:
        self._pool.shutdown(wait=False, cancel_futures=True, **kwargs)

    def finish(self, *, desc: str = "") -> list[T]:
        return [
            future.result()
            for future in tqdm(
                concurrent.futures.as_completed(self._futures),
                total=len(self._futures),
                desc=desc,
            )
        ]


def finish_all(futures: list[concurrent.futures.Future[T]]) -> list[T]:
    return [
        future.result()
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures))
    ]
