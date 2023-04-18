from io import StringIO
import anonypy
from core_pandas import dfAnonymizer
from ds4ml import DataSet
from src.protos import skynet_pb2
import s3fs
import pandas as pd
import numpy as np
print("imported anonimsation")


def anonimise(request: skynet_pb2.AnonimiseRequest) -> skynet_pb2.AnonimiseResponse:
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': 'https://'+'minio.k8s-nxt-01.datafid.world'},
                           key=request.minio_info.key,
                           secret=request.minio_info.secret,
                           token=request.minio_info.token,
                           )
    with fs.open(request.file_path, 'rb') as file_in:
        df = pd.read_csv(file_in,
                         low_memory=False,
                         usecols=[
                             key for key in request.deserialization_config.used_cols.keys()],
                         sep=request.deserialization_config.separator,
                         dtype=request.deserialization_config.used_cols,
                         na_values=[na_value for na_value in request.deserialization_config.na_values])

    if ("k_anonyme" == request.WhichOneof('anonimisationStrategy')):
        df = kanonyme(df, request.k_anonyme, request)
    if ("naive_strategy" == request.WhichOneof('anonimisationStrategy')):
        df = naive(df, request.naive_strategy, request)
    if ("synthetise" == request.WhichOneof('anonimisationStrategy')):
        df = synthetise(df, request.synthetise, request)

    with fs.open(request.serialization_config.file_path, 'wb') as file_out:
        csv_buffer = StringIO()
        df.to_csv(path_or_buf=csv_buffer,
                  sep=request.serialization_config.separator,
                  header=request.serialization_config.no_header)
        file_out.write(csv_buffer.getvalue())


def synthetise(df: pd.DataFrame, config: skynet_pb2.SynthetiseStrategy, request: skynet_pb2.AnonimiseRequest) -> pd.DataFrame:
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)

    dataset = DataSet(df, categories=[used_col for used_col in request.used_cols.keys(
    ) if (request.used_cols[used_col].col_types == skynet_pb2.ColType_Category)])

    return dataset.synthesize(epsilon=config.epsilon,
                              records=15000,
                              retains=[
                                  key for key in request.used_cols.keys()])


def naive(df: pd.DataFrame, config: skynet_pb2.NaiveStrategy, request: skynet_pb2.AnonimiseRequest) -> pd.DataFrame:
    anonimised_df = dfAnonymizer(df=df)

    for categorical_col in config.categorical_cols.keys():
        anonimisation_strategy = config.categorical_cols[categorical_col]
        if anonimisation_strategy == skynet_pb2.CATEGORICAL_EMAIL_MASKING:
            anonimised_df.categorical_email_masking(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.CATEGORICAL_FAKE:
            anonimised_df.categorical_fake(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.CATEGORICAL_FAKE_AUTO:
            anonimised_df.categorical_fake_auto(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.CATEGORICAL_RESAMPLING:
            anonimised_df.categorical_resampling(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.CATEGORICAL_TOKENIZATION:
            anonimised_df.categorical_tokenization(
                columns=categorical_col, inplace=True)

    for numerical_col in config.numerical_cols.keys():
        anonimisation_strategy = config.numerical_cols[numerical_col]
        if anonimisation_strategy == skynet_pb2.NUMERIC_BINNING:
            anonimised_df.numeric_binning(
                columns=numerical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.NUMERIC_MASKING:
            anonimised_df.numeric_masking(
                columns=numerical_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.NUMERIC_NOISE:
            mean = df[numerical_col].mean()/10
            anonimised_df.numeric_noise(
                columns=numerical_col, inplace=True, MIN=-mean, MAX=mean)
        elif anonimisation_strategy == skynet_pb2.NUMERIC_ROUNDING:
            anonimised_df.numeric_rounding(
                columns=numerical_col, inplace=True)

    for datetime_col in config.datetime_cols.keys():
        anonimisation_strategy = config.datetime_cols[datetime_col]
        if anonimisation_strategy == skynet_pb2.DATETIME_FAKE:
            anonimised_df.datetime_fake(
                columns=datetime_col, inplace=True)
        elif anonimisation_strategy == skynet_pb2.DATETIME_NOISE:
            anonimised_df.datetime_noise(
                columns=datetime_col, inplace=True)

    return anonimised_df.to_df()


def from_dtype_to_coltype(dtype: np.dtype) -> skynet_pb2.ColType:
    if (dtype.type == np.object_):
        return skynet_pb2.ColType_Object
    if (dtype.type == np.datetime64):
        return skynet_pb2.ColType_DateTime64
    if (dtype.type == np.int64):
        return skynet_pb2.ColType_Int64
    if (dtype.type == np.float64):
        return skynet_pb2.ColType_Float64
    if (dtype.type == np.bool_):
        return skynet_pb2.ColType_Bool
    if (dtype.type == np.timedelta64):
        return skynet_pb2.ColType_TimeDeltaMs
    if (dtype.type == pd.Categorical or dtype.type == pd.CategoricalDtype):
        return skynet_pb2.ColType_Object
    return skynet_pb2.ColType_Infer


def visualize(request: skynet_pb2.VisualizerRequest) -> skynet_pb2.VisualizerResponse:
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': 'https://'+'minio.k8s-nxt-01.datafid.world'},
                           key=request.minio_info.key,
                           secret=request.minio_info.secret,
                           token=request.minio_info.token,
                           )
    df = pd.DataFrame()
    with fs.open(request.file_path, 'rb') as file_in:
        df = pd.read_csv(file_in,
                         low_memory=False, nrows=100,
                         sep=request.deserialization_config.separator,
                         )

    table = dict()
    for key, value in df.dtypes.to_dict().items():
        col_type = from_dtype_to_coltype(value)
        values = []
        if (len(df[key]) < 100):
            values = df[key].astype(str).head(len(df[key])).to_list()
        else:
            values = df[key].astype(str).head(100).to_list()
        table[key] = skynet_pb2.Column(
            values=values,
            col_type=col_type
        )
    return skynet_pb2.VisualizerResponse(table=table)


def kanonyme(df: pd.DataFrame, config: skynet_pb2.KAnonymeStrategy, request: skynet_pb2.AnonimiseRequest) -> pd.DataFrame:
    categorical_columns = [used_col for used_col in request.used_cols.keys(
    ) if (request.used_cols[used_col].col_types == skynet_pb2.ColType_Category)]
    feature_columns = [used_col for used_col in request.used_cols.keys(
    ) if (request.used_cols[used_col].col_types != skynet_pb2.ColType_Category)]

    for name in categorical_columns:
        df[name] = df[name].astype("category")

    p = anonypy.Preserver(df,
                          feature_columns,
                          config.studied_column)

    if (config.algorithm == skynet_pb2.K_Anonym):
        rows = p.anonymize_k_anonymity(k=config.k)
    elif (config.algorithm == skynet_pb2.L_Diversity):
        rows = p.anonymize_l_diversity(k=config.k)
    elif (config.algorithm == skynet_pb2.T_CLOSENESS):
        rows = p.anonymize_t_closeness(k=config.k)
    return pd.DataFrame(rows)
