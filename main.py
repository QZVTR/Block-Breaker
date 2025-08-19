from agent import DQNAgent
from environment import Environment
import pygame 
import matplotlib.pyplot as plt 
import os 
import argparse 

def playManual():
    env = Environment()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        action = 2  # Stay
        if keys[pygame.K_LEFT]:
            action = 0  # Left
        if keys[pygame.K_RIGHT]:
            action = 1  # Right
        state, reward, done, _ = env.step(action)
        env.render()
        clock.tick(60)
    env.close()

def train(modelPath=None,startEpisode=1100):
    env = Environment()
    agent = DQNAgent(stateDim=8, actionDim=3) # 9 on normal version 8 on 1 health per block
    clock = pygame.time.Clock() 
    episodes = 10000 
    batchSize = 64 
    maxReward = {"episode": 0, "reward": float("-inf")}
    allRewards = []

    os.makedirs("models/v3", exist_ok=True)

    if modelPath is not None:
        try:
            agent.load(modelPath)
            if startEpisode > 100:
                agent.epsilon = 0.01
            print(f"Loaded model from {modelPath}") 
        except FileNotFoundError as e:
            print(f"Error loading model: {e}") 
            env.close()
            return 
    else: 
        print("No model path provided, starting from scratch")

    for episode in range(startEpisode,episodes+1):
        state = env.reset() 
        totalReward = 0
        done = False 
        

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    env.close()
                    return 
        
            action = agent.act(state)
            nextState, reward, done, _ = env.step(action) 
            agent.replayBuffer.push(state, action, reward, nextState, done)
            state = nextState 
            totalReward += reward 
            agent.train(batchSize) 
            env.render(episode=episode + 1)
            clock.tick(60)


            if done:
                print(f"Episode {episode+1}, total reward: {totalReward}, score: {env.score}, epsilon: {agent.epsilon:.2f}")
                if totalReward > maxReward["reward"]:
                    maxReward["episode"] = episode
                    maxReward["reward"] = totalReward
                allRewards.append(totalReward)
                break 

        if episode % 100 == 0:
            agent.save(f"models/v3/blockhitter_{episode}.pth")
    env.close()

    plt.figure(figsize=(10,8))
    plt.plot(range(startEpisode, episodes+1), allRewards)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title(f"Block Hitter Training (Max Reward: {maxReward['reward']:.2f} at Episode {maxReward['episode']})")
    plt.savefig("rewards_v3.png")

def test(modelPath='models/blockhitter_0.pth'): 
    env = Environment() 
    agent = DQNAgent(stateDim=8, actionDim=3)

    try: 
        agent.load(modelPath)
    except FileNotFoundError as e:
        print(f"Error loading model: {e}") 
        env.close()
        return
    
    agent.epsilon = 0 
    clock = pygame.time.Clock() 
    finished = False 

    while not finished:
        env.reset() 

        state = env.getState()
        totalReward = 0 
        done = False 

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    env.close()
                    return
                
            action = agent.act(state)
            nextState, reward, done, _ = env.step(action) 
            state = nextState 
            totalReward += reward 
            env.render(episode='N/A')
            clock.tick(60)
    env.close()
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='main.py', description='Block Breaker')
    parser.add_argument("mode", choices=["train", "test", "play"], help="train, test or play")
    parser.add_argument("--model", help="Path to model file")
    args = parser.parse_args()
 
    if args.mode == "train":
        train(args.model)
    elif args.mode == "test":
        test(args.model)
    elif args.mode == "play":
        playManual()
    else:
        print("Invalid mode")
