# Moon Knight: The Pyramid's Curse

**Moon Knight: The Pyramid's Curse** is a single-player, turn-based custom puzzle game where you battle an AI trained via reinforcement learning. This game is a custom variation of the famous game - Nim. The game’s objective is to input a sequence of moves so that the opponent (AI) picks up the last block and loses. The interactive UI accepts direct inputs without needing to press 'Enter' after every move, creating a fluid gameplay experience.

## About the Project

This project showcases a unique puzzle game that combines strategic decision-making with an AI opponent. The game is designed for both casual players and enthusiasts looking to challenge an AI whose difficulty scales with the chosen level.

To play the game, simply run "app.py"

## Overview of Game Mechanics

### 1. Main Menu

- **Difficulties:**  
  Choose from 5 difficulty levels by pressing the corresponding number:
  - **Easy:** AI trained for 1,000 iterations.
  - **Normal:** AI trained for 2,500 iterations.
  - **Challenger:** AI trained for 5,000 iterations.
  - **Expert:** AI trained for 10,000 iterations.
  - **Mastermind:** AI trained for 20,000 iterations.
- **Additional Options:**
  - Press `I` for Instructions.
  - Press `Q` to quit the program.

### 2. Level Selection Menu

- **Levels:**  
  There are 9 different levels (maps) within each difficulty. These vary by the number of pillars, blocks per pillar, and the maximum number of blocks that can be removed in one turn.
- **Navigation:**  
  Use the left and right arrow keys to select the level and press `Enter` to confirm your choice.

### 3. In-Game

- **Gameplay:**
  - The game alternates turns between you and the opponent AI.
  - The player always makes the first move.
  - You win when the opponent AI picks up the last block; you lose if you do.
- **Controls:**
  - **Pillar Selection:** Use the left/right arrow keys.
  - **Block Removal Selection:** Use the up/down arrow keys.
  - **Confirm Move:** Press `Enter`.
- **User Interface:**
  - **Player’s Turn:**
    - The **left section** displays your selected pillar, the number of blocks you intend to remove, and the maximum blocks allowed per turn (indicated by `{N} Blocks Maximum`).
    - The **right section** shows the AI’s last move, including its selected pillar and number of blocks removed.
  - **Opponent AI’s Turn:**
    - The **left section** displays "You need to wait!"
    - The **right section** displays "AI's Turn! thinking".

### 4. Victory / Defeat Page

- After the game concludes, the Victory/Defeated page is shown.
- Press `B` to navigate back to the Main Menu.
