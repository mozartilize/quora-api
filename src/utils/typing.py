from typing import Tuple, Union
from flask.wrappers import Response

ResponseType = Union[
    Response,
    Tuple[Response, int],
    Tuple[Response, int, dict]
]
