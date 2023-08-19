import os, sys
from glob import glob
from ..log import logger


def dir_path(path: str) -> None:
    """Check if given path actually exists.

    Args:
        path (str): path for the validation

    Raises:
        NotADirectoryError
    """
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def file_exists_prompt(export_file_path, pkg_name):
    """Check if file exists. If exists, ask for user input.

    Arguments:
        export_file_path -- Path to be checked
        pkg_name -- Name for the package.
    """
    if os.path.isfile(export_file_path):
        logger.debug(
            f"os.path.isfile(export_file_path) = {os.path.isfile(export_file_path)}"
        )
        answer = input(
            f"File {pkg_name}.apkg already exists! Do you want to proceed anyway? (y/n): "
        )
        if answer.lower() in ["y", "Y"]:
            pass
        else:
            logger.info("Anki package was not created.")
            sys.exit()


def pdf_file_arg(arg):
    """Check if the given path argument(and plain path) is valid and according file(s) exist(s).

    Arguments:
        arg -- Path argument (can also contain wildcard)

    Raises:
        FileNotFoundError
    """
    if len(glob(arg)) == 0:
        raise FileNotFoundError(
            f"Cannot find any files that matches the following argument: {arg}"
        )
    else:
        pass
