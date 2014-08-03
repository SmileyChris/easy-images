from easy_images import processor_utils


class Processor(object):
    filters = [
        'colorspace',
        'autocrop',
        'scale',
        'crop',
        'filters',
    ]

    def __init__(self, source):
        self.source = source

    def __call__(self, image_settings):
        """
        Run the source through all filters.
        """
        img = self.source
        for attr in self.filters:
            new_img = getattr(self, attr)(img, **image_settings)
            if new_img:
                img = new_img
        return img

    def colorspace(self, img, bw, replace_alpha, **kwargs):
        is_transparent = img.is_transparent()
        if is_transparent and replace_alpha:
            img = img.replace_alpha(color=replace_alpha)
            is_transparent = False

        if bw:
            func = img.mode_grayscale
        else:
            func = img.mode_rgb

        return func(transparent=is_transparent)

    def autocrop(self, img, autocrop=False, **kwargs):
        """
        Remove any unnecessary whitespace from the edges of the source image.

        This processor should be listed before :func:`scale_and_crop` so the
        whitespace is removed from the source image before it is resized.

        autocrop
            Activates the autocrop method for this image.
        """
        if autocrop:
            return img.whitespace_trim()

    def scale(self, img, size=None, crop=False, upscale=False, **kwargs):
        if not size:
            return

        source_x, source_y = [float(v) for v in img.size()]
        target_x, target_y = [float(v) for v in size]

        if crop or not target_x or not target_y:
            func = max
        else:
            func = min
        scale = func(target_x / source_x, target_y / source_y)

        # Handle one-dimensional targets.
        if not target_x:
            target_x = source_x * scale
        elif not target_y:
            target_y = source_y * scale

        if scale < 1.0 or (scale > 1.0 and upscale):
            # Resize the image to the target size boundary. Round the scaled
            # boundary sizes to avoid floating point errors.
            boundary_size = (
                int(round(source_x * scale)),
                int(round(source_y * scale)),
            )
            return img.resize(boundary_size)

    def crop(self, img, size=None, crop=False, crop_focus=None, **kwargs):
        if not size or not crop or crop == 'scale':
            return

        if crop == 'smart':
            box = filter_utils.smart_crop(img)
        else:
            if not crop_focus:
                crop_focus = filter_utils.edge_focus(img, crop)
            box = filter_utils.bound_box(size, img.size(), crop_focus)

        return img.crop(box)

    def filters(self, img, sharpen=False, **kwargs):
        """
        Pass the source image through post-processing filters.

        sharpen
            Sharpen the thumbnail image. Pass ``1`` (or ``True``) for a mild
            sharpen, ``2`` for a sharp image, or larger numbers for an even
            more intense sharpen still.
        """
        if not sharpen:
            return
        try:
            sharpen = int(sharpen)
        except (ValueError, TypeError):
            sharpen = 1
        return img.sharpen(sharpen)


