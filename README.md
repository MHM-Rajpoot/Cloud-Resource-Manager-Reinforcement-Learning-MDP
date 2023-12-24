# Cloud Resource Manager - Reinforcement Learning

Cloud Resource Manager is a system designed for managing cloud resources using a Reinforcement Learning approach based on Markov Decision Process (MDP).

## Overview

This system consists of two main components:

1. **User Management System**
    - Manages user login, registration, and resource allocation.
    - Utilizes reinforcement learning principles to allocate and deallocate resources based on user behavior.
    - Tracks user usage patterns and optimizes resource allocation.

2. **Root System**
    - Manages overall system state and resource availability.
    - Utilizes Markov Decision Process (MDP) to make decisions on reserving and unreserving cloud resources.
    - Manages user rewards based on system usage patterns.

## How It Works

### User Management System

- Users can log in, register, and interact with the system.
- The system monitors and updates user resource usage in real-time.
- Users can allocate and deallocate resources based on their needs.
- The system uses reinforcement learning to optimize resource allocation and deallocation.

### Root System

- Manages overall system state and resource availability.
- Utilizes Markov Decision Process to decide when to reserve and unreserve cloud resources.
- Manages user rewards based on system usage patterns.
- Allocates and deallocates resources based on user behavior and system state.

## Usage

1. **Installation**
    ```bash
    # Clone the repository
    git clone https://github.com/your_username/Cloud_Resource_Manager.git
    cd Cloud_Resource_Manager

    # Install dependencies (if any)
    # Add any specific instructions for setting up the environment
    ```

2. **Run the System**
    ```bash
    # Run the user and root systems
    python user_system.py
    python root_system.py
    ```

3. **Interact with the System**
    - Follow the on-screen prompts to log in, register, and interact with the system.
    - Observe the resource allocation and system behavior based on user actions.

## Contributions

Contributions are welcome! If you have ideas for improvements, new features, or bug fixes, feel free to submit a pull request.

## License

**This project is for Demonstration purposes only. Use it for non-profitable and non-commercial purposes only.**

---

**Cloud Resource Manager** is a project developed for educational and learning purposes.
