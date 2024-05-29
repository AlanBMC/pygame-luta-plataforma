from stable_baselines3 import PPO
from ia import env

# Crie o modelo com um buffer de rollout menor
model = PPO("CnnPolicy", env, verbose=1, n_steps=512)

# Treine o modelo com um número menor de timesteps para teste
model.learn(total_timesteps=5000)

# Salve o modelo
model.save("ppo_soldada")
