from __future__ import annotations
from vtk import vtkImageData
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import numpy as np
import copy

def np2vtk(img_arr, spacing, origin, direction, data_type = None,):
    dimension = img_arr.shape[::-1]
    vtk_data = numpy_to_vtk(
        img_arr.flatten(), array_type = data_type)
    vtk_img = vtkImageData()
    vtk_img.SetDimensions(dimension) # xyz
    vtk_img.SetSpacing(spacing)
    vtk_img.SetOrigin(origin)
    vtk_img.SetDirectionMatrix(direction)
    vtk_img.GetPointData().SetScalars(vtk_data)
    # vtk_img.Modified()
    return vtk_img

def vtk2np(vtk_img):
    vtk_data = vtk_img.GetPointData().GetScalars()
    img_arr = vtk_to_numpy(vtk_data)
    dimension = vtk_img.GetDimensions()[::-1]
    img_arr = img_arr.reshape(dimension)
    return img_arr

class myImageData():
    def __init__(self) -> None:
        self.np_arr = None
        self.spacing = None
        self.origin = None
        self.direction = None
        self.size = None
        self.vtkImageData = None
        #
        self.predicted_modal = 'CT'
        self.np_hist = None
        self.np_bins = None
        #
        self.max = None # label要用 提前计算
        self.metadata = {} # 附加信息 dcm专用
        # modal
        self.clips = [-1000, 1000, 300] # clip_min, clip_max, upper_th

    def setReadData(self, read_data):
        self.np_arr = read_data['arr']
        self.spacing = list(read_data['spacing'])
        self.origin = list(read_data['origin'])
        self.direction = list(read_data['direction'])
        self.size = list(read_data['size'])
        self.vtkImageData = np2vtk(self.np_arr, self.spacing, self.origin, self.direction)
        ## guess modal
        self.guessModal()
        ## hist
        hist,bins = np.histogram(self.np_arr.ravel(), bins=500)
        self.np_hist = hist # n
        self.np_bins = bins # n+1        
        ## metadata
        metadata = read_data.get('metadata', {})
        for name,value in metadata.items():
            self.metadata[name] = value

    def setReadLabel(self, read_data):
        self.np_arr = read_data['arr']
        self.np_arr = np.uint8(self.np_arr)
        self.max = np.max(self.np_arr)
        self.spacing = list(read_data['spacing'])
        self.origin = list(read_data['origin'])
        self.direction = list(read_data['direction'])
        self.size = list(read_data['size'])
        self.vtkImageData = np2vtk(self.np_arr, self.spacing, self.origin, self.direction)

    def setNpArr(self, arr, spacing, origin, direction, compute_hist = False):
        self.np_arr = arr
        self.spacing = spacing
        self.origin = origin
        self.direction = direction
        self.max = np.max(arr)
        self.size = list(arr.shape[::-1])
        self.vtkImageData = np2vtk(self.np_arr, self.spacing, self.origin, self.direction)
        ## guess modal
        self.guessModal()
        if compute_hist:
            hist,bins = np.histogram(self.np_arr.ravel(), bins=500)
            self.np_hist = hist # n
            self.np_bins = bins # n+1

    def guessModal(self):
        ## guess modal
        # if np.max(self.np_arr) - np.min(self.np_arr) <= 3: # -1 +1 加采样余量
        #     self.predicted_modal = "Preprocessed"
        #     self.clips = [np.min(self.np_arr), np.max(self.np_arr), 0]
        # elif np.min(self.np_arr)< -100: 
        #     self.predicted_modal = "CT"            
        #     self.clips = [-1000, 1000, 300]
        # else: # 通常MRI的value为时间或者强度 非负
        #     self.predicted_modal = "MRI"     
        #     max_ = np.percentile(self.np_arr, 98)
        #     self.clips = [0, max_, 0] ###
        
        self.predicted_modal = "CT_mimics_label"    
        # max_ = np.percentile(self.np_arr, 99.5)  
        min_ = max(-1000, np.min(self.np_arr))
        max_ = np.max(self.np_arr)     
        self.clips = [min_, max_, 0]

    def updateLabelNpArr(self):
        self.np_arr = vtk2np(self.vtkImageData)
        self.max = np.max(self.np_arr)

    def copy(self):
        image = myImageData()
        image.np_arr = self.np_arr.copy()
        image.spacing = self.spacing.copy()
        image.origin = self.origin.copy()
        image.direction = self.direction.copy()
        if self.size:
            image.size = self.size.copy()
        if self.vtkImageData:
            image.vtkImageData = vtkImageData()
            image.vtkImageData.DeepCopy(self.vtkImageData)
        if self.max:
            image.max = self.max
        if self.predicted_modal is not None:
            image.predicted_modal = self.predicted_modal        
        if self.np_hist is not None:
            image.np_hist = self.np_hist.copy()
            image.np_bins = self.np_bins.copy()     
        ##
        image.clips = copy.deepcopy(self.clips)

        return image
    
    def sameSizeAs(self, img:myImageData):
        if self.size == img.size:
            return True
        else:
            return False




Zero_image = myImageData()
Zero_image.setNpArr(np.zeros((10,10,10)), [1,1,1], [0,0,0], [1,0,0,0,1,0,0,0,1])












