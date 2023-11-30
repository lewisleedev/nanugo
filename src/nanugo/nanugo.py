import genanki, tempfile, os, logging, itertools, shutil
from .tools import images
from collections import namedtuple
from .log import logger

log = logging.getLogger(__name__)

BuilderDeck = namedtuple("BuilderDeck", "deck media_list")
BuilderDeck.__doc__ = """Builds Anki deck object with media file list.
Args:
    deck (genanki.Deck): built deck object
    media_list (list): paths to media files
"""


class Builder:
    """Builder for nanugo. __init__ Prepares Model and tempdir.."""

    def __init__(self):
        self.model = genanki.Model(
            # Number below is intended to be hardcoded. It is not nessesary to be changed. Leave it as-is unless needed.
            2015122512,
            "Nanugo Model",
            fields=[{"name": "QuestionSide"}, {"name": "AnswerSide"}],
            templates=[
                {
                    "name": "Card1",
                    "qfmt": "{{QuestionSide}}<br>",
                    "afmt": '{{FrontSide}}<hr id="answer">{{AnswerSide}}',
                }
            ],
        )
        self.tempdir = tempfile.mkdtemp(
            prefix="nanugo_"
        )  # This should be deleted manually...
        logger.debug(f"tempdir created: {self.tempdir}")

    def build_deck(
        self,
        deck_name: str,
        pdf_path: str,
        vertical: bool = False,
        ratio: tuple = (0.5, 0.5),
        inversed: bool = False,
        rows: int = 1,
    ) -> BuilderDeck:
        """Builds Anki deck object with media file list.

        Args:
            deck_name (str): name of the deck
            pdf_path (str): path of the pdf file to make deck from.
            vertical (bool, optional): when enabled, pages will be split vertically and not horizontally. Defaults to False.
            ratio (tuple, optional): ratio to which each page will be split. If the sum of the ratios are not 1, it will raise a warning but not an error. If you intend to use non-sum-one numbers, you can ignore said warning. Defaults to (0.5, 0.5).
            inversed (bool, optional): when enabled, question side and answer side will be reversed, making top/left side the answer side and vice versa. Defaults to False.

        Returns:
            BuilderDeck: A BuilderDeck Object that has both genanki.Deck object and lists of paths to media files temporarily saved in tempdir.
        """
        if rows > 1 and vertical == True:
            logger.warning(
                "Multiple row conversion selected. Vertical setting will be ignored."
            )

        # DeckID is also intended to be hardcoded.
        deck = genanki.Deck(1564947522, deck_name)
        logger.debug(f"Conversion started: {os.path.split(pdf_path)[-1]}")
        converted_pdf = images.convert_pdf(pdf_path)
        logger.debug(f"Splitting started: {os.path.split(pdf_path)[-1]}")
        split_pdf = list(
            map(
                lambda page: images.split_page(
                    page, vertical=vertical, ratio=ratio, rows=rows
                ),
                converted_pdf,
            )
        )
        logger.debug(f"Splitting finished: {os.path.split(pdf_path)[-1]}")
        media_list = []

        for set in split_pdf:
            for index, page in enumerate(
                set
            ):  # This is where you should probably add progress bar to.
                q_side, a_side = page[::-1] if inversed else page

                q_side_path = os.path.join(
                    self.tempdir, f"{deck_name}_p{index}_q.jpeg"
                )  # TODO: randomizing name might be needed.
                a_side_path = os.path.join(self.tempdir, f"{deck_name}_p{index}_a.jpeg")
                q_side.save(q_side_path)
                logger.debug(f"Saved: {q_side_path}")
                a_side.save(a_side_path)
                logger.debug(f"Saved: {a_side_path}")

                media_list.extend([q_side_path, a_side_path])

                note = genanki.Note(
                    model=self.model,
                    fields=[
                        f'<div style="text-align: center;"><img src="{deck_name}_p{str(index)}_q.jpeg" /></div>',
                        f'<div style="text-align: center;"><img src="{deck_name}_p{str(index)}_a.jpeg" /></div>',
                    ],
                )

                deck.add_note(note)
                logger.debug("Deck successfully created.")

        return BuilderDeck(deck, media_list)

    def build_pkg(self, builder_decks: list) -> genanki.Package:
        """Builds genaki.Package object with provided deck(s) and media file(s).

        Args:
            builder_decks (list): List of BuilderDeck object.

        Returns:
            genanki.Package: A genanki.Package object containing all the decks and list of media files.
        """
        decks, media_list = map(list, zip(*builder_decks))
        logger.info(f"Total {len(decks)} deck(s) will be added to the package.")
        pkg = genanki.Package(decks)
        pkg.media_files = itertools.chain(*media_list)
        return pkg

    def __del__(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
            logger.debug(
                f"tempdir {self.tempdir} was removed and the Builder object will be deleted."
            )
