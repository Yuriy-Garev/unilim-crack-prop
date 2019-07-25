from numpy import newaxis, vstack, sqrt, arctan, zeros, cos, sin, float_, diag, savetxt, dot
from numpy.linalg import pinv, norm
from numpy.linalg import svd as np_svd

from _models.data_keeper_model import DataKeeper
from _models.helpers.data_type_converter import list2array
from templates.helpers.clamp_value import ClampPositive as clamp


class SvdModel:
    def __init__(self, rowsNum, colsNum, x1_0=0., x2_0=0., kappa=1.9):
        self.Kappa = kappa  # Material property constant
        self.Csv = None  # numpy array with points coordinates (and/or forces acting on the object)
        self.RowsNum = rowsNum  # number of rows to read from csv file
        self.ColsNum = colsNum  # number of columns to read from csv file
        self.X1_0 = x1_0  # the crack origin ...
        self.X2_0 = x2_0  # ... (origin of forces application)
        self.X1 = None  # new positions ...
        self.X2 = None  # ... of points on the object
        self.U = None  # vector of points displacement
        self.P = zeros((rowsNum, 2 * colsNum), dtype=float_)  # vector of basis functions for William's series
        self.Q = zeros((rowsNum, 2 * colsNum), dtype=float_)  # vector of basis functions for William's series
        self.B = None  # matrix built from P and Q
        self.R2Norm = []  # vector of radius' values from each point on the object to the crack center
        self.Theta = []  # vector of angles for each point on the object
                         # relative to vertical axis passing through the crack center
        self.Solution = None  # vector Solution (in this particular case represents Forces applied
        # to crack the object and cause a displacement of the initial points coordinates on the value U

    @staticmethod
    def GetColumn(numpy_array, idx):
        """
        Retrieves a column (in column form) from numpy.array()
        :param numpy_array: numpy.array()
        :param idx: int()
        :return: numpy.array()
        """
        return numpy_array[:, idx][:, newaxis]

    def EvalNorm(self):
        for i in range(self.RowsNum):
            self.R2Norm.append(sqrt((self.X1[i] - self.X1_0)**2 + (self.X2[i] - self.X2_0)**2))
        self.R2Norm = list2array(self.R2Norm)

    def EvalTheta(self):
        for i in range(self.RowsNum):
            self.Theta.append(arctan((self.X2[i] - self.X2_0) / (self.X1[i] - self.X2_0)))
        self.Theta = list2array(self.Theta)

    def BuildMatrixP(self):
        for i in range(self.RowsNum):
            for j in range(self.ColsNum):
                self.P[i, 2 * j] = (self.R2Norm[i]**((j+1)/2)) * (self.Kappa * cos((j+1) * self.Theta[i]/2) -
                                        ((j+1)/2) * cos(((j+1)/2 - 2) * self.Theta[i]) + ((j+1)/2 + (-1)**(j+1)) * cos((j+1) * self.Theta[i]/2))
                self.P[i, 2 * j + 1] = (self.R2Norm[i]**((j+1)/2)) * (-self.Kappa * sin((j+1) * self.Theta[i]/2) +
                                        ((j+1)/2) * sin(((j+1)/2 - 2) * self.Theta[i]) - ((j+1)/2 - (-1)**(j+1)) * sin((j+1) * self.Theta[i]/2))

    def BuildMatrixQ(self):
        for i in range(self.RowsNum):
            for j in range(self.ColsNum):
                self.Q[i, 2 * j] = (self.R2Norm[i]**((j+1)/2)) * (self.Kappa * sin((j+1) * self.Theta[i]/2) +
                                        ((j+1)/2) * sin(((j+1)/2 - 2) * self.Theta[i]) - ((j+1)/2 + (-1)**(j+1)) * sin((j+1) * self.Theta[i]/2))
                self.Q[i, 2 * j + 1] = (self.R2Norm[i]**((j+1)/2)) * (self.Kappa * cos((j+1) * self.Theta[i]/2) +
                                        ((j+1)/2) * cos(((j+1)/2 - 2) * self.Theta[i]) - ((j+1)/2 - (-1)**(j+1)) * cos((j+1) * self.Theta[i]/2))

    def ErrorValue(self):
        return norm(dot(self.B, self.Solution) - self.U)

    @staticmethod
    def SaveAsCsv(array_like_data, file_name_str="csv_file"):
        savetxt(DataKeeper().root_dir+f"/solution/{file_name_str}.csv",
                array_like_data,
                fmt='%.4f',
                delimiter=',')

    def ApplyDecomposition(self):
        self.Csv = DataKeeper().GetEntryByKey('csv_model_data')
        self.RowsNum = clamp(self.RowsNum, self.Csv.shape[0])
        self.ColsNum = clamp(self.ColsNum, self.Csv.shape[1])

        x1_i = self.GetColumn(self.Csv, 0)  # initial coordinates ...
        x2_i = self.GetColumn(self.Csv, 1)  # ... of points on the object
        u1 = self.GetColumn(self.Csv, 2)
        u2 = self.GetColumn(self.Csv, 3)

        self.U = vstack([u1, u2])
        self.X1 = x1_i + u1
        self.X2 = x2_i + u2

        self.EvalNorm()
        self.EvalTheta()

        self.BuildMatrixP()
        self.BuildMatrixQ()
        self.B = vstack([self.P, self.Q])

        self.SaveAsCsv(self.B, "B")

        # U, S, V = sp_svd(self.B)
        U, S, V = np_svd(self.B)

        S = vstack([diag(S), zeros((U.shape[0]-S.size, S.size), dtype=float_)])

        self.SaveAsCsv(U, "U")
        self.SaveAsCsv(S, "S")
        self.SaveAsCsv(V.T, "V")

        self.Solution = dot(dot(V.T, pinv(S)), dot(U.T, self.U))  # looking for the solution in the least square meaning
        # self.Solution[0, 0] = 0

        self.SaveAsCsv(self.Solution, "_Solution")

        DataKeeper().AddEntries(svd_model_data={'B': self.B,
                                                'U': U, 'S': S, 'V': V,
                                                'Solution': self.Solution,
                                                'Error': self.ErrorValue()})
