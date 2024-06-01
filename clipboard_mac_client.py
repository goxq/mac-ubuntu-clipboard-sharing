import objc
import requests
import signal
import sys
from functools import partial
from AppKit import NSPasteboard, NSPasteboardTypeString, NSApplication, NSTimer, NSObject
import base64

class ClipboardListener(NSObject):
    def init_with_target(self, target):
        self = objc.super(ClipboardListener, self).init()
        self.target = target
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.change_count = self.pasteboard.changeCount()
        self.txt_types = ["public.utf8-plain-text"]
        self.img_types = ["public.png"]
        self.previous_data = None
        return self
    
    def send_to_server(self, data, data_type):
        local_url = "http://127.0.0.1:9024/update_self"
        url = f'http://{self.target}/update_clipboard'
        payload = {'data': data, 'data_type': data_type}
        requests.post(local_url, json=payload)

        requests.post(url, json=payload)
        print(f"Sent clipboard update to {self.target}")

    def get_mime_type(self, data_type):
        if data_type == "public.utf8-plain-text":
            return "text/plain"
        elif data_type == "public.png":
            return "image/png"
        else:
            raise ValueError(f"Unknown data type: {data_type})")
        
    def checkClipboard_(self, timer):
        if self.pasteboard.changeCount() != self.change_count:
            # print('Clipboard changed')
            self.change_count = self.pasteboard.changeCount()

            text_available_type = self.pasteboard.availableTypeFromArray_(self.txt_types)
            image_available_type = self.pasteboard.availableTypeFromArray_(self.img_types)
            if text_available_type:
                # print(text_available_type)
                # print(f"Sending data to {self.target}")
                text = self.pasteboard.dataForType_(text_available_type).decode('utf-8')
                mime_type = self.get_mime_type(text_available_type)
                if text != self.previous_data:
                    self.previous_data = text
                    self.send_to_server(text, mime_type)
            elif image_available_type:
                # print(image_available_type)
                # print(f"Sending data to {self.target}")
                image = self.pasteboard.dataForType_(image_available_type)
                image = base64.b64encode(image).decode('utf-8')
                mime_type = self.get_mime_type(image_available_type)
                if image != self.previous_data:
                    self.previous_data = image
                    self.send_to_server(image, mime_type)
    

def signal_handler(app, signal, frame):
    print('Exiting...')
    app.terminate_(None)

if __name__ == "__main__":
    target = "10.1.96.28:9024"
    listener = ClipboardListener.alloc().init_with_target(target)
    timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        1.0, listener, objc.selector(listener.checkClipboard_, signature=b'v@:'), None, True)
    app = NSApplication.sharedApplication()
    signal.signal(signal.SIGINT, partial(signal_handler, app))
    app.run()
