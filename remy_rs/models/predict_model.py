#!/usr/bin/env python3
from collections import defaultdict
from typing import List, Tuple

import click
import surprise
import numpy as np

from remy_rs.utils.constants import DEBUG, DITHERING_ENABLED, model_fn


class ModelNotTrainedError(RuntimeError):
    pass


def load_model() -> surprise.prediction_algorithms.AlgoBase:
    print('model_fn', model_fn)
    _, model = surprise.dump.load(model_fn)
    return model


def predict(model: surprise.prediction_algorithms.AlgoBase,
            user_id: int,
            recipe_id: int,
            ) -> surprise.prediction_algorithms.predictions.Prediction:
    iuid, irid = model.trainset.to_inner_uid(user_id), model.trainset.to_inner_iid(recipe_id)
    r_ui = dict(model.trainset.ur.get(iuid, [])).get(irid, None)
    return model.predict(uid=user_id, iid=recipe_id, r_ui=r_ui, verbose=DEBUG)


# TODO
# 1. Predecir ratings para todas las recipes
# 2. Sort by rating
# 3. Dithering?
# 4. Devolver n primeras
# 5. Hacer post procesamiento en Remy API! ... o acá??
def top_n(model: surprise.prediction_algorithms.AlgoBase,
          user_id: int,
          n: int = 10,
          ) -> List[surprise.prediction_algorithms.predictions.Prediction]:
    # 1. Buildear testset con lista de user_id,[cada recipe_id]
    # 2. model.test(testset)
    # 3. ...
    iuid = model.trainset.to_inner_uid(user_id)
    # print(user_id, 'user_id')
    # print(iuid, 'iuid')
    # print('user biases', model.bu)
    # print('item biases', model.bi)
    # print('model.trainset.ir', model.trainset.ir)
    # print('model.trainset.ur', model.trainset.ur)
    # print('default_prediction', model.default_prediction())

    user_ratings = dict(model.trainset.ur.get(iuid, defaultdict(lambda: None)))
    # print('user_ratings', user_ratings)

    # TODO: breaks if it grabs something not in the trainset
    # TODO: quite inefficient to not just store list of raw ids in trained model
    testset = [(user_id, model.trainset.to_raw_iid(iiid), user_ratings.get(iiid, None))
               for iiid in model.trainset.ir.keys()]

    predictions = model.test(testset)

    # for prediction in predictions:
    #     print('>', prediction)

    predictions.sort(key=lambda p: -(p.r_ui if p.r_ui else p.est))
    if DITHERING_ENABLED:
        predictions = dither_recs(predictions)

    for prediction in predictions:
        print('<', prediction)

    if n:
        predictions = predictions[:n]
    return predictions


def dither_recs(recs):
    sigma = 0.8
    dist = np.random.default_rng().normal(0.0, sigma, len(recs))
    new_ranks = np.array([np.log(rank + 1) for rank in range(len(recs))]) + dist
    return [p for p, r in sorted(zip(recs, new_ranks), key=lambda t: t[1])]


# TODO: similar_recipes con model.get_neighbors ?


# TODO: here and everywhere: replace all print's with logging
class RemyPredictor:
    model: surprise.prediction_algorithms.AlgoBase = None

    def __init__(self):
        self.reload()
        if self.model:
            print('Predictor ready!')

    # TODO: how to detect changes in model file and reload? or should Airflow tell me?
    def reload(self):
        try:
            self.model = load_model()
            print('Model reloaded')
        except FileNotFoundError:
            print('Model file not found, you should train more')
            self.model = None

    def verify_model(self):
        if not self.model:
            self.reload()
        if not self.model:
            raise ModelNotTrainedError

    def predict_rating(self, **kwargs) -> float:
        self.verify_model()
        return predict(model=self.model, **kwargs)

    def top_n(self, **kwargs) -> List[Tuple[int, float]]:
        self.verify_model()
        return top_n(model=self.model, **kwargs)


@click.command()
@click.argument('user_id', type=click.INT)
@click.argument('recipe_id', type=click.INT)
def main(user_id: int, recipe_id: int) -> float:
    # global model
    # model = load_model()
    model: surprise.prediction_algorithms.AlgoBase = load_model()
    print('model loaded')

    prediction = predict(model, user_id, recipe_id)
    print(f'predicted value: {prediction.est}')
    # print(prediction)
    # Return estimation

    n = 100
    _ = top_n(model, user_id, n=n)
    print(f'\nTOP N={n} for user {user_id}')
    # for p in predictions:
    #     print(p)

    return prediction.est


if __name__ == '__main__':
    main()
