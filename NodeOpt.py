from Node import Node
from NodeH import NodeH
from copy import copy, deepcopy


class NodeOpt(NodeH):
    """Extinde clasa NodeH, schimband functia de generat succesori.
    """
    def __init__(self, x: Node, euristic="banal"):
        super().__init__(x, euristic)

    def generate_next(self, current_list, euristic):
        """Functia genereaza succesorii starii curente.

        Args:
            current_list = lista curenta de noduri

        Returns:
            Un vector de NodParcurgere reprezentand succesorii starii curente.
        """
        new_states = []
        # vis[i][j] ne spune daca am incercat sa eliminam zona din care face parte elementul (i, j)
        n, m = len(self.info), len(self.info[0])
        vis = [[False] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if not vis[i][j] and self.info[i][j] != '#':
                    # Facem o copie a starii curente si umplem zona data de (i, j) cu '#'.
                    new_state = deepcopy(self.info)
                    nr_deleted = self.fill(new_state, vis, i, j)
                    if nr_deleted < 3:
                        continue
                    
                    # Simulam caderea literelor: atat timp cat a "cazut" o litera, continuam.
                    changed = True
                    while changed:
                        changed = False
                        for x in range(n):
                            for y in range(m):
                                if new_state[x][y] == '#':
                                    if x-1 >= 0 and new_state[x-1][y] != '#':
                                        new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
                                        changed = True
                                    elif y+1 < m and new_state[x][y+1] != '#':
                                        new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
                                        changed = True

                    # Cautam cate placute avem de culoarea (i, j) in total.
                    nr_total = 0
                    for x in range(n):
                        for y in range(m):
                            if self.info[x][y] == self.info[i][j]:
                                nr_total += 1
                    
                    # Calculam costul dupa formula data.
                    cost = 1 + (nr_total - nr_deleted) / nr_total
                
                    # Adaugam estimarea la stare.
                    node = NodeOpt(Node(new_state, self.cost + cost, self), euristic)

                    # Daca nodul poate duce spre rezultat, il adaugam in lista.
                    if node.can_be_sol():
                        new_states.append(node)

        return new_states  
