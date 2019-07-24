import csv
from _models.input_model import InputModel
from _models.helpers.data_type_converter import list2array
from _models.data_keeper_model import DataKeeper


class CsvModel(InputModel):
    @staticmethod
    def ParseEntry(entry):
        return str(entry).split(',')

    def ReadFromFile(self, filePath=None):
        if filePath is None:
            raise Exception("Incorrect file_path")
        else:
            with open(filePath, 'r') as csvFile:
                reader = csv.reader(csvFile, quoting=csv.QUOTE_NONNUMERIC)
                for row in reader:
                    self.Entries.append(row)
            csvFile.close()
        DataKeeper().AddEntries(csv_model_data=list2array(self.Entries))
