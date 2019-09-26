from gym.envs.registration import register

register(
    id='Pyrace-v0',
    entry_point='gym_race.envs:RaceEnv',
    max_episode_steps=2000,
)
