#!/usr/bin/env python3
import pandas as pd
import surprise

from remy_rs.utils.constants import processed_data_fn, model_fn


def get_df_from_parquet() -> pd.DataFrame:
    return pd.read_parquet(processed_data_fn)


def train(dataset: surprise.dataset.Dataset) -> surprise.prediction_algorithms.AlgoBase:
    algo = surprise.SVD()

    cv_iterator = 5
    # cv_iterator = surprise.model_selection.ShuffleSplit(n_splits=10, test_size=0.2)

    surprise.model_selection.cross_validate(
        algo, dataset, cv=cv_iterator, n_jobs=-1,
        measures=['rmse', 'mae'],  # 'fcp'
        return_train_measures=True, verbose=True,
    )

    trainset = dataset.build_full_trainset()
    testset = trainset.build_testset()

    # TODO: Verificar
    algo.fit(trainset)

    print('running test')
    predictions = algo.test(testset)
    print('test done')
    surprise.accuracy.rmse(predictions)

    return algo


def save_model(model: surprise.prediction_algorithms.AlgoBase):
    surprise.dump.dump(model_fn, algo=model)


def main():
    df = get_df_from_parquet()
    print('data loaded')

    dataset = surprise.Dataset.load_from_df(
        df[['uid', 'rid', 'rating']], surprise.Reader(rating_scale=(0, 5))
    )

    trainset = dataset.build_full_trainset()
    print(trainset.global_mean, trainset.rating_scale)

    model = train(dataset)

    save_model(model)


if __name__ == '__main__':
    main()
