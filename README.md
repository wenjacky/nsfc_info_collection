
**国家自然科学基金自动分析程序**

本自动分析程序的主要功能是从国家自然科学基金网站上自动根据预置的条件显示基金的信息并保存成文件。更多资讯请访问[我的主页](https://cskxie.github.io)

# 配置文件说明
* year.config 查询年份的配置文件，不能空
* keyword.config 关键词的配置文件，可为空
* subject.config 申请代码的配置文件，不能空
* grant.config 资助类别的配置文件，不能空
* done.config 保存当前运行的位置，当程序异常退出，再次执行时自动从上次退出的位置运行，初始值为0
* result.txt 保存结果的文件,每次都是在文件末尾写入新的结果。每次查询结束的结果需要手动删除。

上述配置文件都是每行一个值，**注意文件末尾不要留空行**
 

# 运行
    在命令行下，执行 python auto_search.py

# 依赖环境
* [python 3.6.5](https://www.python.org/downloads/)，在2.x的环境中有些unicode字符编码的问题
* 安装PIP： sudo apt-get install python-pip python-dev
* 开源的OCR图片识别[tesseract](https://github.com/tesseract-ocr/tesseract)
* Pillow, [基本安装方法](https://pillow.readthedocs.io/en/5.1.x/)
* 安装[pytesseract](https://github.com/madmaze/pytesseract)
* 安装[selenium](https://pypi.org/project/selenium/)
* 安装selenium的webdriver驱动Firefox的驱动程序[geckodriver](https://github.com/mozilla/geckodriver/releases)，本程序仅支持Firefox. 

    **注意依赖环境请根据操作系统版本选择对应的安装包和安装方法**，目前在[Ubuntu 18.04 LTS](https://www.ubuntu.com/download/desktop)和macOS High Sierra上测试通过。其他系统没有进行过测试，请一定确保依赖环境配置正确。

