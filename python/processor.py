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
import argparse
import json
import numpy as np
import os.path

from collab import PostProcessor

def main(log_file, json_file):
    pp = PostProcessor(log_file, json_file)
    # print header
    print(pp.session.name)
    print("{0:>5},{4:>10},{1:>25},{2:>3},{3:>3},{5:>10},{6:>10},{7:>10},{8:>10},{9:>10},{10:>10}".format(
        "Order", "Name", "N", "n", "Designers", "Score", "Time (s)", "Actions", "Productive", "Distance", "Error"))
    # print rows for each task
    for i, round in enumerate(pp.session.rounds):
        for task in round.tasks:
            print("{0:>5},{4:>10},{1:>25},{2:>3},{3:>3},{5:>10},{6:>10},{7:>10},{8:>10},{9:>10},{10:>10}".format(
                i+1,
                round.name.replace(' (Individual)', '').replace(' (Pair)', ''),
                sum(task.num_inputs),
                len(task.designers),
                '+'.join(map(lambda d: str(d+1), task.designers)),
                "{:10.0f}".format(task.score/1000) if task.score else 0,
                "{:10.2f}".format((task.time_complete - task.time_start)/1000) if task.time_complete else '',
                "{:10d}".format(task.getCountActions()),
                "{:10d}".format(task.getCountProductiveActions()),
                "{:10.2f}".format(task.getCumulativeInputDistanceNorm()),
                "{:10.2f}".format(task.getCumulativeErrorNorm())
            ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "This program post-processes experimental data."
    )
    parser.add_argument('-l', '--log', type = str, required = True,
                        help = 'Experiment log file path')
    parser.add_argument('-j', '--json', type = str, required = True,
                        help = 'Experiment json file path')
    args = parser.parse_args()
    main(args.log, args.json)
