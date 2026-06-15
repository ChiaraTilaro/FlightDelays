
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choisePartenza = None
        self._choiseArrivo = None

    def handleAnalizza(self , e):
        nMin = self._view._txtInCMin.value
        if nMin == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un numero minimo di compagnie",
                        color="red")
            )
            self._view.update_page()
            return
        try:
            cMin = int(nMin)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un numero interno minimo di compagnie",
                        color="red")
            )
            self._view.update_page()
            return
        if cMin <=0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero di compagnie deve essere un intero positivo",
                        color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(cMin)
        nNodes , nEdges = self._model.getGraphDetailes()
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
                ft.Text("Grafo correttamente creato",
                        color="greem")
            )
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
                ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi" ,
                        color="green")
            )

        allNodes = self._model.getAllNodes()
        self.fillDropdown(allNodes)
        self._view.update_page()


    def handleConnessi(self , e):
        if self._choisePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di partenza")
            )
            self._view.update_page()
            return
        viciniT = self._model.getViciniOrdinati(self._choisePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(
                ft.Text(f"{v[0]} - peso {v[1]}")
            )
        self._view.update_page()

    def handleCercaItinerario(self , e):
        t = self._view._txtInNTratteMax.value
        try:
            tInt = int(t)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore intero")
            )
            self._view.update_page()
            return
        path , score = self._model.getCamminoOttimo(self._choisePartenza , self._choiseArrivo , tInt)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
                ft.Text(f"Cammino fra {self._choisePartenza} e {self._choiseArrivo} trovato")
            )
        self._view._txtResults.controls.append(
                ft.Text(f"Il cammino ha uno score complessivo pari a {score} e contienei seguenti nodi:")
            )
        for p in path:
            self._view._txtResults.controls.append(
                ft.Text(p)
            )

        self._view.update_page()




    def handleTestConnessione(self , e):
        if self._choisePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di partenza")
            )
            self._view.update_page()
            return
        if self._choiseArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di partenza")
            )
            self._view.update_page()
            return
        if not self._model.hasPath(self._choisePartenza , self._choiseArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {self._choisePartenza} e {self._choiseArrivo}" ,
                        color="orange")
            )
            self._view.update_page()
            return
        path = self._model.getPath(self._choisePartenza , self._choiseArrivo)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
                ft.Text("Ho trovato un cammino:")
            )
        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()


    def fillDropdown(self , allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self._choiseDdPartenza)
            )
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self._choiseDdArrivo)
            )

    def _choiseDdPartenza(self , e):
        self._choisePartenza = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choisePartenza}")

    def _choiseDdArrivo(self , e):
        self._choiseArrivo = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choiseArrivo}")



