from .main import create_app, create_limiters

__all__ = ["create_app"]
__version__ = "0.3.1"


app = create_app(create_limiters())
