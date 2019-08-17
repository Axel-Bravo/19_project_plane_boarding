from gym.envs.registration import register

register(
    id='onboarding-v0',
    entry_point='gym_onboarding.envs:OnboardingEnv',
)