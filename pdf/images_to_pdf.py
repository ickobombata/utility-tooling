# python images_to_pdf.py lk*.png doc.png dec.png
# python images_to_pdf.py aa/a*

from fpdf import FPDF
from PIL import Image
import sys
from os import walk, remove
import math

x_screen = 595
y_screen = 841

def resize_image(width, height):
    w_ratio = x_screen / width
    h_ratio = y_screen / height
    if (w_ratio < 1 and w_ratio > 0) or (h_ratio < 1 and h_ratio > 0):
        ratio = w_ratio if w_ratio < h_ratio else h_ratio
        width, height = float(width * ratio), float(height * ratio)

    return width, height


def calculate_image_start_location(width, height):
    return (x_screen - width) // 2, (y_screen - height) // 2


def addImage(pdf, image):
    cover = Image.open(image)
    width, height = cover.size

    width, height = resize_image(width, height)
    x_start, y_start = calculate_image_start_location(width, height)

    temporary_file = cover.resize((int(width), int(height)))
    temporary_file.save('temporary_file_' + image)
    pdf.add_page()
    pdf.image('temporary_file_' + image, x_start, y_start)
    remove('temporary_file_' + image)


def get_files_in_folder():
    return next(walk('.'), (None, None, []))[2]  # [] if no file


def find_all_images(formatedFilePath):
    if ('*' not in formatedFilePath):
        return [formatedFilePath]

    (prefix, sufix) = formatedFilePath.split('*')

    # get all file names from the folder
    fileNames = get_files_in_folder()
    return filter(lambda x: x.startswith(prefix) and x.endswith(sufix), fileNames)


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


class FixedStepProgressIndicator:
    def __init__(self, size, number_of_items):
        self.progress_step = (size + 0.00001) / number_of_items
        self.progress = 0

        print('# Progress ' + '-'* (size - 12) + '#')

    def update_progress(self):
        next_progress = self.progress + self.progress_step
        prev_int = math.floor(self.progress)
        num_sym = math.floor(next_progress) - prev_int
        if num_sym >= 1:
            print("#" * num_sym, sep='', end='')
        self.progress = next_progress


if __name__ == '__main__':
    print("Program starts with arguments: " + str(sys.argv))
    pdf = FPDF(unit='pt', format=(x_screen, y_screen))

    formatedFilePaths = sys.argv[1:-1]

    imageFilePaths = flatten_concatenation([[image for image in find_all_images(formattedFilePath)] for formattedFilePath in formatedFilePaths])

    progress = FixedStepProgressIndicator(100, len(imageFilePaths))

    for image in imageFilePaths:
        addImage(pdf, image)
        progress.update_progress()

    pdf.output(sys.argv[-1], "F")
    print("Program ends")
