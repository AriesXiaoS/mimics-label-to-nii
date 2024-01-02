from __future__ import annotations
import os, traceback

import numpy as np
from SimpleITK import ReadImage,ImageSeriesReader,GetArrayFromImage
from PySide6.QtCore import QThread, Signal

from common import myImageData, cfg, signalBus, User_cfg

class sitkReader():
    def __init__(self, path: str, type = 'nii') -> None:
        self.path = path
        self.type = type
        assert type in ['nii', 'dcm']

    def readNii(self):
        image = ReadImage(self.path)
        return image

    def readDcm(self):
        series_IDs = ImageSeriesReader.GetGDCMSeriesIDs(self.path)
        series_file_names = [ImageSeriesReader.GetGDCMSeriesFileNames(self.path, seriesID) for seriesID in series_IDs]
        series_file_names_lengths = [len(series_file_name) for series_file_name in series_file_names]
        max_index = np.argmax(series_file_names_lengths)
        target_file_names = series_file_names[max_index]

        reader = ImageSeriesReader()
        reader.SetFileNames(target_file_names)
        reader.LoadPrivateTagsOn()
        reader.MetaDataDictionaryArrayUpdateOn()
        image = reader.Execute()

        # 读取 metadata
        # _image = ReadImage(target_file_names[0])
        # metadata_keys = _image.GetMetaDataKeys()
        # additonal_tags = {}
        # for key,name in DICOM_TAGS.items():
        #     if key in metadata_keys:
        #         value = _image.GetMetaData(key)
        #         additonal_tags[name] = value
        
        return image, {}
    
    def read(self):
        additonal_tags = {}
        if self.type=='nii':
            image = self.readNii()
        elif self.type=='dcm':
            image, additonal_tags = self.readDcm()

        # ignore_direction = cfg.ignoreDirection.value
        ignore_direction = False
        if ignore_direction:
            direction = [1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0]
        else:
            direction = image.GetDirection()
        
        res = {
            'arr': GetArrayFromImage(image),
            'spacing': image.GetSpacing(),
            'origin': image.GetOrigin(),
            'direction': direction,
            'size': image.GetSize()
        }
        res['metadata'] = additonal_tags
        return res



class ImageReader(QThread):
    readFinished = Signal(dict)
    def __init__(self):
        super().__init__()
        self.index = 0
        self.dicom_path = ''
        self.file_type = 'dcm'

    def setReadInfo(self, index, dicom_path, nii_path):
        self.index = index
        self.dicom_path = dicom_path
        self.nii_path = nii_path

    def run(self):
        try:
            if not os.path.exists(self.dicom_path):
                raise ValueError(f'{self.dicom_path} file not found')
            # signalBus.stateTooltip.emit({
            #     'title': '读取文件',
            #     'content': self.dicom_path,
            #     'show': True
            # })
            reader = sitkReader(self.dicom_path, 'dcm')        
            read_data = reader.read()
            image = myImageData()
            image.setReadData(read_data)

            if os.path.exists(self.nii_path):
                label_reader = sitkReader(self.nii_path, 'nii')
                label_read_data = label_reader.read()                
            else:
                label_read_data = {
                    'arr': np.zeros_like(read_data['arr'], dtype=np.uint8),
                    'spacing': read_data['spacing'],
                    'origin':   read_data['origin'],
                    'direction': read_data['direction'],
                    'size':   read_data['size']
                }
            label = myImageData()
            label.setReadLabel(label_read_data)
            Label_names = User_cfg.get('Label_names', None)
            if Label_names is not None:
                keys = list(Label_names.keys())
                label.max = np.max(keys)
            else:
                label.max = 9

            res = {
                'index': self.index,
                'image': image,
                'label': label
            }
            self.readFinished.emit(res)

        except Exception as e:
            tb = traceback.format_exc()  # 获取详细的异常信息
            print(tb)
            signalBus.alertInfo.emit({
                'title': '读取文件失败',
                'content': tb,
                'duration':-1,
                'type': 'error'
            })
            self.readFinished.emit({
                'index': self.index,
            })




