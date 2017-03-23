from PIL import Image


def read_image(path):
    im = Image.open(path)
    pixels = list(im.getdata())
    return [x / 255 for x in pixels]
    result = []
    p = iter(pixels)
    width, height = im.size
    for h in range(height):
        result.append([])
        for w in range(width):
            result[h].append(p.__next__())
    return [x / 255 for x in result]
