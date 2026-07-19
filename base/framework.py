from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class State(ABC):
    operation: Operation


class Operation(ABC):
    @abstractmethod
    def execute(self, state: State) -> tuple[None , State]:
        """
        state를 수정하고 실행 결과와 state를 반환한다.
        """
        raise NotImplementedError

    def connect(self, result, state: State,) -> Operation:
        return IdentityOperation()

def execute_operation(state: State) -> State:
    
    result, state = state.operation.execute(state)
    state.operation = state.operation.connect(result)

    return state

class IdentityOperation(Operation):

    def execute(self, state: State) -> tuple[None, State]:
        return None, state

    def connect(self, result, state: State) -> Operation:
        return IdentityOperation()
