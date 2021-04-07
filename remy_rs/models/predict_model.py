#!/usr/bin/env python3
from collections import defaultdict, namedtuple
from typing import List, Tuple

import click
import surprise
import surprise.prediction_algorithms as surprise_algos
import numpy as np

from remy_rs.utils.constants import DEBUG, DITHERING_ENABLED, model_fn
from remy_rs.data.db.models import Recipe


class ModelNotTrainedError(RuntimeError):
    pass


GroupPrediction = namedtuple('GroupPrediction', ['iid', 'est'])


def load_model() -> surprise_algos.AlgoBase:
    print('model_fn', model_fn)
    _, model = surprise.dump.load(model_fn)
    return model


def get_iuid(model: surprise_algos.AlgoBase, user_id: int) -> int:
    try:
        return model.trainset.to_inner_uid(user_id)
    except ValueError:
        # unknown user
        # TODO: replace with UNKNOWN_USER constant
        return -1


def predict(model: surprise_algos.AlgoBase,
            user_id: int,
            recipe_id: int,
            ) -> surprise_algos.predictions.Prediction:
    try:
        iuid, irid = model.trainset.to_inner_uid(user_id), model.trainset.to_inner_iid(recipe_id)
        r_ui = dict(model.trainset.ur.get(iuid, [])).get(irid, None)
    except ValueError:
        # unknown user or recipe
        r_ui = None
    return model.predict(uid=user_id, iid=recipe_id, r_ui=r_ui, verbose=DEBUG)


def predict_for_user(
        model: surprise_algos.AlgoBase,
        user_id: int
        ) -> List[surprise_algos.predictions.Prediction]:
    iuid = get_iuid(model, user_id)
    user_ratings = dict(model.trainset.ur.get(iuid, defaultdict(lambda: None)))

    recipes_ids = {model.trainset.to_raw_iid(iiid): iiid for iiid in model.trainset.ir.keys()}

    testset = [(user_id, recipe.id, user_ratings.get(recipes_ids.get(recipe.id, None), None))
               for recipe in Recipe.objects.all()]

    return model.test(testset)


def top_n(model: surprise_algos.AlgoBase,
          user_id: int,
          n: int = 10,
          ) -> List[surprise_algos.predictions.Prediction]:
    predictions = predict_for_user(model, user_id)

    predictions.sort(key=lambda p: -(p.r_ui if p.r_ui else p.est))
    if DITHERING_ENABLED:
        predictions = dither_recs(predictions)

    for prediction in predictions:
        print('<', prediction)

    if n:
        predictions = predictions[:n]
    return predictions


def group_top_n(
        model: surprise_algos.AlgoBase,
        user_ids: List[int],
        n: int = 10,
        ) -> List[GroupPrediction]:

    users_predictions = [predict_for_user(model, user_id) for user_id in user_ids]

    def avg_score(recipe_predictions):
        recipe_scores = ([(up.r_ui if up.r_ui else up.est) for up in recipe_predictions])
        return sum(recipe_scores) / len(recipe_scores)

    # transpose list and determine a group score/prediction for each recipe
    group_predictions = [GroupPrediction(iid=rpp[0].iid, est=avg_score(rpp))
                         for rpp in list(map(list, zip(*users_predictions)))]

    group_predictions.sort(key=lambda p: -p.est)
    if DITHERING_ENABLED:
        group_predictions = dither_recs(group_predictions)

    for prediction in group_predictions:
        print('<', prediction)

    if n:
        group_predictions = group_predictions[:n]
    return group_predictions


def dither_recs(
        recs: List[surprise_algos.predictions.Prediction],
        sigma: float = 0.7
        ) -> List[surprise_algos.predictions.Prediction]:
    # add normally distributed "noise" to log of original rank
    dist = np.random.default_rng().normal(0.0, sigma, len(recs))
    new_ranks = np.array([np.log(rank + 1) for rank in range(len(recs))]) + dist
    # sort recommendations with new rank, without altering score
    return [p for p, r in sorted(zip(recs, new_ranks), key=lambda t: t[1])]


# TODO: similar_recipes con model.get_neighbors ?


# TODO: here and everywhere: replace all print's with logging
class RemyPredictor:
    model: surprise_algos.AlgoBase = None

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

    def group_top_n(self, **kwargs):
        self.verify_model()
        return group_top_n(model=self.model, **kwargs)


@click.command()
@click.argument('user_id', type=click.INT)
@click.argument('recipe_id', type=click.INT)
def main(user_id: int, recipe_id: int) -> float:
    # global model
    # model = load_model()
    model: surprise_algos.AlgoBase = load_model()
    print('model loaded')

    prediction = predict(model, user_id, recipe_id)
    print(f'predicted value: {prediction.est}')
    # print(prediction)
    # Return estimation

    n = 100
    print(f'\n--- TOP N={n} for user {user_id} ---')
    _ = top_n(model, user_id, n=n)
    # for p in predictions:
    #     print(p)

    print('\n--- GROUP TOP N ---')
    group_top_n(model, [user_id, 3, 5], n=n)

    return prediction.est


if __name__ == '__main__':
    main()
