# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 13:24:31 2020

@author: Highhh0
"""     
import tkinter as tk
import keyboard
import pyautogui as pag
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 
import pyperclip
import time


def translate_text():
    try:
        ##########################重要##########################
        cred = credential.Credential("去腾讯云申请翻译接口 得到SecretId填这里", "去腾讯云申请翻译接口 得到SecretKey填这里") 
        ##########################重要##########################
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)  
        req = models.TextTranslateBatchRequest()
        text=pyperclip.paste()    
        text_for_translate_delete_RN=str(text.replace('\r\n',' '))
        params = '{\"Source\":\"auto\",\"Target\":\"zh\",\"ProjectId\":0,\"SourceTextList\":[\"%s\"]}'%text_for_translate_delete_RN
        req.from_json_string(params)
        resp = client.TextTranslateBatch(req) 
        translate_result=resp.to_json_string()
        translate_result=eval(translate_result)  
        translate_result_text=translate_result['TargetTextList']
        return(translate_result_text) 

    
    except TencentCloudSDKException as err: 
        return(err)



class ScreenShot():
        
    def __init__(self, scaling_factor=2):
        x,y = pag.position()
        y=y+20
        self.win = tk.Tk()
        self.win.overrideredirect(True)
        self.win.attributes('-alpha', 0.90)
        self.is_selecting = False
        self.win.wm_attributes('-topmost',1) #窗口置顶      
        self.win.bind('<Button-1>', self.win_exit)
        text_t=translate_text()
        self.win.geometry('+%d+%d'%(x,y)) 
        L1 = tk.Label(self.win, text=text_t,fg='black',wraplength = 590,justify = 'left')
        L1.pack(side='left',padx=5,pady=5) 
        self.win.mainloop()
    def win_exit( self, event=None ):
        self.win.destroy()


root=tk.Tk() 
root.title('By Renne')
root.geometry('450x80+500+500')       
L1 = tk.Label(root, text="快捷键激活使用：Right CTRL",fg='green')
L1.pack(padx=5,pady=5) 
L2 = tk.Label(root, text="说明：选中文本按右CTRL即可翻译,翻译窗口用鼠标左键关闭",fg='black')
L2.pack(padx=5,pady=5) 

def copy_text():
    pag.keyDown('ctrl')
    pag.press('c')
    pag.keyUp('ctrl')

def test(x): 
    if x.event_type == 'down' and x.name == 'right ctrl':
        time.sleep(1)
        copy_text()
        ScreenShot()
        x.event_type =''
        x.name == ''

def on_closing():   
    root.quit()
    root.destroy()  
    
keyboard.hook(test)          
root.protocol("WM_DELETE_WINDOW", on_closing) 
root.mainloop()