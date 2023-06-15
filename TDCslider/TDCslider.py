import json
import cv2
import requests
import random
import execjs

img_bg =  './img/'+'1.png'
img_slider=  './img/'+'0.png'
#img_rect=  './img/'+'2.png'
sliderfactor = 0.4166666666666667
list_crtJs = []
#def loadJs(js):
 #   with open(js, 'r', encoding='utf-8') as f:
 #       js_code = f.read()
  #  list_crtJs.append(execjs.get().compile(js_code))
def setMidText(text,leftText,rightText,writeText):
    idx1 = text.index(leftText)
    idx2 = text.index(rightText)
    newText = text[0:idx1] + writeText +text[idx2:-1]
    return  newText
def getMidText(text,leftText,rightText,leftgap=0):
    idx1 = text.index(leftText)
    idx2 = text.index(rightText)
    return text[idx1+leftgap:idx2]
def getSliderImg(img_url,imgpath):
    img_url = "https://t.captcha.qq.com" + img_url
    res = requests.get(url=img_url)
    img_data = res.content
    with open(imgpath,'wb') as fp:
        fp.write(img_data)

def getRandomNum(num):
    timesample = ''.join(random.choice("0123456789") for i in range(num))
    return timesample

def getSliderX(bgPic,sliderPic):
    img_slider = cv2.imread(sliderPic)
    img_bg = cv2.imread(bgPic)
    cropped = img_slider[slider_pos[1]:slider_pos[1] + slider_pixel[1], slider_pos[0]:slider_pos[0] + slider_pixel[0]]
    srcCropped = img_bg[init_pos[1]:init_pos[1] + slider_pixel[1], 0:img_bg.shape[1]]
    res = cv2.matchTemplate(srcCropped, cropped, cv2.TM_CCOEFF_NORMED)
    min_Val, max_Val, min_Loc, max_Loc = cv2.minMaxLoc(res)
    top_left = max_Loc
    cv2.rectangle(srcCropped, top_left, (top_left[0] + slider_pixel[1], top_left[1] + slider_pixel[0])
                  , (0, 0, 255), 3)
    cv2.imshow('srcCropped',srcCropped)
    cv2.waitKey(0)
    return top_left[0]

def getSliderValue(X):
    sliderSum = X*0.75
    sliderSum = int(sliderSum)
    listValue = []
    listValue.append([3,sliderSum, 20])
    while sliderSum < X:
        i = 0
        if int(getRandomNum(1)) <2:
            i=i-int(getRandomNum(1))
            listValue.append([int(getRandomNum(1)),i,int(getRandomNum(1))])
        else:
            i = i + int(getRandomNum(1))
            listValue.append([int(getRandomNum(1)), i, int(getRandomNum(1))])
        sliderSum = sliderSum+i
    return listValue

uin = "819456221"#QQ号
pwd = "M1321313"#密码
verifycode = ''
ticket = ''
url0 = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=716027609&daid=383&style=33&login_text=%E7%99%BB%E5%BD%95&hide_title_bar=1&hide_border=1&target=self&s_url=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Flogin_jump&pt_3rd_aid=102013353&pt_feedback_link=https%3A%2F%2Fsupport.qq.com%2Fproducts%2F77942%3FcustomInfo%3D.appid102013353&theme=10&verify_theme="
text = requests.get(url=url0)
resCookies = requests.utils.dict_from_cookiejar(text.cookies)
pt_login_sig = resCookies['pt_login_sig']
url  = "https://ssl.ptlogin2.qq.com/check?regmaster=&pt_tea=2&pt_vcode=1&uin="+uin+"&appid=716027609&js_ver=23061410&js_type=1&login_sig="+pt_login_sig+"&u1=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Flogin_jump&r=0."+getRandomNum(16)+"&pt_uistyle=40&daid=383&pt_3rd_aid=102013353&o1vId=d1a82827a846e0222b6dec734b181960&pt_js_version=v1.45.1"
res = requests.get(url)
sliderChecktext = getMidText(res.text,"','","','\\x", len("','"))
ptdrvs = getMidText(res.text,"'2','","')", len("'2','"))
idx = ptdrvs.index("','")
sid = ptdrvs[idx+3:]
ptdrvs = ptdrvs[:idx]
if(len(sliderChecktext) != 4 ):
    url = "https://t.captcha.qq.com/cap_union_prehandle?aid=716027609&protocol=https&accver=1&showtype=embed&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84Ni4wLjQyNDAuMTk4IFNhZmFyaS81MzcuMzY%3D&noheader=1&fb=1&aged=0&enableAged=1&enableDarkMode=0&sid=1260580354830987861&grayscale=1&clientype=2&cap_cd=&uid=&lang=zh-cn&entry_url=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Flogin_jump&elder_captcha=0&js=%2Ftcaptcha-frame.12921619.js&login_appid=&wb=2&subsid=1&callback=_aq_" + getRandomNum(
        6) + "&sess="
    res = requests.get(url)
    res = getMidText(res.text, "(", ")", 1)
    res = json.loads(res)
    sess = res['sess']
    img_url = res['data']['dyn_show_info']['bg_elem_cfg']['img_url']
    init_pos = res['data']['dyn_show_info']['fg_elem_list'][1]['init_pos']
    slider_pos = res['data']['dyn_show_info']['fg_elem_list'][1]['sprite_pos']
    slider_pixel = res['data']['dyn_show_info']['fg_elem_list'][1]['size_2d']
    getSliderImg(img_url,img_bg)
    getSliderImg(setMidText(img_url,"img_index","&image","img_index=0"),img_slider)
    X = getSliderX(img_bg,img_slider)
    listValue =  getSliderValue(int((X - init_pos[0])*sliderfactor))
    text = '{"cd":[24,"https://graph.qq.com/oauth2.0/login_jump","iframe",["zh-CN","zh"],[300,230],"https://captcha.gtimg.com/1/template/drag_ele.html?rand=1519713624347","Google Inc.",[],1536,"","GgoAAAANSUhEUgAAASwAAACWCAYAAAAVfRkrjqcq6KB3gOI94mc0xLyzpzr9D/AMAMnw/ifFbyAAAAAElFTkSuQmCC","Win32",2,0,"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",511,  [[103,173,27],[0,-1,55],[0,-1,30],[-1,0,290],[-1,0,2],[0,1,2],[-1,0,1],[0,1,1],[-1,0,1],[-1,0,5],[0,1,0],[-1,0,1],[-1,0,2],[-1,0,0],[0,1,1],[-1,1,1],[-1,0,1],[-1,1,1],[-1,0,1],[-1,0,2],[-2,0,1],[-1,1,1],[0,1,1],[-2,0,1],[-1,1,1],[-1,0,1],[-2,1,1],[-1,0,1],[-2,1,1],[-2,2,0],[-1,0,1],[-2,1,2],[-2,1,1],[-2,0,1],[-2,1,1],[-3,1,1],[-2,1,1],[-3,0,1],[-3,2,0],[-2,1,2],[-2,1,1],[-5,1,1],[-3,2,1],[-1,1,2],[-5,0,0],[-3,2,1],[-4,2,1],[-5,0,1],[-4,3,1],[-5,1,1],[-5,1,1],[-4,2,2],[-5,1,1],[22,-79,3856],[0,0,3],[4,3,2],[1,0,6],[1,0,62],[0,1,1],[0,1,5],[1,1,12]]                       ,0,0,"+08","98k",0,"ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)",1686748684,1923646086,10,1,"",1686748678,8,1,864,746952190,1686152394,"183.230.242.239","UTF-8","1536-864-816-24-*-*-|-*",0],          "sd":{"od":"C","ft":"qf_7P___H"}}'
    text =  setMidText(text,'[[103,173,27]','[0,1,5]',str(listValue))
    with open('tdc_slider.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    ctx = execjs.get().compile(js_code)
    result = ctx.call('encodeTDCslider',text)
    print(len(result))
    data={
        "collect":result,
        "tlg":len(result),
        "eks":'anq02VYo1jlGLLkh+Ph5IUgMfaCn+KsmF7AXeGksaMqQEIlWQxXGv6LKDlGtrmMZ5j0r9DPZQIqmQVdUhMqY0Pcv1jMlhu2SWFYGxMka+0pW4oYGTvAmUdsps6983JDB6AXXpLucwdlgFPvpUZMdQCkgU4fGic50kyaW93rt0N+UZsShmrUn9UAcN0HKfgy4SuX8uY70tNtRe1UXwbqwdIPyoPg/z/RWnDBDltQN2Qo=',
        "sess":sess,
        "ans":'[{"elem_id":1,"type":"DynAnswerType_POS","data":"'+str(X )+','+str(init_pos[1])+'"}]',
        "pow_answer":"967a3a2b8b1b78f7#1565",
        "pow_calc_time":"49"
    }
    print(data)
    res = requests.post("https://t.captcha.qq.com/cap_union_new_verify",data=data)
    res = json.loads(res.text)
    print(res)
    verifycode = res['randstr']
    ticket = res['ticket']

else:
    verifycode = sliderChecktext
    ticket = getMidText(res.text,"','","','2'", len("','"))
    idx = ticket.index("','")
    ticket = ticket[idx+3:]
    idx = ticket.index("','")
    ticket = ticket[idx + 3:]

with open('QQrsa.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.get().compile(js_code)
result = ctx.call('$.Encryption.getEncryption',pwd,uin,verifycode,'')
url = "https://ssl.ptlogin2.qq.com/login?u="+uin+"&verifycode="+verifycode+"&pt_vcode_v1=1&pt_verifysession_v1="+ticket+"&p="+result+"&pt_randsalt=2&u1=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Flogin_jump&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=2-2-1686749762403&js_ver=23061410&js_type=1&login_sig="+pt_login_sig+"&pt_uistyle=40&aid=716027609&daid=383&pt_3rd_aid=102013353&ptdrvs="+ptdrvs+"&sid="+sid+"&&o1vId=d1a82827a846e0222b6dec734b181960&pt_js_version=v1.45.1"
res = requests.get(url)

loginCheck = res.text.find("'登录成功！', '")
if(loginCheck != -1):
    print("登录成功，用户名为",res.text[loginCheck+len("'登录成功！', '"):])
else:
    print(res.text)









