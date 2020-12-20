#!/usr/bin/env python3
import logging

from dotenv import find_dotenv, load_dotenv
import pandas as pd
import click

from remy_rs.utils.constants import processed_data_fn
from db.models import Interaction


def do_etl() -> pd.DataFrame:
    """Get all user-recipe ratings and store in pandas DataFrame."""
    interaction_field_names = ('uid', 'rid', 'rating')
    df = pd.DataFrame.from_records(
        Interaction.objects.all().values(*interaction_field_names)
    )
    return df


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    interactions_count = Interaction.objects.count()
    users_count = Interaction.objects.distinct('uid').count()
    recipes_count = Interaction.objects.distinct('rid').count()
    logger.info(f'''
        Some stats:
        User with reviews: {users_count}
        Recipe reviewed: {recipes_count}
        Interactions: {interactions_count}
    ''')

    dataset = do_etl()
    logger.debug(dataset[0:5])

    # Write to file
    # dataset.to_parquet(path=processed_data_fn, compression='uncompressed')
    dataset.to_parquet(path=processed_data_fn)
    logger.info(f'Wrote all interactions to {processed_data_fn}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found,
    # then load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
