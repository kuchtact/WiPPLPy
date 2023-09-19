"""
The `~wipplypy.modules` subpackage contains commonly used functions and classes 
for loading and modifying data.
"""
__all__ = ["shot_loader"]

from wipplpy.modules import shot_loader
from wipplpy.modules.shot_loader import (
    get_connector,
    get_remote_shot_tree,
    most_recent_shot,
)
