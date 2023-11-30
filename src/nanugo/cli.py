from glob import glob
from .tools import validations
from .log import logger
from .nanugo import Builder
import pkg_resources
import argparse, sys, os, logging


def main(args=None):
    parsed_args = get_args(args)

    if parsed_args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(parsed_args)

    pkg_name = parsed_args.package_name[0]
    export_file_path = os.path.join(parsed_args.dest, f"{pkg_name}.apkg")

    validations.file_exists_prompt(export_file_path, pkg_name)

    file_paths = []

    for arg in parsed_args.pdf_files:
        try:
            validations.pdf_file_arg(arg)
            file_paths += glob(arg)
        except:
            sys.exit()

    logger.info(f"Total {len(file_paths)} file(s) will be converted.")

    builder = Builder()
    decks = []

    file_name_only = lambda path: os.path.splitext(os.path.basename(path))[0]

    for file in file_paths:
        deck = builder.build_deck(
            file_name_only(file),
            file,
            ratio=tuple(parsed_args.ratio),
            vertical=parsed_args.vertical,
            inversed=parsed_args.inversed,
            rows=parsed_args.rows,
        )
        decks.append(deck)

    pkg = builder.build_pkg(decks)
    pkg.write_to_file(export_file_path)

    logger.info(f"Conversion completed: {export_file_path}")

    # No need for explicit return
    # return pkg


def get_args(args):
    parser = get_parser()
    return parser.parse_args(args)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description="Turn your handwritten pdf sheets to Anki deck(s).",
        epilog="by @lewisleedev",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "package_name",
        action="store",
        type=str,
        nargs=1,
        help="File name for your .apkg file. Do not put file extension in the end.",
    )
    parser.add_argument(
        "pdf_files",
        help="Input PDF file to convert",
        nargs="*",
    )
    parser.add_argument(
        "-d,",
        "--dest",
        dest="dest",
        metavar="",
        action="store",
        type=validations.dir_path,
        default="./",
        help="Destination folder for your .apkg output. Defaults to current directory.",
    )
    parser.add_argument(
        "--ratio",
        dest="ratio",
        metavar="",
        action="store",
        type=float,
        nargs=2,
        default=(0.5, 0.5),
        help="Custom ratio to which each pages will be split. Defaults to (0.5 0.5). It's best to keep the sum of the ratios to 1. First number is the ratio for the top or left.",
    )
    parser.add_argument(
        "--inversed",
        "-i",
        dest="inversed",
        action="store_true",
        help="Inverses the Question/Answer side.",
    )
    parser.add_argument(
        "--vertical",
        "-v",
        dest="vertical",
        action="store_true",
        help="Splits vertically instead of horizontally",
    )
    parser.add_argument(
        "--debug",
        "--d",
        dest="debug",
        action="store_true",
        help="For even bigger nerds",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=pkg_resources.get_distribution("nanugo").version,
        help="Shows version and exits.",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=1,
        help="Number of rows for vertical splitting (default: 1). By having rows value bigger than 1, each row will only be cut vertically.",
    )

    return parser


if __name__ == "__main__":
    main()
