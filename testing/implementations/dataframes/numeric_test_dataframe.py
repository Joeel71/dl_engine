import os

from flogo.data.columns.categorical import CategoricalColumn
from flogo.data.columns.number import NumericColumn
from flogo.data.readers.delimeted_file_reader import DelimitedFileReader
from flogo.preprocessing.mappers.leaf.normalization_mapper import NormalizationMapper
from flogo.preprocessing.mappers.leaf.one_hot_mapper import OneHotMapper
from flogo.preprocessing.mappers.leaf.standarization_mapper import StandardizationMapper
from flogo.preprocessing.orchestrator import Orchestrator


def abs_path(part_path):
    return os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))) + part_path


path = abs_path("/resources/dataset_with_header.csv")

columns = {
    "work_year": CategoricalColumn(),
    "experience_level": CategoricalColumn(),
    "employment_type": CategoricalColumn(),
    "job_title": CategoricalColumn(),
    "salary": NumericColumn()}

dataframe = DelimitedFileReader(",").read(path, columns)

dataframe = Orchestrator(OneHotMapper(), NormalizationMapper(min=-1, max=1), StandardizationMapper()) \
    .process(dataframe,
             ["work_year", "experience_level", "employment_type", "job_title"],
             ["salary"],
             ["salary'"])

print(dataframe.column_names())
