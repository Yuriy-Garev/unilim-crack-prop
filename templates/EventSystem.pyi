from __future__ import annotations
from typing import Callable, Any, List, Iterable, Optional


class EventVisitor: ...
# Label-Interface for <Event> class objects
#
# Inheriting from this class labels child as <EventVisitor> for <Event> subscription.
# This label allows methods of such class to be added to an <Event> subscribers list.


class Event:
    # An Interface for EventSystem events like objects
    # Inheriting from this class gives a child an <Event> features
    # which allow <Subscriber> to be subscribed to it.
    __subscribers: List

    @property
    def Subscriptions(self) -> Optional[List[Callable], None]: ...
    # Returns a list of the <Event> subscribers

    @Subscriptions.setter
    def Subscriptions(self, *subscribers: Optional[Iterable[Callable], Callable]) -> None: ...
    # Adds new <Event> subscribers"""

    @Subscriptions.deleter
    def Subscriptions(self, *subscribers: Optional[Iterable[Callable], Callable]) -> None: ...
    # Removes all the <Event> subscribers

    def __iadd__(self, other: Callable) -> Event: ...
    # Adds new subscriber
    # Overloaded += assignment operator

    def __isub__(self, other: Callable) -> Event: ...
    # Removes a subscriber
    # Overloaded -= assignment operator

    def Notify(self) -> None: ...
    # Notify all subscribers of the new <Event> State

    @property
    def State(self) -> Any: ...
    # Returns current <Event> State

    @State.setter
    def State(self, value: Any) -> None: ...
    # Sets current <Event> State

    @State.deleter
    def State(self) -> None: ...
    # Resets current <Event> State to the default

    @staticmethod
    def isVisitor(other: object) -> bool: ...


class Subscriber(EventVisitor):
    # An Interface for EventSystem subscribers like objects
    # Inheriting from this class gives a child an <Subscriber> features
    # which allow it to be subscribed to <Event> objects.
    __event: Optional[Event, None]

    def __init__(self, event: Event) -> None: ...

    def Update(self) -> None: ...
    # Invoked whenever the <Event> State (the subscriber is subscribed to) has been changed
