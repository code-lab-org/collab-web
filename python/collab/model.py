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
from scipy.linalg import orth
import numpy as np

class Session(object):
    """
    An experimental session. Includes settings and the
    list of tasks (training and experimental).
    """
    def __init__(self, name='', num_designers=4, error_tol=0.05, training = [], rounds = []):
        """
        Initializes this session.

        @param name: the session name
        @type name: str

        @param num_designers: the number of designers
        @type num_designers: int

        @param error_tol: the error tolerance for solutions
        @type error_tol: float

        @param training: the training rounds
        @type training: array(Round)

        @param rounds: the experimental rounds
        @type rounds: array(Round)
        """
        self.name = name
        self.num_designers = num_designers
        self.error_tol = error_tol
        self.training = training
        self.rounds = rounds

    @staticmethod
    def parse(json):
        return Session(
            name = json.get('name', ''),
            num_designers = json.get('num_designers', 4),
            error_tol = json.get('error_tol', 0.05),
            training = list(map(lambda r: Round.parse(r), json.get('training', []))),
            rounds = list(map(lambda r: Round.parse(r), json.get('rounds', [])))
        )

class Round(object):
    """
    An experimental round with a set of technical tasks.
    """
    def __init__(self, name, assignments, tasks, max_time):
        """
        Initializes this round.

        @param name: the name
        @type name: str

        @param assignments: the task assignments: list of lists of designers
        @type assignments: list(list(int))

        @param tasks: the technical tasks
        @type array(Task)

        @param max_time: the maximum allowable time (milliseconds)
        @type number
        """
        self.name = name
        self.assignments = assignments
        self.tasks = tasks
        self.max_time = max_time

    def getDesignerTask(self, designer):
        return next((t for t in self.tasks if designer in t.designers))

    @staticmethod
    def parse(json):
        return Round(
            name = json.get('name'),
            assignments = json.get('assignments'),
            tasks = list(map(lambda t: Task.parse(t), json.get('tasks'))),
            max_time = json.get('max_time')
        )

    @staticmethod
    def generate(name, size, assignments, is_coupled=True, max_time=None, random=np.random):
        return Round(
            name = name,
            assignments = assignments,
            tasks = [Task.generate(designers, size, is_coupled=is_coupled, random=random) for designers in assignments],
            max_time = max_time*1000 if max_time is not None else None
        )

class Task(object):
    """
    An experimental task.
    """
    def __init__(self, designers, num_inputs, num_outputs, coupling, target, inputs, outputs):
        """
        Initializes this task.

        @param designers: the designers asigned to this task
        @type designers: list(int)

        @param num_inputs: the number of inputs per designer
        @type num_inputs: list(int)

        @param num_outputs: the number of outputs per designer
        @type num_outputs: list(int)

        @param coupling: the coupling matrix (M)
        @type coupling: list(float)

        @param target: the target vector (y_star)
        @type target: list(float)

        @param inputs: the input assignments
        @type inputs: list(int)

        @param outputs: the output assignments
        @type outputs: list(int)
        """
        self.designers = designers
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.coupling = coupling
        self.target = target
        self.inputs = inputs
        self.outputs = outputs

        self.time_start = None # set by post-processor
        self.time_complete = None # set by post-processor
        self.actions = None # set by post-processor
        self.score = None # set by post-processor

    def getSolution(self):
        """
        Gets the zero-error solution for this task.

        @returns: the solution vector
        @rtype numpy.Array(float)
        """
        return np.matmul(np.array(self.coupling).T, self.target)

    def getCountActions(self, designer=None):
        return np.sum([1 if i > 0 and not np.array_equal(a.getInput(self, designer), self.actions[i-1].getInput(self, designer)) else 0 for i,a in enumerate(self.actions)])

    def getCountProductiveActions(self, designer=None):
        return np.sum([1 if i > 0 and a.getErrorNorm(self, designer) < self.actions[i-1].getErrorNorm(self, designer) else 0 for i,a in enumerate(self.actions)])

    def getCumulativeInputDistanceNorm(self, designer=None):
        return np.sum([np.linalg.norm(a.getInput(self, designer) - self.actions[i-1].getInput(self, designer)) if i > 0 else 0 for i,a in enumerate(self.actions)])

    def getCumulativeErrorNorm(self, designer=None):
        return np.sum([a.getErrorNorm(self, designer) for a in self.actions])

    @staticmethod
    def parse(json):
        return Task(
            designers = json.get('designers'),
            num_inputs = json.get('num_inputs'),
            num_outputs = json.get('num_outputs'),
            coupling = json.get('coupling'),
            target = json.get('target'),
            inputs = json.get('inputs'),
            outputs = json.get('outputs')
        )

    @staticmethod
    def generate(designers, size, inputs=None, outputs=None, is_coupled=True, random=np.random):
        if inputs is None:
            # try to assign equally among designers
            inputs = [designers[int(i//(size/len(designers)))] for i in range(size)]
        num_inputs = [np.sum(np.array(inputs) == designer).item() for designer in designers];
        if outputs is None:
            # try to assign equally among designers
            outputs = [designers[int(i//(size/len(designers)))] for i in range(size)]
        num_outputs = [np.sum(np.array(outputs) == designer).item() for designer in designers];

        coupling = np.zeros((size, size))
        if is_coupled:
            # coupling matrix is orthonormal basis of random matrix
            coupling = orth(random.rand(size, size))
        else:
            # coupling matrix has random 1/-1 along diagonal
            coupling = np.diag(2*random.randint(0,2,size)-1)

        # find a target with no solution values "close" to initial condition
        solution = np.zeros(size)
        while np.any(np.abs(solution) <= 0.20):
            target = orth(2*random.rand(size,1)-1)
            # solve using dot product of coupling transpose and target
            solution = np.matmul(coupling.T, target)

        return Task(designers, num_inputs, num_outputs, coupling.tolist(), target[:,0].tolist(), inputs, outputs)

class Action(object):
    """
    An experimental action.
    """
    def __init__(self, time, input):
        """
        Initializes this action.

        @param time: the action time (milliseconds)
        @type time: long

        @param input: the resulting input vector
        @type input: np.Array(float)
        """
        self.time = time
        self.input = input

    def getError(self, task, designer = None):
        """
        Gets the error in design after this action for a task.

        @param task: the task
        @type task: Task

        @param designer: the designer (optional, default = None)
        @type designer: int

        @returns: the error
        @rtype: numpy.Array(float)
        """
        # compute error as outputs - targets
        if designer is None:
            return self.getOutput(task, designer) - task.target
        else:
            return (self.getOutput(task, designer)[np.array(task.outputs) == designer]
                    - np.array(task.target)[np.array(task.outputs) == designer])

    def getErrorNorm(self, task, designer = None):
        """
        Gets the error norm in design after this action for a task.

        @param task: the task
        @type task: Task

        @param designer: the designer (optional, default = None)
        @type designer: int

        @returns: the error norm
        @rtype: float
        """
        # compute 2-norm of error
        return np.linalg.norm(self.getError(task, designer))

    def getElapsedTime(self, task):
        """
        Gets the elapsed time of this action.

        @param task: the task
        @type task: Task

        @returns: the elapsed time (milliseconds)
        @rtype: long
        """
        return self.time - task.time_start

    def isSolved(self, session, task):
        """
        Checks if the task is solved.

        @param session: the experimental session
        @type session: Session

        @param task: the task
        @type task: Task

        @returns: true, if this action solves the task
        @rtype: bool
        """
        # all errors must be less than tolerance values
        return all(abs(e) < session.error_tol for e in self.getError(task))

    def getInput(self, task, designer = None):
        """
        Gets the input for a designer.

        @param task: the task
        @type task: Task

        @param designer: the designer (optional, default = None)
        @type designer: int

        @returns: the input vector
        @rtype: numpy.Array(float)
        """
        if designer is None:
            return np.array(self.input)
        else:
            return np.array(self.input)[np.array(task.inputs) == designer]

    def getOutput(self, task, designer = None):
        """
        Gets the output for a designer.

        @param task: the task
        @type task: Task

        @param designer: the designer (optional, default = None)
        @type designer: int

        @returns: the output vector
        @rtype: numpy.Array(float)
        """
        if designer is None:
            return np.matmul(task.coupling, self.input)
        else:
            return np.matmul(task.coupling, self.input)[np.array(task.outputs) == designer]
