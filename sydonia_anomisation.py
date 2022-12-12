from protos import protos
import s3fs
import pandas as pd
import hashlib
from io import StringIO


def anonimise_sydonia(request: protos.SydoniaAnonimiserRequest) -> protos.SydoniaAnonimiserResponse:
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': 'https://'+'minio.k8s-nxt-01.datafid.world'},
                           key=request.minio_info.key,
                           secret=request.minio_info.secret,
                           token=request.minio_info.token,
                           )
    return SadGeneralSadItemAnonimiser(request.sad_general_segment_and_sad_item_strategy, fs)


def SadGeneralSadItemAnonimiser(conf: protos.GeneralSegmentAndSadItemStrategy, fs: s3fs.S3FileSystem) -> protos.SydoniaAnonimiserResponse:
    protos.DeserializationConfig
    with fs.open(conf.general_segment_config.file_path, 'rb') as file_in:
        df_general_segment = pd.read_csv(file_in,
                                         low_memory=False,
                                         usecols=conf.general_segment_config.deserialization_config.used_cols.keys()[
                                             0],
                                         sep=conf.general_segment_config.deserialization_config.separator,
                                         dtype=conf.general_segment_config.deserialization_config.used_cols,
                                         na_values=conf.general_segment_config.deserialization_config.na_values)

    with fs.open(conf.sad_item_config.file_path, 'rb') as file_in:
        df_sad_item = pd.read_csv(file_in,
                                  low_memory=False,
                                  usecols=conf.sad_item_config.deserialization_config.used_cols.keys()[
                                      0],
                                  sep=conf.sad_item_config.deserialization_config.separator,
                                  dtype=conf.sad_item_config.deserialization_config.used_cols,
                                  na_values=conf.sad_item_config.deserialization_config.na_values)
    df_asycuda = pd.merge(df_sad_item, df_general_segment,
                          on="INSTANCEID", how="outer")

    # Rule 1: Remove products with less than 3 importers
    df_asycuda["nb_importateur_product"] = df_asycuda.groupby(
        "TAR_HSC_NB1")["CMP_CON_COD"].transform('count')
    df_asycuda = df_asycuda.loc[df_asycuda["nb_importateur_product"] >= 3]
    df_asycuda.drop(columns=['nb_importateur_product'])

    # Rule 2: Filter out products for which one importer represents more than 85% of the value
    df_asycuda["totval"] = df_asycuda.groupby(
        'TAR_HSC_NB1')['VIT_STV'].transform('sum')
    df_asycuda["totval_con"] = df_asycuda.groupby(['TAR_HSC_NB1', 'CMP_CON_COD'])[
        'VIT_STV'].transform('sum')
    df_asycuda[:, 'ratio'] = df_asycuda.loc[:,
                                            'totval_con'] / df_asycuda.loc[:, 'totval']

    df_asycuda = df_asycuda.loc[df_asycuda['ratio'] <= 0.85]['TAR_HSC_NB1']
    df_asycuda.drop(columns=['totval', 'totval_con', 'ratio'])

    hash_md5 = hashlib.md5()
    # Anonimise columns
    for column in ['CMP_CON_COD', 'CMP_EXP_COD', 'CMP_FIS_COD', 'DEC_COD', 'EXA_EXA', 'EXA_CEX']:
        df_asycuda[column] = df_asycuda[column].apply(
            lambda x: anonimise_md5_value(hash_md5, x) if (pd.notnull(x)) else x, axis=1)

    with fs.open(conf.serialization_config.file_path, 'wb') as file_out:
        csv_buffer = StringIO()
        df_asycuda.to_csv(path_or_buf=csv_buffer,
                          sep=conf.serialization_config.separator,
                          header=conf.serialization_config.no_header)
        file_out.write(csv_buffer.getvalue())

    return df_asycuda, conf


def anonimise_md5_value(hash_md5: hashlib._Hash, value: str):
    hash_md5 = hash_md5.update(value)
    hash_md5.hexdigest()
