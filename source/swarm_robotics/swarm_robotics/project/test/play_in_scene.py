# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""
This script demonstrates policy inference in a prebuilt USD environment.

In this example, we use a locomotion policy to control the H1 robot. The robot was trained
using Isaac-Velocity-Rough-H1-v0. The robot is commanded to move forward at a constant velocity.

.. code-block:: bash

    # Run the script
    ./isaaclab.sh -p scripts/tutorials/03_envs/policy_inference_in_usd.py --checkpoint /path/to/jit/checkpoint.pt

"""

"""Launch Isaac Sim Simulator first."""


import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Tutorial on inferencing a policy on an H1 robot in a warehouse.")
parser.add_argument("--checkpoint",
                    default="/project/EXP/Simulation/logs/rsl_rl/anymal_d_rough/2025-03-12_19-12-33/2025-03-05_14-36-30/exported/policy.pt",
                    type=str, help="Path to model checkpoint exported as jit.", required=False)

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""
import io
import os
import torch

import omni

from isaaclab.envs import ManagerBasedRLEnv
from isaaclab.terrains import TerrainImporterCfg
# from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

from swarm_robotics.tasks.locomotion.velocity.config.h1.rough_env_cfg import H1RoughEnvCfg_PLAY
# from isaaclab_tasks.manager_based.locomotion.velocity.config.anymal_c.rough_env_cfg import AnymalCRoughEnvCfg_PLAY


"""
In order to use a prebuilt USD environment instead of the terrain generator specified, 
we make the following changes to the config before passing it to the ManagerBasedRLEnv.
"""
"""
After running the play script, the policy will be exported to jit and onnx files under the experiment logs directory. 
Note that not all learning libraries support exporting the policy to a jit or onnx file. 
For libraries that don’t currently support this functionality, 
please refer to the corresponding play.py script for the library to learn about how to initialize the policy.
"""


# from isaaclab.assets import ArticulationCfg
# from isaaclab.sim import sim_utils

# robot_cfg = ArticulationCfg(
#     spawn=sim_utils.UsdFileCfg(
#         usd_path="path/to/robot.usd",
#         scale=(2.0, 2.0, 2.0),  # 统一放大两倍
#     ),
#     init_state=ArticulationCfg.InitialStateCfg(
#         pos=(0.0, 0.0, 0.0),
#     ),
# )


def main():
    """Main function."""
    # load the trained jit policy
    policy_path = os.path.abspath(args_cli.checkpoint)
    file_content = omni.client.read_file(policy_path)[2]
    file = io.BytesIO(memoryview(file_content).tobytes())
    policy = torch.jit.load(file)
    env_cfg = H1RoughEnvCfg_PLAY()
    
    # env_cfg = AnymalCRoughEnvCfg_PLAY()
    env_cfg.scene.num_envs = 20
    env_cfg.curriculum = None
    env_cfg.scene.terrain = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="usd",
        # usd_path=f"{ISAAC_NUCLEUS_DIR}/Environments/Simple_Warehouse/warehouse.usd",
        usd_path="/project/EXP/Sence/Senc/Warehouse/Warehouse.usd",
    )
    # robot=env_cfg.scene[]
    env_cfg.sim.device = "cpu"
    env_cfg.sim.use_fabric = False
    env = ManagerBasedRLEnv(cfg=env_cfg)
    
    obs, _ = env.reset()
    while simulation_app.is_running():
        action = policy(obs["policy"])  # run inference
        obs, _, _, _, _ = env.step(action)


if __name__ == "__main__":
    main()
    simulation_app.close()
