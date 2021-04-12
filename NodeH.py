from Node import Node
from copy import copy, deepcopy
from string import ascii_lowercase
from typing import Dict


class NodeH(Node):
    """Extinde clasa Node continand estimarea <h>.
    """

    def __init__(self, x: Node, euristic="banal"):
        super().__init__(x.info, x.cost, x.parinte)
        self.h = self.calculate_h(euristic)

    def generate_next(self, euristic="banal"):
        # Preluam starile care nu contin estimarea.
        states = super().generate_next()

        # Acest vector va contine starile cu tot cu estimare.
        new_states = []
        for state in states:
            new_states.append(NodeH(state, euristic))

        return new_states

    def calculate_h(self, euristic: str):
        if euristic == "banal":
            if self.final() is False:
                return 1
            return 0
        elif euristic == "adm1":
            # Calculam frecventa fiecarei litere.
            freq: Dict[str, int] = {}
            for line in self.info:
                for c in line:
                    if c in freq:
                        freq[c] += 1
                    else:
                        freq[c] = 1

            # Calculam costul total ca fiind costul daca eliminam fiecare litera printr-o singura mutare.
            cost_total: float = 0
            for c in ascii_lowercase:
                if c in freq and freq[c] != 0:
                    cost_total += 1

            return cost_total
        elif euristic == "adm2":
            # Aceasta euristica ne da costul minim al urmatoarei mutari.
            n = len(self.info)
            m = len(self.info[0])
            min_cost = float(n * m + 1)

            # Calculam frecventa fiecarei litere.
            freq = {}
            for line in self.info:
                for c in line:
                    if c in freq:
                        freq[c] += 1
                    else:
                        freq[c] = 1

            # Incercam toate mutarile posibile si vedem cat ne-ar costa.
            vis = [[False] * m for _ in range(n)]
            temp_state = deepcopy(self.info)
            for i in range(n):
                for j in range(m):
                    if not vis[i][j] and self.info[i][j] != '#':
                        # Dimensiunea zonei
                        dim = self.fill(temp_state, vis, i, j)

                        # Calculam costul.
                        cost = 1 + (freq[self.info[i][j]] - dim) / freq[self.info[i][j]]

                        # Actualizam minimul.
                        min_cost = min(min_cost, cost)

            if min_cost == n * m + 1:
                min_cost = 0

            # Returnam costul minim al unei mutari.
            return min_cost
        elif euristic == "neadm":
            # Aceasta euristica ne da costul daca eliminam toate zonele asa cum sunt acum, fara sa se uneasca nimic.
            n = len(self.info)
            m = len(self.info[0])
            cost_total = 0

            # Calculam frecventa fiecarei litere.
            freq = {}
            for line in self.info:
                for c in line:
                    if c in freq:
                        freq[c] += 1
                    else:
                        freq[c] = 1

            # Incercam toate mutarile posibile si vedem cat ne-ar costa.
            vis = [[False] * m for _ in range(n)]
            temp_state = deepcopy(self.info)
            for i in range(n):
                for j in range(m):
                    if not vis[i][j] and self.info[i][j] != '#':
                        # Dimensiunea zonei
                        dim = self.fill(temp_state, vis, i, j)

                        # Calculam costul.
                        cost = 1 + (freq[self.info[i][j]] - dim) / freq[self.info[i][j]]

                        # Costul total.
                        cost_total += cost

            # Returnam costul total.
            return cost_total

    def f(self):
        """ Returneaza suma dintre cost si estimare.
        """
        return self.cost + self.h
