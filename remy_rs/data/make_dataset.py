#!/usr/bin/env python3
import os
os.environ.setdefault('DB_APP_NAME', 'db')
import logging  # noqa: E402

from dotenv import find_dotenv, load_dotenv  # noqa: E402
import pandas as pd  # noqa: E402
import click  # noqa: E402

from remy_rs.utils.constants import processed_data_fn  # noqa: E402
from db.models import Interaction  # noqa: E402


DEBUG = os.getenv('DEBUG', os.getenv('ENV', 'production') != 'production')


def do_etl() -> pd.DataFrame:
    """Get all user-recipe ratings and store in pandas DataFrame."""
    interaction_field_names = ('uid', 'rid', 'rating')
    user_ratings = Interaction.objects.filter(rating__isnull=False)
    df = pd.DataFrame.from_records(
        user_ratings.all().values(*interaction_field_names)
    )
    return df


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    user_ratings = Interaction.objects.filter(rating__isnull=False)
    logging.info(f'All interactions with rating:\n{user_ratings}')
    interactions_count = Interaction.objects.count()
    users_count = user_ratings.distinct('uid').count()
    recipes_count = user_ratings.distinct('rid').count()
    logger.info(f'''
        Some stats:
        User with reviews: {users_count}
        Recipe reviewed: {recipes_count}
        Interactions: {interactions_count}
    ''')

    dataset = do_etl()
    logger.debug(dataset[0:5])

    # Write to file
    if DEBUG:
        dataset.to_parquet(path=processed_data_fn, compression='uncompressed')
    else:
        dataset.to_parquet(path=processed_data_fn)
    logger.info(f'Wrote all interactions to {processed_data_fn}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found,
    # then load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
