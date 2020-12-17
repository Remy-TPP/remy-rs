import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


DEBUG = True

data_root_dir = Path(os.getenv('DATA_ROOT_DIR', Path(__file__).resolve().parents[2]))
print('data_root_dir', data_root_dir)

models_dir = data_root_dir / 'models'
models_dir.mkdir(parents=True, exist_ok=True)

model_fn = models_dir / 'model.dump'

processed_data_dir = data_root_dir / 'data' / 'processed'
processed_data_dir.mkdir(parents=True, exist_ok=True)

processed_data_fn = processed_data_dir / 'ratings.parquet'
