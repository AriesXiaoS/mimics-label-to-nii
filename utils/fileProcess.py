
import SimpleITK as sitk
import numpy as np



def loadDcm(dcm_dir):
    series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(dcm_dir)
    series_file_names = [sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dcm_dir, seriesID) for seriesID in series_IDs]
    series_file_names_lengths = [len(series_file_name) for series_file_name in series_file_names]
    max_index = np.argmax(series_file_names_lengths)
    target_file_names = series_file_names[max_index]

    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(target_file_names)
    reader.LoadPrivateTagsOn()
    reader.MetaDataDictionaryArrayUpdateOn()
    image = reader.Execute()
    image_arr = sitk.GetArrayFromImage(image)
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    direction = image.GetDirection()
    return image_arr, spacing, origin, direction














