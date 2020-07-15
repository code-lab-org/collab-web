# Collaborative Design Web Platform: Python Toolkit

Paul T. Grogan, [ptgrogan@stevens.edu](mailto:pgrogan@stevens.edu)

## Introduction

This software generates experiment session files and post-processes data recorded during experimental sessions. The data from these experiments takes two forms: a JSON file which describes the technical problems in the experiment (coupling matrices, input and output assignments, and labels), and a log file which records the actions taken by participants during the experimental session.

## Pre-requisites

This software is written in Python and requires either version 2.X or 3.X with the `numpy` and `scipy.linalg` packages. The authors recommend an integrated Python environment such as Anaconda for ease of use.

## Generator Usage

The `generator.py` script is used to generate experiment files for each session following a particular experimental design. The default generator follows the following rules:
 * 5 Training Tasks
  1. 1x1 Individual
  2. 2x2 Individual
  3. 2x2 (Uncoupled) Pair
  4. 2x2 Pair
  5. 3x3 Pair
 * 10 Experimental Tasks (Randomized Order)
  * 4 replications of 2x2 Pair
  * 4 replications of 3x3 Pair
  * 2 replications of 4x4 Pair

After running, the generator will output a JSON file (`experimentXXX.json`) for each requested experimental session.

## Post-processor Usage

The `processor.py` script is used to post-process experiment results to support analysis. It accepts two command-line arguments:
```shell
python processor.py -l [log_file] -j [json_file]
```
where `[log_file]` is the file path to the resulting log file written by the server during the experiment and `[json_file]` is the file path to the original JSON experiment document created by the generator script.

After running, the processor script will output to standard out (console) a table showing the time and score of each participant in each round.

## References

Grogan, P.T. and O.L. de Weck (2016). "Collaboration and complexity: an experiment on the effect of multi-actor coupled design," *Research in Engineering Design*, Vol. 27, No. 3, pp. 221-235. [Online](http://link.springer.com/article/10.1007%2Fs00163-016-0214-7).

Alelyani, T., Y. Yang, and P.T. Grogan (2017). "Understanding Designers Behavior in Parameter Design Activities" *2017 ASME International Design Engineering Technical Conferences and Computers and Information in Engineering Conference*, August 6-9, Cleveland, Ohio. [Online](http://proceedings.asmedigitalcollection.asme.org/proceeding.aspx?articleid=2662424)

Grogan, P.T. (2018). "Data on Multi-actor Parameter Design Tasks by Engineering Students with Variable Problem Size, Coupling, and Team Size," *Data in Brief*, Vol. 20, pp. 1079-1084. [Online](https://doi.org/10.1016/j.dib.2018.08.162)

## License

Copyright 2019 Paul T. Grogan

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
