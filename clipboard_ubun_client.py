# ubuntu_clipboard_monitor.py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import requests
from PIL import ImageGrab, UnidentifiedImageError
import base64
import io
import threading



class ClipboardMonitor:
    def __init__(self, target):
        self.target = target
        self.previous_data = None
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.connect('owner-change', self.on_clipboard_change)
        Gtk.main()

    def send_update(self, data, data_type):
        local_url = "http://127.0.0.1:9024/update_self"
        url = f'http://{self.target}/update_clipboard'
        payload = {'data': data, 'data_type': data_type}
        requests.post(local_url, json=payload)

        requests.post(url, json=payload)
        print(f"Sent clipboard update to {self.target}")
      

    def on_clipboard_change(self, clipboard, event):
        # Check for image content first
        try:
            image = ImageGrab.grabclipboard()
            if image:
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                if image_base64 != self.previous_data:
                    self.previous_data = image_base64
                    self.send_update(image_base64, 'image/png')
                return
        except UnidentifiedImageError:
            pass

        # If no image, check for text content
        current_content = self.clipboard.wait_for_text()
        if current_content:
            if current_content != self.previous_data:
                self.previous_data = current_content
                self.send_update(current_content, "text/plain")

def start_monitor(target):
    ClipboardMonitor(target)

if __name__ == '__main__':
    target = '10.1.80.58:9024'
    threading.Thread(target=start_monitor, args=(target,)).start()
