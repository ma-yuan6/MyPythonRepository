import os
import json
from configparser import ConfigParser
import yagmail
import streamlit as st
from streamlit_lottie import st_lottie
from loggs import get_file_logger, without_file_logger, upload_file_logger


# 主要访问页面


@st.cache_resource
def get_config(section, file_location='conf/configs.ini'):
    '''
    :param file_location: 配置文件位置
    :param section: 配置项, subjects -> 科目 preview -> 预览文件网址
    :return: 配置项
    '''
    cfp = ConfigParser()
    cfp.read(file_location, encoding='utf-8')
    if section == 'preview':
        settings = cfp.get('preview', 'url') + ':' + cfp.get('preview', 'port')
    elif section == 'subjects':
        settings = dict(cfp.items(section))
    else:
        settings = dict(cfp.items(section))
    return settings


# 获取 html文件或者源代码
@st.cache_resource
def convert_df(subject, date, file_type):
    '''
    :param subject: 科目
    :param date: 第几次作业
    :param file_type: 文件类型 "html" 或者 "source"
    :return: 二进制文件
    '''
    folder_path = f'SourceFolder/{subject}/{date}'
    file_name = subject + '-' + date + '-'

    if file_type == 'html':
        file_path = folder_path + '/work.html'
        file_name = file_name + 'work.html'
    else:
        for fi in os.listdir(folder_path):
            if not fi.endswith('html'):
                file_path = folder_path + '/' + fi
                file_name = file_name + fi
    with open(file_path, 'r', encoding='utf-8') as f:
        file = f.read()
    return file_name, file


# 将数字前面用 0 补齐以匹配文件夹
def int2str(num):
    if num < 10:
        return '0' + str(num)
    else:
        return str()


st.header('资料分享与交流📄', divider='rainbow')
st.write('')
with open('car-loading2-data.json', 'r', encoding='utf-8') as f:
    animation_json = f.read()

# 获取和预览文件模块
subjects_map = get_config('subjects')
anim, setings = st.columns(2)
with anim:
    lottie_json = json.loads(animation_json)
    st_lottie(lottie_json, quality="high", height=400, speed=0.5)
with setings:
    st.subheader('参数设置')
    option = st.selectbox('在这里选择科目', options=subjects_map.keys(), label_visibility='collapsed', index=None,
                          placeholder='在这里选择科目')
    st.write()
    date = st.number_input('你需要第几次作业的资料 ？', min_value=1, max_value=14, step=1)
    date = int2str(date)
    if not option:
        st.warning('请选择科目！')
        st.stop()
    subject = subjects_map[option]
    st.write('')

    if not os.path.exists(f'SourceFolder/{subject}/{date}/work.html'):
        st.warning('暂时还没有此文件哟！')


        def without_file_log():
            without_file_logger.warning(f'希望要 <{option}> 的第 {date} 次作业')
            st.toast('正在加紧赶制中...')


        _, reminder_btn = st.columns(2)
        with reminder_btn:
            st.button(label='点击这里催一下', on_click=without_file_log, use_container_width=True)


    else:
        preview_url = get_config('preview')
        _, link = st.columns(2)  # 将按钮挤到右边
        with link:
            url = preview_url + f'/SourceFolder/{subject}/{date}/work.html'
            st.link_button('点击这里预览文件', url, use_container_width=True)
            # st.markdown(f'''<a href="{url}"><button style="background-color: greenyellow; font-size: 16px;padding: 10px 30px;
            #             border: none; border-radius: 6px; cursor: pointer;">点击预览文件</button></a>''',
            #             unsafe_allow_html=True)
        st.write('')

        btn1, btn2 = st.columns(2, gap='large')
        with btn1:
            def log_download_source():
                get_file_logger.info(f'下载了 <{option}> 的第 {date} 次源代码')


            source_file_name, source_file = convert_df(subject, date, 'source')
            st.download_button(label='下载源代码', data=source_file, file_name=source_file_name,
                               mime='application/octet-stream', use_container_width=True,
                               on_click=log_download_source)
        with btn2:
            def log_download_html():
                get_file_logger.info(f'下载了 <{option}> 的第 {date} 次 HTML 文件')


            html_file_name, html_file = convert_df(subject, date, 'html')
            st.download_button(label='下载 HTML 文件', data=html_file, file_name=html_file_name,
                               mime='application/octet-stream', use_container_width=True,
                               on_click=log_download_html)

# 上传文件模块
st.header('你可以在这里分享你的资料', divider='rainbow')
st.write('')
option_upload = st.selectbox('选择科目', options=subjects_map.keys(), label_visibility='collapsed', index=None,
                             placeholder='选择科目')
st.write('')
date_upload = st.number_input('你要上传第几次的作业', min_value=1, max_value=12, step=1)
date_upload = int2str(date_upload)
st.write('')
name = st.text_input('你的名字是')
st.write('')
if option_upload and date_upload and name:
    subject_upload = subjects_map[option_upload]
    uploaded_file = st.file_uploader("Choose a SourceFolder", label_visibility='collapsed')
    if uploaded_file is not None:
        upload_file_logger.warning(f'有人上传了 <{option_upload}> 的第 {date_upload} 次作业')
        # 获取上传的文件
        bytes_data = uploaded_file.getvalue()
        uploaded_file_name = uploaded_file.name
        # 拼接文件名
        upload_file_name = name + '-' + subject_upload + '-' + date_upload + '-' + uploaded_file_name
        # 保存文件
        with open('Upload/' + upload_file_name, 'wb') as f:
            f.write(bytes_data)
        st.toast('文件上传成功')

        # 发送邮件提醒有人上传文件了
        mail_dic = get_config('mail')
        received = [mail_dic['user']]
        yag = yagmail.SMTP(user=mail_dic['user'], password=mail_dic['password'],
                           host=mail_dic['host'])
        contents = [
            f'<b> <font color="#FF1493" size="10">有人上传 {option_upload} 的第 {date_upload} 次作业啦!!! </font> </b>']
        yag.send(received, '有人上传作业啦!', contents)
        yag.close()

else:
    st.warning('请填完完整信息！')
