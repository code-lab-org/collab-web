# Collaborative Design Web Platform (collab-web)

Paul T. Grogan, [pgrogan@stevens.edu](mailto:pgrogan@stevens.edu)

## Introduction

This project contains two components in support of Collaborative Design experiments:

1. Python Toolkit - a set of Python scripts that generate experiments and post-process resulting log files
2. Web Application - a client-server Node.js application to conduct designer experiments

More information on both components is provided in the subdirectory README files.

This project implements a similar interface to a [prior project](https://github.com/code-lab-org/collab-java); however, without requiring an IEEE 1516-2010 High Level Architecture (HLA) runtime infrastructure (RTI).

## Requirements

You must have Python (compatible with version 2 or 3) installed on your machine to run the Python toolkit.

You must have Node.js installed on your server to run the web application.

## Getting Started

This application is only intended for use on private networks. Access to the designer and administrator interfaces are not restricted.

Before running the web application, first run the Python generator to create experiment files:
```shell
cd python
python generator.py
```
Next, run the web application:
```shell
cd app
npm install
npm start
```
which will launch with a primary entry point of port 80:
* [http://localhost:80](http://localhost:80): designer interface
* [http://localhost:80/admin.html](http://localhost:80/admin.html): administrator interface

More detailed information is available in the `README.md` files in the `python/` and `app/` directories.

## References

Grogan, P.T. and O.L. de Weck (2016). "Collaboration and complexity: an experiment on the effect of multi-actor coupled design," *Research in Engineering Design*, Vol. 27, No. 3, pp. 221-235. [Online](http://link.springer.com/article/10.1007%2Fs00163-016-0214-7).

Alelyani, T., Y. Yang, and P.T. Grogan (2017). "Understanding Designers Behavior in Parameter Design Activities" *2017 ASME International Design Engineering Technical Conferences and Computers and Information in Engineering Conference*, August 6-9, Cleveland, Ohio. [Online](http://proceedings.asmedigitalcollection.asme.org/proceeding.aspx?articleid=2662424)

Grogan, P.T. (2018). "Data on Multi-actor Parameter Design Tasks by Engineering Students with Variable Problem Size, Coupling, and Team Size," *Data in Brief*, Vol. 20, pp. 1079-1084. [Online](https://doi.org/10.1016/j.dib.2018.08.162)

## License

Copyright 2019 Paul T. Grogan

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
