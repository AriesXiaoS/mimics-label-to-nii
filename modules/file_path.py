import os
from common import cfg, NAMES, signalBus

def parseFilePath(file_path):
    '''
    处理文件路径 比如网络位置的文件路径开头为 'file:'需要去掉
    '''
    file_path = file_path.replace('file:///', '')  # drop event 返回的路径
    file_path = file_path.replace('file:', '')  # 网络路径 需要保留前面的 \\ 两个斜杠
    # file_path = file_path.replace('/', '\\') #  windows \ / 可以混用
    return file_path

class PATHMANAGER():
    def __init__(self):
        self.display_path = cfg.initOneCfg(NAMES.MAIN_FOLDER_PATH, os.path.expanduser('~'))
        self.dicom_name = cfg.initOneCfg(NAMES.DICOM_NAME, 'DICOM_label')
        self.nii_name = cfg.initOneCfg(NAMES.NII_NAME, 'label.nii.gz')
    
    def setHistFolder(self, folder_path):
        if folder_path:
            folder_path = parseFilePath(folder_path)
            cfg.set(NAMES.MAIN_FOLDER_PATH, folder_path)
            self.display_path = folder_path
    
    def getHistFolder(self):
        return self.display_path

    def getDicomName(self):
        return self.dicom_name
    
    def getNiiName(self):
        return self.nii_name

    def setDisplayPath(self, path, mode = NAMES.MAIN_FOLDER_PATH):
        if mode == NAMES.MAIN_FOLDER_PATH:
            self.display_path = path
        elif mode == NAMES.DICOM_NAME:
            self.dicom_name = path
        elif mode == NAMES.NII_NAME:
            self.nii_name = path

    ##
    def parserPaths(self):
        if not os.path.exists(self.display_path):
            signalBus.alertInfo.emit({
                'title':'错误', 'content':f'文件夹不存在: {self.display_path}'
            })
            return []
        cfg.set(NAMES.MAIN_FOLDER_PATH, self.display_path)
        cfg.set(NAMES.DICOM_NAME, self.dicom_name)
        cfg.set(NAMES.NII_NAME, self.nii_name)
        all_names = os.listdir(self.display_path)

        if len(all_names)==0:
            signalBus.alertInfo.emit({
                'title':'错误', 'content':f'文件夹为空: {self.display_path}'
            })
            return []
        
        res = []
        for name in all_names:
            dicom_dir = os.path.join(self.display_path, name, self.dicom_name)
            nii_path = os.path.join(self.display_path, name, self.nii_name)
            if os.path.exists(dicom_dir):
                res.append({
                    'name': name,
                    'dicom_dir': dicom_dir,
                    'nii_path': nii_path,
                    'nii_exist': os.path.exists(nii_path)
                })
        #
        if len(res)==0:
            signalBus.alertInfo.emit({
                'title':'错误', 'content':f'没有找到DICOM子文件夹: {self.dicom_name}'
            })
            return []
        #
        signalBus.alertInfo.emit({
            'title':'更新完成', 'content':f'共找到 {len(res)} 例有效数据',
            'type': 'success'
        })
        return res




PathManager = PATHMANAGER()

