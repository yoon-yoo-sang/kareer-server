from abc import ABC, abstractmethod

from authentication.models import AuthUser


class AuthenticationStrategyInterface(ABC):

    @abstractmethod
    def authenticate(self, **credentials) -> AuthUser:
        pass

    @abstractmethod
    def signup(self, **credentials) -> AuthUser:
        pass
