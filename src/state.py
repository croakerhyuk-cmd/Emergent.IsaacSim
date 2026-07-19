from ..base.framework import State, Operation


class RobotState(State):
    def __init__(self, operation: Operation, robot_state: dict, env):
        super().__init__(operation)
        self.robot = robot_state
        self.operation = operation
        self._env = env
    
    def set_position(self, position):
        self.env.set_robot_position(position)

    def get_spawn_list(self):
        return self.env.get_spawn_list()  
    
    def exert_torque(self):
        return self.env.exert_torque()

    def check_collision(self):
        return self.env.check_collision()
    
    def terminate(self):
        return self.env.terminate()

    def set_target(self, target):
        return self.env.set_target(target)

    def get_target(self):
        return self.env.get_target()
    



