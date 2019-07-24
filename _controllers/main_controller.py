from _models.csv_model import CsvModel
from _models.data_keeper_model import DataKeeper
from _models.svd_model import SvdModel
from _views.main_view import MainView

# creating DataKeeper model
dk = DataKeeper()

# Instantiating Views:

# creating view
mainView = MainView(dk, dk.DataDir)

# Instantiating models:

# creating csv model
csvModel = CsvModel()

# creating svd model
svdModel = SvdModel(10, 4)


def BeginInvoke():

    # reading csv to model
    csvModel.ReadFromFile(mainView.DataPath)
    svdModel.ApplyDecomposition()
    dk.Notify()


def StartController():
    mainView.StartView()
    BeginInvoke()
    return mainView.EndView()
