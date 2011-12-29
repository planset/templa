# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""

import os
from PIL import Image
from cStringIO import StringIO


class ThumbnailSize(object):
    small = "small"
    medium = "medium"
    big = "big"
    
#
THUMBNAIL_SIZE_DICT = {ThumbnailSize.small:(80, 80),
                       ThumbnailSize.medium:(210, 150), 
                       ThumbnailSize.big:(560, 315)}

#
THUMBNAIL_FILE_NAME = "{filename}_{sizename}.{extension}"
THUMBNAIL_QUALITY = 'ANTIALIAS'

    
class Thumbnail(object):
    """
    
    """
    image = None

    def __init__(self, root_path, thumbnail_dirname, 
                 static_dirname = "static",
                 sizes=THUMBNAIL_SIZE_DICT,
                 data=None,
                 filepath=None,
                 format="jpg",
                 quality=THUMBNAIL_QUALITY):
        self.root_path = root_path
        self.thumbnail_dirname = thumbnail_dirname
        self.static_dirname = static_dirname
        self.thumbnail_dirpath = os.path.join(root_path, static_dirname, thumbnail_dirname)
        self.sizes = sizes
        if data:
            self.from_data(data)
        elif filepath:
            self.froom_file(filepath)
        self.format = format
        self.extension = self.__get_extension(format)
        self.quality = quality
    
    def __get_extension(self, format):
        if format.upper() == "JPG":
            return "jpg"
        else:
            raise Exception()
        
    def from_file(self, filepath):
        self.image = Image.open(filepath)

    def from_data(self, data):
        self.image = Image.open(StringIO(data))
    
    def get_thumbnail_name(self, filename, sizename):
        return os.path.join(
                    self.thumbnail_dirname, 
                    self.__getsavename(filename, sizename))
        
    def get_thumbnail_path(self, filename, sizename):
        return self.__getsavepath(filename, sizename)

    def __getsavename(self, filename, sizename):
        return THUMBNAIL_FILE_NAME.format(
                filename=filename,
                sizename=sizename,
                extension=self.extension)
        
    def __getsavepath(self, filename, sizename):
        return os.path.join(
            self.thumbnail_dirpath,
            self.__getsavename(filename, sizename)
            )

    def save(self, filename, sizename, width, height):
        if self.image is None:
            raise Exception()
            
        if width > height:
            w = width
            h = self.image.size[1] * width / self.image.size[0]
        else:
            w = self.image.size[0] * height / self.image.size[1]
            h = height
        
        t = self.image.resize((w, h), getattr(Image, self.quality))
        t = t.crop((0, 0, width, height))
        t.save(self.__getsavepath(filename, sizename))
   
    def saveall(self, filename):
        for sizename, size in self.sizes.items():
            self.save(filename, sizename, size[0], size[1])

