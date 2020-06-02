import requests
from cairosvg import svg2png

SVG_IMAGES_URL_FORMAT = "https://colonist.io/dist/images/{}.svg?v82.1"


def svg_url_to_png(url, outfile):
    """
    Writes svg file from url to png.
    :param url: svg url.
    :param outfile:png outfile.
    """
    svg2png(bytestring=requests.get(url).content, write_to=outfile)
