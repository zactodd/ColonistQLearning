import cv2
import pytesseract
import matplotlib.pyplot as plt
from itertools import product
from colonist_ql.game_structure.structures import *
import colonist_ql.facts as facts
import colonist_ql.utils as utils
from skimage import measure
import os
from collections import defaultdict


RESOURCE_COLOUR_RANGES = {
    facts.RESOURCES.LUMBER: (np.asarray((70, 195, 100)), np.asarray((10, 20, 15))),
    facts.RESOURCES.BRICK: (np.asarray((106, 130, 240)), np.asarray((30, 44, 200))),
    facts.RESOURCES.WOOL: (np.asarray((30, 183, 158)), np.asarray((0, 142, 100))),
    facts.RESOURCES.GRAIN: (np.asarray((60, 220, 255)), np.asarray((5, 150, 180))),
    facts.RESOURCES.ORE: (np.asarray((178, 182, 176)), np.asarray((131, 133, 129))),
    facts.TILES.DESERT: (np.asarray((230, 230, 220)), np.asarray((115, 140, 180)))
}

SEA_COLOUR_RANGE = (np.asarray((170, 110, 20)), np.asarray((160, 90, 0)))


def find_contours(grey_image):
    """
    Finds all the contours from a grey scale image.
    :param grey_image: A grey scale image.
    :return: a list of contours
    """
    _, thresh = cv2.threshold(grey_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def contour_centre(contour):
    """
    Calculates the centre of the contour.
    :param contour: The contour in which to obtain the centre.
    :return: x axis centre, y axis centre.
    """
    m = cv2.moments(contour)
    return m["m10"] / m["m00"], m["m01"] / m["m00"]


def filter_contours_by_area(contours, upper=20000, lower=5000):
    """
    Filters a list of contours by area.
    :param contours: A list of contours.
    :param upper: The upper area bound.
    :param lower: The lower area bound.
    :return: The filtered list of contours.
    """
    return [c for c in contours if upper >= cv2.contourArea(c) >= lower]


def filter_contours_by_distance(contours, point, upper=500, lower=300):
    """
    Filters a list of contours by distance from point.
    :param contours: A list of contours.
    :param point: The point at which the contours distance is calculated.
    :param upper: The upper distance bound.
    :param lower: The lower distance bound.
    :return: The filtered list of contours.
    """
    return [c for c in contours if upper >= utils.distance(contour_centre(c), point) >= lower]


def draw_contours(image, contours):
    """
    Draws contours on the image.
    :param image: The image to draw on top of.
    :param contours: THe list of contours to draw.
    """
    plot_image = image.copy()
    xs, ys = [], []
    for i, c in enumerate(contours):
        x, y = contour_centre(c)
        xs.append(x)
        ys.append(y)
        plot_image = cv2.drawContours(plot_image, contours, i, (0, 255, 0), 3)

    plot_image = cv2.cvtColor(plot_image, cv2.COLOR_BGR2RGB)
    plt.imshow(plot_image)

    # Contour centres.
    plt.scatter(xs, ys)
    h, w, *_ = image.shape

    # Centre contour.
    plt.scatter(np.mean(xs), np.mean(ys), c="r")
    plt.show()


def dilation_consensus_text_extraction(image, tesseract_config, synonyms={}, ignores=[]):
    """
    Extras text from the image using a variety of dilations.
    :param image: The image of the  text.
    :param tesseract_config: The config string for tesseract.
    :param synonyms: A dictionary for converting a guess to another result.
    :param ignores: A list of results to ignore.
    :return: The guess for the image.
    """

    # Creates the dimensions for the dilations of the image.
    h_size, v_size = range(2, 5), range(2, 5)

    images = [image]
    images.extend(cv2.dilate(image, np.ones((h, v)), iterations=1) for h, v in product(h_size, v_size))
    return consensus_text_extraction(images, tesseract_config, synonyms, ignores)


def erosion_consensus_text_extraction(image, tesseract_config, synonyms={}, ignores=[]):
    """
    Extras text from the image using a variety of eriosions.
    :param image: The image of the  text.
    :param tesseract_config: The config string for tesseract.
    :param synonyms: A dictionary for converting a guess to another result.
    :param ignores: A list of results to ignore.
    :return: The guess for the image.
    """

    # Creates the dimensions for the dilations of the image.
    h_size, v_size = range(0, 3), range(0, 3)

    images = [image]
    images.extend(cv2.erode(image, np.ones((h, v)), iterations=1) for h, v in product(h_size, v_size))
    return consensus_text_extraction(images, tesseract_config, synonyms, ignores)


def consensus_text_extraction(images, tesseract_config, synonyms={}, ignores=[]):
    """
    Extras the consensus text from a list of imges.
    :param images: The list of images.
    :param tesseract_config: The config string for tesseract.
    :param synonyms: A dictionary for converting a guess to another result.
    :param ignores: A list of results to ignore.
    :return: The guess for the image.
    """
    guesses = {}
    threshold = len(images)
    for i in images:
        text = pytesseract.image_to_string(i, config=tesseract_config)
        if text in synonyms:
            text = synonyms[text]
        if text in ignores:
            continue
        guesses[text] = guess_count = 1 + guesses[text] if text in guesses else 1
        if guess_count > threshold:
            break
    return max(guesses.keys(), key=lambda g: guesses[g])


def hex_value(image):
    """
    Get the dice value of a hex.
    :param image: The game image.
    :return: An int of the hex value or None if a invalid value is found.
    """
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
    value_contour = filter_contours_by_area(find_contours(thresh), 3000, 1000)
    if len(value_contour) == 1:
        x, y, w, h = cv2.boundingRect(value_contour[0])
        bb = image[y:y + h, x + 6:x + w - 6]
        text = dilation_consensus_text_extraction(
            bb,
            "--psm 13 --oem 3 -c tessedit_char_whitelist=012345689",
            {"1": "11"}
        )
        return int(text) if text != "" else None
    else:
        return None


def match_images(image, candidate_directory, threshold=None):
    """
    Determines which image is the best match from a collection of images.
    :param image:
    :param candidate_directory: The directory which stores the candidate images
    :return: The name of the candidate that best matches image.
    """
    h, w, *_ = image.shape
    results = {}
    for t in next(os.walk(candidate_directory))[2]:
        test_image = cv2.imread(f"{candidate_directory}/{t}")
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGRA2BGR)
        test_image = cv2.resize(test_image, (w, h), interpolation=cv2.INTER_AREA)
        results[t] = measure.compare_ssim(image, test_image, multichannel=True)
    if threshold is not None and all(threshold > v for v in results.values()):
        return None
    else:
        return max(results, key=lambda x: results[x])


def extract_port(image):
    """
    Extracts the port type from the image if the image contains a port.
    :param image:
    :return: string that matches the port type if there is a port otherwise None.
    """
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
    port_contour = filter_contours_by_area(find_contours(thresh), 1500, 700)
    if len(port_contour) == 1:
        x, y, w, h = cv2.boundingRect(port_contour[0])
        ratio = image[y + 20:y + h - 5, x + 6:x + w - 6]
        text = erosion_consensus_text_extraction(
            ratio,
            "--psm 13 --oem 3 -c tessedit_char_whitelist=123:",
            {"2": "2:1", "2:": "2:1", "21": "2:1", "3": "3:1", "3:": "3:1", "31": "3:1"},
            ["", "1"]
        )
        if text == "2:1":
            icon = image[y + 5:y + h - 20, x + 6:x + w - 6]
            port_type = match_images(icon, facts.PORT_IMAGE_DIR)[:-4]
            text = f"{text}\n{port_type}"
        return text
    else:
        return None


def extract_land_information(image):
    """
    Extracts the resource triple from the image.
    :param image: The game image.
    :return: A set of Hex(). e.g. {..., Hex(...), ...}.
    """
    contours_dict = {
        k: filter_contours_by_area(find_contours(cv2.inRange(image, lower, upper)))
        for k, (upper, lower) in RESOURCE_COLOUR_RANGES.items()
    }

    classes = {
        contour_centre(c): (k, hex_value(utils.contour_bounding_box(image, c)) if k in facts.RESOURCES else None)
        for k, contour in contours_dict.items() for c in contour
    }

    x, y = list(zip(*classes.keys()))
    cx, cy = np.mean(x), np.mean(y)
    size = max([utils.distance((cx, cy), p) for p in classes.keys()]) / 3
    return {Hex(cc.pixel_to_cube((x - cx, y - cy), size), (x, y), r, v) for (x, y), (r, v) in classes.items()}


def extracts_sea_information(image, board_centre):
    """
    Extracts the sea information include hex and ports from the image.
    :param image: The game image.
    :return: A set of Hex objects and a set of port objects
        e.g. {..., Hex(...), ...}, {..., Port(...), ...}
    """
    upper, lower = SEA_COLOUR_RANGE
    mask = cv2.inRange(image, lower, upper)

    contours = find_contours(mask)
    contours = filter_contours_by_area(contours)
    contours = filter_contours_by_distance(contours, board_centre)

    ports = []
    points = []
    for c in contours:
        points.append(contour_centre(c))
        ports.append(extract_port(utils.contour_bounding_box(image, c)))

    x, y = list(zip(*points))
    cx, cy = np.mean(x), np.mean(y)
    size = max([utils.distance((cx, cy), p) for p in points]) / 5

    hexes = set()
    for (x, y), p in zip(points, ports):
        ap = x - cx, y - cy
        c = cc.pixel_to_cube(ap, size)
        if p is not None:
            Port(c, facts.PORT_PLACEMENT[c], p)
        hexes.add(Hex(c, (x, y), facts.TILES.SEA, p))
    return hexes


def initial_board_extraction(image):
    """
    Extracts the initial information for the board.
    :param image: The game image.
    :return:
    """
    inner = extract_land_information(image)
    board_centre = next(h.real_coords for h in inner if h.cube_coords == (0, 0, 0))
    outer = extracts_sea_information(image, board_centre)
    return inner | outer


def extract_roads(image, road_positions, padding=7):
    """
    Extracts the positions of the roads given a set of possible positions.
    :param image: The game image.
    :param road_positions: A set of bounding boxes representing possible new road locations.
    :param padding: THe padding to add to ede of the positions.
    :return: The position of the roads if they are in the :param road_positions.
    """
    for (x0, x1), (y0, y1) in road_positions:
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        bb = image[y0 - padding:y1 + padding, x0 - padding:x1 + padding, ...]
        plt.imshow(bb)
        plt.show()
        # TODO set up image matching
        # match = match_images(bb, )


def extract_settlements(image, triples):
    """
    Extracts the positions of the settlements given a set of possible positions.
    :param image: The game image.
    :param triples: A set of triples representing the possible settlement positions.
    :return: The position of the roads if they are in the :param open_settlement_positions.
    """
    triples_colour = defaultdict(set)
    for t in triples:
        x, y = real_triple_location(t)
        x, y = int(x), int(y)
        bb = image[y - 40:y + 30, x - 30:x + 30, ...]

        match = match_images(bb, facts.SETTLEMENT_IMAGES_DIR, 0.10)
        if match is not None:
            colour = match.split("_")[1][:-4]
            triples_colour[colour].add(t)
    return triples_colour


def extract_cities(image, settlements_position):
    """
    Extracts the positions of the cities given a set of possible positions.
    :param image: The game image.
    :param settlements_position: A set of bounding boxes representing possible city locations.
    :return: The position of the roads if they are in the :param settlements_position.
    """
    pass


