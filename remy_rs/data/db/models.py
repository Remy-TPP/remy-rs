from django.db import models


class Interaction(models.Model):
    # TODO: replace with actual models?
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    uid = models.IntegerField()
    # recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    rid = models.IntegerField()
    rating = models.FloatField()
    # TODO: change to DECIMAL
    # TODO: validator for rating in range [0; 5]

    class Meta:
        # TODO: managed = False?
        db_table = 'recipe_interactions'
        unique_together = ['uid', 'rid']

    def __str__(self) -> str:
        return f'{self.rating} for user {self.uid} and recipe {self.rid}'
