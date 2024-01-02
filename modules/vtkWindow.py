import numpy as np
import math
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vtk import (
    vtkRenderer, vtkInteractorStyleTrackballCamera, vtkInteractorStyle,
)
from PySide6.QtCore import (
    Signal
)
from PySide6.QtWidgets import (
    QHBoxLayout, 
)
from common import signalBus, globalVar

# from .smallTools import hex2rgb
#######


class vtkWidget(QVTKRenderWindowInteractor):
    cameraDirection  = Signal(list)
    def __init__(self, parent=None):
        super().__init__()
        # self.parent = parent
        self.layout = QHBoxLayout(parent)        
        self.layout.addWidget(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.Initialize()
        # self.Start()

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(0,0,1)
        self.renderer.SetBackgroundAlpha(1)
        
        self.renderer.SetUseDepthPeeling(1)
        self.renderer.SetMaximumNumberOfPeels(100)
        self.renderer.SetOcclusionRatio(0.1)
        self.renderer.SetBackground([1,1,1])

        self.renWin = self.GetRenderWindow()
        self.renWin.AddRenderer(self.renderer)
        self.renWin.Render()

        self.iren = self.renWin.GetInteractor()
        self.origin_interactor = vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.origin_interactor)
        self.iren.Initialize()
        self.iren.Start()

        self.initCamera()
        self.initSignal()
    
    def closeIt(self):
        pass

    def initSignal(self):
        # signalBus.themeColorChanged.connect(self.changeTheme)
        # signalBus.rotatingStopped.connect(self.stopCameraRotating)
        pass

    def getViewPoint(self, p):
        '''
        p:  world三位坐标点
        return 在屏幕上显示的二位坐标  屏幕左下为原点
        '''
        size = self.renWin.GetSize()
        self.renderer.SetWorldPoint(p[0], p[1], p[2], 1)
        self.renderer.WorldToView()
        p_view = self.renderer.GetViewPoint()
        res = [
                size[0] * (p_view[0]+1)/2,
                size[1] * (p_view[1]+1)/2
            ]
        return res

    ########
    ## Camera
    def setCameraData(self, focus, length):
        '''
        vtkWidget获得图像数据后 设置camera中心和观察的物体的大小 然后计算距离
        '''
        self.camera_focus = np.array(focus)
        self.camera_object_length = length
        view_ang = self.camera.GetViewAngle()
        self.camera_distance = length/0.75 /2 /math.tan(math.radians(view_ang/2))
        self.resetCamera()
    
    def setCameraDataAuto(self, set_direction=False):
        self.renderer.ResetCamera()
        self.camera_focus = self.camera.GetFocalPoint()
        position = self.camera.GetPosition()
        self.camera_distance = np.linalg.norm(np.array(position) - np.array(self.camera_focus))
        
        if set_direction:
            self.resetCamera()

    def initCamera(self):
        '''
        获得imageData之后 初始化相机参数 
        主要计算相机与图像中心的距离
        '''
        # self.rotating_interactor = rotatingInteractor()
        self.camera = self.renderer.GetActiveCamera()
        self.camera.AddObserver('ModifiedEvent', self.cameraMoved)
        self.camera_focus = [0,0,0]
        self.camera_object_length = 2
        ##
        view_ang = 30
        self.camera.SetViewAngle(view_ang)
        ## 默认相机距离
        self.camera_distance = self.camera_object_length/0.75 /2 / math.tan(math.radians(view_ang/2))
        ##
        self.resetCamera()

    def resetCamera(self):
        '''
        重置摄像机视角 默认从y-到y+
        在RAI下为胸前正视图
        '''
        direction = np.array([0,-1,0])
        view_up = [0,0,1]
        self.setCamera(direction, view_up)
        # signalBus.rotatingStopped.emit() ## 同时停止旋转

    def setCamera(self, direction, view_up):
        '''
        direction: 原点指向camera 即视角反方向 单位向量: np
        '''
        direction = np.array(direction)
        self.camera.SetFocalPoint(self.camera_focus)
        self.camera.SetPosition(self.camera_focus + direction * self.camera_distance)
        self.camera.SetViewUp(view_up)
        self.renderer.ResetCameraClippingRange()
        self.renWin.Render()

    def cameraMoved(self, caller, event):
        '''
        相机移动事件
        '''
        focal = self.camera.GetFocalPoint()
        position = self.camera.GetPosition()
        viewup = self.camera.GetViewUp()
        direction = np.array(position) - np.array(focal)
        direction = direction/np.linalg.norm(direction)
        ##
        self.cameraDirection.emit([direction, viewup])
        
    def getCameraInfo(self):
        focal = self.camera.GetFocalPoint()
        position = self.camera.GetPosition()
        viewup = self.camera.GetViewUp()
        # viewang = self.camera.GetViewAngle()
    
    def getCurrentCameraDirection(self):
        focal = self.camera.GetFocalPoint()
        position = self.camera.GetPosition()
        viewup = self.camera.GetViewUp()
        direction = np.array(position) - np.array(focal)
        direction = direction/np.linalg.norm(direction)
        viewup = np.array(viewup)
        return direction, viewup

    def updateRender(self):
        # self.renderer.Render()
        self.renWin.Render()

    def setInteractorStyle(self, interactor):
        '''
        外部设置 interactor
        '''
        self.origin_interactor = interactor
        self.iren.SetInteractorStyle(interactor)
        self.iren.Initialize()
        self.iren.Start()

    #######
    ## Actors
    def addActors(self, actors:list):
        for a in actors:
            self.addActor(a)
        self.updateRender()
    
    def addActor(self, actor):
        if not self.renderer.HasViewProp(actor):
            self.renderer.AddActor(actor)
    
    def removeActor(self, actor):
        if self.renderer.HasViewProp(actor):
            self.renderer.RemoveActor(actor)

    def clearRenderer(self):
        self.renderer.RemoveAllViewProps()





