import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._grafo = nx.Graph()
        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self , v0 , v1 , t):
        self._bestCammino = []
        self._bestScore = 0
        parziale = [v0]
        self.ricorsione(parziale , v1 , t)
        return self._bestCammino , self._bestScore

    def ricorsione(self , parziale , v1 , t):
        # verifico se parziale è una soluzione valida ed in caso la salvo
        if parziale[-1] == v1: # potenzialmente questa è una sol accettabile
              if self.getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self.getScore(parziale)

        # verifico se ha senso continuare ad aggiungere elementi in parziale
        if len(parziale) == t+1: # parziale ha raggiunto il numero massimo di tratte
            return

        # espando parziale e rifaccio la ricorsione con backtracking
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale , v1 , t)
                parziale.pop()

    def getScore(self, parziale):
        sumPesi = 0
        for i in range(0 , len(parziale)-1):
            sumPesi += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return sumPesi

    def buildGraph(self , nMin):
        nodes = DAO.getAllNodes(nMin , self._idMapAirports)
        self._grafo.add_nodes_from(nodes)
        #self.addEdges()
        self._grafo.clear_edges()
        self.addEdgesv2()
        print(len(self._grafo.nodes))
        print(len(self._grafo.edges))


    def addEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        # queste tratte hanno due problemi: 1) ho archi diretti e inversi, e quindi dovroò fare la somma a mano
        # 2) ho archi tra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._grafo and t.aeroportoA in self._grafo:
                # allora posso aggiungerlo
                if self._grafo.has_edge(t.aeroportoP, t.aeroportoA):
                    self._grafo[t.aeroportoP][ t.aeroportoA]["weight"] += t.peso
                else:
                    self._grafo.add_edge(t.aeroportoP, t.aeroportoA , weight = t.peso)

    def addEdgesv2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._grafo and t.aeroportoA in self._grafo:
                    self._grafo.add_edge(t.aeroportoP, t.aeroportoA , weight = t.peso)

    def getViciniOrdinati(self , source):
        # restituisce tutti i vicini di source ordinati per peso dell'arco che collegano source al vicino
        vicini = self._grafo.neighbors(source)
        viciniTm = []
        for i in vicini:
            viciniTm.append((i  , self._grafo[source][i]["weight"]))
        viciniTm.sort(key=lambda x : x[1] , reverse=True)
        return viciniTm

    def hasPath(self , v0 , v1):
        # restituisce true se un qualche cammino tra v0 e v1 esiste, altrimenti False
        return v1 in nx.node_connected_component(self._grafo , v0)

    def getPath(self , v0 , v1):
        dictOfPredecessors = dict(nx.bfs_predecessors(self._grafo , v0))
        # avrei potuto fare la stessa identica cosa con dfs_predecessors
        #path = [v1]
        #while path[0] != v0:
         #   path.insert(0 , dictOfPredecessors[path[0]])

        # v2
       # path = nx.shortest_path(v0 , v1)

        # v4
        path = nx.dijkstra_path(self._grafo , v0 , v1 , weight=None)

        return path




    def getGraphDetailes(self):
        return len(self._grafo.nodes) , len(self._grafo.edges)

    def getAllNodes(self):
        nodes =  list(self._grafo.nodes)
        nodes.sort(key=lambda x : x.IATA_CODE)
        return nodes



