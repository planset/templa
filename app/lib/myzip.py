# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import zipfile
import zlib
import json

class TemplateFileInfo(object):
    __index_filename= ""
    filelist = None
    INDEX_LIST = ["INDEX.HTML", "INDEX.HTM"]
    
    def __init__(self, filelist=[]):
        self.filelist = self.__sort_tree(filelist)
        self.__index_filename = self.__search_index(self.filelist)

    @property
    def index_filename(self):
        return self.__index_filename
    @property
    def json_filelist(self):
        return json.dumps(self.filelist)
    @property
    def compressed_filelist(self):
        return zlib.compress(self.json_filelist)
        
    def set_compressed_filelist(self, compressed_filelist):
        self.filelist = json.loads(zlib.decompress(compressed_filelist))
        
    def __search_index(self, filelist):
        for filepath in filelist:
            filename=os.path.basename(filepath).upper()
            if filename in self.INDEX_LIST:
                return filepath
        return ""
        
    def __sort_tree(self, filelist):
        result = {}
        for filepath in filelist:
            hierarchy = len(filepath.split("/")) 
            if hierarchy in result:
                result[hierarchy].append(filepath)
            else:
                result[hierarchy] = [filepath]
        result_list = []
        for key in range(len(result)):
            if not key+1 in result:
                continue
            for value in result[key+1]:
                result_list.append(value)
        return result_list
    
def get_fileinfo(filepath, compress_type="zip"):
    if compress_type=="zip":
        return get_zip_fileinfo(filepath)
    else:
        return None

def get_zip_fileinfo(filepath):
    zf = zipfile.ZipFile(filepath)
    filelist = zf.namelist()
    return TemplateFileInfo(filelist)
    
if __name__ == "__main__":
    tfi = get_fileinfo(os.path.dirname(os.path.abspath(__file__))+"/../../tests/data/html5-v2.zip")
    print tfi.filelist
    print tfi.json_filelist
    print tfi.compressed_filelist


