Team name: Dolma.
Team members: Aliev Aikhan, Hasanli Ramal, Hajiyev Hajiaga.
Game Description:
The game is a 2D top-down safari management simulation where players run an African wildlife park. Players must manage animals, build infrastructure, and attract tourists to generate income. The game features dynamic animal behavior, poachers, and procedurally generated maps. Players can adjust game speed (hour/day/week), place plants and water sources, and handle financial decisions. The goal is to maintain a thriving safari while preventing extinction and bankruptcy.
SubTasks:

Mini map
Poachers
Map Generation
Terrain Obstacles
Day-Night Cycle(for the 4th milestone.)

Functional Requirements:
Safari Park Management

Players can purchase animals, plants, roads, and jeeps.
Animals behave autonomously, seeking food, water, and safety.
Tourists rent jeeps to explore the safari, generating revenue.

Mini Map Functionality

Displays an overview of the safari.
Clickable areas allow quick navigation.
Updates in real-time to reflect environmental changes.

Poacher System

Poachers appear randomly and attempt to hunt or capture animals.

Procedural Map Generation

The game generates different maps for each session, affecting replayability.
Algorithms ensure logical placement of terrain, water, and foliage.

Terrain Obstacles Implementation

Hills and rivers affect movement and visibility.
Certain animals may traverse obstacles more easily than others.
Pathfinding accounts for different terrain difficulties.

Day-Night Cycle Mechanics

The game cycles between day and night dynamically.

Game Win/Loss Conditions

Players win by maintaining a stable safari for a certain period, based on difficulty.
The game ends if all animals die or if the player goes bankrupt.

Non-Functional Requirements:
Technology Stack

Programming Language: Python
Game Engine/Library: Pygame (for 2D graphics and event handling)

Performance Requirements

The game run at a minimum of 30 FPS.
Efficient memory management to handle large maps and dynamic elements.
AI (such as animal movement and poacher behavior).

Usability and UI

User Interface: Tkinter or Pygame’s built-in UI elements for menus and buttons.
Input Handling: Keyboard and mouse support for navigation and interaction.
Accessibility: Clear font sizes, distinguishable colors, and tooltips for game elements.

Scalability

The game supports different map sizes without significant performance drops.
Modular code structure to allow easy expansion (adding more animals, new obstacles).
The AI system is designed for scalability, allowing for more complex behaviors in future updates.

Graphics & Rendering

Sprite-based 2D rendering using Pygame.
Optimization techniques like sprite batching and pre-loading assets to reduce lag.
Animations for animals and vehicles to enhance visual appeal.
