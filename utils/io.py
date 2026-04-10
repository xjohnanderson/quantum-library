# utils/io.py
# Manages a volatile outputs directory and provides script-specific prefixes.

import os
import shutil
import inspect

def prepare_output_dir(dir_name="outputs"):
    """
    Clears the specified directory relative to the script that called this function.
    Returns: (out_dir_path, script_prefix)
    """
    # Get the file path of the script that called this function
    frame = inspect.stack()[1]
    caller_path = os.path.abspath(frame.filename)
    caller_dir = os.path.dirname(caller_path)
    
    # Get script name without extension (e.g., 'teleportation_demo')
    script_prefix = os.path.splitext(os.path.basename(caller_path))[0]
    
    base_path = os.path.join(caller_dir, dir_name)
    
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    
    os.makedirs(base_path, exist_ok=True)
    return base_path, script_prefix