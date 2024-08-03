from flask import Flask, request, make_response
import hashlib
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    token = '83_3AQ5fFylIoYp0A_eysbsjXpbzIn-Du2gMlEX4EI4ylCNbzZRJnzkue6H7_P69-vGn1c15HuEtX3_1T2GMkCk0kutKHapU2WaGTqp33PV7X-nfAg8tdS-rJEt130AXGhAAALIR'  # 设置自己的Token，确保和微信公众平台上的Token一致

    if request.method == 'GET':
        # 获取请求的参数
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        # 验证签名
        s = ''.join(sorted([token, timestamp, nonce]))
        if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
            return echostr
        else:
            return 'Unauthorized', 401

    elif request.method == 'POST':
        # 接收微信服务器发送的POST数据（XML格式）
        xml = request.data
        event = parse_event(xml)

        # 判断是否是关注事件
        if event['Event'] == 'subscribe':
            scene_id = event['EventKey'].replace('qrscene_', '')
            response_message = get_response_message(scene_id, event)
            return make_response(response_message)
        
        # 判断是否是已关注用户的二维码扫描事件
        elif event['Event'] == 'SCAN':
            scene_id = event['EventKey']
            response_message = get_response_message(scene_id, event)
            return make_response(response_message)

        return 'success'

def parse_event(xml):
    """
    解析XML数据，提取事件信息
    """
    root = ET.fromstring(xml)
    event = {child.tag: child.text for child in root}
    return event

def get_response_message(scene_id, event):
    """
    根据场景ID返回相应的图文消息
    """
    messages = {
        '1001': '图文消息1的内容',  # 场景一对应的图文消息内容
        '1002': '图文消息2的内容',  # 场景二对应的图文消息内容
        # 可以为其他场景设置不同的消息内容
    }
    # 构建XML格式的响应消息
    response_template = '''<xml>
    <ToUserName><![CDATA[{0}]]></ToUserName>
    <FromUserName><![CDATA[{1}]]></FromUserName>
    <CreateTime>{2}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{3}]]></Content>
    </xml>'''
    content = messages.get(scene_id, '默认消息内容')  # 获取对应场景的消息内容
    # 格式化返回消息
    return response_template.format(event['FromUserName'], event['ToUserName'], int(time.time()), content)

if __name__ == '__main__':
    app.run(port=80)  # 启动Flask服务器，监听80端口
