import math

from PIL import Image, ImageFilter, ImageChops
try:
    from cStringIO import cStringIO as BytesIO
except ImportError:
    from six import BytesIO

from easy_images.sources import base


class PILSource(base.BaseSource):

    @staticmethod
    def read(file_obj):
        # Use a BytesIO wrapper because if the source is an incomplete file
        # like object, PIL may have problems with it. For example, some image
        # types require tell and seek methods that are not present on all
        # storage File objects.
        source = BytesIO(file_obj.read())
        try:
            image = Image.open(source)
            # Fully load the image now to catch any problems with the image
            # contents.
            image.load()
        except Exception:
            return
        return image

    @base.action
    def mode_grayscale(self, transparent, **kwargs):
        if transparent:
            return self.img.convert('LA')
        return self.img.convert('L')

    @base.action
    def mode_rgb(self, transparent, **kwargs):
        if transparent:
            return self.img.convert('RGBA')
        return self.img.convert('RGB')

    @base.action
    def replace_alpha(self, color, **kwargs):
        img = self.mode_rgb(self.img, transparent=True)
        base = Image.new('RGBA', img.size, color)
        base.paste(img, mask=img)
        return img

    @base.action
    def whitespace_trim(self, **kwargs):
        bw = self.img.convert('1')
        bw = bw.filter(ImageFilter.MedianFilter)
        # White background.
        bg = Image.new('1', self.img.size, 255)
        diff = ImageChops.difference(bw, bg)
        bbox = diff.getbbox()
        if bbox:
            return self.img.crop(bbox)
        return self.img

    @base.action
    def resize(self, size, **kwargs):
        return self.img.resize(size, resample=Image.ANTIALIAS)

    @base.action
    def crop(self, box, **kwargs):
        return self.img.crop(box)

    @base.action
    def sharpen(self, strength, **kwargs):
        if strength <= 1:
            return self.img.filter(ImageFilter.DETAIL)
        img = self.img
        for i in range(strength-1):
            img = img.filter(ImageFilter.SHARPEN)
        return img

    def size(self):
        return self.img.size

    def is_transparent(self):
        return (
            self.img.mode in ('RGBA', 'LA') or
            (self.img.mode == 'P' and 'transparency' in self.img.info)
        )

    def is_grayscale(self):
        return self.img.mode in ('L', 'LA')

    def is_rgb(self):
        return self.img.mode in ('L', 'LA', 'RGB', 'RGBA')

    def entropy(self):
        hist = self.img.histogram()
        hist_size = float(sum(hist))
        hist = [h / hist_size for h in hist]
        return -sum([p * math.log(p, 2) for p in hist if p != 0])


# class PILAnimatedSource(PILSource):

#     @staticmethod
#     def read(file_obj):
#         pass
