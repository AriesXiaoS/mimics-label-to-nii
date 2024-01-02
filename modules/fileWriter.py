from __future__ import annotations
from SimpleITK import GetImageFromArray, WriteImage
from common import myImageData

class sitkWriter():
    def __init__(self, path: str = '', type = 'nii') -> None:
        self.path = path
        self.type = type
    
    def setFilePath(self, path):
        self.path = path

    def writeNii(self, image: myImageData):
        out = GetImageFromArray(image.np_arr)
        out.SetSpacing(image.spacing)
        out.SetOrigin(image.origin)
        out.SetDirection(image.direction)
        WriteImage(out, self.path)

    def writeDcm(self, image: myImageData):
        pass

    def write(self, image:myImageData):
        if self.type == 'nii':
            self.writeNii(image)
        elif self.type == 'dcm':
            self.writeDcm(image)


class ImageWriter():
    def __init__(self):

        self.file_path = ''
        self.writer_type = 'sitk'
        self.file_type = 'nii'
        self.support_reader_type = ['sitk',]
        self.support_file_type = ['nii', 'dcm']

    def setFilePath(self, path):
        self.file_path = path
    
    def setFileType(self, file_type):
        assert file_type in self.support_file_type
        self.file_type = file_type

    def setWriterType(self, writer_type):
        assert writer_type in self.support_reader_type
        self.writer_type = writer_type
    
    def write(self, image:myImageData):
        if self.writer_type == 'sitk':
            writer = sitkWriter(self.file_path, self.file_type)
            writer.write(image)
        else:
            raise NotImplementedError




    





