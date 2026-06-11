import cv2
import pytesseract
import numpy as np
import time

import os


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"D:\OCR\tesseract.exe"
    )


def extract_board(uploaded_file):

    start_time = time.time()

    uploaded_file.seek(0)

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    img = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if img is None:
        raise Exception(
            "Image failed to load."
        )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    height, width = gray.shape

    cell_h = height // 9
    cell_w = width // 9

    board = []

    ocr_calls = 0

    for i in range(9):

        row = []

        for j in range(9):

            cell = gray[
                i * cell_h:(i + 1) * cell_h,
                j * cell_w:(j + 1) * cell_w
            ]

            margin = 5

            cell = cell[
                margin:-margin,
                margin:-margin
            ]

            if np.mean(cell) > 240:

                row.append(0)
                continue

            cell = cv2.resize(
                cell,
                None,
                fx=2,
                fy=2
            )

            _, cell = cv2.threshold(
                cell,
                150,
                255,
                cv2.THRESH_BINARY
            )

            ocr_calls += 1

            text = pytesseract.image_to_string(
                cell,
                config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789"
            )

            text = text.strip()

            if text.isdigit():

                digit = int(text)

                if 1 <= digit <= 9:
                    row.append(digit)
                else:
                    row.append(0)

            else:

                row.append(0)

        board.append(row)

    print("\n========== OCR DEBUG ==========")
    print("OCR Calls:", ocr_calls)
    print("OCR Time:", time.time() - start_time)
    print("Detected Board:")
    print(board)
    print("================================\n")

    return board