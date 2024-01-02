from __future__ import annotations

import os,sys
from typing import Optional
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

import math
import numpy as np
import vtk
from vtk import(
    vtkImageSliceMapper, vtkImageSlice, vtkImageData, vtkLineSource,
    vtkInteractorStyleTrackballCamera, vtkPropPicker,
    vtkLookupTable,  vtkInteractorStyle, vtkInteractorStyleTrackballCamera,
    vtkPoints, vtkCellArray, vtkLine, vtkPolyData, vtkPolyDataMapper, vtkActor,
)


from modules.vtkWindow import vtkWidget
from common import myImageData, Zero_image, signalBus, globalVar, NAMES
from utils.imageProcess import *
from utils.vtkAssembly import *
from utils.imageProcess import getLabelColor

class SliceViewInteractor(vtk.vtkInteractorStyleTrackballCamera):
    '''
    单个slice 窗口的交互器
    '''
    def __init__(self, slice_view: SliceView) -> None:
        super().__init__()
        self.slice_view = slice_view
        self.RemoveAllObservers()
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)
        self.AddObserver("MouseWheelForwardEvent", self.mouseWheelForwardEvent)
        self.AddObserver("MouseWheelBackwardEvent", self.mouseWheelBackwardEvent)
        ##
        self.mode = 'cursor'
        ##
        self.pick_actor = None
        self.cursor_picking = False ## 鼠标左键点击按住 可以移动cursor
        self.pen_active = False
        self.drawing = False ## 鼠标左键绘制
        self.erasing = False ## 鼠标右键擦除
        self.picker = vtk.vtkPropPicker() ## 硬件picker
        self.picker.PickFromListOn()
    
    def setPickerActor(self, actor):
        if self.pick_actor is not None:
            self.picker.DeletePickList(self.pick_actor)
        self.pick_actor = actor
        self.picker.AddPickList(actor)
    
    def setMode(self, mode):
        if mode in ['cursor','move','edit']:
            self.mode = mode
            if mode == 'edit':
                self.pen_active = True

    def leftButtonPressEvent(self, obj, event):
        if self.mode == 'move':
            super().OnMiddleButtonDown()  # 调用原有的MiddleButtonDown方法，实现平移功能
        elif self.mode == 'edit':
            if self.pick_actor is not None:
                self.drawing = True
                self.drawLabel(1)
                self.slice_view.updateRender() ## 就点击的第一下 需要渲染
        elif self.mode == 'cursor':
            if self.pick_actor is not None:
                self.getMouseCursor()
            # self.cursor_picking = True
    
    def leftButtonReleaseEvent(self, obj, event):
        if self.cursor_picking:
            self.cursor_picking = False
        if self.drawing:
            self.drawing = False
        super().OnLeftButtonUp()
    
    def mouseMoveEvent(self, obj, event):
        if self.mode == 'cursor' and self.cursor_picking:
            self.getMouseCursor()
        elif self.mode == 'edit':
            if self.pen_active:
                self.updatePen()
            if self.drawing:
                self.drawLabel(1)
            elif self.erasing:
                self.drawLabel(0)
            else: # 不画图的时候允许中键移动
                super().OnMouseMove() 
        else:
            super().OnMouseMove()
    
    def getMousePosittion(self):
        '''
        获取鼠标所在的坐标
        '''
        clickPos = self.GetInteractor().GetEventPosition()
        self.picker.Pick(clickPos[0], clickPos[1], 0, self.slice_view.renderer)
        picked_actor = self.picker.GetProp3D()
        if picked_actor == self.pick_actor :
            picked = self.picker.GetPickPosition()
            return picked
        else:
            return None

    def getMouseCursor(self):
        '''
        鼠标点击或移动时 获取指针所在位置的index
        '''
        pos = self.getMousePosittion()
        if pos:
            self.slice_view.onPickCursor(pos)
    
    def updatePen(self, render = True):
        '''
        更新笔刷的位置
        '''
        pos = self.getMousePosittion()
        if pos:
            self.slice_view.setPenPosition(pos, render=render)

    ##
    def drawLabel(self, mode = 0):
        '''
        mode:
        0 擦除
        1 绘制
        '''
        pos = self.getMousePosittion()
        if pos:
            self.slice_view.drawLabel(pos, mode)

    ##
    def rightButtonPressEvent(self, obj, event):
        if self.mode == 'cursor' or self.mode == 'move':
            super().OnRightButtonDown()
        elif self.mode == 'edit':
            self.erasing = True
            self.drawLabel(0)
    
    def rightButtonReleaseEvent(self, obj, event):
        self.slice_view.updateCurrentCameraDistance()
        if self.erasing:
            self.erasing = False
        return super().OnRightButtonUp()

    def middleButtonPressEvent(self, obj, event):
        # 平移
        super().OnMiddleButtonDown() 

    def mouseWheelForwardEvent(self, obj, event):
        # print('mouseWheelForwardEvent')
        self.slice_view.wheelChangeSlice(-1)

    def mouseWheelBackwardEvent(self, obj, event):
        # print('mouseWheelBackwardEvent')
        self.slice_view.wheelChangeSlice(1)

class SliceView(vtkWidget):
    '''
    通过vtkImageSlice显示图像 比QGraphicView简单 但占用内存更多
    切换切片时同时也要平移摄像机以保持图像大小不变
    '''
    def __init__(self, orientation=0, label_name=None, parent=None) -> None:
        super().__init__(parent=parent)
        signalBus.cursorChanged.connect(self.updateDisplay)
        self.image = None
        self.image_mapper = None
        self.image_actor = None
        
        self.label = None
        self.label_mapper = None
        self.label_actor = None

        self.label_name = label_name
        self.label_offset = 0.005
        ##
        self.current_slice = 0   
        self.cursor_lines = [None, None]
        
        self.cursor_line_color = hexToRgb('#409EFF')
        self.cursor_line_color = [i/255.0 for i in self.cursor_line_color]
        self.cursor_line_opacity = 1
        self.cursor_line_width = 1.5
        self.cursor_line_offset = 0.01 ## cursor line 与图像slice 的距离 保证在slice上面
        self.slice_num = 0 # 总数
        self.scale = 1 # scale = 1 图像完整显示
        self.mouse_mode = 'cursor'
        ## 修改label的笔刷
        self.pen_mode = 'square'
        self.pen_size = 1
        self.pen_polydata = None
        self.pen_actor = None
        self.pen_voxels = [] ## 笔刷的相对体素
        self.label_selected = 0
        ##
        self.orientation = orientation
        self.initCamera_()
        ##
        self.interactor = SliceViewInteractor(self)
        self.setInteractorStyle(self.interactor)
    
    def initCamera_(self):
        '''
        初始化相机方向
        direction: 原点指向camera 即视角反方向 单位向量: np
        '''
        # camera
        self.view_ang = 30
        self.camera.SetViewAngle(self.view_ang)
        if self.orientation == 0:
            self.camera_direction = [1,0,0]
            self.camera_viewup = [0,0,1]
        elif self.orientation == 1:
            self.camera_direction = [0,-1,0]
            self.camera_viewup = [0,0,1]
        else: # self.orientation == 2
            self.camera_direction = [0,0,-1]
            self.camera_viewup = [0,-1,0]
        self.camera_direction = np.array(self.camera_direction)
        self.camera_viewup = np.array(self.camera_viewup)
    
    def setImageLabel(self, image: myImageData, label:myImageData):
        self.image = image
        self.label = label
        if self.image_actor is not None:
            self.removeActor(self.image_actor)
            
        self.image_mapper = vtkImageSliceMapper()
        self.image_mapper.SetOrientation(self.orientation)
        self.image_mapper.SetInputData(self.image.vtkImageData)
        self.image_actor = vtkImageSlice()
        self.image_actor.SetMapper(self.image_mapper)
        self.addActor(self.image_actor)
        self.interactor.setPickerActor(self.image_actor)
        # #
        self.setLabel(label)
        ##
        self.slice_num = self.image.size[self.orientation]
        self.reComputeCameraDistance()
        self.initCursorLine()
        self.updateRender()
    
    def setLabel(self, label: myImageData):
        self.label = label
        
        if self.label_actor is not None:
            self.removeActor(self.label_actor)
        self.label_mapper = vtkImageSliceMapper()
        self.label_mapper.SetOrientation(self.orientation)
        self.label_mapper.SetInputData(self.label.vtkImageData)
        self.label_actor = vtkImageSlice()
        self.label_actor.SetMapper(self.label_mapper)
        label_offset = np.array([0,0,0]) + self.camera_direction * self.label_offset
        self.label_actor.SetPosition(label_offset)
        self.addActor(self.label_actor)

        label_max = label.max
        # 创建一个查找表
        lookupTable = vtkLookupTable()
        lookupTable.SetTableRange(0.0, 1.0)  # 设置标量值的范围
        lookupTable.SetAlphaRange(0.0, 1.0)  # 设置透明度的范围
        lookupTable.SetNumberOfTableValues(label_max+1)  # 设置查找表的大小
        lookupTable.Build()

        lookupTable.SetTableValue(0, 0, 0, 0, 0)
        alpha = 1
        for i in range(1, label_max+1):
            r,g,b = getLabelColor(i)            
            lookupTable.SetTableValue(i, r, g, b, alpha)
        ##
        self.label_actor.GetProperty().SetColorLevel(label_max/2.0)
        self.label_actor.GetProperty().SetColorWindow(label_max)
        self.label_actor.GetProperty().SetLookupTable(lookupTable)
        label_opacity = globalVar.get(NAMES.LABEL_OPACITY, 0.5)
        self.label_actor.GetProperty().SetOpacity(label_opacity)

    def reComputeCameraDistance(self):
        '''
        重置 distance 全部显示
        '''
        length = np.array(self.image.size) * np.array(self.image.spacing)
        length = np.delete(length, self.orientation)
        length = np.max(length)
        self.camera_distance = length/1 /2 / math.tan(math.radians(self.view_ang/2))

    def setColor(self, level, window):
        self.image_actor.GetProperty().SetColorLevel(level)
        self.image_actor.GetProperty().SetColorWindow(window)
    
    def setLabelOpacity(self, opacity):
        if self.label_actor:
            self.label_actor.GetProperty().SetOpacity(opacity)
            self.updateRender()

    def setSlice(self, i):
        '''
        改变slice显示
        '''
        cursor = globalVar.get(NAMES.CURSOR, None)
        if cursor is None:
            return
        cursor[self.orientation] = i
        signalBus.cursorChanged.emit()

    def resetCamera_(self):
        '''
        _ 与原始区分
        '''
        if self.image:
            ##
            self.reComputeCameraDistance()
            center_index = np.array(self.image.size)/2
            center_index[self.orientation] = self.current_slice
            center_point = np.array([0,0,0])
            self.image.vtkImageData.TransformContinuousIndexToPhysicalPoint(center_index, center_point)
            ##
            self.camera.SetFocalPoint(center_point)
            self.camera.SetPosition(center_point + self.camera_direction * self.camera_distance)
            self.camera.SetViewUp(self.camera_viewup)
            self.renderer.ResetCameraClippingRange()
            self.renWin.Render()

    def resetCameraDistance_(self):
        '''
        切换切片时 摄像机保持与切片的距离移动 达成相对静止
        '''
        if self.image:
            focal_point = self.camera.GetFocalPoint()
            focal_point = np.array(focal_point)
            ## 当前切片的中心
            center_index = np.array(self.image.size)/2
            center_index = np.around(center_index).astype(np.int32)
            center_index[self.orientation] = self.current_slice
            center_point = np.array([0,0,0], dtype=np.float32)
            self.image.vtkImageData.TransformIndexToPhysicalPoint(center_index, center_point)
            focal_point[self.orientation] = center_point[self.orientation]
            self.camera.SetFocalPoint(focal_point)
            self.camera.SetPosition(focal_point + self.camera_direction * self.camera_distance)
            self.renWin.Render()
    
    def updateCurrentCameraDistance(self):
        '''
        更新当前摄像机距离
        '''
        focal_point = self.camera.GetFocalPoint()
        focal_point = np.array(focal_point)
        position = self.camera.GetPosition()
        position = np.array(position)        
        self.camera_distance = np.linalg.norm(focal_point - position)

    def setMouseMode(self, mode):
        self.mouse_mode = mode
        self.interactor.setMode(mode)
        if mode =='edit':
            self.initPen()
        else:
            self.hidePen()
    
    def wheelChangeSlice(self, delta):
        '''
        由鼠标滚轮直接触发的一层一层的切换
        delta +- 1
        '''
        next_slice = self.current_slice + delta
        if next_slice <0:
            next_slice = 0
        elif next_slice >= self.slice_num:
            next_slice = self.slice_num-1
            
        self.setSlice(next_slice)
        
    ## cursor 改变 更新
    def updateDisplay(self):
        if self.image is None:
            return
        cursor = globalVar.get(NAMES.CURSOR, None)
        i = cursor[self.orientation]
        self.current_slice = i
        if self.image_mapper:
            self.image_mapper.SetSliceNumber(i)
        if self.label_mapper:
            self.label_mapper.SetSliceNumber(i)
        if self.mouse_mode == 'edit':
            self.updatePenPosition(render = False) # 避免闪烁
        ##
        self.updateCursorLine(render=False)
        self.resetCameraDistance_()


    
    def computeCursorLinePoints(self):
        # self.camera_direction
        points = []
        cursor = globalVar.get(NAMES.CURSOR, None)
        for i in range(3):
            if i != self.orientation:
                start_index = cursor.copy()
                start_index[i] = 0
                end_index = cursor.copy()
                end_index[i] = self.image.size[i]-1
                start_point = np.array([0,0,0], dtype=np.float32)
                end_point = np.array([0,0,0], dtype=np.float32)
                self.image.vtkImageData.TransformIndexToPhysicalPoint(start_index, start_point)
                # self.image.vtkImageData.TransformIndexToPhysicalPoint()
                self.image.vtkImageData.TransformIndexToPhysicalPoint(end_index, end_point)
                points.append([start_point, end_point])
        #
        # print(f'curosr points: {points}')
        return points

    def initCursorLine(self):    
        cursor_points = self.computeCursorLinePoints()
        j = 0
        for i in range(3):
            if i != self.orientation:
                if self.cursor_lines[j] is None:
                ##
                    start_point, end_point = cursor_points[j]
                    line = vtkLineSource()
                    line.SetPoint1(start_point)
                    line.SetPoint2(end_point)
                    line.Update()
                    actor = getActor(line.GetOutput(), self.cursor_line_color, self.cursor_line_opacity, 1)
                    actor.SetPosition(self.camera_direction * self.cursor_line_offset) # 稍微往上一点
                    actor.GetProperty().SetLineWidth(self.cursor_line_width)
                    self.cursor_lines[j] = {
                        'source': line,
                        'actor': actor
                    }
                    self.addActor(actor)
                    j += 1

    def updateCursorLine(self, render=True):
        if len(self.cursor_lines)>0:
            cursor_points = self.computeCursorLinePoints()
            self.cursor_lines[0]['source'].SetPoint1(cursor_points[0][0])
            self.cursor_lines[0]['source'].SetPoint2(cursor_points[0][1])
            self.cursor_lines[0]['source'].Update()
            self.cursor_lines[1]['source'].SetPoint1(cursor_points[1][0])
            self.cursor_lines[1]['source'].SetPoint2(cursor_points[1][1])
            self.cursor_lines[1]['source'].Update()
            
            if render:
                self.updateRender()

    ## pick
    def onPickCursor(self, pos):
        '''
        鼠标点击坐标 转换为index
        '''
        index = np.array([0,0,0], dtype=np.float32)
        self.image.vtkImageData.TransformPhysicalPointToContinuousIndex(pos, index)
        cursor = np.around(index).astype(np.int32)
        
        globalVar.set(NAMES.CURSOR, cursor)
        signalBus.cursorChanged.emit()
    
    #######
    ## pen
    def initPen(self):
        if self.pen_actor :
            self.removeActor(self.pen_actor)
        self.updatePenShape()
    
    def updatePenShape(self):
        vtk_points = vtkPoints()
        vtk_lines = vtkCellArray()
        axis = [np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])]
        spacing = np.array(self.image.spacing)
        axis.pop(self.orientation)
        c = np.array([0,0,0])
        
        points = []
        self.pen_voxels = []
        if self.pen_mode == 'square':    
            '''
            正方形的中心c 在体素的中心
            若边长为偶数 c偏移0.5 仍保持在体素中心 但就不在正方形中心了
            '''
            ## points 边框
            if self.pen_size % 2 == 1:   
                l0 = self.pen_size /2
                l1 = self.pen_size /2
                ## 体素index range
                r0 = self.pen_size //2
                r1 = self.pen_size - r0
                range_ = [-int(r0), int(r1)]
            else: 
                l0 = self.pen_size /2 - 0.5
                l1 = self.pen_size /2 + 0.5   
                r0 = self.pen_size //2
                r1 = self.pen_size - r0
                range_ = [-int(r0)+1, int(r1)+1]
            points.append((c - axis[0] *l0 - axis[1] *l0)*spacing )
            points.append((c + axis[0] *l1 - axis[1] *l0)*spacing )
            points.append((c + axis[0] *l1 + axis[1] *l1)*spacing )
            points.append((c - axis[0] *l0 + axis[1] *l1)*spacing )
            ## voxel 
            for i in range(range_[0], range_[1]):
                for j in range(range_[0], range_[1]):
                    self.pen_voxels.append( axis[0] *i + axis[1] *j )

        elif self.pen_mode == 'circle':       
            ## voxel      
            pen = getCirclePen(self.pen_size)
            voxels_len = pen.getPenvoxels()
            for item in voxels_len:
                self.pen_voxels.append( axis[0] *item[0] + axis[1] *item[1] )
            ## points 边框
            path_index = pen.getPathPoints()
            for item in path_index:
                points.append((c + axis[0] *item[0] + axis[1] *item[1])*spacing )
        ##
        for i in range(len(points)):
            vtk_points.InsertNextPoint(points[i])
            line = vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, (i+1)%len(points))
            vtk_lines.InsertNextCell(line)
            if not self.pen_polydata:
                self.pen_polydata = vtkPolyData()
            self.pen_polydata.SetPoints(vtk_points)
            self.pen_polydata.SetLines(vtk_lines)
            self.pen_polydata.Modified()
        ##
        if not self.pen_actor:
            self.pen_actor = getActor(self.pen_polydata, [1,0,0], 1, 1)

    def setPenPosition(self, pos, render = True):
        '''
        pos 鼠标所在的物理坐标
        需要先确定物理坐标最近的index 再转换为物理坐标
        '''
        index = self.getPenIndex(pos)
        pos = np.array([0,0,0], dtype=np.float32)
        self.image.vtkImageData.TransformIndexToPhysicalPoint(index, pos)
        self.pen_actor.SetPosition(pos + self.camera_direction * self.cursor_line_offset) # 稍微往上一点
        if render:
            self.updateRender()
    
    def getPenIndex(self, pos):
        '''
        鼠标所在坐标 最近的index
        '''
        continuous_index = np.array([0,0,0], dtype=np.float32)
        self.image.vtkImageData.TransformPhysicalPointToContinuousIndex(pos, continuous_index)
        index = np.around(continuous_index).astype(np.int32)
        return index
    
    def updatePenPosition(self, render=True):
        '''
        更新pen坐标
        '''
        
        self.interactor.updatePen(render = render)

    def setPenStyle(self, pen_size, pen_mode):
        self.pen_size = pen_size
        self.pen_mode = pen_mode
        if self.mouse_mode == 'edit':
            self.updatePenShape()
            self.updateRender()

    def setSelectedLabel(self, index):
        self.label_selected = index

    def hidePen(self):
        if self.pen_actor:
            self.removeActor(self.pen_actor)
    
    def showPen(self):
        if self.pen_actor:
            self.addActor(self.pen_actor)

    ## 鼠标事件
    def leaveEvent(self, event) -> None:
        # print('leaveEvent')
        if self.mouse_mode =='edit':
            self.hidePen()
            self.updateRender()
        return super().leaveEvent(event)

    def enterEvent(self, ev):
        if self.mouse_mode =='edit':
            self.showPen()
        return super().enterEvent(ev)

    ## draw label
    def drawLabel(self, pos, mode = 0):
        '''
        画图事件  pos为鼠标点击的位置
        直接改变 self.label.vtkImageData
        mode: 0 擦除 1 绘制
        '''
        index = self.getPenIndex(pos)
        value = self.label_selected
        for item in self.pen_voxels:
            target = index + item
            size = np.array(self.label.size)
            if np.all(target>=0) and np.all(target<size):
                if mode:
                    self.label.vtkImageData.SetScalarComponentFromFloat(target[0], target[1], target[2], 0, value)
                else:
                    old_val = self.label.vtkImageData.GetScalarComponentAsFloat(target[0], target[1], target[2], 0)
                    if old_val == value:
                        self.label.vtkImageData.SetScalarComponentFromFloat(target[0], target[1], target[2], 0, 0)
        ##
        self.label.vtkImageData.Modified()
        ## modified 就行了 不用render


    ## 键盘输入
    def keyPressEvent(self, event):
        key = event.key()
        # print(type(key), key)
        signalBus.keyPressed.emit(key)









