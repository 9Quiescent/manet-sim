# MANET-Sim: Mobile Ad Hoc Network Visualiser & Simulator--
An open-source, lightweight project for real-time visualisation and simulation of mobile ad hoc networks (MANETs). Devices are displayed as nodes (circles) with dynamic peer-to-peer wireless connections (lines). In-range nodes automatically connect and exchange messages, modeling real-world ad hoc network behavior.

# FEATURES
-**Real-time visualisation:** See nodes move and links form/break as devices enter or leave range.

-**Peer-to-peer messaging:** Nodes within range can send and relay messages.

-**Dynamic topology:** Add/remove/move nodes to see the network adapt live.

-**Lightweight security:** Input validation, simple message signing, and static code analysis with Bandit.

-**Docker-ready:** Run nodes in isolated containers to simulate distributed deployments.

# USAGE WITHOUT DOCKER
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

python main.py

# USAGE WITH DOCKER
## Clone The Project
Open A Terminal and run the following commands to clone the repository:
```bash
git clone https://github.com/9Quiescent/manet-sim.git
cd manet-sim
```
## Build the Docker image:
```bash
docker build -t manet-sim. (Dependencies Are automatically handled by the docker file.)
```
## Run The Simulator!
```bash
docker run --rm -it manet-sim
```

# BASIC SECURITY CONSIDERATIONS
Input validation on all node and message data.

Basic message integrity check with SHA256 signatures.

Static code analysis using Bandit (bandit -r .).

# CREDITS
Developed by Dennis Kalongonda
