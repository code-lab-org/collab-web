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

import json
import os.path
import re
import numpy as np

from .model import Session, Round, Task, Action

class PostProcessor(object):
    """
    Performs post-processing functions on experimental data.
    """
    def __init__(self, logFile, jsonFile=None):
        """
        Loads experimental results from file.

        @param logFile: the experimental log file
        @type logFile: str

        @param jsonFile: the experimental json file
        @type jsonFile: str

        @param errTolerance: the error tolerance
        @type errTolerance: float
        """

        # parse json file to instantiate session, rounds, and tasks
        with open(jsonFile) as jsonData:
            sessionJson = json.load(jsonData)
            self.session = Session.parse(sessionJson)

        # parse log file to instantiate actions
        with open(logFile) as logData:
            session = None
            round = None

            # iterate over each line in log
            for line in logData.read().splitlines():
                # parse time, type, and content fields
                data = line.split(';')
                time = int(data[0])
                type = data[1]
                content = json.loads(data[2])

                # handle opened event: check for session match
                if type == 'load':
                    if content == self.session.name:
                        session = self.session
                    else:
                        session = None

                # handle initialized event: append initial action to corresponding task
                elif type == 'round' and session is not None:
                    # find the round corresponding to the name
                    round = next((t for t in session.training + session.rounds if t.name == content))
                    # set round start time
                    round.time_start = time
                    for task in round.tasks:
                        # append an action with initial inputs and outputs
                        task.time_start = -1
                        task.current_input = np.zeros(np.sum(task.num_inputs))
                        task.actions = [Action(
                            time = time,
                            input = task.current_input.copy()
                        )]
                # handle updated event: append new action to corresponding task
                elif type == 'action' and round is not None:
                    designer = content.get('designer')
                    input = content.get('input')
                    task = round.getDesignerTask(designer)
                    # skip actions with no change in inputs
                    if not np.array_equal(task.current_input[np.array(task.inputs) == designer], input):
                        if task.time_start < 0:
                            task.time_start = time
                        task.current_input[np.array(task.inputs) == designer] = input
                        task.actions.append(Action(
                            time = time,
                            input = task.current_input.copy()
                        ))
                # handle score event
                elif type == 'score' and round is not None:
                    # reset round
                    for task in round.tasks:
                        task.score = content[task.designers[0]]
                # handle round complete
                elif type == 'complete' and round is not None and content == round.name:
                    round.time_complete = time
                # handle task complete
                elif type == 'complete' and round is not None:
                    designer = content.get('designers')[0]
                    task = round.getDesignerTask(designer)
                    task.time_complete = time
