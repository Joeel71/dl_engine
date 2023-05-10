import numpy as np

from flogo.data.columns.categorical import CategoricalColumn
from flogo.data.columns.number import NumericColumn
from flogo.data.dataframe import Dataframe
from flogo.preprocessing.mapper import Mapper


class OneHotMapper(Mapper):

    def map(self, dataframe: Dataframe, indexes):
        result = Dataframe()
        for column_name in indexes:
            categories, columns = self.apply(dataframe.get(column_name))
            dataframe.append_columns(self.__get_new_column_names(column_name, categories), columns)
        result.update(dataframe)
        return result

    def apply(self, column: CategoricalColumn):
        categories, inverse = np.unique(column.values, return_inverse=True)
        return categories, self.__create_columns(np.eye(categories.shape[0])[inverse])

    def __get_new_column_names(self, column_name, names):
        return [column_name + "_" + name for name in names]

    @staticmethod
    def __create_columns(one_hot_array):
        return [NumericColumn(one_hot_array[:, index]) for index in range(one_hot_array.shape[1])]
