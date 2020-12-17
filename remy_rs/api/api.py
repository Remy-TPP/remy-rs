from typing import List

from fastapi import FastAPI, responses
from pydantic import BaseModel

from remy_rs.models.predict_model import RemyPredictor


api: FastAPI = FastAPI()
rs: RemyPredictor = RemyPredictor()


class RecipePrediction(BaseModel):
    recipe_id: int
    rating: float
    real: bool


class UserPrediction(BaseModel):
    user_id: int
    prediction: RecipePrediction


class UserPredictions(BaseModel):
    user_id: int
    size: int
    predictions: List[RecipePrediction]


def roundRating(r: float) -> float:
    return round(r, 3)


@api.get('/')
def home():
    return responses.RedirectResponse('/docs')


@api.get('/recommendations/user/{user_id}/recipe/{recipe_id}')
def predict_a_rating(user_id: int, recipe_id: int) -> UserPrediction:
    (uid, rid, r_ui, est, _) = rs.predict_rating(user_id=user_id, recipe_id=recipe_id)
    # If already rated use that instead
    predicted_rating, real = (r_ui, True) if r_ui else (est, False)
    pred = RecipePrediction(recipe_id=recipe_id, rating=roundRating(predicted_rating), real=real)
    return UserPrediction(user_id=user_id, prediction=pred)


# TODO: document falsey value (0 or None) for n give all recs for user
@api.get('/recommendations/user/{user_id}')
def user_top_n(user_id: int, n: int = 10) -> UserPredictions:
    predictions = rs.top_n(user_id=user_id, n=n)
    # If already rated use that instead
    predictions = [RecipePrediction(recipe_id=rid, rating=roundRating(r_ui if r_ui else est), real=bool(r_ui))
                   for (uid, rid, r_ui, est, _) in predictions]
    return UserPredictions(user_id=user_id, size=len(predictions), predictions=predictions)
