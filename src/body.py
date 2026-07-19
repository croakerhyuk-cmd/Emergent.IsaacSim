
from ..base.framework import Operation

class Spwan(Operation):
    def execute(self, state):
        spwan = state.get_spawn_list()
        success = state.set_position(spwan)
        
        return success, state

class Stabilize(Operation):
    def execute(self, state):
        success = state.set_velocity(0)
        return success, state
    
class SetTarget(Operation):
    def execute(self, state):
        target = state.get_target_pose_world()
        success = state.get_target_pose_world(target)
        
        return success, state

class PlanPathBrake(Operation):
    def execute(self, state):
        video = state.get_video()
        path, brake = state.planner(video)
        
        state.set_brake(brake)

        path_plan_index = state.get_current_path_index()
        if path_plan_index >= state.PATH_PLAN_LENGTH:
            state.set_path(path)
            state.path_plan_index(0)
            return True, state
        
        return False, state
    
class PlanSpeed(Operation):
    def execute(self, state):
        current_speed = state.get_current_speed()
        path = state.get_path()
        brake = state.get_brake()

        target_speed = current_speed + brake - path ##가짜

        state.set_target_speed(target_speed)

        return True, state
    
class PlanTorque(Operation):
    def execute(self, state):
        
        torque = state.controller(state.current_speed, state.target_speed)
        torque_plan_index = state.get_current_torque_index()

        if torque_plan_index < state.TORQUE_PLAN_LENGTH:
            state.set_torque(torque)
            state.set_current_torque_index(torque_plan_index + 1)
            return True, state
        
        state.set_current_torque_index(0)
        return False, state
        
class CheckCollision(Operation):
    def execute(self, state):
        collision = state.check_collision()
        return collision, state     
    
class CheckTargetCompleted(Operation):
    def execute(self, state):
        current_pose = state.get_pose_world()
        target_pose = state.get_target_pose_world()
        if torch.norm(current_pose - target_pose) < state.TARGET_COMPLETE_THRESHOLD:
            return True, state
        return False, state
    
class Terminate(Operation):
    def execute(self, state):
        success = state.terminate()
        return success, state

class SaveData(Operation):
    def execute(self, state):
        state.save_data()
        return None, state

    