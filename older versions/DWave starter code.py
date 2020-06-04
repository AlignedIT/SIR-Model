#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Copyright 2020 Alex Khan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Things to do:
 - Please name this file <demo_name>.py
 - Fill in [yyyy] and [name of copyright owner] in the copyright (top line)
 - Add demo code below
 - Format code so that it conforms with PEP 8
"""

import numpy as np
from numpy.random import rand

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from minorminer import find_embedding
import networkx as nx
import dwave.inspector

dim=50
Q =  2*rand(dim,dim) - 1
Q = (Q+Q.T)/2
for k in range(dim):
    Q[k,k] = np.abs(Q[k,k])

print(Q)

linear={('a'+str(k), 'a'+str(k)):Q[k][k] for k in range(dim)}

quadratic={('a'+str(i+1), 'a'+str(j)):Q[i+1][j] for i in range(dim-1) for j in range(dim-1) if j<i+1}

QDwave = dict(linear)
QDwave.update(quadratic)

print(QDwave)

chainstrength = 10
numruns = 100

#clique = nx.complete_graph(7).edges()
#target_graph = nx.random_regular_graph(d=4, n=30).edges()
#embedding = find_embedding(clique, target_graph)
#print(embedding)

sampler = EmbeddingComposite(DWaveSampler())


response = sampler.sample_qubo(QDwave, chain_strength=chainstrength, num_reads=numruns)
print(response)
dwave.inspector.show(QDwave,response)


# In[ ]:




