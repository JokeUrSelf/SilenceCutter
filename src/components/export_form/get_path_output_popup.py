from typing import Optional
from tkinter import filedialog

from lib.tk_popup import TkPopup


class GetPathOutputPopup(TkPopup):

    def __init__(self, supported_formats):
        super().__init__(supported_formats)

    def handle_popup(self, root):
        file_path: Optional[str] = filedialog.asksaveasfilename(
            filetypes=[
                (x.replace(".", "").upper(), x)
                for x in self.supported_formats
            ],
            initialfile="untitled",
            parent=root,
            defaultextension=self.supported_formats
        )
        if file_path: self.notify_listeners(file_path)

    def show(self):
        root = self.create_tk_popup_field()
        self.handle_popup(root)
        self.destroy_tk_popup_field(root)
