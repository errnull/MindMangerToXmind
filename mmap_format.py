from xml.dom import minidom
import xml.etree.ElementTree as ET
import zipfile
import tkinter as tk
from tkinter.messagebox import showinfo
import windnd
import os
import urllib.request
import time
import random

color_dic = {"#B2B2FE": "purple",
             "#ADD2FF": "blue",
             "#FFFFAA": "",
             "#BEFFBE": "green",
             "#ADD2FF": "blue",
             "#FFAABE": "red",
             "#FFFF00": "yellow",
             "#00FF00": "green",
             "#00BEFF": "blue",
             "#FF0000": "red",
             "#FF8000": "yellow",
             "#008040": "green",
             "#003EB3": "blue",
             "#CF1B11": "red",
             "#7F7F7F": "",
             "#DADADA": "",
             "#B4B4B4": "",
             "#C39DE0": "purple"}


dir_name = None
is_root = True
namespaces = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def mm_format(mm_fpath):
    global dir_name, is_root
    is_root = True
    try:
        dir_name = path + "/mmformat" + str(int(time.time()))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        z = zipfile.ZipFile(mm_fpath, "r")
        content = z.read("Document.xml").decode('UTF-8')
        root = ET.fromstring(content)
        OneTopic = root.find('ap:OneTopic', namespaces).find(
            'ap:Topic', namespaces)
        new_root = ET.Element('map')
        buildTree(OneTopic, new_root)
        xmlstr = minidom.parseString(ET.tostring(new_root, 'utf-8')).toprettyxml(indent="   ")
        with open(dir_name + '/res.mm', "w", encoding='utf-8') as f:
            f.write(xmlstr)
        return True
    except Exception as e:
        print(e)
        return False


def buildTree(root, new_root):
    node = ET.SubElement(new_root, 'node')
    global is_root
    if is_root:
        is_root = False
        node.set('ID', 'root')
    else:
        node.set('ID', genId())

    node.set('STYLE', 'FORK')
    text = ""
    color = "#FFFFAA"
    if root.find("ap:Color", namespaces) != None:
        color = root.find("ap:Color", namespaces).attrib['FillColor']
        color = "#" + color[2:].upper()
    if root.find("ap:Text", namespaces) != None:
        text = root.find("ap:Text", namespaces).attrib['PlainText']
        # if text[-1] == '。':
        #     text = text[:-1]
        node.set('TEXT', text)

    span_class = color_span =  ""
    if color in color_dic:
        color_span = color_dic[color]
    if color_span != "":
        span_class = "class=\" text-color-" + color_span + "\""
    mubu_text = urllib.parse.quote("<span " + span_class + " >" + text + "</span>", safe="=/,+:")
    node.set('_mubu_text', mubu_text)
    
    if root.find("ap:SubTopics", namespaces):
        for t in root.find("ap:SubTopics", namespaces).findall("ap:Topic", namespaces):
            buildTree(t, node)
            
    return

def genWord(l):
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
           'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    str = ""

    for i in range(l):
        index = random.randint(0, len(arr) - 1)
        str += arr[index]

    return str


def genId():
    return genWord(8) + '-' + genWord(4) + '-' + genWord(4) + '-' + genWord(4) + '-' + genWord(12)


ori = res = path = None


def dragged_files(files):
    global ori, res, path
    ori = str(files[0].decode('gbk'))
    (file, ext) = os.path.splitext(ori)
    if ext != '.mmap':
        showinfo("错误", "格式不正确")
        return
    (path, filename) = os.path.split(ori)
    # res = file + "format" + str(int(time.time())) + ".mm"
    st_defalut()
    entry1.delete(0, "end")
    entry1.insert(0, ori)
    # entry2.delete(0, "end")
    # entry2.insert(0, res)


entry1 = entry2 = st = b = None


def st_defalut():
    st.config(text='还未转换')
    st.config(fg="#0000CD")


def st_process():
    st.config(text='正在转换')
    st.config(fg="#DA70D6")


def st_error():
    st.config(text='转换失败')
    st.config(fg="#DC143C")


def st_success():
    st.config(text='转换成功')
    st.config(fg="#228B22")


def init_tk():
    global entry1, entry2, st
    rootWindow = tk.Tk()
    rootWindow.title('Mmap转幕布')
    width = 380
    height = 80
    screenwidth = rootWindow.winfo_screenwidth()
    screenheight = rootWindow.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height,
                                (screenwidth-width)/2, (screenheight-height)/2)
    rootWindow.geometry(size_geo)
    rootWindow.resizable(0, 0)
    tk.Label(rootWindow, text="原文件位置").grid(row=0, sticky='w')
    tk.Label(rootWindow, text="").grid(row=1, sticky='w')
    entry1 = tk.Entry(rootWindow)
    entry1.insert(0, "请将文件拖到此处")
    entry1.grid(row=0, column=1, padx=8, ipadx=50)
    # entry2 = tk.Entry(rootWindow)
    # entry2.grid(row=1, column=1, padx=8, ipadx=50)
    windnd.hook_dropfiles(entry1, func=dragged_files)
    st = tk.Label(rootWindow, text="还未转换", fg='#0000CD')
    st.grid(row=2, sticky='w')
    b = tk.Button(rootWindow, text="开始转换", command=format_main)
    b.grid(row=2, column=1, sticky='e')
    rootWindow.mainloop()


def format_main():
    st_process()
    if mm_format(ori):
        st_success()
    else:
        st_error()
    return

if __name__ == '__main__':
    init_tk()
    # mm_format('a.mmap')
