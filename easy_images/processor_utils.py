import re

import six


def _compare_entropy(img, start_slice, end_slice, slice, difference):
    """
    Calculate the entropy of two slices (from the start and end of an axis),
    returning a tuple containing the amount that should be added to the start
    and removed from the end of the axis.

    """
    start_entropy = img.entropy(start_slice)
    end_entropy = img.entropy(end_slice)
    if end_entropy and abs(start_entropy / end_entropy - 1) < 0.01:
        # Less than 1% difference, remove from both sides.
        if difference >= slice * 2:
            return slice, slice
        half_slice = slice // 2
        return half_slice, slice - half_slice
    if start_entropy > end_entropy:
        return 0, slice
    else:
        return slice, 0


def smart_crop(img, size):
    """
    Trim slices off the sides of the image with the least entropy until cropped
    down to the dimensions.
    """
    source_x, source_y = img.size()
    target_x, target_y = [float(v) for v in size]

    # Difference between new image size and requested size.
    diff_x = int(source_x - min(source_x, target_x))
    diff_y = int(source_y - min(source_y, target_y))

    left = top = 0
    right, bottom = source_x, source_y
    while diff_x:
        slice = min(diff_x, max(diff_x // 5, 10))
        start = img.crop((left, 0, left + slice, source_y))
        end = img.crop((right - slice, 0, right, source_y))
        add, remove = _compare_entropy(img, start, end, slice, diff_x)
        left += add
        right -= remove
        diff_x = diff_x - add - remove
    while diff_y:
        slice = min(diff_y, max(diff_y // 5, 10))
        start = img.crop((0, top, source_x, top + slice))
        end = img.crop((0, bottom - slice, source_x, bottom))
        add, remove = _compare_entropy(img, start, end, slice, diff_y)
        top += add
        bottom -= remove
        diff_y = diff_y - add - remove
    return (left, top, right, bottom)


def bound_box(source_size, target_size, focus=None):
    """
    Calculate the box location to crop a source image down to a target size.

    The box location can target a certain focus point (if no focus point is
    given, centre the box).

    Centre the box if no focus point is given::

        >>> bound_box((100, 200), (10, 10))
        (45, 95, 55, 105)

    Otherwise, centre around the focus point::

        >>> bound_box((100, 100), (20, 10), focus=(40, 40))
        (30, 35, 50, 45)

    Don't let the box go outside the source dimensions::

        >>> bound_box((100, 100), (20, 10), focus=(4, 4))
        (0, 0, 20, 10)
        >>> bound_box((100, 100), (20, 10), focus=(92, 99))
        (80, 90, 100, 100)

    The box is constrained to the source dimensions::

        >>> bound_box((10, 10), (11, 9))
        (0, 0, 10, 9)
        >>> bound_box((10, 10), (9, 11))
        (0, 0, 9, 10)
    """
    source_x, source_y = source_size
    target_x, target_y = target_size

    if focus:
        focus_x, focus_y = focus
    else:
        focus_x, focus_y = source_x // 2, source_y // 2

    if target_x >= source_x:
        x, x2 = 0, source_x
    else:
        x = max(0, min(source_x, focus_x + (target_x // 2)) - target_x)
        x2 = x + target_x

    if target_y >= source_y:
        y, y2 = 0, source_y
    else:
        y = max(0, min(source_y, focus_y + (target_y // 2)) - target_y)
        y2 = y + target_y

    return x, y, x2, y2


def edge_focus(img, focus_text):
    """
    Set the focus point when given a percentage string.

    The percentage string is the format ``'40,40'``. For example::

        >>> class Img(object):
        ...     def size(self):
        ...         return 500, 500

        >>> edge_focus(Img(), '40,40')
        (200, 200)
        >>> edge_focus(Img(), '10,90')
        (50, 450)
    """
    if not isinstance(focus_text, six.string_types):
        return

    focus_match = re.match(r'(\d+)?, ?(\d+)?$', focus_text)
    if not focus_match:
        return

    source_x, source_y = img.size()
    x_crop, y_crop = focus_match.groups()
    x_crop = int(x_crop) if x_crop else 50
    y_crop = int(y_crop) if y_crop else 50

    return int(source_x * x_crop / 100.0), int(source_y * y_crop / 100.0)


if __name__ == '__main__':
    import doctest
    failure_count, test_count = doctest.testmod()
    if not failure_count:
        print('{} tests passed'.format(test_count))
