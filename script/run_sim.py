from ..src.state import RobotState
from ..src.body import *

class IsaacSimEnv:

    def __init__(self, config):
        self.config = config

    def operation_step(self):
        operation_length_in_phys_steps = self.config.get("operation_length_in_phys_steps")
        for _ in range(operation_length_in_phys_steps):
            self.step()

spawn = Spwan()
stabilize = Stabilize()
set_target = SetTarget()
check_collision = CheckCollision()
check_target_completed = CheckTargetCompleted()
terminate = Terminate()

plan_path_brake = PlanPathBrake()
plan_speed = PlanSpeed()
plan_torque = PlanTorque()


spawn.connect = lambda result: stabilize if result else spawn
stabilize.connect = lambda result: set_target if result else stabilize
set_target.connect = lambda result: plan_path_brake if result else terminate
check_collision.connect = lambda result: terminate if result else check_target_completed
check_target_completed.connect = lambda result: set_target if result else plan_path_brake
terminate.connect = lambda result: spawn

plan_path_brake.connect = lambda result: plan_speed
plan_speed.connect = lambda result: plan_torque if result else terminate
plan_torque.connect = lambda result: plan_torque if result else check_collision



if __name__ == "__main__":
    env = IsaacSimEnv()
    from ..base.framework import execute_operation

    state = RobotState(operation=spawn, robot_state={"position": None}, env=env,)
    env.step()    

    for _ in range(1000):
        state = execute_operation(state)
        env.operation_step()
    
