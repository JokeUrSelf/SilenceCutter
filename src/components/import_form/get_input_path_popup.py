from tkinter import filedialog
from lib.tk_popup import TkPopup


class GetInputPathPopup(TkPopup):
    def __init__(self, supported_formats):
        super().__init__(supported_formats)

    def handle_popup(self, root):
        file_path: str = filedialog.askopenfilename(
            filetypes=[
                ("Media", " ".join(self.supported_formats))
            ],
            parent=root
        )
        self.notify_listeners(file_path)

    def show(self):
        root = self.create_tk_popup_field()
        self.handle_popup(root)
        self.destroy_tk_popup_field(root)
