import csv
import datetime
import os
import shutil
import h5py
import numpy as np


def create_dir(folder_name):
    """
    创建文件夹
    :param folder_name:
    :return:
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def recreate_dir(folder_name):
    """
    重建文件夹
    :param folder_name:
    :return:
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        shutil.rmtree(folder_name)
        create_dir(folder_name)


def load_hdf5(in_file_path):
    """
    载入hdf5文件
    :param in_file_path:
    :return:返回该文件
    """
    with h5py.File(in_file_path, "r") as f:
        return f["image"][()]


def write_hdf5(data, out_file_path):
    """
    写入hdf5文件
    :param data:
    :param out_file_path:
    :return:
    """
    with h5py.File(out_file_path, "w") as f:
        f.create_dataset("image", data=data, dtype=data.dtype)


def shuffle_file(img_file_list, label_file_list):
    """
    打乱img和label的文件列表顺序 并返回两列表 seed已固定
    :param img_file_list:
    :param label_file_list:
    :return:
    """
    np.random.seed(10)
    index = [i for i in range(len(img_file_list))]
    np.random.shuffle(index)
    img_file_list = np.array(img_file_list)[index]
    label_file_list = np.array(label_file_list)[index]
    return img_file_list, label_file_list


def distribution_file(dis_img_file_list,
                      dis_label_file_list,
                      dis_img_file_path,
                      dis_label_file_path):
    """
    将img和label从一文件夹转至其他位置
    :param dis_img_file_list:
    :param dis_label_file_list:
    :param dis_img_file_path:
    :param dis_label_file_path:
    :return:
    """
    recreate_dir(dis_img_file_path)
    recreate_dir(dis_label_file_path)
    for img_file, label_file in zip(dis_img_file_list, dis_label_file_list):
        img_name = img_file.split('\\')[-1]
        label_name = label_file.split('\\')[-1]
        shutil.copyfile(img_file, dis_img_file_path + img_name)
        shutil.copyfile(label_file, dis_label_file_path + label_name)
        print(img_file, label_file, dis_img_file_path + img_name, dis_label_file_path + label_name)


def print_cost_time(start_time):
    """
    计算花费时长
    :param start_time:
    :return:
    """
    end_time = datetime.datetime.now()
    print('time:\t' + str(end_time - start_time).split('.')[0])


def onehot_to_class(onehot_predict_list, mask_size=256):
    """
    对以独热码形式的预测转化为数值标签的形式
    :param onehot_predict_list: 这里是一堆预测图
    :param mask_size:
    :return:
    """
    print(onehot_predict_list.shape)
    predict_list = []
    for onehot_predict in onehot_predict_list:
        predict = np.empty(shape=(mask_size, mask_size), dtype=np.uint8)
        for row in range(mask_size):
            for col in range(mask_size):
                onehot_array = onehot_predict[row][col]
                list_onehot_array = onehot_array.tolist()
                max_index = list_onehot_array.index(max(list_onehot_array))  # 返回最大值的索引
                predict[row, col] = max_index
        predict_list.append(predict)

    return predict_list


def onehot(label, num_classes):
    """
    生成该标签的独热码数组
    :param label:
    :param num_classes:
    :return:
    """
    onehot_label = np.eye(num_classes)[label]
    return onehot_label


def get_color():
    """
    返回各值对应颜色
    :return:
    """
    file = csv.reader(open('data/color150.csv', 'r'))
    color_list = np.empty(shape=(151, 3), dtype=np.uint8)
    color_list[0, :] = 0
    index = 1
    for row in file:
        color_list[index, 0] = row[0]
        color_list[index, 1] = row[1]
        color_list[index, 2] = row[2]
        index += 1

    return color_list

