import os
import os.path as pt


current_dir = os.getcwd()

DEFAULT_MODEL_FILE = pt.join(current_dir, 'CP/cp_model.mzn')
DEFAULT_INSTANCES_DIR = pt.join(current_dir, 'CP/instances_json')
DEFAULT_CP_OUTPUT_DIR = pt.join(current_dir, 'CP/cp_out')

os.makedirs(DEFAULT_CP_OUTPUT_DIR, exist_ok=True)
