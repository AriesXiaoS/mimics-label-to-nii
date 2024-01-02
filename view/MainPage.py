import os, sys, traceback
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from .ui.Ui_main_page import Ui_MainPage

from common import signalBus, globalVar, NAMES, myImageData, DOC_APP_FOLDER, ICON

from modules.file_path import PathManager
from modules.fileReader import ImageReader
from modules.fileWriter import ImageWriter

from components.file_item.FileItem import FileItem
from components.label_item.LabelItem import LabelItem
from components.image_view.main_image_view import ImageView
from components.image_view.mesh_view import MeshView

from utils.imageProcess import *
from utils.decorator import *

class MainPage(QWidget, Ui_MainPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        globalVar.set(NAMES.IMAGES, {})
        globalVar.set(NAMES.CURSOR, np.array([0, 0, 0]))
        globalVar.set(NAMES.LABEL_OPACITY, 0.5)

        self.displaying_all_view = True
        
        self.selected_index = -1

        self.readImage_th = None
        self.readLabel_th = None

        self.current_slice = [0, 0, 0]

        self.labels = {}
        self.label_editing = False # editing = not saved
        globalVar.set(NAMES.LABEL_OPACITY, 0.5)
        self.labelOpacitySpinBox.setValue(0.5)

        self.mouse_mode = NAMES.CURSOR
        self.image_set = False  # 加载图像后才运行切换 笔
        self.label_selected = 0

        self.initWidgets()
        self.initImageView()
        self.initLabels()
        #
        self.initSignals()
        self.updatePath()
        self.setMouseMode(NAMES.CURSOR)


    def initSignals(self):
        self.selectFolderBtn.clicked.connect(self.selectFolder)
        self.updatePathBtn.clicked.connect(self.updatePath)
        #
        self.folderPathTextEdit.textChanged.connect(self.setDisplayFolder)
        self.dicomNameLineEdit.textChanged.connect(lambda val : self.setDisplayName(val, NAMES.DICOM_NAME))
        self.niiNameLineEdit.textChanged.connect(lambda val : self.setDisplayName(val, NAMES.NII_NAME))
        #
        signalBus.cursorChanged.connect(self.onCursorChanged)
        signalBus.keyPressed.connect(self.keyBoardSetLabel)
        #
        self.settingBtn.clicked.connect(lambda : os.startfile(DOC_APP_FOLDER))
        self.labelOpacitySpinBox.valueChanged.connect(self.setLabelOpacity)
        #
        self.confirmSaveBtn.clicked.connect(self.saveLabel)
        self.cursorBtn.clicked.connect(lambda : self.setMouseMode(NAMES.CURSOR))
        self.penBtn.clicked.connect(lambda : self.setMouseMode(NAMES.EDIT))
        self.penSizeSlider.valueChanged.connect(self.setPenSize)

    def initWidgets(self):
        self.folderPathTextEdit.setPlainText(PathManager.getHistFolder())
        self.dicomNameLineEdit.setText(PathManager.getDicomName())
        self.niiNameLineEdit.setText(PathManager.getNiiName())
        ##
        self.files_layout = QVBoxLayout()
        self.files_layout.setContentsMargins(0, 0, 0, 0)
        self.files_layout.setSpacing(0)
        self.files_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.filesListContent.setLayout(self.files_layout)
        #
        self.settingBtn.setIcon(FIF.SETTING)
        #
        # label 
        self.labels_layout = QVBoxLayout()
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.labels_layout.setSpacing(0)
        self.labels_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.labelListContent.setLayout(self.labels_layout)
        #
        self.cursorBtn.setIcon(ICON.CURSOR_LINE)
        self.penBtn.setIcon(FIF.EDIT)
        #
        self.questionBtn.setIcon(FIF.QUESTION)
        self.questionBtn.setFixedSize(22, 22)
        self.questionBtn.setIconSize(QSize(12, 12))
        self.questionBtn.hide()
        
    ##################
    #### 左侧 文件 路径

    @try_except_decorator
    def selectFolder(self):
        '''
        选择文件夹
        '''
        open_path = PathManager.getHistFolder()
        folder_path = QFileDialog.getExistingDirectory(self,
            QCoreApplication.translate("File", 'dialog-select-folder'), open_path) 
        #
        if folder_path:
            PathManager.setHistFolder(folder_path)
            self.folderPathTextEdit.setPlainText(folder_path)
            self.updatePath()

    def setDisplayFolder(self, mode = NAMES.MAIN_FOLDER_PATH):
        '''
        修改 plain text edit 但不修改配置文件
        '''
        PathManager.setDisplayPath(self.folderPathTextEdit.toPlainText(), mode)

    def setDisplayName(self, name, mode = NAMES.MAIN_FOLDER_PATH):
        '''
        修改 line edit 但不修改配置文件
        '''
        PathManager.setDisplayPath(name, mode)

    @try_except_decorator
    def updatePath(self):
        global_images = globalVar.get(NAMES.IMAGES, {})
        for k,v in global_images.items():
            read_th = v.get('read_th', None)
            if read_th is not None:
                read_th.terminate()
                read_th = None
            #
            item = v.get('item', None)
            if item is not None:
                item.setLoadingState(0)
                self.files_layout.removeWidget(item)
                item.setParent(None)
        #clear
        global_images = {}

        files = PathManager.parserPaths()
        
        for i,f in enumerate(files):
            item_dict = {}
            item_dict.update(f)
            item_dict['read_th'] = None
            item_dict['image'] = None # myImageData
            item_dict['label'] = None # myImageData

            item = FileItem(i, f['name'], f['nii_exist'])
            item.Click.connect(self.onSelectedFile)
            self.files_layout.addWidget(item)
            item_dict['item'] = item
            #
            global_images[i] = item_dict
        #
        globalVar.set(NAMES.IMAGES, global_images)
        self.selected_index = -1

    ##################
    #### 选择文件
    def onSelectedFile(self, index, reset = False):
        post_save = 1
        pre_load = 1
        
        if self.label_editing:
            title = '标签未保存'
            content = '标签未保存，是否保存当前？'
            msg = Dialog(title, content, self.window())
            if msg.exec():
                self.saveLabel(index)
                return
            else:                    
                self.label_editing = False
            
        
        global_images = globalVar.get(NAMES.IMAGES, {})
        len_images = len(list(global_images.keys()))
        
        if reset:
            self.selected_index = -1
        if index == self.selected_index or index >= len(global_images):
            return
        #
        for i in range(len(global_images)):
            if i == index:
                global_images[i]['item'].setSelected(True)
            else:
                global_images[i]['item'].setSelected(False)
        self.selected_index = index

        all_indexs = [i for i in range(len_images)]
        keep_indexs = [i for i in range(index-pre_load, index+post_save+1)]
        remove_indexs = list(set(all_indexs) - set(keep_indexs))
        # 删除
        for i in remove_indexs:
            image = global_images[i]['image']
            read_th = global_images[i]['read_th']
            if read_th is not None:
                read_th.terminate()
                del global_images[i]['read_th']
                global_images[i]['read_th'] = None
            if image is not None:
                del global_images[i]['image']
                global_images[i]['image'] = None
            if label is not None:
                del global_images[i]['label']
                global_images[i]['label'] = None
            global_images[i]['item'].setLoadingState(0)
        
        ## 清除 mesh
        self.view_bl.clear()

        ## 加载选择项
        image = global_images[index]['image']
        if image is not None:
            self.showImage(index)
        else:
            read_th = global_images[index]['read_th']
            if read_th is None:
                global_images[index]['item'].setLoadingState(1)
                image_dcm_path = global_images[index]['dicom_dir']
                label_nii_path = global_images[index]['nii_path']
                read_th = ImageReader()
                read_th.setReadInfo(index, image_dcm_path, label_nii_path)
                read_th.readFinished.connect(self.onReadFile)
                read_th.start()
                global_images[index]['read_th'] = read_th
        ## i+1 预加载
        ii = index+1
        if ii in global_images:
            image_2 = global_images[ii]['image']
            read_th_2 = global_images[ii]['read_th']
            if image_2 is None and read_th_2 is None:
                global_images[ii]['item'].setLoadingState(1)
                image_dcm_path = global_images[ii]['dicom_dir']
                label_nii_path = global_images[ii]['nii_path']
                read_th_2 = ImageReader()
                read_th_2.setReadInfo(ii, image_dcm_path, label_nii_path)
                read_th_2.readFinished.connect(self.onReadFile)
                read_th_2.start()
                global_images[ii]['read_th'] = read_th_2

        globalVar.set(NAMES.IMAGES, global_images)
        
    def onReadFile(self, res:dict):  
        index = res['index']
        image = res.get('image', None)
        label = res.get('label', None)

        global_images = globalVar.get(NAMES.IMAGES, {})
        global_images[index]['read_th'] = None

        if image is None or label is None:
            return
        
        global_images[index]['item'].setLoadingState(2)
        global_images[index]['image'] = image
        global_images[index]['label'] = label
        if index == self.selected_index:
            self.showImage(index)        
    
    def showImage(self, index):
        global_images = globalVar.get(NAMES.IMAGES, {})
        image = global_images[index]['image']
        label = global_images[index]['label']
        
        if image is None:
            return
        self.view_tl.setImageLabel(image, label)
        self.view_tr.setImageLabel(image, label)
        self.view_br.setImageLabel(image, label)
        self.view_bl.setLabel( label)
        cursor = np.array([ image.size[i]//2 for i in range(3) ])
        globalVar.set(NAMES.CURSOR, cursor)
        signalBus.cursorChanged.emit()
        self.image_set = True

    ##############
    #### 中间 图像显示
    def initImageView(self):
        self.view_tl = ImageView(0)
        self.view_tr = ImageView(1)
        self.view_br = ImageView(2)
        self.view_bl = MeshView()

        self.view_tl.changeView.connect(lambda : self.changeView('tl'))
        self.view_tr.changeView.connect(lambda : self.changeView('tr'))
        self.view_br.changeView.connect(lambda : self.changeView('br'))
        self.view_bl.changeView.connect(lambda : self.changeView('bl'))

        self.view_layout_tl = QVBoxLayout(self.viewWidget_tl)
        self.view_layout_tl.setContentsMargins(0, 0, 0, 0)
        self.view_layout_tr = QVBoxLayout(self.viewWidget_tr)
        self.view_layout_tr.setContentsMargins(0, 0, 0, 0)
        self.view_layout_bl = QVBoxLayout(self.viewWidget_bl)
        self.view_layout_bl.setContentsMargins(0, 0, 0, 0)
        self.view_layout_br = QVBoxLayout(self.viewWidget_br)
        self.view_layout_br.setContentsMargins(0, 0, 0, 0)
        #
        self.view_layout_tl.addWidget(self.view_tl)
        self.view_layout_tr.addWidget(self.view_tr)
        self.view_layout_br.addWidget(self.view_br)
        self.view_layout_bl.addWidget(self.view_bl)
    
    def changeView(self, name):
        if self.displaying_all_view:
            self.displaying_all_view = False
            if name == 'tl':
                self.viewWidget_tl.show()
                self.viewWidget_tr.hide()
                self.viewWidget_bl.hide()
                self.viewWidget_br.hide()
            elif name == 'tr':
                self.viewWidget_tl.hide()
                self.viewWidget_tr.show()
                self.viewWidget_bl.hide()
                self.viewWidget_br.hide()
            elif name == 'bl':
                self.viewWidget_tl.hide()
                self.viewWidget_tr.hide()
                self.viewWidget_bl.show()
                self.viewWidget_br.hide()
            elif name == 'br':
                self.viewWidget_tl.hide()
                self.viewWidget_tr.hide()
                self.viewWidget_bl.hide()
                self.viewWidget_br.show()
        else:
            self.displaying_all_view = True
            self.viewWidget_tl.show()
            self.viewWidget_tr.show()
            self.viewWidget_bl.show()
            self.viewWidget_br.show()

    ### 光标移动
    def onCursorChanged(self):
        cursor = globalVar.get(NAMES.CURSOR)
        global_images = globalVar.get(NAMES.IMAGES, {})
        if self.selected_index < 0:
            return
        image = global_images[self.selected_index]['image']
        label = global_images[self.selected_index]['label']

        x,y,z = cursor
        image_value = image.vtkImageData.GetScalarComponentAsFloat(x,y,z,0)
        image_value = int(image_value)
        self.imageValue.setText(f'{image_value}')
        label_value = label.vtkImageData.GetScalarComponentAsFloat(x,y,z,0)
        label_value = int(label_value)
        self.labelValue.setText(f'{label_value}')

    ## label
    def initLabels(self):
        label_names = User_cfg.get('label_names', None)
        if label_names is None:
            signalBus.alertInfo.emit({
                'title': '错误',
                'content': '未设置标签名称',
                'duration': -1,
                'type': 'error',
            })
            return
        ##
        for i,name in label_names.items():
            item = LabelItem(int(i), name)
            color = getLabelColor(int(i))
            item.setColor(color)
            item.SetLabel.connect(self.setCurrentCursorLabel)
            item.Delete.connect(self.deleteLabel)
            item.Edit.connect(self.onSelectedLabel)
            item.Click.connect(self.onSelectedLabel)
            self.labels_layout.addWidget(item)
            self.labels[int(i)] = item

    def setLabelsMode(self, mode):
        for k,v in self.labels.items():
            v.setMode(mode)

    @try_except_decorator
    def setCurrentCursorLabel(self, label_i:int):
        # print('setCurrentCursorLabel', label_i)
        # print(self.labels)
        if label_i not in self.labels:
            print(f'未定义标签 {label_i}')
            return
        cursor = globalVar.get(NAMES.CURSOR)
        global_images = globalVar.get(NAMES.IMAGES, {})
        if self.selected_index < 0:
            return
        ## 开始修改label
        self.label_editing = True
        self.setCursor(Qt.WaitCursor)
        x,y,z = cursor
        image = global_images[self.selected_index]['image']
        label = global_images[self.selected_index]['label']
        image_arr = image.np_arr
        cursor_value = image.vtkImageData.GetScalarComponentAsFloat(x,y,z,0)
        wh = np.where(image_arr == cursor_value)
        points = list(zip(*wh))
        # print(cursor_value, label_i, len(points))
        for p in points:
            z,y,x = p
            label.vtkImageData.SetScalarComponentFromFloat(x,y,z, 0, label_i)

        label.vtkImageData.Modified()
        self.view_tl.updateRender()
        self.view_tr.updateRender()
        self.view_br.updateRender()
        # 修改完成
        self.setCursor(Qt.ArrowCursor)
        self.onCursorChanged()

    def keyBoardSetLabel(self, key_int):
        # print('keyBoardSetLabel', key_int)
        label_i = None
        addition_keyboard = User_cfg.get('addition_keyboard', None)
        if key_int >= 49 and key_int <= 57:
            label_i = key_int - 48
        elif key_int == 48:
            label_i = 10
        else:
            if addition_keyboard is not None:
                key_int_str = str(key_int)
                label_i = addition_keyboard.get(key_int_str, None)
        if label_i is not None:
            self.setCurrentCursorLabel(label_i)

    @try_except_decorator
    def deleteLabel(self, index):
        if self.selected_index < 0:
            return
        title = f'清除标签 {index}'
        content = f'确认清除所有标签 {index} ？'
        msg = Dialog(title, content, self.window())
        if msg.exec():
            ## 开始修改label
            self.setCursor(Qt.WaitCursor)
            global_images = globalVar.get(NAMES.IMAGES, {})
            label = global_images[self.selected_index]['label']
            label.updateLabelNpArr()
            label_arr = label.np_arr
            wh = np.where(label_arr == index)
            points = list(zip(*wh))

            for p in points:
                z,y,x = p
                label.vtkImageData.SetScalarComponentFromFloat(x,y,z, 0, 0)

            label.vtkImageData.Modified()
            self.view_tl.updateRender()
            self.view_tr.updateRender()
            self.view_br.updateRender()
            # 修改完成
            self.setCursor(Qt.ArrowCursor)
            self.onCursorChanged()
            self.label_editing = True

    def setLabelOpacity(self, val):
        globalVar.set(NAMES.LABEL_OPACITY, val)
        self.view_tl.slice_view.setLabelOpacity(val)
        self.view_tr.slice_view.setLabelOpacity(val)
        self.view_br.slice_view.setLabelOpacity(val)

    @try_except_decorator
    def saveLabel(self, goto_target_index = None):
        if self.selected_index < 0 :
            return
        # save and goto next
        global_images = globalVar.get(NAMES.IMAGES, {})
        label = global_images[self.selected_index]['label']
        label.updateLabelNpArr()
        label_path = global_images[self.selected_index]['nii_path']

        wirter = ImageWriter()
        wirter.setFilePath(label_path)
        wirter.write(label)
        ## 修改完成
        name = global_images[self.selected_index]['name']
        signalBus.alertInfo.emit({
            'title': '保存成功',
            'content': f'{name} Nifti label 保存完成',
            'duration': 2000,
            'type': 'success'
        })
        global_images[self.selected_index]['nii_exist'] = True
        global_images[self.selected_index]['item'].setNiiState(True)
        self.label_editing = False
        if goto_target_index is not None:
            self.onSelectedFile(goto_target_index)
        else:
            self.onSelectedFile(self.selected_index+1)

    ###################
    ## 鼠标模式
    def setMouseMode(self, mode= NAMES.CURSOR):
        self.mouse_mode = mode
        if mode == NAMES.CURSOR:
            self.onSelectedLabel(0, force=True)
            self.cursorBtn.setChecked(True)
            self.penBtn.setChecked(False)
            self.view_tl.slice_view.setMouseMode(mode)
            self.view_tr.slice_view.setMouseMode(mode)
            self.view_br.slice_view.setMouseMode(mode)
            self.setLabelsMode(mode)
        else:
            if not self.image_set:
                signalBus.alertInfo.emit({
                    'title': '注意',
                    'content': '请先加载图像',
                    'duration': 3000,
                    'type': 'warning'
                })
                self.cursorBtn.setChecked(True)
                self.penBtn.setChecked(False)
            else:
                self.cursorBtn.setChecked(False)
                self.penBtn.setChecked(True)
                self.view_tl.slice_view.setMouseMode(mode)
                self.view_tr.slice_view.setMouseMode(mode)
                self.view_br.slice_view.setMouseMode(mode)
                self.setLabelsMode(mode)
                self.onSelectedLabel(1)

    def setPenSize(self, size):
        self.penSizeLabel.setText(f'{size}')
        self.view_tl.slice_view.setPenStyle(size, 'square')
        self.view_tr.slice_view.setPenStyle(size, 'square')
        self.view_br.slice_view.setPenStyle(size, 'square')

    def onSelectedLabel(self, index, force = False):
        self.label_selected = index
        if force or self.mouse_mode == NAMES.EDIT:
            for k,v in self.labels.items():
                if k==index:
                    self.labels[index].setEditing(True)
                else:
                    self.labels[k].setEditing(False)
            self.view_tl.slice_view.setSelectedLabel(index)
            self.view_tr.slice_view.setSelectedLabel(index)
            self.view_br.slice_view.setSelectedLabel(index)


