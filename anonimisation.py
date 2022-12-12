from ds4ml import DataSet
from protos import protos
import s3fs
import pandas as pd
from anonympy.pandas import dfAnonymizer
from kalgoritm.algorithms import basic_mondrian, clustering_based, mondrian, top_down_greedy, datafly
from io import StringIO


def anonimise(request: protos.AnonimiseRequest) -> protos.AnonimiseResponse:
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': 'https://'+'minio.k8s-nxt-01.datafid.world'},
                           key=request.minio_info.key,
                           secret=request.minio_info.secret,
                           token=request.minio_info.token,
                           )
    protos.DeserializationConfig
    with fs.open(request.file_path, 'rb') as file_in:
        df = pd.read_csv(file_in,
                         low_memory=False,
                         usecols=request.deserialization_config.used_cols.keys()[
                             0],
                         sep=request.deserialization_config.separator,
                         dtype=request.deserialization_config.used_cols,
                         na_values=request.deserialization_config.na_values)

    with fs.open(request.serialization_config.file_path, 'wb') as file_out:
        csv_buffer = StringIO()
        df.to_csv(path_or_buf=csv_buffer,
                  sep=request.serialization_config.separator,
                  header=request.serialization_config.no_header)
        file_out.write(csv_buffer.getvalue())


def synthetise(df: pd.DataFrame, config: protos.SynthetiseStrategy, request: protos.AnonimiseRequest) -> pd.DataFrame:
    dataset = DataSet(df, categories=[used_col for used_col in request.used_cols.keys(
    ) if (request.used_cols[used_col].col_types == protos.ColType.ColType_Category)])

    return dataset.synthesize(epsilon=config.epsilon,
                              records=request.serialization_config.records_limit)


def naive(df: pd.DataFrame, config: protos.NaiveStrategy, request: protos.AnonimiseRequest) -> pd.DataFrame:
    anonimised_df = dfAnonymizer(df=df)
    for categorical_col in config.categorical_cols.keys():
        anonimisation_strategy = config.categorical_cols[categorical_col]
        if anonimisation_strategy == protos.CategoricalAnonimisation.CATEGORICAL_EMAIL_MASKING:
            anonimised_df.categorical_email_masking(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == protos.CategoricalAnonimisation.CATEGORICAL_FAKE:
            anonimised_df.categorical_fake(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == protos.CategoricalAnonimisation.CATEGORICAL_FAKE_AUTO:
            anonimised_df.categorical_fake_auto(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == protos.CategoricalAnonimisation.CATEGORICAL_RESAMPLING:
            anonimised_df.categorical_resampling(
                columns=categorical_col, inplace=True)
        elif anonimisation_strategy == protos.CategoricalAnonimisation.CATEGORICAL_TOKENIZATION:
            anonimised_df.categorical_tokenization(
                columns=categorical_col, inplace=True)

    for numerical_col in config.numerical_cols.keys():
        anonimisation_strategy = config.numerical_cols[numerical_col]
        if anonimisation_strategy == protos.NumericAnonimisation.NUMERIC_BINNING:
            anonimised_df.numeric_binning(
                columns=numerical_col, inplace=True)
        elif anonimisation_strategy == protos.NumericAnonimisation.NUMERIC_MASKING:
            anonimised_df.numeric_masking(
                columns=numerical_col, inplace=True)
        elif anonimisation_strategy == protos.NumericAnonimisation.NUMERIC_NOISE:
            anonimised_df.numeric_noise(
                columns=numerical_col, inplace=True)
        elif anonimisation_strategy == protos.NumericAnonimisation.NUMERIC_ROUNDING:
            anonimised_df.numeric_rounding(
                columns=numerical_col, inplace=True)

    for datetime_col in config.datetime_cols.keys():
        anonimisation_strategy = config.datetime_cols[datetime_col]
        if anonimisation_strategy == protos.DateTimeAnonimisation.DATETIME_FAKE:
            anonimised_df.datetime_fake(
                columns=datetime_col, inplace=True)
        elif anonimisation_strategy == protos.DateTimeAnonimisation.DATETIME_NOISE:
            anonimised_df.datetime_noise(
                columns=datetime_col, inplace=True)

    return anonimised_df.to_df()


def kanonyme(df: pd.DataFrame, config: protos.KAnonymeStrategy, request: protos.AnonimiseRequest) -> pd.DataFrame:
    if (config.algorithm == protos.KAnonymeAlgorithm.BASIC_MONDRIAN):
        basic_mondrian.basic_mondrian_anonymize(df)
    elif (config.algorithm == protos.KAnonymeAlgorithm.DATAFLY):
        datafly.datafly_anonymize(df)
    elif (config.algorithm == protos.KAnonymeAlgorithm.CLASSIC_MONDRIAN):
        basic_mondrian.basic_mondrian_anonymize(df)
    elif (config.algorithm == protos.KAnonymeAlgorithm.TOPDOWN_GREEDY):
        top_down_greedy.tdg_anonymize(df)
    elif (config.algorithm == protos.KAnonymeAlgorithm.INCOGNITO):
        clustering_based.cluster_based_anonymize(df)
