from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Dict

events: Dict = {}


def sub2event(sub: Callable = None,
              event: Callable = None) -> None:
    """
    Appends a pair subscriber - event to events dictionary and
    decorates event to make it execute all subscribers
    after event execution

    :param sub: a function following an execution of event
    :param event: a function followed by subscribers
    """
    if sub and event is not None:
        if event.__name__ not in events.keys():
            cp = event_tracker(event)
            events.update({event.__name__: [sub]})
            CloseEmptyEvents()
            return cp
        else:
            tmp = events[event.__name__].copy()
            tmp.append(sub)
            events.update({event.__name__: tmp})
            del tmp
            return event


def CloseEmptyEvents() -> None:
    if not events:
        for key, val in events.items():
            if not val:
                del events[key]


def notify(event: Callable) -> None:
    if event.__name__ in events.keys() and events[event.__name__]:
        for f in events[event.__name__]:
            if callable(f):
                f()


def EndSubscription(sub: Callable,
                    event: Callable) -> None:
    if event.__name__ in events.keys():
        events[event.__name__].remove(sub.__name__)
    CloseEmptyEvents()


def event_tracker(event: Callable):
    if not hasattr(event, "wrapped"):
        @wraps(event)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            e = event(*args, **kwargs)
            notify(event)
            return e

        wrapper.wrapped = True
        return wrapper
