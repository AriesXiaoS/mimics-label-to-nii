
import os,sys
from typing import Optional
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF


import numpy as np
import vtk
from .Ui_mesh import Ui_meshView
from common import myImageData, signalBus, globalVar, NAMES, ICON

from modules.mesh import LabelToMesh
from modules.vtkWindow import vtkWidget
from utils.vtkAssembly import *

class MeshView(QWidget, Ui_meshView):
    changeView = Signal()
    def __init__(self,):
        super().__init__()
        self.setupUi(self)

        self.label = None
        self.mesh_th = None
        self.stateTooltip = None

        self.meshes = dict()

        self.initView()
        self.initSetting()
        self.initSignals()

    def initSetting(self):
        self.resetBtn.setFixedWidth(18)
        self.resetBtn.setFixedHeight(18)
        self.resetBtn.setIcon(FIF.SYNC)
        self.resetBtn.setIconSize(QSize(12, 12))

        self.soloBtn.setFixedWidth(18)
        self.soloBtn.setFixedHeight(18)
        self.soloBtn.setIcon(FIF.ZOOM)
        self.soloBtn.setIconSize(QSize(12, 12))

        self.sideWidget.setFixedWidth(18)
        #
        self.updateBtn.setFixedWidth(18)
        self.updateBtn.setFixedHeight(32)
        self.updateBtn.setIcon(ICON.D3_3D)
        self.updateBtn.setIconSize(QSize(14, 14))

    def initSignals(self):
        self.soloBtn.clicked.connect(self.changeView.emit)
        self.updateBtn.clicked.connect(self.updateAllLabel)
        self.resetBtn.clicked.connect(self.resetCamera)

    def initView(self):
        self.mesh_view = vtkWidget(self.viewWidget)

    def setLabel(self, label:myImageData):
        self.label = label
    
    def resetCamera(self):
        self.mesh_view.setCameraDataAuto()
        self.mesh_view.updateRender()

    def updateAllLabel(self):
        if self.label is None:
            return
        if self.mesh_th is None:
            self.mesh_th = LabelToMesh()
            self.mesh_th.setLabel(self.label)
            self.mesh_th.Finished.connect(self.meshGot)
            self.mesh_th.Info.connect(self.setMeshStateTooltipContent)
            self.mesh_th.start()
            self.setMeshStateTooltip(True)


    def meshGot(self, res:dict):     
        
        for k,v in res.items():
            if k in self.meshes:
                item = self.meshes[k]
                actor = item.get('actor',None)
                if actor is not None:
                    self.mesh_view.removeActor(actor)
            else:
                item = dict()

            polydata = v['polydata']
            color = v['color']
            opacity = 1
            actor = getActor(polydata, color, opacity)
            self.mesh_view.addActor(actor)
            item['actor'] = actor
            self.meshes[k] = item
            
        # self.mesh_view.updateRender()
        self.mesh_view.setCameraDataAuto()
        self.mesh_view.updateRender()
        self.mesh_th = None
        self.setMeshStateTooltip(False)

    def setMeshStateTooltip(self, show):
        if show:
            self.stateTooltip = StateToolTip('生成中', '' , self)
            self.stateTooltip.move(15, 15)
            self.stateTooltip.show()
        else:
            if self.stateTooltip:
                self.stateTooltip.setContent('完成')
                self.stateTooltip.setState(True)
                self.stateTooltip = None

    def setMeshStateTooltipContent(self, content):
        if self.stateTooltip:
            self.stateTooltip.setContent(content)

    def clear(self):
        self.mesh_view.clearRenderer()
        self.meshes = dict()

