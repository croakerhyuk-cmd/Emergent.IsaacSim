from ..base.framework import State, Operation


class RobotState(State):
    def __init__(self, operation: Operation, robot_state: dict, env):
        super().__init__(operation)
        self.robot = robot_state
        self.operation = operation
        self.env = env

    def __getattr__(self, name):
        """RobotState에 없는 속성/메서드는 환경에 위임한다.

        ``__getattr__``는 일반적인 속성 탐색이 실패했을 때만 호출되므로,
        RobotState에 정의된 메서드와 인스턴스 속성이 항상 우선한다.
        """
        env = object.__getattribute__(self, "env")
        return getattr(env, name)
    


