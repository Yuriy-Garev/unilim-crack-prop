from numpy import newaxis, vstack, sqrt, arctan, zeros, cos, sin, float_, diag, savetxt, dot
from numpy.linalg import pinv, norm
from numpy.linalg import svd as np_svd

from _models.data_keeper_model import DataKeeper
from _models.helpers.data_type_converter import list2array
from templates.helpers.clamp_value import ClampPositive as clamp


class SvdModel:
    def __init__(self, rowsNum, colsNum, x1_0=0., x2_0=0., kappa=1.9):
        self.Kappa = kappa
        self.Csv = None
        self.RowsNum = rowsNum
        self.ColsNum = colsNum
        self.X1_0 = x1_0
        self.X2_0 = x2_0
        self.X1 = None
        self.X2 = None
        self.U = None
        self.P = zeros((rowsNum, 2 * colsNum), dtype=float_)
        self.Q = zeros((rowsNum, 2 * colsNum), dtype=float_)
        self.B = None
        self.R2Norm = []
        self.Theta = []
        self.Solution = None

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
        savetxt(DataKeeper().root_dir+'/solution'+'/{}.csv'.format(file_name_str), array_like_data, fmt='%.4f', delimiter=',')

    def ApplyDecomposition(self):
        self.Csv = DataKeeper().GetEntryByKey('csv_model_data')
        self.RowsNum = clamp(self.RowsNum, self.Csv.shape[0])
        self.ColsNum = clamp(self.ColsNum, self.Csv.shape[1])

        x1_i = self.GetColumn(self.Csv, 0)
        x2_i = self.GetColumn(self.Csv, 1)
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

        self.Solution = dot(dot(V.T, pinv(S)), dot(U.T, self.U))
        # self.Solution[0, 0] = 0

        self.SaveAsCsv(self.Solution, "_Solution")

        DataKeeper().AddEntries(svd_model_data={'B': self.B,
                                                'U': U, 'S': S, 'V': V,
                                                'Solution': self.Solution,
                                                'Error': self.ErrorValue()})
