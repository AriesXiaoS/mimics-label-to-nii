import numpy as np
import math

from vtk import (
    vtkPolyDataMapper, vtkActor, vtkPolyData, 
    vtkPoints, vtkDoubleArray, vtkVertex, vtkCellArray,
    vtkGlyph3D, vtkBillboardTextActor3D, vtkVectorText,
    vtkArrowSource, vtkPlaneSource, vtkLineSource, vtkFollower,
    vtkSphereSource,
)


def createSingleVectorArrowData(origin, direction, length):
    '''
    输入: origin起点坐标,target终点朝向坐标,length箭头长度
    输出: vtkPolyData箭头几何数据
    '''
    points = vtkPoints()  #记录起点坐标
    points.InsertNextPoint(origin)
    vertex = vtkVertex() #建立起点的拓扑(不建立拓扑的话是不行的)
    vertex.GetPointIds().SetNumberOfIds(points.GetNumberOfPoints())
    for i in range(points.GetNumberOfPoints()):
        vertex.GetPointIds().SetId(i,i)
    ## 创建法向量属性,存入向量的朝向 direction
    normals = vtkDoubleArray()
    normals.SetNumberOfComponents(3)
    normals.InsertNextTuple(direction)
    ## 创建标量属性,存入向量的长度length
    scalars = vtkDoubleArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName('scalars')
    scalars.InsertNextTuple1(length)
    ## 将建立的拓扑用vtkCellArray封装,用于赋予vtkPolyData
    vertices = vtkCellArray()
    vertices.InsertNextCell(vertex)

    polydata = vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(vertices)
    polydata.GetPointData().SetNormals(normals)
    polydata.GetPointData().SetScalars(scalars)
    return polydata

def generateNormalsArrow(polydata, 
    tip_radius = 0.06, tip_resolution = 50, tip_len = 0.15,
    shaft_radius = 0.025, shaft_resolution = 50,
    ):
    '''
    输入:polyData来自CreateSingleVectorArrowData函数输出的箭头数据
    输出:vtkPolyData能够用于显示的箭头几何实体
    '''
    arrow = vtkArrowSource()
     # 头部圆锥
    arrow.SetTipRadius(tip_radius)
    arrow.SetTipResolution(tip_resolution)
    arrow.SetTipLength(tip_len) # 圆锥高度比例
     # 主干圆柱
    arrow.SetShaftRadius(shaft_radius)
    arrow.SetShaftResolution(shaft_resolution)
    arrow.Update()
    glyph = vtkGlyph3D()
    glyph.SetInputData(polydata)
    glyph.SetSourceData(arrow.GetOutput())
    glyph.SetScaleFactor(1)
    glyph.SetVectorModeToUseNormal()
    glyph.Update()
    return glyph.GetOutput()


def getActor(polydata, color, opacity, diffuse=None):
    '''
    vtkPolydata -> vtkActor
    '''
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.ScalarVisibilityOff()
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)
    if diffuse:
        actor.GetProperty().SetDiffuse(diffuse)
    return actor

######

def getArrowActor(origin, direction, length, color = [1,1,1], opacity=1,
    tip_radius = 0.06, tip_resolution = 50, tip_len = 0.15,
    shaft_radius = 0.025, shaft_resolution = 50,
    ):
    polydata = createSingleVectorArrowData(origin, direction, length)
    polydata = generateNormalsArrow(polydata,tip_radius, tip_resolution,tip_len, shaft_radius,shaft_resolution)
    return getActor(polydata, color, opacity, 1)

def getPlaneActor3P( origin, p1, p2, color = [1,1,1], opacity = 1, diffuse=1):
    '''
    三点确定一个平面
    平面位置方向边界形状: 三点组成四边形
    '''
    plane = vtkPlaneSource()
    # plane.SetCenter(center)
    # plane.SetNormal(normal)
    plane.SetOrigin(origin)
    plane.SetPoint1(p1)
    plane.SetPoint2(p2)
    plane.Update()
    return getActor(plane.GetOutput(), color, opacity, diffuse)

def getLineActor(p1, p2, lineWidth=1, color = [1,1,1], opacity = 1):
    line = vtkLineSource()
    line.SetPoint1(p1)
    line.SetPoint2(p2)
    line.Update()
    actor = getActor(line.GetOutput(), color, opacity, 1)
    actor.GetProperty().SetLineWidth(lineWidth)
    return actor

def getFollowingTextActor(text, position, font_size = 1, color = [1,1,1], opacity = 1):
    '''
    未完成
    '''
    t = vtkVectorText()
    t.SetText(text)   

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(t.GetOutputPort())
    
    actor = vtkFollower()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)
    actor.SetScale(0.2)
    actor.SetPosition(position)
    
    return actor

def getFixedTextActor(self):
    pass


def getBillBoardTextActor(text, position, font_size = 16, color = [1,1,1], bold = True ):
    '''
    文字锚定在三维空间中
    但文字朝向永远面向摄像机, 即不论哪个角度都是正视文字, 锚点为文字中心
    '''
    actor = vtkBillboardTextActor3D()
    actor.SetInput(text)
    actor.SetPosition(position)
    actor.ForceOpaqueOn()
    prop = actor.GetTextProperty()
    prop.SetFontSize(font_size)
    if bold:
        prop.BoldOn()
    else:
        prop.BoldOff()
    prop.SetColor(color)
    prop.SetJustificationToCentered()
    prop.SetVerticalJustificationToCentered()
    return actor


def getSphereActor(center, radius, color = [1,1,1], opacity = 1):
    '''
    球体
    '''
    sphere = vtkSphereSource()
    sphere.SetCenter(center)
    sphere.SetRadius(radius)
    sphere.Update()
    return getActor(sphere.GetOutput(), color, opacity, 1)







