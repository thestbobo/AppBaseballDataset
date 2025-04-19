import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._allTeams = []
        self._myGraph = nx.Graph()
        self._salMap = {}

        self._weight_best = None
        self._best_path = None

        pass

    def buildGraph(self, year):
        self._myGraph = nx.Graph()
        self._myGraph.clear()
        self._myGraph.add_nodes_from(self._allTeams)

        self.addEdges(year)

    def addEdges(self, year):
        self._salMap = {}
        # creo mappa salario totale - codice squadra

        for arr in DAO.getSalariesOfYear(year):
            self._salMap[arr[0]] = arr[1]


        # salaries = DAO.getSalariesOfYear(year)
        # self._salMap.clear()
        # self._salMap = {teamID: salary for teamID, salary in salaries}


        for t1 in self._allTeams:
            for t2 in self._allTeams:
                if t1.ID != t2.ID and not self._myGraph.has_edge(t1.ID, t2.ID):
                    peso = float(self.getTeamSalary(t1.teamCode)) + float(self.getTeamSalary(t2.teamCode))
                    self._myGraph.add_edge(t1, t2, weight=peso)


        pass

    def getTeamSalary(self, ID):
        return self._salMap.get(ID)


    def getYears(self):
        return DAO.getAllYears()

    def getTeamsYear(self, year):
        self._allTeams = []
        self._allTeams = DAO.getTeamsOfYear(year)
        return self._allTeams

    def getDetails(self, team):
        neighbors = self._myGraph.neighbors(team)
        #presi vicini
        edges = []

        #prendo edges tra nodo selezionato e vicini e metto in lista
        for n in neighbors:
            weight = self._myGraph[team][n]['weight']
            tupleTemp = n, weight
            edges.append(tupleTemp)
        edges.sort(key=lambda edge: edge[1])
        return edges

    def getBestPath(self, start_node):
        self._weight_best = 0
        self._best_path = []
        partial = [start_node]

        for n in self._myGraph.neighbors(start_node):
            partial.append(n)
            self._recursion(partial)
            partial.pop()

        return self._best_path, self._weight_best

    def _recursion(self, partial):
        current_node = partial[-1]
        if self.getWeight(partial) > self._weight_best:
            self._weight_best = self.getWeight(partial)
            self._best_path = copy.deepcopy(partial)
            return

        for n in self._myGraph.neighbors(current_node):
            if n not in partial:
                if self._myGraph[current_node][n]["weight"] < self._myGraph[partial[-2]][current_node]["weight"]:
                    partial.append(n)
                    self._recursion(partial)
                    partial.pop()
                    return



    def getWeight(self, partial):
        if len(partial) <= 1:
            return 0
        weight = 0
        for i in range(1, len(partial)-1):
            weight += self._myGraph[partial[i]][partial[i+1]]["weight"]

        return weight

