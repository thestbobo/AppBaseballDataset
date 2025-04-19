import flet as ft
from database.DAO import DAO
from model.team import Team


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_year = None
        self._selected_team = None

    def fillDDyears(self):
        years = self._model.getYears()
        ddYears = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = ddYears
        self._view.update_page()
        pass

    def handleDDYear(self, e):
        self._view._txtOutSquadre.controls.clear()
        self._selected_year = self._view._ddAnno.value

        teams = self._model.getTeamsYear(self._selected_year)

        self._view._txtOutSquadre.controls.append(ft.Text(
            f"Ecco l'elenco delle {len(teams)} squadre che hanno giocato nell'anno {self._view._ddAnno.value}: "))
        self._view._ddSquadra.disabled = False
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"Code: {t.teamCode} - Name: {t.name} "))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t, text=t.name, on_click=self.readDDTeam))
        self._view.update_page()

        pass

    def readDDTeam(self, e):
        if e.control.data is None:
            self._selected_team = None
        else:
            self._selected_team = e.control.data



    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._selected_year)
        self._view._txt_result.controls.append(ft.Text(
            f"Grafo creato correttamente - (nNodes={len(self._model._myGraph.nodes)}, nEdges={len(self._model._myGraph.edges)})"))
        self._view._btnPercorso.disabled = False
        self._view.update_page()
        pass

    def handleDettagli(self, e):
        det = self._model.getDetails(self._selected_team)
        self._view._txt_result.controls.append(ft.Text(f"Ecco i dettagli della squadra {self._selected_team}:"))
        for edge in det:
            self._view._txt_result.controls.append(ft.Text(f'Team: {edge[0]} - Salaries: {edge[1]}'))
        self._view.update_page()
        pass

    def handlePercorso(self, e):
        path, weight = self._model.getBestPath(self._selected_team)
        self._view._txt_result.controls.append(ft.Text(
            f"Ecco il percorso di peso massimo a partire da {self._selected_team}, con peso uguale a {weight} "))
        for t in path:
            self._view._txt_result.controls.append(ft.Text(
                f"- Team: {t}"
            ))
        pass