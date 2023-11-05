import requests
import paho.mqtt.client as mqtt
import base64
import hmac
import time
from urllib.parse import quote

class get():
    def __init__(self) -> None:
        # 产品、设备参数
        ## OneNET使用TCP方式连接时的主机地址
        self.BrokerHost = '183.230.40.39'
        ## OneNET使用TCP方式连接时的主机端口号
        self.BrokerPort = 6002
        ## 设备ID
        self.DeviceId = '1133749763'
        ## 产品ID
        self.ProductId = '614494'
        ## 可以是设备单独的APIKey，也可以是产品的MasterAPIKey
        self.APIKey = "GVCm0ksST2aYVnR4pOA2Qi00T1o="
        ## 设备key
        self.access_key = 'pIz1vWzB8MWYda0x42XmybRpLIt9bcKLSleaWdTQ2v0='
        ## 获取数据点
        self.download_url = "http://api.heclouds.com/devices/1133749763/datastreams/RTK"
        ## 上传数据点
        self.upload_url = "http://api.heclouds.com/devices/1133749763/datapoints"
        ## LBS基站定位
        self.LBS_url = "http://api.heclouds.com/devices/1133749763/lbs/latestLocation"

        # 设置请求头
        self.headers = {
            "Authorization": self.token(self.ProductId, self.access_key)
        }

        self.latitude = 0
        self.longitude = 0
    
    def run(self):
        try:
            response = requests.get(self.download_url, headers=self.headers)
            self.latitude = response.json()["data"]["current_value"]["latitude"]
            self.longitude = response.json()["data"]["current_value"]["longitude"]
            return self.longitude,self.latitude
        except requests.exceptions.RequestException as e:
            return self.longitude,self.latitude

    # 获取鉴权信息token
    def token(self, id, access_key):
        version = '2018-10-31'

        res = 'products/%s' % id  # 通过产品ID访问产品API

        # 用户自定义token过期时间
        et = str(int(time.time()) + 3600)

        # 签名方法，支持md5、sha1、sha256
        method = 'sha1'

        # 对access_key进行decode
        key = base64.b64decode(access_key)

        # 计算sign
        org = et + '\n' + method + '\n' + res + '\n' + version
        sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
        sign = base64.b64encode(sign_b.digest()).decode()

        # value 部分进行url编码，method/res/version值较为简单无需编码
        sign = quote(sign, safe='')
        res = quote(res, safe='')

        # token参数拼接
        token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)

        return token

    # 连接结果
    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print("连接失败:" + mqtt.connack_string(rc))
            return
        print("连接成功")