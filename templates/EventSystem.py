from __future__ import annotations
from typing import Any
from templates.helpers.object_type_checker import *
from getclass import getclass


class Event:
    def __init__(self):
        """Instantiated the object type of <Event> with the list() of Subscriptions"""

        self.__subscribers = list()

    def __str__(self) -> str:
        return '{}:\t{}'.format(type(self).__name__, hex(id(self)))

    def __iadd__(self, other):
        """Adds new subscriber

        Overloaded += assignment operator.

        This function works ONLY with objects type of:
        - <static function>
        - <IEventVisitor>
        - <method IEventVisitor>
        """
        if self.isVisitor(other):
            self.__subscribers.append(other)
            return self
        else:
            raise ValueError("ONLY objects of the following type are allowed to be an Event subscribers"
                             "\n\t- <static function>\n"
                             "\t- <IEventVisitor>\n"
                             "\t- <method IEventVisitor>")

    def __isub__(self, other):
        """Removes a subscriber

        Overloaded -= assignment operator
        """

        self.__subscribers.remove(other)
        return self

    @property
    def Subscriptions(self):
        """Returns list of the <Event> subscribers"""

        return self.__subscribers

    @Subscriptions.setter
    def Subscriptions(self, *subscribers):
        """Adds new <Event> subscribers"""

        for sub in subscribers:
            self.__iadd__(sub)

    @Subscriptions.deleter
    def Subscriptions(self):
        """Removes all the <Event> subscribers"""

        for sub in self.__subscribers:
            del sub.Subscription
        self.__subscribers.clear()

    @staticmethod
    def isVisitor(obj):
        """Check if object is type of <IEventVisitor>"""
        IsAnyIn = lambda arg1, arg2: any(i in arg2 for i in arg1)
        allowedToProceed = (eval("IEventVisitor"), eval("Subscriber"))

        if isFunction(obj):
            return True
        elif isMethod(obj):
            bases = type(getclass(obj)).__bases__
            return IsAnyIn(allowedToProceed, bases)
        else:
            bases = type(obj).__bases__
            if IsAnyIn(allowedToProceed, bases):
                return True
            else:
                try:
                    return issubclass(obj, allowedToProceed)
                except TypeError:
                    return False

    def Notify(self):
        """Notifies all subscribers of the new <Event> State"""

        if self.__subscribers:
            for sub in self.__subscribers:
                try:
                    sub.Update()
                except (AttributeError, TypeError):
                    sub()

    @property
    def State(self):
        """Returns current <Event> State"""

        raise NotImplementedError

    @State.setter
    def State(self, value):
        """Sets current <Event> State"""

        raise NotImplementedError

    @State.deleter
    def State(self):
        """Resets current <Event> State to the default"""

        raise NotImplementedError


class Subscriber:
    def __init__(self, event):
        """Instantiates the object type of <Subscriber>

        Whenever <Subscriber> is instantiated
        keeps an event link to give an access to the <Event> data
        """

        self.__event = None
        self.Subscription = event

    def __str__(self):
        return '{}:\t{}'.format(type(self).__name__, hex(id(self)))

    @property
    def Subscription(self) -> Event:
        """Returns the <Event> which the <Subscriber> object is subscribed to"""

        return self.__event

    @Subscription.setter
    def Subscription(self, event: Event) -> None:
        """Sets the <Event> subscription for the <Subscriber> object"""

        if self.__event is None and event is not None:
            self.__event = event
            event += self
        elif self.__event is not None:
            raise ValueError('The object is already subscribed to: \n{}\n'
                             'Please, Unsubscribe before new subscription'.format(self.__event))
        elif event is None:
            raise ValueError('Subscription cannot be type of None')
        else:
            raise ValueError("{} is not allowed value type".format(event))

    @Subscription.deleter
    def Subscription(self) -> None:
        """Resets the <Event> which the <Subscriber> object was subscribed to

        Sets the value of subscription to None.
        """

        self.__event = None

    def Unsubscribe(self) -> None:
        """Deletes the subscription and removes <Subscriber> object from the list of the <Event> subscribers"""

        self.__event -= self
        del self.Subscription

    @property
    def EventState(self) -> Any:
        """Returns current State of an <Event>"""

        return self.Subscription.State

    def Update(self):
        """Method is invoked whenever an <Event> State (the subscriber is subscribed to) has been changed"""

        raise NotImplementedError
