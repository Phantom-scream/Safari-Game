# 🐘 Safari Park Simulator

**Team Name:** Dolma  
**Team Members:** Aliev Aikhan, Hasanli Ramal, Hajiyev Hajiaga  

## 🎮 Game Description

Safari Park Simulator is a 2D top-down wildlife management game where players run an African safari park. You’ll manage animal populations, build infrastructure, attract tourists, and protect your park from poachers—all while ensuring the ecosystem thrives.

Key gameplay features include:
- Dynamic animal behavior
- Real-time strategy mechanics
- Randomly generated maps
- Poacher threats and park defense
- Scalable time controls (hour/day/week)
- Financial and ecological balance

---

## 🧩 Subtasks & Features

### ✅ Core Gameplay
- **Safari Park Management:** Buy animals, place resources, and build roads/jeeps.
- **Autonomous Animals:** Seek food, water, and safety on their own.
- **Tourist Interaction:** Tourists explore the park via rented jeeps, generating income.

### 🗺 Mini Map
- Real-time overview of the park
- Clickable for fast navigation

### 🦹 Poachers
- Appear randomly
- Attempt to hunt or capture animals

### 🌍 Procedural Map Generation
- Unique layout for every game session
- Logical placement of terrain, water, and foliage

### 🧱 Terrain Obstacles
- Includes hills and rivers
- Affects movement, visibility, and pathfinding
- Terrain difficulty varies per animal species

### 🌙 Day-Night Cycle *(4th Milestone)*
- Real-time cycling of day and night
- Affects gameplay dynamics

### 🎯 Win/Loss Conditions
- **Win:** Sustain a stable, profitable park for a set duration
- **Loss:** All animals die or you go bankrupt

---

## 📋 Functional Requirements

- **Purchasables:** Animals, plants, roads, jeeps
- **Real-time Map Updates:** Mini map reflects environment changes
- **Autonomous AI:** Animals and poachers behave independently
- **Pathfinding:** Accounts for terrain type and obstacles
- **Navigation:** Keyboard + mouse input
- **UI:** Clear layout, accessible fonts/colors, tooltips

---

## 🛠 Non-Functional Requirements

### ⚙ Technology Stack
- **Language:** Python  
- **Engine/Library:** Pygame (2D rendering & event handling)  
- **UI:** Pygame UI / Tkinter (menus, buttons)

### 🚀 Performance
- Minimum 30 FPS
- Memory-efficient design for large, active maps
- Optimized AI logic for real-time decision-making

### 💻 Usability & Accessibility
- Responsive controls
- Tooltips for interface elements
- Distinct, readable visuals

### 📈 Scalability
- Supports various map sizes without FPS drops
- Modular architecture for future expansions

### 🖼 Graphics & Rendering
- Sprite-based 2D rendering using Pygame
- Techniques like sprite batching and pre-loading assets
- Animated animals and vehicles to enhance immersion
