"""
configuration for comac's AGV

the location of 4 wheel is analogous to shape of X
"""
import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR

left_back_joint
left_front_joint
lift_joint
right_back_joint
right_front_joint

# left_back_link
# left_front_link
# lift_link
# right_back_link
# right_front_link

COMAC_AGV=ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path="/project/EXP/Sence/Warehouse/comac_agv.usd",

    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(),
        joint_pos={
        "left_back_joint":,
        "left_front_joint":,
        "lift_joint":,
        "right_back_joint":,
        "right_front_joint":,
        }
    )
    
)