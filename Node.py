from copy import copy, deepcopy
from typing import List, Dict

class Node:
    def __init__(self, info: List[List[str]], cost: int, parinte):
        self.info: List[List[str]] = info
        self.cost: int = cost
        self.parinte: Node = parinte  # parintele din arborele de parcurgere

    def get_path(self):
        """Returneaza drumul pana la nodul curent.
        """
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def print_path(self, file):
        """Afiseaza drumul pana la nodul curent.
        """
        stari = self.get_path()
        for x in stari[0].info:
            file.write(''.join(x) + "\n")
        file.write("\n")
        for i in range(1, len(stari)):
            for x in stari[i].info:
                file.write(''.join(x) + "\n")
            file.write("Cost mutare: " + str(stari[i].cost - stari[i].parinte.cost) + "\n")
            file.write("\n")
        file.write("S-au realizat " + str(len(stari)-1) + " mutari cu costul " + str(self.cost) + ".\n")

    def final(self) -> bool:
        """Verifica daca starea curenta este stare finala sau nu.

        Returns:
            True daca este stare finala si False altfel.
        """
        # Verificam daca toate caracterele sunt #.
        for line in self.info:
            for c in line:
                if c != '#':
                    return False
        
        return True

    def generate_next(self):
        """Functia genereaza succesorii starii curente.

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
                
                    node = Node(new_state, self.cost + cost, self)

                    if node.can_be_sol():
                        new_states.append(node)

        return new_states  

    @staticmethod
    def fill(mat: List[List[str]], vis: List[List[bool]], start_x: int, start_y: int) -> int:
        """Inlocuieste in matricea mat zona care incepe pe elementul (start_x, start_y) cu caracterul '#'.
           Marcheaza in vectorul vis toate elementele prin care trece.

           Returns:
           Numarul de caractere inlocuite
        """
        # Initializam vectorii de directie si niste variabile ajutatoare.
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        n = len(mat)
        m = len(mat[0])
        c = mat[start_x][start_y]

        # Marcam matricea si vectorul.
        mat[start_x][start_y] = "#"
        vis[start_x][start_y] = True
        ret = 1

        for i in range(4):
            new_x = start_x + dx[i]
            new_y = start_y + dy[i]

            if new_x >= 0 and new_x < n and new_y >= 0 and new_y < m and mat[new_x][new_y] == c and vis[new_x][new_y] == False:
                ret += Node.fill(mat, vis, new_x, new_y)
        
        return ret

    # Functie de la laborator
    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        ret = "\n"
        for line in self.info:
            for c in line:
                ret += c
            ret += "\n"
        return ret

    def can_be_sol(self) -> bool:
        """Functia ne spune daca nodul curent poate fi pe drumul spre rezultat.
           Daca frecventa unei litere este < 3, sigur nu poate fi.
        """
        freq: Dict[str, int] = {}
        for line in self.info:
            for c in line:
                if c in freq:
                    freq[c] += 1
                else:
                    freq[c] = 1

        for line in self.info:
            for c in line:
                if freq[c] < 3:
                    return False
        
        return True

