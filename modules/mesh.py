from __future__ import annotations
import os, traceback

import vtk
import numpy as np
from PySide6.QtCore import QThread, Signal

from common import myImageData, cfg, signalBus, np2vtk
from utils.imageProcess import getLabelColor

def simpleMC(vtk_image_data):
    mc = vtk.vtkMarchingCubes()
    mc.ComputeNormalsOn()
    mc.ComputeGradientsOn()
    mc.SetInputData(vtk_image_data)
    mc.SetValue(0, 0.5)  
    mc.Update()
    res = mc.GetOutput()
    return res


class LabelToMesh(QThread):
    Finished = Signal(dict)
    Info = Signal(str)

    def __init__(self):
        super().__init__()
        self.target_indexs = []

    def setLabel(self, label: myImageData):
        self.label = label

    def setTargets(self, target_indexs:list):
        self.target_indexs = target_indexs

    def run(self):
        try:
            self.label.updateLabelNpArr()
            label_arr = self.label.np_arr
            spacing = self.label.spacing
            origin = self.label.origin
            direction = self.label.direction

            res = dict()

            indexs = range(1, int(np.max(label_arr))+1)
            if len(self.target_indexs) > 0:
                indexs = self.target_indexs

            for i in indexs:
                arr = np.zeros_like(label_arr, dtype=np.uint8)
                arr[label_arr == i] = 1
                vtk_img = np2vtk(arr, spacing, origin, direction)
                polydata = simpleMC(vtk_img)
                self.Info.emit(f'{i+1}/{len(indexs)}')
                res[i] = {
                    'polydata': polydata,
                    'color': getLabelColor(i)
                }

            self.Finished.emit(res)

        except Exception as e:
            tb = traceback.format_exc()  # 获取详细的异常信息
            print(tb)
            signalBus.alertInfo.emit({
                'title': 'mesh生成失败',
                'content': tb,
                'duration':-1,
                'type': 'error'
            })
            self.Finished.emit({})






