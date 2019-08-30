"""
Copyright 2019 Paul T. Grogan, Stevens Institute of Technology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import division
import json
import numpy as np
import os

from collab import Session, Round

NUMBER_EXPERIMENTS = 10

for seed in range(NUMBER_EXPERIMENTS):
    random = np.random.RandomState(seed)
    training = [
        Round.generate(name='Training Task 1/5 (Individual)', size=1, assignments=[[0],[1],[2],[3]], max_time=90, random=random),
        Round.generate(name='Training Task 2/5 (Individual)', size=2, assignments=[[0],[1],[2],[3]], max_time=120, random=random),
        Round.generate(name='Training Task 3/5 (Pair)', is_coupled=False, size=2, assignments=[[0,1],[2,3]], max_time=270, random=random),
        Round.generate(name='Training Task 4/5 (Pair)', size=2, assignments=[[0,1],[2,3]], max_time=270, random=random),
        Round.generate(name='Training Task 5/5 (Pair)', size=3, assignments=[[0,1],[2,3]], max_time=540, random=random)
    ]
    rounds = [
        #Round.generate(name='Flat Sleep (Individual)', size=2, assignments=[[0],[1],[2],[3]], max_time=120, random=random),
        #Round.generate(name='Economic Motion (Individual)', size=2, assignments=[[0],[1],[2],[3]], max_time=120, random=random),
        #Round.generate(name='Unwritten Experience (Individual)', size=3, assignments=[[0],[1],[2],[3]], max_time=240, random=random),
        #Round.generate(name='Noiseless Stone (Individual)', size=3, assignments=[[0],[1],[2],[3]], max_time=240, random=random),
        #Round.generate(name='Impolite Heat (Individual)', size=4, assignments=[[0],[1],[2],[3]], max_time=600, random=random),
        #Round.generate(name='Arrogant Flame (Individual)', size=4, assignments=[[0],[1],[2],[3]], max_time=600, random=random),
        Round.generate(name='Staking System (Pair)', size=2, assignments=[[0,1],[2,3]], max_time=180, random=random),
        Round.generate(name='Towering Test (Pair)', size=2, assignments=[[0,1],[2,3]], max_time=180, random=random),
        Round.generate(name='Thinkable Ink (Pair)', size=2, assignments=[[0,1],[2,3]], max_time=180, random=random),
        Round.generate(name='Breezy Rain (Pair)', size=2, assignments=[[0,1],[2,3]], max_time=180, random=random),
        Round.generate(name='Better Behavior (Pair)', size=3, assignments=[[0,1],[2,3]], max_time=360, random=random),
        Round.generate(name='Hallowed Sign (Pair)', size=3, assignments=[[1,0],[3,2]], max_time=360, random=random),
        Round.generate(name='Absorbed Copper (Pair)', size=3, assignments=[[1,0],[3,2]], max_time=360, random=random),
        Round.generate(name='Statuesque Name (Pair)', size=3, assignments=[[1,0],[3,2]], max_time=360, random=random),
        #Round.generate(name='Husky Verse (Pair)', size=4, assignments=[[0,1],[2,3]], max_time=720, random=random),
        Round.generate(name='Chief Government (Pair)', size=4, assignments=[[0,1],[2,3]], max_time=720, random=random),
        Round.generate(name='Chemical Rhythm (Pair)', size=4, assignments=[[0,1],[2,3]], max_time=720, random=random)
    ]

    # perform an initial shuffle of the tasks
    random.shuffle(rounds)

    # shuffle rounds until there are no size=4 tasks in first half of session
    while any(sum(rounds[i].tasks[0].num_inputs) == 4 for i in range(0, len(rounds)//2)):
        random.shuffle(rounds)

    session = Session(
        name = 'experiment{:03d}'.format(seed+1),
        num_designers = 4,
        error_tol = 0.05,
        training = training,
        rounds = rounds
    )

    # write experiment files to the server app directory
    with open(os.path.join('..', 'app', 'experiment{:03d}.json'.format(seed+1)), 'w') as out_file:
        json.dump(session, out_file, default=lambda o: o.__dict__)
