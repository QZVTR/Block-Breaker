# Block Breaker 

A simple game where the player must break blocks to score points. The game is played on a grid of 15 columns and 5 rows. The player controls a paddle that moves left and right to hit the ball. The ball bounces off the paddle and the blocks. 

## V2 

- three lives trained on 700 episodes. 
- Stopped after 700 because the model was stuck on a broken tatic of just hitting the ball once and taking the points, losing a life then repeating. It wasn't able to learn the game.
- Really struggles at kick off by moving straight to the left hand side of the screen, Then staying there.
- Did find optimum strategy though to hit ball to the side to get it go all the way to the back of the blocks.

## V3 

- avgBlockHealth / 5 Fixed to avgBlockHealth / 10 removed
- All blocks are now 1 health 
- no gaps around blocks or edges of screen paddle needs to breack through 
