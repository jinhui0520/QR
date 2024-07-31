from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        token = 'your_token'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        return echostr

    if request.method == 'POST':
        xml_str = request.data
        xml = ET.fromstring(xml_str)
        msg_type = xml.find('MsgType').text
        event = xml.find('Event').text
        event_key = xml.find('EventKey').text

        if msg_type == 'event' and event == 'subscribe':
            if event_key == 'qrscene_scene_1':
                media_id = 'MEDIA_ID_1'
            elif event_key == 'qrscene_scene_2':
                media_id = 'MEDIA_ID_2'
            else:
                media_id = 'DEFAULT_MEDIA_ID'

            response_xml = f"""
                <xml>
                    <ToUserName><![CDATA[{xml.find('FromUserName').text}]]></ToUserName>
                    <FromUserName><![CDATA[{xml.find('ToUserName').text}]]></FromUserName>
                    <CreateTime>{int(time.time())}</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                        <item>
                            <Title><![CDATA[图文消息标题]]></Title>
                            <Description><![CDATA[图文消息描述]]></Description>
                            <PicUrl><![CDATA[图文消息图片URL]]></PicUrl>
                            <Url><![CDATA[图文消息URL]]></Url>
                        </item>
                    </Articles>
                </xml>
            """
            response = make_response(response_xml)
            response.content_type = 'application/xml'
            return response
            
@app.route('/healthz')
def health_check():
    return 'ok', 200

@app.route('/ready')
def readiness_check():
    return 'ok', 200
    
if __name__ == '__main__':
    app.run(port=80, debug=True)
