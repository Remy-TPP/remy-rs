from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class Interaction(models.Model):
    uid = models.IntegerField(db_column='profile_id')
    rid = models.IntegerField(db_column='recipe_id')
    cooked_at = ArrayField(models.DateTimeField(), default=list)
    rating = models.DecimalField()

    class Meta:
        # TODO: managed = False?
        managed = False
        db_table = 'recipes_interaction'
        unique_together = ['uid', 'rid']

    def __str__(self) -> str:
        return f'{self.rating} for user {self.uid} and recipe {self.rid}'


class Recipe(models.Model):

    class Meta:
        managed = False
        db_table = 'recipes_recipe'

    def __str__(self) -> str:
        return f'Recipe with id {self.pk}'
