# Pygame Game Boilerplate

A comprehensive, feature-rich boilerplate for pygame game development, perfect for game jams and rapid prototyping.

## Features

- **State Management**: Intro, Game, Pause, and Game Over states
- **Delta Time**: Frame-rate independent movement
- **Scrolling Background**: Infinitely scrolling vertical background
- **Collision Detection**: 
  - Rectangle-Rectangle collision
  - Circle-Circle collision
  - Stub for pixel-perfect collision
- **Animation System**: Simple frame-based animation
- **Particle System**: For explosions, effects, etc.
- **Sound Support**: Music and SFX integration
- **Text Input**: For player names or commands
- **Basic Enemy System**: Spawning and movement

## Prerequisites

- Python 3.6+
- Pygame

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install pygame
```

## Running the Game

Once you've installed the dependencies, run the game with:

```bash
python game.py
```

## Controls

- **W, A, S, D**: Move player
- **P**: Pause/unpause game
- **ENTER**: Start game from intro screen
- **R**: Restart game after game over
- **ESC**: Quit game
- **Typing**: Enter name in the intro screen

## Structure

The boilerplate uses a state machine architecture with dedicated update and draw methods for each state:

- `STATE_INTRO`: Title screen with name input
- `STATE_GAME`: Main gameplay
- `STATE_PAUSE`: Paused game state
- `STATE_GAME_OVER`: End game state

## Customization

This boilerplate is designed to be customized for your specific game:

- Modify constants at the top of the file to adjust window size, colors, etc.
- Replace placeholder graphics with your own game assets
- Adjust player and enemy behaviors in their respective update methods
- Add your own game mechanics by extending the existing systems

## For Game Jam Participants

1. **Start with minimal changes**: Get familiar with the code structure before making major modifications
2. **Asset integration**: Use `pygame.image.load()` to add your sprites
3. **Game mechanics**: Modify the update methods to implement your unique gameplay
4. **Sound effects**: Uncomment the audio sections and add your own sounds
5. **Performance**: The code includes collision optimizations and particle system with automatic cleanup

## License

This boilerplate is free to use for any purpose, commercial or non-commercial.

---

Happy jamming!