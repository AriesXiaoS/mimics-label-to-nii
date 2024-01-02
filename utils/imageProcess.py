import SimpleITK as sitk
import numpy as np


from common import User_cfg

def normalizeArr255(arr):
    arr = arr.astype(np.float32)
    arr = np.clip(arr, -1000, None)
    max_ = np.percentile(arr, 99.5)
    min_ = np.percentile(arr, 0.5)
    arr = (arr - min_) / (max_ - min_)
    arr = np.clip(arr, 0, 1)
    arr = (arr * 255).astype(np.uint8)
    return arr



def hexToRgb(hex_color:str):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def getLabelColor(index):
    '''
    label color
    return [r,g,b]
    '''
    label_color_map = User_cfg.get('label_color_map')
    j = (index-1) % len(label_color_map)
    return label_color_map[j]





