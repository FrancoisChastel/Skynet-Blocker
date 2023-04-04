from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CATEGORICAL_EMAIL_MASKING: CategoricalAnonimisation
CATEGORICAL_FAKE: CategoricalAnonimisation
CATEGORICAL_FAKE_AUTO: CategoricalAnonimisation
CATEGORICAL_RESAMPLING: CategoricalAnonimisation
CATEGORICAL_TOKENIZATION: CategoricalAnonimisation
ColType_Bool: ColType
ColType_Category: ColType
ColType_DateTime64: ColType
ColType_Float64: ColType
ColType_Infer: ColType
ColType_Int64: ColType
ColType_Object: ColType
ColType_TimeDeltaMs: ColType
DATETIME_FAKE: DateTimeAnonimisation
DATETIME_NOISE: DateTimeAnonimisation
DESCRIPTOR: _descriptor.FileDescriptor
K_Anonym: AnonymApproach
L_Diversity: AnonymApproach
NUMERIC_BINNING: NumericAnonimisation
NUMERIC_MASKING: NumericAnonimisation
NUMERIC_NOISE: NumericAnonimisation
NUMERIC_ROUNDING: NumericAnonimisation
T_CLOSENESS: AnonymApproach

class AnonimiseRequest(_message.Message):
    __slots__ = ["deserialization_config", "file_path", "k_anonyme", "minio_info", "naive_strategy", "serialization_config", "synthetise", "used_cols"]
    class UsedColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ColConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ColConfig, _Mapping]] = ...) -> None: ...
    DESERIALIZATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    K_ANONYME_FIELD_NUMBER: _ClassVar[int]
    MINIO_INFO_FIELD_NUMBER: _ClassVar[int]
    NAIVE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    SERIALIZATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SYNTHETISE_FIELD_NUMBER: _ClassVar[int]
    USED_COLS_FIELD_NUMBER: _ClassVar[int]
    deserialization_config: DeserializationConfig
    file_path: str
    k_anonyme: KAnonymeStrategy
    minio_info: MinioInfo
    naive_strategy: NaiveStrategy
    serialization_config: SerializationConfig
    synthetise: SynthetiseStrategy
    used_cols: _containers.MessageMap[str, ColConfig]
    def __init__(self, minio_info: _Optional[_Union[MinioInfo, _Mapping]] = ..., file_path: _Optional[str] = ..., used_cols: _Optional[_Mapping[str, ColConfig]] = ..., serialization_config: _Optional[_Union[SerializationConfig, _Mapping]] = ..., k_anonyme: _Optional[_Union[KAnonymeStrategy, _Mapping]] = ..., naive_strategy: _Optional[_Union[NaiveStrategy, _Mapping]] = ..., synthetise: _Optional[_Union[SynthetiseStrategy, _Mapping]] = ..., deserialization_config: _Optional[_Union[DeserializationConfig, _Mapping]] = ...) -> None: ...

class AnonimiseResponse(_message.Message):
    __slots__ = ["anonimised_file_path", "mapper_file_path"]
    ANONIMISED_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MAPPER_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    anonimised_file_path: str
    mapper_file_path: str
    def __init__(self, anonimised_file_path: _Optional[str] = ..., mapper_file_path: _Optional[str] = ...) -> None: ...

class ColConfig(_message.Message):
    __slots__ = ["col_types", "to_psuedonimise"]
    COL_TYPES_FIELD_NUMBER: _ClassVar[int]
    TO_PSUEDONIMISE_FIELD_NUMBER: _ClassVar[int]
    col_types: ColType
    to_psuedonimise: bool
    def __init__(self, col_types: _Optional[_Union[ColType, str]] = ..., to_psuedonimise: bool = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ["col_type", "values"]
    COL_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    col_type: ColType
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, col_type: _Optional[_Union[ColType, str]] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class DeserializationConfig(_message.Message):
    __slots__ = ["na_values", "separator", "used_cols"]
    class UsedColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ColConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ColConfig, _Mapping]] = ...) -> None: ...
    NA_VALUES_FIELD_NUMBER: _ClassVar[int]
    SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    USED_COLS_FIELD_NUMBER: _ClassVar[int]
    na_values: _containers.RepeatedScalarFieldContainer[str]
    separator: str
    used_cols: _containers.MessageMap[str, ColConfig]
    def __init__(self, used_cols: _Optional[_Mapping[str, ColConfig]] = ..., na_values: _Optional[_Iterable[str]] = ..., separator: _Optional[str] = ...) -> None: ...

class GeneralSegmentAndSadItemStrategy(_message.Message):
    __slots__ = ["general_segment_config", "sad_item_config", "serialization_config"]
    GENERAL_SEGMENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SAD_ITEM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SERIALIZATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    general_segment_config: SydoniaFileConfig
    sad_item_config: SydoniaFileConfig
    serialization_config: SerializationConfig
    def __init__(self, general_segment_config: _Optional[_Union[SydoniaFileConfig, _Mapping]] = ..., sad_item_config: _Optional[_Union[SydoniaFileConfig, _Mapping]] = ..., serialization_config: _Optional[_Union[SerializationConfig, _Mapping]] = ...) -> None: ...

class KAnonymeStrategy(_message.Message):
    __slots__ = ["algorithm", "k", "studied_column"]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    STUDIED_COLUMN_FIELD_NUMBER: _ClassVar[int]
    algorithm: AnonymApproach
    k: int
    studied_column: str
    def __init__(self, algorithm: _Optional[_Union[AnonymApproach, str]] = ..., studied_column: _Optional[str] = ..., k: _Optional[int] = ...) -> None: ...

class MinioInfo(_message.Message):
    __slots__ = ["key", "secret", "token"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    key: str
    secret: str
    token: str
    def __init__(self, key: _Optional[str] = ..., secret: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class NaiveStrategy(_message.Message):
    __slots__ = ["categorical_cols", "datetime_cols", "lang", "numerical_cols"]
    class CategoricalColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CategoricalAnonimisation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CategoricalAnonimisation, str]] = ...) -> None: ...
    class DatetimeColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DateTimeAnonimisation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DateTimeAnonimisation, str]] = ...) -> None: ...
    class NumericalColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NumericAnonimisation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[NumericAnonimisation, str]] = ...) -> None: ...
    CATEGORICAL_COLS_FIELD_NUMBER: _ClassVar[int]
    DATETIME_COLS_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    NUMERICAL_COLS_FIELD_NUMBER: _ClassVar[int]
    categorical_cols: _containers.ScalarMap[str, CategoricalAnonimisation]
    datetime_cols: _containers.ScalarMap[str, DateTimeAnonimisation]
    lang: str
    numerical_cols: _containers.ScalarMap[str, NumericAnonimisation]
    def __init__(self, lang: _Optional[str] = ..., categorical_cols: _Optional[_Mapping[str, CategoricalAnonimisation]] = ..., numerical_cols: _Optional[_Mapping[str, NumericAnonimisation]] = ..., datetime_cols: _Optional[_Mapping[str, DateTimeAnonimisation]] = ...) -> None: ...

class SerializationConfig(_message.Message):
    __slots__ = ["file_path", "no_header", "separator"]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    NO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    no_header: bool
    separator: str
    def __init__(self, file_path: _Optional[str] = ..., no_header: bool = ..., separator: _Optional[str] = ...) -> None: ...

class SydoniaAnonimiserRequest(_message.Message):
    __slots__ = ["minio_info", "sad_general_segment_and_sad_item_strategy"]
    MINIO_INFO_FIELD_NUMBER: _ClassVar[int]
    SAD_GENERAL_SEGMENT_AND_SAD_ITEM_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    minio_info: MinioInfo
    sad_general_segment_and_sad_item_strategy: GeneralSegmentAndSadItemStrategy
    def __init__(self, minio_info: _Optional[_Union[MinioInfo, _Mapping]] = ..., sad_general_segment_and_sad_item_strategy: _Optional[_Union[GeneralSegmentAndSadItemStrategy, _Mapping]] = ...) -> None: ...

class SydoniaAnonimiserResponse(_message.Message):
    __slots__ = ["anonimised_file_path"]
    class AnonimisedFilePathEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ANONIMISED_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    anonimised_file_path: _containers.ScalarMap[str, str]
    def __init__(self, anonimised_file_path: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SydoniaFileConfig(_message.Message):
    __slots__ = ["deserialization_config", "file_path", "used_cols"]
    class UsedColsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ColConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ColConfig, _Mapping]] = ...) -> None: ...
    DESERIALIZATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    USED_COLS_FIELD_NUMBER: _ClassVar[int]
    deserialization_config: DeserializationConfig
    file_path: str
    used_cols: _containers.MessageMap[str, ColConfig]
    def __init__(self, file_path: _Optional[str] = ..., used_cols: _Optional[_Mapping[str, ColConfig]] = ..., deserialization_config: _Optional[_Union[DeserializationConfig, _Mapping]] = ...) -> None: ...

class SynthetiseStrategy(_message.Message):
    __slots__ = ["epsilon"]
    EPSILON_FIELD_NUMBER: _ClassVar[int]
    epsilon: float
    def __init__(self, epsilon: _Optional[float] = ...) -> None: ...

class VisualizerRequest(_message.Message):
    __slots__ = ["minio_info"]
    MINIO_INFO_FIELD_NUMBER: _ClassVar[int]
    minio_info: MinioInfo
    def __init__(self, minio_info: _Optional[_Union[MinioInfo, _Mapping]] = ...) -> None: ...

class VisualizerResponse(_message.Message):
    __slots__ = ["table"]
    class TableEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Column
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Column, _Mapping]] = ...) -> None: ...
    TABLE_FIELD_NUMBER: _ClassVar[int]
    table: _containers.MessageMap[str, Column]
    def __init__(self, table: _Optional[_Mapping[str, Column]] = ...) -> None: ...

class AnonymApproach(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CategoricalAnonimisation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DateTimeAnonimisation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class NumericAnonimisation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ColType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
