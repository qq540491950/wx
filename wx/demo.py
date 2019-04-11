import itchat
import os
import requests
import json
from aip import AipSpeech
from pydub import AudioSegment
from itchat.content import *

""" 你的 APPID AK SK """
APP_ID = '11265930'
API_KEY = 'kDcOkAPBXP3rBowovA62Xo9Z'
SECRET_KEY = 'cZZVxka161RKgTsxKRw0nsuBjKRZGvIC'
# 机器人接口
url = "http://openapi.tuling123.com/openapi/api/v2"


# 调取机器人接口
def get_resp(msg):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "西安",
                    "province": "陕西",
                    "street": "文艺路"
                }
            }
        },
        "userInfo": {
            "apiKey": "4184322a301a466b9a0aa662854b8714",
            "userId": "lirt"
        }
    }
    data = json.dumps(data)
    res = requests.post(url, data=data)
    return res.json()["results"][0]["values"]["text"]


# MP3转wav
def get_wav(mp3File, wavFile):
    sound = AudioSegment.from_mp3(mp3File)
    sound.export(wavFile, format="wav")


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 调取百度语音API接口
def bai_api(fileName):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    s = client.asr(get_file_content(fileName), 'wav', 16000, {
        'dev_pid': 1536,
    })
    return s


# MsgType
# 文字 Text
# 图片 自定义表情 表情 Picture
# 语音 Recording
# 小视频 Video
# 地址 Map
@itchat.msg_register(msgType=[TEXT, PICTURE, VIDEO, VOICE, RECORDING, MAP])
def get_info(msg):
    # print(msg)
    friend = msg.FromUserName
    if self_userName != friend:
        if msg.Type == 'Text':
            rec_msg = get_resp(msg.Text)
            itchat.send_msg(rec_msg, friend)
            print("\033[1;35m" + msg.User.NickName + "\033[0m" + " 发送文字消息：" + msg.Text)
            print("\033[1;35m自己回复：\033[0m" + rec_msg)
        elif msg.Type == 'Picture':
            print("\033[1;35m" + msg.User.NickName + "\033[0m" + " 发送图片消息")
            itchat.send_image('shuai.jpg', friend)
        elif msg.Type == 'Recording':
            # 下载MP3语音
            msg.Text(msg.FileName)
            # 转换成wav
            wavName = msg.FileName.split('.')[0] + '.wav'
            get_wav(msg.FileName, wavName)
            # 语音识别
            s = bai_api(wavName)
            # 调取机器人
            rec_msg = get_resp(s['result'][0])
            itchat.send_msg(rec_msg, friend)
            print("\033[1;35m" + msg.User.NickName + "\033[0m" + " 发送语音消息，识别出为：" + s['result'][0])
            print("\033[1;35m自己回复：\033[0m" + rec_msg)
            os.remove(msg.FileName)
            os.remove(wavName)


itchat.auto_login(hotReload=True)
self_userName = itchat.web_init()["User"]["UserName"]
# print(self_userName)
itchat.run()
