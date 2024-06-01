import threading
from flask import Flask, request
import base64
import subprocess
import AppKit


app = Flask(__name__)

previous_message = None

@app.route('/update_self', methods=['POST'])
def update_self():
    global previous_message
    previous_message = request.json['data']
    return 'previous_message received', 200


@app.route('/update_clipboard', methods=['POST'])
def update_clipboard():
    global previous_message
    js = request.json
    if js['data'] == previous_message:
        return 'No need to update clipboard', 200

    data = js['data']
    data_type = js['data_type']
    if 'text' in data_type:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=data.encode())
    elif "image" in data_type:
        data = base64.b64decode(data) # type(data) is bytes
        # 创建NSImage
        image_data = AppKit.NSData.dataWithBytes_length_(data, len(data))

        # 创建剪贴板对象
        pasteboard = AppKit.NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        
        # 将图像数据写入剪贴板
        pasteboard.declareTypes_owner_(["public.png"], None)
        pasteboard.setData_forType_(image_data, "public.png")
    return 'Clipboard updated', 200

def run_server():
    app.run(host='0.0.0.0', port=9024)

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()