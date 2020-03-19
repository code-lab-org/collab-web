from collab import Session, Task, Action
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def random_walk(session, task, random):
    # main loop to keep walking until the task is solved
    while not task.actions[-1].isSolved(session, task):
        # randomly choose which design variable shall be changed
        design_var = random.choice(range(len(task.inputs)))
        # randomly choose the sign of the change (down or up)
        delta_sign = random.choice([-1,1])
        # randomly choose the size of the change (small or big)
        delta_size = random.choice([0.01, 0.1])
        # copy over the previous inputs
        design = task.actions[-1].input.copy()
        # change the selected design variable by the selected amount (with bounds between -1 and 1)
        design[design_var] = min(1, max(-1, design[design_var] + delta_sign*delta_size))
        # append the action to the task
        task.actions.append(Action(datetime.now().timestamp(), design))
    # log the completion time
    task.time_complete = datetime.now().timestamp()

# initialize the random number stream for generating tasks
rng_generate = np.random.RandomState(0)

# initialize the random number stream for generating behavior
rng_behavior = np.random.RandomState(0)

# build a session (required to set the error tolerance value)
session = Session(name='test', num_designers=1, error_tol=0.05)

# build a task (one-designer, two variables)
task = Task.generate(designers=[0], size=2, random=rng_generate)

# set the task start time
task.time_start = datetime.now().timestamp()

# set the initial task action
task.actions = [Action(time=datetime.now().timestamp(), input=[0,0])]

# execute random walk algorithm
random_walk(session, task, rng_behavior)

# print the results
print('finished the task in {:f} milliseconds and {:d} actions'.format(task.getDuration(), len(task.actions)))

# plot the results
plt.plot([a.getElapsedTime(task) for a in task.actions], [a.getErrorNorm(task) for a in task.actions], '-r')
plt.ylabel('Normalized Error')
plt.xlabel('Time (ms)')