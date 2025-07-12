# MANET-Sim: Mobile Ad Hoc Network Visualiser & Simulator--
An open-source, lightweight project for real-time visualisation and simulation of mobile ad hoc networks (MANETs). Devices are displayed as nodes (circles) with dynamic peer-to-peer wireless connections (lines). In-range nodes automatically connect and exchange messages, modeling real-world ad hoc network behavior.

# FEATURES
-**Real-time visualisation:** See nodes move and links form/break as devices enter or leave range.

-**Peer-to-peer messaging:** Nodes within range can send and relay messages.

-**Opt-in participants:** Nodes can opt in or out of being ad-hoc participants.

-**Dynamic topology:** Add and move nodes to see the network adapt live.

-**Lightweight security:** Simple encryption simulation.

-**Docker-ready:** Project runs in a sandboxed container to simulate distributed deployments.

## Prerequisite: Docker Installation
To quickly test logic without dealing with OS-specific quirks and needing to manually install dependencies, ensure you have docker installed to on your machine. 
This will let you run a sandboxed version of the program suited to your operating system (note that this is at the cost of the GUI), please install Docker for your platform:

- **[Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)**
- **[Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)**
- **[Docker for Linux](https://docs.docker.com/engine/install/)**

After installing, launch Docker Desktop (if needed) and ensure the `docker` command works in your terminal:
```bash
docker --version
```

> **NOTE: Before running any Docker commands (USAGE WITH DOCKER), make sure Docker Desktop is installed and running.**
> - On Mac, Linux and Windows, launch Docker Desktop from your Applications (or Start Menu) before opening your terminal.
> - Wait until the Docker whale icon appears in your menu bar or system tray.
> - Once running, the `docker` command will be available in your terminal.

# USAGE WITHOUT DOCKER (Manual) - USE THIS FOR THE GUI.
## Clone The Project
Open A Terminal and run the following commands to clone the repository:
```bash
git clone https://github.com/9Quiescent/manet-sim.git
cd manet-sim
```
## Install Project Dependencies
Within the same Terminal, install the project's dependencies by running this command:
```bash
pip install -r requirements.txt
```
## Run The Simulator!
Then run the simulator using this command.:
```bash
python main.py
```


# USAGE WITH DOCKER (Automatic)
## Note that using Docker here = No GUI, by default Docker has no display access.
## Clone The Project
Open A Terminal and run the following commands to clone the repository:
```bash
git clone https://github.com/9Quiescent/manet-sim.git
cd manet-sim
```
## Build the Docker image (Do this on the first run and anytime changes are made to the project):
```bash
docker build -t manet-sim. (Dependencies Are automatically handled by the docker file.)
```
## Run The Simulator! (Do this everytime you want to run the project)
```bash
docker run --rm -it manet-sim
```

# BASIC SECURITY CONSIDERATIONS
Simulated E2EE  on the user end in the GUI.

Static code analysis using Bandit 
```bash 
bandit -r ..
```
# CREDITS
Developed by Dennis Kalongonda
