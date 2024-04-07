from configparser import ConfigParser
from flask import Flask, render_template
from loggs import get_file_logger

'''
发送 html文件以供预览
'''
app = Flask(__name__, template_folder='SourceFolder')


# 视图函数（路由）
@app.route('/SourceFolder/<subject>/<date>/work.html')
def send_file(subject, date):
    get_file_logger.info(f'预览了 <{subject}> 的第 {date} 次作业')
    return render_template(f'{subject}/{date}/work.html')


# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('conf/configs.ini', encoding='utf-8')
    port = cfg.get('preview', 'port')
    app.run(host='0.0.0.0', port=port)