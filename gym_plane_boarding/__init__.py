from gym.envs.registration import register

register(
    id='b737-v0',
    entry_point='gym_plane_boarding.envs:PlaneBoardingB737Environment',
)
register(
    id='b747-v0',
    entry_point='gym_plane_boarding.envs:PlaneBoardingB747Environment',
)
register(
    id='a380-v0',
    entry_point='gym_plane_boarding.envs:PlaneBoardingA380Environment',
)