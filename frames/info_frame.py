from tkhtmlview import HTMLLabel


class InfoFrame:
    def __init__(self, root):
        with open('info_frame_text.html', 'r', encoding='utf-8') as file:
            self.info_label = HTMLLabel(root, html=file.read())
        self.info_label.pack(fill="both", expand=True)
