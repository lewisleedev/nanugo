from typing import List, Dict, Tuple
import pypdfium2 as pdfium
import PIL, logging, warnings, os
from ..log import logger


def convert_pdf(pdf_path: str) -> List[Dict[int, PIL.Image.Image]]:
    """Converts PDF files to PIL.Image.Image object.

    Args:
        pdf_path (str): Path for the pdf file to be converted

    Returns:
        List[Dict[int, PIL.Image.Image]]: List of PIL.Image.Image objects.
    """
    result = []

    pdf_file = pdfium.PdfDocument(pdf_path)
    page_indicies = [i for i in range(len(pdf_file))]

    # If your code shall be frozen into an executable, multiprocessing.freeze_support() needs to be called at the start of the if __name__ == "__main__": block if using this method.
    renderer = pdf_file.render(pdfium.PdfBitmap.to_pil, page_indices=page_indicies)

    for image in renderer:
        result.append(image)

    logger.debug(
        f"{len(result)} pages has been successfully rendered: {os.path.split(pdf_path)[-1]}"
    )

    return result


def split_page(
    image: PIL.Image.Image,
    vertical: bool = False,
    ratio: tuple = (0.5, 0.5),
    rows: int = 1,
) -> Tuple[PIL.Image.Image, PIL.Image.Image]:
    """Splits given PIL.Image.Image object into two.

    Args:
        image (PIL.Image.Image): PIL.Image.Image object to be split
        vertical (bool, optional): if true, the image will be split vertically, not horizontally. Defaults to False.
        ratio (tuple, optional): ratio to which the image will be split. Defaults to (0.5, 0.5).

    Returns:
        Tuple[PIL.Image.Image, PIL.Image.Image]: A tuple of two PIL.Image.Image objects. First Image will going to be the top/left one by default.
    """
    d_width, d_height = image.size  # Get default sizes

    if sum(ratio) != 1:
        warnings.warn(
            "Custom ratio was given but the sum of it is not 1. If this is intended, you can safely ignore this warning.",
            UserWarning,
        )

    if rows == 1:
        if vertical:
            ratio_l, ratio_r = ratio
            image_l = image.crop((0, 0, d_width * ratio_l, d_height))
            image_r = image.crop((d_width * (1 - ratio_r), 0, d_width, d_height))

            return [(image_l, image_r)]

        else:
            ratio_t, ratio_b = ratio
            image_t = image.crop((0, 0, d_width, d_height * ratio_t))
            image_b = image.crop((0, d_height * (1 - ratio_b), d_width, d_height))

            return [(image_t, image_b)]

    elif rows > 1:
        ratio_l, ratio_r = ratio
        row_height = d_height // rows

        image_sets = []

        for i in range(rows):
            row_start = i * row_height
            row_end = (i + 1) * row_height if i < rows - 1 else d_height

            image_row = image.crop((0, row_start, d_width, row_end))

            image_row_l = image_row.crop((0, 0, d_width * ratio_l, row_height))
            image_row_r = image_row.crop(
                (d_width * (1 - ratio_r), 0, d_width, row_height)
            )

            image_sets.append((image_row_l, image_row_r))

        return image_sets
