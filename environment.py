import pygame
import random
import numpy as np


class Block:
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.width = 40  # Larger blocks for visibility
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 1 #random.randint(5, 10)  # Reduced health for faster gameplay
        self.font = font
    def draw(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, (255, 165, 0), self.rect)  # Orange color
            healthText = self.font.render(str(self.health), True, (255, 255,255))
            healtTextRect =healthText.get_rect(center=self.rect.center)
            screen.blit(healthText, healtTextRect)

class Environment:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.PADDLEWIDTH, self.PADDLEHEIGHT = 90, 15
        self.BALLSIZE = 10
        self.PADDLESPEED = 7
        self.BALLSPEED = 7 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255, 204, 0)
        

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Block Hitter')

        self.font = pygame.font.Font(None, 56)
        self.blockFont = pygame.font.Font(None, 24)  # Smaller font for block health

        self.reset()

    def reset(self):
        """
        Reset Paddle, ball, and Blocks
        """
        self.player = pygame.Rect(self.WIDTH // 2 - self.PADDLEWIDTH // 2, self.HEIGHT - self.PADDLEHEIGHT - 10, self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.ball = pygame.Rect(self.WIDTH // 2 - self.BALLSIZE // 2, self.HEIGHT // 2 - self.BALLSIZE // 2, self.BALLSIZE, self.BALLSIZE)
        self.blocks = [] 
        for row in range(5):
            for col in range(20): #15
                blockX = col * 40  #+ 30 
                blockY = row * 20 + 50  #+ 50 
                #blockX = col * 50 + 30
                #blockY = row * 30 + 50
                self.blocks.append(Block(blockX, blockY, self.blockFont))
    
        self.score = 0
        self.lives = 1 # switch to 3 for normal version

        self.resetBall()
        return self.getState()
    
    def reset1(self):
        """
        Reset Paddle, ball, and Blocks
        """
        self.player = pygame.Rect(self.WIDTH // 2 - self.PADDLEWIDTH // 2, self.HEIGHT - self.PADDLEHEIGHT - 10, self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.ball = pygame.Rect(self.WIDTH // 2 - self.BALLSIZE // 2, self.HEIGHT // 2 - self.BALLSIZE // 2, self.BALLSIZE, self.BALLSIZE)
        self.blocks = []
        
        # Adjusting offsets
        block_offset_x = 30  # Adjust as needed
        block_offset_y = 50  # Adjust as needed

        # Create a dummy block instance to get the width and height
        dummy_block = Block(0, 0, self.blockFont)
        block_width = dummy_block.width
        block_height = dummy_block.height

        for row in range(5):
            for col in range(15):
                blockX = col * block_width + block_offset_x
                blockY = row * block_height + block_offset_y
                self.blocks.append(Block(blockX, blockY, self.blockFont))

        self.score = 0
        self.lives = 1 # switch to 3 for normal version

        self.resetBall()
        return self.getState()

    def resetBall(self):
        self.resetPaddle()
        ballX = self.player.centerx - self.BALLSIZE // 2
        ballY = self.player.top - self.BALLSIZE - 5
        self.ball.center = (ballX, ballY)
        self.ballSpeed = [0, -self.BALLSPEED]  # Always move upward initially

    def resetPaddle(self):
        self.player.x = self.WIDTH // 2 - self.PADDLEWIDTH // 2

    def draw(self, episode):
        """
        Draw all objects to the screen
        """
        self.screen.fill(self.BLACK)
        self.drawPaddle()
        self.drawBall()
        self.drawBlocks()
        livesText =self.font.render(f"Lives: {self.lives}", False, self.WHITE)
        playerText = self.font.render(f"Score: {self.score}", False, self.WHITE)
        episodeText  = self.font.render(f"Episode: {episode}", False, self.WHITE)
        self.screen.blit(playerText, (30, 250))
        self.screen.blit(livesText, (270, 300))
        self.screen.blit(episodeText, (500, 250))

    def drawPaddle(self):
        """
        Draw the paddle to the screen
        """
        pygame.draw.rect(self.screen, self.WHITE, self.player)

    def drawBall(self):
        """
        Draw the ball to the screen
        """
        pygame.draw.ellipse(self.screen, self.WHITE, self.ball)

    def drawBlocks(self):
        """
        Draw the blocks to the screen
        """
        for block in self.blocks:
            block.draw(self.screen)

    def update(self):
        """
        Update the game state
        """
        self.movePaddle()
        self.moveBall()


    def movePaddle(self, paddle, left):
        if left and paddle.x > 0:
            paddle.x -= self.PADDLESPEED
        if not left and paddle.x < self.WIDTH - self.PADDLEWIDTH:
            paddle.x += self.PADDLESPEED

    def moveBall(self):
        self.ball.x += self.ballSpeed[0]
        self.ball.y += self.ballSpeed[1]
        ballHit = False
        if self.ball.x < 0 or self.ball.x > self.WIDTH - self.BALLSIZE:
            self.ballSpeed[0] = -self.ballSpeed[0]
        if self.ball.y < 0:
            self.ballSpeed[1] = -self.ballSpeed[1]
        if self.ball.y > self.HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.resetBall()
            return

        if self.ball.colliderect(self.player) and self.ballSpeed[1] > 0:
            self.ballSpeed[1] = -self.ballSpeed[1]
            # Calculate normalized hit position (0 to 1 across paddle width)
            hitPos = (self.ball.centerx - self.player.left) / self.PADDLEWIDTH
            ballHit = True
            # Map hitPos from [0,1] to [-0.5,0.5] and scale by BALLSPEED
            if hitPos < 0.5:
                self.ballSpeed[0] = -self.BALLSPEED 
            else: 
                self.ballSpeed[0] = self.BALLSPEED
            #self.ballSpeed[0] = self.BALLSPEED * (hitPos - 1)

        for block in self.blocks[:]:
            if self.ball.colliderect(block.rect) and block.health > 0:
                block.health -= 1
                self.score += 1
                self.ballSpeed[1] = -self.ballSpeed[1]
                if block.health == 0:
                    self.blocks.remove(block)
                break
        
        return ballHit
                    
    def step(self, playerAction):
        oldScore = self.score 
        oldLives = self.lives 

        if playerAction == 0:
            self.movePaddle(self.player, left=True)
        elif playerAction == 1:
            self.movePaddle(self.player, left=False)
        elif playerAction == 2:
            pass 
        
        ballHit = self.moveBall() 

        nextState = self.getState()
        done = self.lives <= 0 or len(self.blocks) == 0 
        reward = 0  
        #if ballHit:
        #    reward += 3
        if self.score > oldScore: 
            reward += 5 
        if self.lives < oldLives: 
            reward -= 50 
        if len(self.blocks) == 0:
            reward += 100 
        if self.lives <= 0:
            reward -= 100

        if done:
            self.reset()

        return nextState, reward, done, {}
        
                
    def getState(self):
        blockCount = len(self.blocks)
        avgBlockY = sum(block.y for block in self.blocks) / blockCount if blockCount > 0 else 0
        #avgBlockHealth = sum(block.health for block in self.blocks) / blockCount if blockCount > 0 else 0
        paddleBallDist = abs(self.player.centerx - self.ball.centerx) / self.WIDTH
        return np.array([
            self.player.x / self.WIDTH,
            self.ball.x / self.WIDTH,
            self.ball.y / self.HEIGHT,
            self.ballSpeed[0] / self.BALLSPEED,
            self.ballSpeed[1] / self.BALLSPEED,
            blockCount / 75, #75
            avgBlockY / self.HEIGHT,
            #avgBlockHealth / 10,
            paddleBallDist
        ])
    
    def render(self, episode=0):
        self.draw(episode)
        pygame.display.flip()

    def close(self):
        pygame.quit()