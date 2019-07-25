from typing import Optional, Iterable, List, Union

from numpy import array


class SvdModel:
    Kappa: float
    Csv: Optional[array]
    RowsNum: int
    ColsNum: int
    X1_0: Optional[int, float]
    X2_0: Optional[int, float]
    X1: Optional[array]
    X2: Optional[array]
    U: Optional[array]
    P: array
    Q: array
    B: Optional[array]
    R2Norm: List
    Theta: List
    Solution: Optional[Iterable]
    def __init__(self, rowsNum: int,
                       colsNum: int,
                          x1_0: Union[int, float] = 0.,
                          x2_0: Union[int, float] = 0.,
                         kappa: float = 1.9) -> None: ...


    @staticmethod
    def GetColumn(numpy_array: array, idx: int) -> array: ...

    def EvalNorm(self) -> None: ...

    def EvalTheta(self) -> None: ...

    def BuildMatrixP(self) -> None: ...

    def BuildMatrixQ(self) -> None: ...

    def ErrorValue(self) -> float: ...

    @staticmethod
    def SaveAsCsv(array_like_data: array, file_name_str: str = "csv_file") -> None: ...

    def ApplyDecomposition(self) -> None: ...
