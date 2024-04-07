import os
from configparser import ConfigParser
import shutil

'''
将所有作业文件夹拷贝到指定文件夹的脚本
'''


def copytree(subjects_map, folder_location):
    '''
    :param subjects_map: 科目与英文的映射
    :param folder_location: 指定文件夹
    '''
    for work in subjects_map.keys():
        print(f'{work} 拷贝完毕!')
        src = folder_location + f'/{work}/works'
        dst = f'SourceFolder/{subjects_map[work]}'
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copytree(src, dst, symlinks=False, ignore=shutil.ignore_patterns('.*', '_*'),
                        copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=True)


if __name__ == '__main__':
    cfp = ConfigParser()
    cfp.read('conf/configs.ini', encoding='utf-8')
    # 读取配置
    subjects_map = dict(cfp.items('subjects'))
    folder_location = cfp.get('folder', 'location')
    copytree(subjects_map, folder_location)
    print('所有文件夹拷贝完成！！！')
