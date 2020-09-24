# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:56:25 2020

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
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup  
from collections import Counter
from hashlib import md5
import random
import re


class get_original_text:
    def __init__(self):
        self.text=pyperclip.paste()
    
    def treat_text(self):
        self.text_for_translate_delete_RN=str((self.text.replace('\r\n',' ')).replace('. ','.'))                       
        return(self.text_for_translate_delete_RN)


class translate_or_dictall:
    def __init__(self):
        self.text=get_original_text().treat_text()
       
    def dictall(self):
        url='http://www.dictall.com/dictall/result.jsp'
        data={
                'cd':'UTF-8',
                'keyword': self.text
                }  
        header={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'www.dictall.com',
                'Origin': 'http://www.dictall.com',
                'Pragma': 'no-cache',
                'Proxy-Connection': 'keep-alive',
                'Referer': 'http://www.dictall.com/dictall/result.jsp',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
                }    
        try:
            response=requests.post(url,headers=header,data=data)
            if response.status_code==200:
                result=response.text
                soup = BeautifulSoup(result,'lxml')
                ch_word=str(soup.select('div div[class="cn"]')[0]).replace('<div class="cn">','').replace('</div>','')
                en_word=str(soup.select('div div[class="en"]')[0])
                pattern=re.compile('<span.+span>')
                en_word_result=pattern.findall(en_word)[0].replace('\xa0','').replace('</span>','').replace('<span>1)','')
                ch_sentence=str(soup.select('div div[class="cn_sen"]')[0]).replace('<div class="cn_sen">','').replace('</div>','')
                en_sentence=str(soup.select('div div[class="en_sen"]')[0])
                pattern2=re.compile('<div.+\r')
                en_sen_result=pattern2.findall(en_sentence)[0]
                en_sen_result=re.sub(u"\\<.*?\\>", "", en_sen_result)
                dictalltext=en_word_result+'\n'+ch_word+'\n'+en_sen_result+ch_sentence            
                return(dictalltext)
            else:
                err='post Error'
                return(err)
        except :
            err='dictall Error'
            return(err)

    def translate_text_tencent(self):
        try:
            cred = credential.Credential("xxxxxxxxxxxxxx", "xxxxxxxxxxxxxx") 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)  
            req = models.TextTranslateBatchRequest()
            params = '{\"Source\":\"auto\",\"Target\":\"zh\",\"ProjectId\":0,\"SourceTextList\":[\"%s\"]}'%self.text
            req.from_json_string(params)
            resp = client.TextTranslateBatch(req) 
            translate_result=resp.to_json_string()
            translate_result=eval(translate_result)  
            translate_result_text=translate_result['TargetTextList']
            text_t='腾讯翻译:'+'\n'+str(translate_result_text[0])
            return(text_t) 
        except TencentCloudSDKException as err: 
            return(err)

    def translate_text_youdao(self):
        appVersion="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        bv = md5(appVersion.encode('utf8')).hexdigest()  #bv 浏览器版本加密数据       
        ts = str(int(time.time()*1000)) #时间戳数据   
        salt= ts+ str(random.randint(0,10))
        sign=md5(("fanyideskweb" + self.text + salt + "]BjuETDhU)zqSxf-=B#7m").encode('utf8')).hexdigest()
        
        url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '3800',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': '_ntes_nnid=d8da66ca04a16cf931aa87990ae7c066,1571377848792; OUTFOX_SEARCH_USER_ID_NCOO=1892923083.7334616; OUTFOX_SEARCH_USER_ID=1687777490@221.7.47.136; _ga=GA1.2.1026858432.1597390896; UM_distinctid=173fc19d1a440c-0cc29ea85b5ed9-3323767-144000-173fc19d1a5da; JSESSIONID=aaat0D9qO39Sgg3LhJKqx; ___rl__test__cookies=1598341265239',
                'Host': 'fanyi.youdao.com',
                'Origin': 'http://fanyi.youdao.com',
                'Pragma': 'no-cache',
                'Referer': 'http://fanyi.youdao.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
        data={
                'i': self.text,
                'from': 'AUTO',
                'to': 'AUTO',
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': salt,
                'sign': sign,
                'lts': ts,
                'bv': bv,
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_CLICKBUTTION'
                }  
        try:    
            response=requests.post(url,headers=headers,data=data)
            if response.status_code==200:
                result=response.json()
                result_all=''
                for i in range(len(result['translateResult'][0])):
                    translateResult=(result['translateResult'][0][i]['tgt'])
                    result_all=result_all+translateResult
                text_t='有道翻译:'+'\n'+result_all
                return text_t
        except RequestException:
            print('请求索引页出错')
            return None

    def translate_text_ciba(self):
        url='http://fy.iciba.com/ajax.php?a=fy'
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Content-Length': '283',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'UM_distinctid=1740bb30ea2b5-0c74d064dc54aa-3323767-144000-1740bb30ea39c5; BAIDU_SSP_lcr=https://www.baidu.com/s?wd=%E9%87%91%E5%B1%B1%E8%AF%8D%E9%9C%B8&rsv_spt=1&rsv_iqid=0xe9dd9ce5000018eb&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=11&rsv_sug1=11&rsv_sug7=100',
                'Origin': 'http://fy.iciba.com',
                'Pragma': 'no-cache',
                'Proxy-Connection': 'keep-alive',
                'Referer': 'http://fy.iciba.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
        data={
                'f': 'auto',
                't': 'auto',
                'w': self.text
                }  
        
        try:    
            response=requests.post(url,headers=headers,data=data)
            if response.status_code==200:
                result=response.json()['content']['out']
                text_t='金山翻译:'+'\n'+(result.replace(' ',''))
                return(text_t)
            return None
        except RequestException:
            print('请求索引页出错')
            return None
################################################################################################################
class text_win():      
    def __init__(self):
        global selectmethod
        x,y = pag.position()
        x=x-50
        y=y+20
        self.win = tk.Tk()
        self.win.overrideredirect(True)
        self.win.attributes('-alpha', 1)
        self.is_selecting = False
        self.win.wm_attributes('-topmost',1) #窗口置顶      
        self.win.bind('<Button-1>', self.win_exit)
        res_counter = Counter(get_original_text().treat_text())
        if res_counter[' '] <=2:
            text_t=translate_or_dictall().dictall()
        elif res_counter[' '] >2 and selectmethod == 'Tencentcloud':
            text_t=translate_or_dictall().translate_text_tencent()
        elif res_counter[' '] >2 and selectmethod == 'Youdao':
            text_t=translate_or_dictall().translate_text_youdao()
        elif res_counter[' '] >2 and selectmethod == 'ciba':
            text_t=translate_or_dictall().translate_text_ciba()
        else:
            text_t='err'        
        self.win.geometry('+%d+%d'%(x,y)) 
        L1 = tk.Label(self.win, text=text_t,fg='black',wraplength = 600,justify = 'left',font=("微软雅黑", 12))
        L1.pack(side='left',padx=5,pady=5) 
        self.win.mainloop()
    def win_exit( self, event=None ):
        self.win.destroy()
        
        
        
        
def print_content1():
    global selectmethod
    global var
    var.set('Tencentcloud')
    selectmethod='Tencentcloud'
def print_content2():
    global selectmethod
    global var
    var.set('Youdao')
    selectmethod='Youdao'
def print_content3():
    global selectmethod
    global var
    var.set('ciba')
    selectmethod='ciba'

def copy_text():
    pag.keyDown('ctrl')
    pag.press('c')
    pag.keyUp('ctrl')
    
def text_hotkey(x): 
    if x.event_type == 'down' and x.name == 'right ctrl':
        time.sleep(1)
        copy_text()
        text_win()
        x.event_type =''
        x.name == ''
                
def shift_hotkey(x):
    global selectmethod
    if x.event_type == 'down' and x.name == 'right shift':
        if selectmethod == 'Tencentcloud':
            print_content2()
            x.event_type =''
            x.name == ''
        elif selectmethod == 'Youdao':
            print_content3()
            x.event_type =''
            x.name == ''
        elif selectmethod == 'ciba':
            print_content1()
            x.event_type =''
            x.name == ''  

def on_closing():
    mainwin.quit()
    mainwin.destroy()

if __name__ == '__main__':
    selectmethod='Tencentcloud'
    mainwin=tk.Tk() 
    mainwin.title('By Renne')
    mainwin.geometry('450x300+550+400')                          
    L2 = tk.Label(mainwin, text="说明：选中文本按右ctrl即可翻译,翻译窗口用鼠标左键关闭 \n 使用按钮或者按下右shift可切换翻译\n 当文本小于等于三个单词时，启用dictall查词",fg='green')
    L2.pack(padx=5,pady=5)
    L3 = tk.Label(mainwin, text="可选择翻译：",fg='black')
    L3.pack(padx=5,pady=5)
    tk.Button(mainwin,text="Tencentcloud",command=print_content1).pack()
    tk.Button(mainwin,text="Youdao",command=print_content2).pack(padx=5,pady=5)
    tk.Button(mainwin,text="ciba",command=print_content3).pack(padx=5,pady=5)               
    L4 = tk.Label(mainwin, text="当前选择的翻译为：",fg='black')
    L4.pack()
    var = tk.StringVar(value='Tencentcloud')
    text_output = tk.Message(mainwin,textvariable=var,width=100) # 将textvariable设为var
    text_output.pack()
    keyboard.hook(text_hotkey) 
    keyboard.hook(shift_hotkey) 
    mainwin.protocol("WM_DELETE_WINDOW", on_closing)   
    mainwin.mainloop()