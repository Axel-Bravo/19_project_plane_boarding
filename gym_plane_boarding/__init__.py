from gym.envs.registration import register

register(
    id='plane-boarding-v0',
    entry_point='gym_plane_boarding.envs:PlaneBoardingEnvironment',
)