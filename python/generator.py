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

from collab import Session

for i in range(2):
    with open('experiment{:03d}.json'.format(i+1), 'w') as out_file:
        json.dump(Session.generate(i), out_file, default=lambda o: o.__dict__)