---
title: "Pacman"
date: 2026-04-01T17:05:11Z
draft: true
categories: ["comp-science"]
tags: []
description: "A short summary shown in post listings."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

This is going to be a longish one. Pacman is of course the classic arcade game. And a gem it is. We forget how good these programmers were, given the limited tool back in the day.

To rewind, it was 1980. Pac-Man was designed by Toru Iwatani head of a nine-man team; the game's development began in early 1979. Nine, yes, less than 10 people. Those were the days. in 1974 he started game creation, at 24. A young person's game then, as is now. They wanted to appeal to women gamers. Visionary in so many ways. The arcade system was Z80A processor, running at 3.072 MHz, 16 kbyte of ROM and 3 kbyte of static RAM. Those are tiny, minuscule numbers by todays standards. This was proper low level programming, where hardware was just as relevant as software. You had to make it work, no github to help. I have so much respect for these early programmers, they faced serious constraints in memory and processing power, but used their imagination to create lasting works of imagination.

Decent overview is on wikipedia. I love that the game was an antidote to "violent" shooter games. If only they were around today to see MoH, insert first person shooter of choice, et al.

---

![Pacman for python](https://pacmancode.com)

---

Anyways. Why? Well its been done before, so no big deal. But at some point in the future I need to train device navigation, and as I know very little (nothing) about that, why not start with machine learning in a maze, with degree of prioritization. Worst case I learned something.

Side note, I tried to one shot this on a nameless AI starting with G, ending in T. It might have had a P in the middle, who knows. Well, about 200 ish mostly manual revisions later, it worked. Should have just done it the hard way by co opting some additional git hubs. Nevermind, got there in the end. Did the trick for forcing me to learn a lot of programming. Funny that.

![Old school hardware](https://www.arcade-museum.com/manuals-videogames/P/Pac-Man.pdf)

Now, this is machine learning exercise, not a game to play. You can find pacman game in python in many places. Go ahead and do that, its still worth it. But they won't work for training agents. So sadly, this is a fairly ugly one, but it was as faithful to the original as I could make it for the intended purpose.

add paper that was inspiration here too.
---

---

### Requirements

This entire package is quite lean given the limted graphics. The shell script refernces the requirements file, which only contains the following:

```
numpy
matplotlib
torch
scipy
```
Only is a bit of a stretch considering what in torch... but its a lean install on purpose.

## Solving the Maze

This took ages, and ages to get right. I ended up splitting it out to a stand alone file I got so sick of editing it. Is also nicer programming to separate it out. Don't stress about code, I will provide full working version on github.

![The simplifed maze](/images/pacman/maze_start.png)

Pretty, no, but it is functional. It is based off Pacman medium grid starting level. There are no other levels in this version of the game, they are not needed and only add to complexity without adding much to the learning.

For anyone interested, who does not want the whole github repo, this the code section:

```
maze.py — Classic Pac-Man arcade maze (28 cols × 31 rows)

# ---------------------------------------------------------------------------
# 28 × 31 flat array, row-major (row 0 = top)
# W=wall  .=dot  o=power  _=empty  T=tunnel(empty)
# ---------------------------------------------------------------------------
_SRC = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",  #  0
    "W............WW............W",  #  1
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  #  2
    "WoWWWW.WWWWW.WW.WWWWW.WWWWoW",  #  3  power pellets
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  #  4
    "W..........................W",  #  5
    "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",  #  6
    "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",  #  7
    "W......WW....WW....WW......W",  #  8
    "WWWWWW.WWWWW.WW.WWWWW.WWWWWW",  #  9
    "WWWWWW.WWWWW.WW.WWWWW.WWWWWW",  # 10
    "WWWWWW.WW__________WW.WWWWWW",  # 11
    "WWWWWW.WW.WWWWWWWW.WW.WWWWWW",  # 12
    "WWWWWW.WW.W______W.WW.WWWWWW",  # 13
    "TTTTTTTT__W______W__TTTTTTTT",  # 14  tunnel row — fully open left/right corridors
    "WWWWWW.WW.W______W.WW.WWWWWW",  # 15
    "WWWWWW.WW.WWWWWWWW.WW.WWWWWW",  # 16
    "WWWWWW.WW__________WW.WWWWWW",  # 17
    "WWWWWW.WW.WWWWWWWW.WW.WWWWWW",  # 18
    "WWWWWW.WW.WWWWWWWW.WW.WWWWWW",  # 19
    "W............WW............W",  # 20
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  # 21
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  # 22
    "Wo..WW................WW..oW",  # 23  power pellets
    "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",  # 24
    "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",  # 25
    "W......WW....WW....WW......W",  # 26
    "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",  # 27
    "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",  # 28
    "W..........................W",  # 29
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",  # 30
]

MAZE_ROWS = 31
MAZE_COLS = 28

_TILE = {'W': 0, '.': 1, 'o': 3, '_': 2, 'T': 2, ' ': 2}

_MAZE_FLAT = [_TILE[ch] for row in _SRC for ch in row]
```
Did not say it looked pretty, but it renders as per above image. And it is functional.

---

## The rest

Here is the basic file structure of the project, just at level 2, eg run this version of tree. Tree is great, I use this all the time across larger project. Highly recommend you install this wonderful tool. This is CLI gold dust, I'll add a tiny explainer under software, to remind my self of the commands as much as anything.

```
brew install tree
tree -L 3 -d
```


```
.
├── configs
├── logs
├── models
├── movement_logs
├── pac4_backup
├── runs
│   ├── run_20260411_111825
│   │   └── gifs
│   └── run_20260411_111914
│       └── gifs
├── src
│   ├── __pycache__
│   ├── agent
│   │   └── __pycache__
│   ├── env
│   │   └── __pycache__
│   ├── eval
│   │   └── __pycache__
│   └── training
│       └── __pycache__
└── venv
    ├── bin
    ├── include
    ├── lib
    │   └── python3.14
    └── share
        └── man

```
It sort of gives you a hint as to the approach. The key files are contained in the expected folders. It is all set up to run from a single bash command that runs everything, include python dependencies. Of which there are very few, as its done in old school programming fashion to make sure it runs cleanly. Then all results are stored down. Now all key settings are in csv files, more on that later.

Files will be in the github repository, but I will go over the key parts of the main one's here for contextual explainer.

[2015 Human-level control through deep reinforcement learning](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf)

There is nothing original in this, as in my work, the above is the foundational paper for RL approach to this. Note this version has basic digitized game. It is possible to repeat this with actual physical game, using video camera to record game screen live, and then simple GPIO tapped into the controller circuit to permit agent to provide actual inputs to game. A robot to move the joystick would be fun, but is overkill really. I do plan on doing this version with an actual console at some point (minus the robot), but too many projects are already sitting on the list. Its also a lot more work and compute to train through graphics, so that is the main reason not to try at this point.

---
## Training - how it works

Here is an overview of the process. Now do mind this reflects the final state of the files, it took me something like 200+ revisions to get it all stable and this neat.

![Training Process Map](./static/images/pacman/agent_learning_flow.png)




### Just the key bits...

#### Summary of train.py
train.py is the top-level orchestrator. It takes two inputs (episodes, max steps), creates a timestamped run folder, then runs the main training loop: for each episode it resets the environment, steps through it action by action calling agent.act() and agent.train() every step, logs results to CSV, and tracks the worst early episode for GIF replay. After the loop it saves the model, captures two GIFs (worst early episode + final greedy run), saves three dark-mode training charts (reward/score, raw scores with rolling mean, epsilon decay), and finally calls build_report() which generates the dashboard, summary CSVs, conclusion text, and path heatmap. Nothing is shown on screen — everything writes to disk.

#### Summary of dqn_agent.py
Three classes working together:
Net is the neural network — a feedforward network with layers 10→512→512→256→4. Input is the 10-dimensional state vector. Output is four Q-values, one per action (UP/DOWN/LEFT/RIGHT). The Q-value for an action represents the expected future discounted reward if that action is taken from the current state and the agent behaves optimally thereafter.
ReplayBuffer is a circular memory of up to 200,000 past transitions (state, action, reward, next_state, done). Rather than learning from each experience immediately and discarding it, the buffer stores them all and training samples random batches. This breaks the temporal correlation between consecutive steps — without it, the network would overfit to whatever the agent is currently doing and forget earlier experience.

Agent ties everything together. act() uses epsilon-greedy selection: with probability ε it picks a random action (exploration), otherwise it passes the state through the network and picks the highest Q-value action (exploitation). train() samples a batch of 128 transitions, computes the current Q-values from the online network, computes target Q-values using the Double DQN formula — the online network selects the next action, but the frozen target network evaluates it. This separation prevents the moving-target problem where the network chases its own predictions. The Huber loss is more stable than MSE for large reward outliers. Gradients are clipped at norm 10 to prevent a single large reward from blowing up the weights. decay_epsilon() is called once per episode, slowly reducing random exploration over ~1150 episodes. update_target() hard-copies online weights to the target network every 10 episodes.

Sounds easy, wasn't to get it all working.

In the world of AI and a lot of nonsense talk about agents, lets look at the code for an old school agent. It's really not much code, so other than the import dependancy statements the whole thing is reproduced here in full:

```
# --- Neural Network ---
# Deeper and wider to handle 28x31 maze complexity.
# Input is now 10D (was 7D) — see get_state() in pacman_env.py.
class Net(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 4),
        )

    def forward(self, x):
        return self.net(x)


# --- Replay Buffer ---
class ReplayBuffer:
    def __init__(self, capacity=200_000):
        self.buffer = deque(maxlen=capacity)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.FloatTensor(np.array(states)),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(np.array(next_states)),
            torch.FloatTensor(dones),
        )

    def __len__(self):
        return len(self.buffer)


# --- Agent ---
class Agent:
    def __init__(self, input_dim):
        self.model  = Net(input_dim)
        self.target = Net(input_dim)
        self.target.load_state_dict(self.model.state_dict())
        self.target.eval()

        # Lower LR — prevents good experiences being overwritten by noisy updates
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0002)

        self.buffer = ReplayBuffer(capacity=200_000)

        # gamma=0.99: agent plans further ahead, values pellets 20+ steps away
        self.gamma      = 0.99
        self.batch_size = 128

        # --- Exploration ---
        # decay=0.998/episode: epsilon reaches floor at ~ep 1150 out of 5000
        # This keeps meaningful exploration for the first 23% of training
        # rather than locking in after just 1.5% (old decay=0.97)
        self.epsilon       = 1.0
        self.epsilon_min   = 0.15   # higher floor = more diversity, escapes local optima
        self.epsilon_decay = 0.998  # floor ~ep 1150 (was 0.97 → floor at ep 77)

        self._train_steps = 0

    def act(self, state, epsilon=None):
        eps = epsilon if epsilon is not None else self.epsilon
        if random.random() < eps:
            return random.randint(0, 3)
        state_t = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_t)
        return torch.argmax(q_values).item()

    def decay_epsilon(self):
        """Call once at the end of each episode."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train(self):
        if len(self.buffer) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.buffer.sample(self.batch_size)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_actions = self.model(next_states).argmax(dim=1)
            next_q       = self.target(next_states).gather(1, next_actions.unsqueeze(1)).squeeze(1)
            target_q     = rewards + self.gamma * next_q * (1.0 - dones)

        loss = nn.SmoothL1Loss()(q_values, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=10)
        self.optimizer.step()

        self._train_steps += 1

    def update_target(self):
        """Sync target network. Call from train.py every N episodes."""
        self.target.load_state_dict(self.model.state_dict())

```

---

---
## Training Runs

For the final run, once the code was stabilized, training was run for 10,000 episodes to see how training improved the results. Now, the way the agent works is, like a human, it can 'see' all the items on the maze grid at every point.

---

### The results

Well, so much for the theory. Code ran, dashboard was fine, it all worked. Perfect? Ah, no. The heatmap showed a concentration in movements. The agent was essentially running around a set area, prioritizing survival by going back and forth. The factors driving the explore / exploit mechanism were not properly running. Long story short, re did the whole code base. Instead of using embedded factors, everything is now run straight for config files. Each run now imports all training factors based in a single csv. In this manner the training can be tested across variations of training factors, with all else being kept as it. This is now includes the steps and episodes data. All the results data is still generated and dumped into a run folder, to permit examination of runs against factor choices. This took me a about a week of faffing around to get it all stable.

before we move, here is a table showing the variations of the heat maps. You can see the concentration in the agent locations. This is the before, if you like. They are in date order. I only did the a small batch, deleting a lot of the original runs as they were noise. This is visual hint only, not a parametric assessment across the factors. That comes last. Here it, in date order of run.

![Pacman Heatmap history](/static/images/pacman/heatmap_aggregate_20260411.png)


---


### The results v2.0


Drum roll please, here are the outputs. This is all saved down under each run into a folder. The actual bash script just has the inputs only, the outputs are generated and saved for each run.

So, assuming you run the package from the single .sh file, it will generate the following in the terminal. FYI for the sake of it, I did this last run on 10,0000 episodes. In reality, this is a bit of overkill, bu hey ho, that is what compute is for. Here is the terminal output:

```
Ep 10000/10000 | avg reward:  -784.7 | avg score:  164.0 | epsilon: 0.150 | dist:  82 | survived: 204

[INFO] Model saved → runs/run_20260407_104447/trained_model.pth

[GIF] Capturing worst-of-first-50 replay  (ep 12, score 10) ...
[GIF] Saved 11 frames → runs/run_20260407_104447/gifs/worst_first50_ep0012.gif
[GIF] Capturing final trained run (greedy, epsilon=0) ...
[GIF] Saved 300 frames → runs/run_20260407_104447/gifs/final_trained_score130.gif
[GIF] Final run score: 130

[PLOT] Saving dark-mode training charts ...
[PLOT] Saved → runs/run_20260407_104447/training_reward_score.png
[PLOT] Saved → runs/run_20260407_104447/score_per_episode.png
[PLOT] Saved → runs/run_20260407_104447/epsilon_decay.png

[REPORT] Building dashboard and conclusion ...
[WARN] scipy not installed — linear trend skipped. Run: pip install scipy
[REPORT] Summary CSV  → runs/run_20260407_104447/run_summary.csv
[REPORT] Decile CSV   → runs/run_20260407_104447/decile_summary.csv
[REPORT] Dashboard    → runs/run_20260407_104447/dashboard.png
[REPORT] Conclusion   → runs/run_20260407_104447/conclusion.txt
[REPORT] GIF player   → runs/run_20260407_104447/gif_player.html
[REPORT]   Copy to Hugo: static/tools/pacman/gif_player.html
[REPORT]   Copy GIFs:   static/tools/pacman/worst_first50_ep0012.gif
[REPORT]                static/tools/pacman/final_trained_score130.gif
[REPORT] Heatmap      → runs/run_20260407_104447/pacman_heatmap.png

=== TRAINING COMPLETE ===
Run folder: runs/run_20260407_104447/
  score_timeseries.csv     — episode-by-episode data
  run_summary.csv          — headline stats CSV
  decile_summary.csv       — stats by 10% training blocks
  dashboard.png            — 9-panel visual report
  training_reward_score.png
  score_per_episode.png
  epsilon_decay.png
  conclusion.txt           — plain-English run summary
  trained_model.pth
  gifs/                    — animated episode replays

Next: python -m src.eval.compare

========================================
   TRAINED vs UNTRAINED COMPARISON
========================================
[INIT] DQN Agent
[INFO] Using run folder: runs/run_20260407_104447
[INFO] Loaded trained model from runs/run_20260407_104447/trained_model.pth

--- Running 50 episodes: UNTRAINED agent ---
  [Untrained] ep 10/50 — score 40
  [Untrained] ep 20/50 — score 20
  [Untrained] ep 30/50 — score 50
  [Untrained] ep 40/50 — score 50
  [Untrained] ep 50/50 — score 30

--- Running 50 episodes: TRAINED agent ---
  [Trained] ep 10/50 — score 170
  [Trained] ep 20/50 — score 160
  [Trained] ep 30/50 — score 150
  [Trained] ep 40/50 — score 170
  [Trained] ep 50/50 — score 150

[INFO] Per-episode comparison saved → runs/run_20260407_104447/comparison.csv

============================================================
METRIC                          UNTRAINED      TRAINED  CHANGE
============================================================
  Avg Score                          37.4        155.0  ▲ 117.6
  Score Std Dev                      16.2         69.9  ▲ 53.7
  Max Score                           110          450  ▲ 340.0
  Min Score                            10           30  ▲ 20.0
  Avg RL Reward                    -977.9       -299.4  ▲ 678.5
  Avg Distance                        7.9         86.6  ▲ 78.7
  Avg Survival Steps                 14.3        274.3  ▲ 260.0
  Avg Pellets Left                  255.3        243.6  ▼ 11.7
  Win Rate %                          0.0          0.0  – 0.0
============================================================
[INFO] Summary saved → runs/run_20260407_104447/summary.csv
[INFO] Comparison plot saved → runs/run_20260407_104447/comparison_plot.png

=== COMPARISON COMPLETE ===
Files saved to runs/run_20260407_104447/:
  comparison.csv      — per-episode data for both agents
  summary.csv         — headline metrics side by side
  comparison_plot.png — score chart, distribution, key metrics
========================================
[INFO] Comparison results saved to ./runs/run_20260407_104447/

[INFO] All done!
[INFO] Outputs → ./runs/run_20260407_104447/

  score_timeseries.csv     episode-by-episode data
  run_summary.csv          headline stats
  decile_summary.csv       stats by 10% block
  dashboard.png            9-panel visual report
  training_reward_score.png
  score_per_episode.png
  epsilon_decay.png
  conclusion.txt           plain-English run summary
  comparison.csv           trained vs untrained per episode
  summary.csv              trained vs untrained headline
  comparison_plot.png      trained vs untrained charts
  pacman_heatmap.png       Pac-Man path heatmap
  trained_model.pth
  gifs/                    animated episode replays

[INFO] Movement logs → ./movement_logs/
```

## Training Output

Each training run produces a timestamped folder under `runs/run_date_time` naming convention containing all outputs. The files are as named in the output above, with data saved as csv files and also as png files for ease of review. Prior files are not overwritten.

---

### Dashboard

The full panel training dashboard summarises every aspect of the run in a single dark-mode figure — score trajectory, cumulative distribution, reward trend, survival, distance, epsilon schedule, pellets remaining, score distribution by quintile, and reference tables for scoring rules and ghost behaviour. It was informed from the google paper, but at no point did I copy the source code from that paper. This project is likely somewhat unique in its implementation given the series of fixes and file changes over time.

![Training Dashboard](/images/pacman/dashboard.png)

---

### Score Over Time

Raw episode scores (scatter) with a 20-episode rolling mean and windowed average overlaid. The upward trend confirms the agent is learning to collect more pellets and survive longer as training progresses.

![Score Per Episode](/images/pacman/score_per_episode.png)

---

### Reward and Score Trend

RL reward (top) and game score (bottom) averaged in 10-episode windows across the full run. The reward signal climbs from strongly negative early on (frequent deaths, no pellets) toward positive values as the agent learns ghost avoidance and pellet routing.

![Training Reward and Score](/images/pacman/training_reward_score.png)

---

### Exploration Schedule

Epsilon decays from 1.0 (fully random) toward the minimum floor of 0.15 over the course of training. With `decay=0.998` per episode the agent remains in meaningful exploration for the first ~1150 episodes before committing to a greedy policy — preventing the early lock-in that caused the flat plateau seen in earlier runs.

![Epsilon Decay](/images/pacman/epsilon_decay.png)

---

### Trained vs Untrained Comparison

50 evaluation episodes each, trained agent at `epsilon=0` (fully greedy), untrained agent at `epsilon=1.0` (fully random).

![Comparison Plot](/images/pacman/comparison_plot.png)

#### Summary Table

Extract csv file here.

---

### Score Distribution by Training Quintile

Performance broken into five equal blocks of the training run. The median and upper quartile rise steadily across quintiles, while the lower quartile remains anchored near zero — reflecting episodes where the agent encounters an unlucky ghost position early and dies before collecting many pellets.




---

### Episode Movement Logs

Every training episode writes a row-by-row movement log to `movement_logs/`. Each file records Pac-Man position, both ghost positions, score, reward, scared timer, and done flag at every step — useful for debugging agent behaviour or replaying specific episodes.



---

### Animated Replays

Two GIFs are saved automatically after each run.

**Worst episode in first 50** — shows the agent at its most confused, typically dying within a few steps of the ghost spawn.

**Final greedy run** — the trained agent at `epsilon=0`, showing the learned policy in action.

---

### Run Statistics





---

need to re run with comparison plot in dark mode added to runs folder each time, also with output score table that bash prints as csv file each time, for every run. Need to explain epsilon decay.

---
### Epsilion function

The epsilon (ε) factor in reinforcement learning controls how often an agent explores new actions versus exploiting what it already knows. In methods like Q-learning, a higher ε means more random exploration, while a lower ε makes the agent choose the best-known action more often. Typically, ε starts high and gradually decreases over time, allowing the agent to first learn about its environment and then optimize its behaviour based on that knowledge.

- controls randomness in action selection  
- High ε = exploration  
- Low ε = exploitation  
- Decay of ε = transition from learning → optimisation  


---
## References

- [Source title](https://url.com)
