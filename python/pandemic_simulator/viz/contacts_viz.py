# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
from typing import List, Any

import networkx
from matplotlib import pyplot as plt

from .pandemic_viz import PandemicViz
from ..environment import PandemicObservation, PandemicSimState, PandemicSim
from ..utils import checked_cast

__all__ = ['ContactViz']


class ContactViz(PandemicViz):

    _sim: PandemicSim
    _num_stages: int
    _graph: networkx.Graph
    _days_per_interval: int
    _last_stage: int

    _stages_per_interval: List[int]
    _num_components_per_interval: List[int]
    _max_components: int

    def __init__(self, sim: PandemicSim, num_stages: int = 5):
        self._sim = sim
        self._num_stages = num_stages
        self._stages_per_interval = []
        self._num_components_per_interval = []
        self._last_stage = -1
        self._max_components = 1
        self._graph = None  # will initialize on the first record() call

    def record(self, data: Any, **kwargs: Any) -> None:
        if isinstance(data, PandemicSimState):
            state = checked_cast(PandemicSimState, data)
            obs = PandemicObservation.create_empty()
            obs.update_obs_with_sim_state(state)
        elif isinstance(data, PandemicObservation):
            obs = data
        else:
            raise ValueError('Unsupported data type')

        stage: int = obs.stage[0, 0, 0]

        if not self._graph or self._last_stage != stage:
            self._graph = networkx.Graph(directed=False)
            self._last_stage = stage

        for a in self._sim._id_to_person.keys():
            contacts = self._sim._contact_tracer.get_contacts(a)
            #self._graph.add_node(a)
            for b in contacts:
                if contacts[b][0] > 0 and not (a, b) in self._graph.edges:
                    self._graph.add_edge(a, b)
                    #self._graph.add_node(b)

    def plot(self) -> None:
        # plt.figure(figsize=(12, 8))
        #
        # nrows = 1
        # ncols = 2
        #
        # plt.subplot(nrows, ncols, 1)
        # plt.plot(self._num_components_per_interval)
        # plt.ylim([-0.1, self._max_components + 1])
        # plt.title('Connected Components')
        # # plt.xlabel('time (intervals)')
        # #
        # # plt.subplot(nrows, ncols, 2)
        # # plt.plot(self._stages_per_interval)
        # # plt.ylim([-0.1, self._num_stages + 1])
        # # plt.title('Stage')
        # # plt.xlabel('time (intervals)')
        # #
        # # plt.tight_layout()
        #
        # print(repr(self._stages_per_interval))
        # print(repr(self._num_components_per_interval))
        networkx.draw(self._graph)
        #plt.show()