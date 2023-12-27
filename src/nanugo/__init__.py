"""
Nanugo allows you to generate Anki decks from PDF files using both an easy-to-use CLI or as a Python module. You can think of it as creating a real-life flashcard—similar to folding (or, in this case, cutting) a piece of paper in half (or with recent update, in multiple pieces!)

## Quickstart
```shell
$ nanugo /path/to/pdf

# Check out all the functionalities with
$ nanugo --help
```

"""

__docformat__ = "google"

from .tools import images
from . import nanugo, log
