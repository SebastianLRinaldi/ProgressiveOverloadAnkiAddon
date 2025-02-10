import sys
# from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QAction
from aqt.webview import AnkiWebView
from aqt import mw

from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.FrontEnd.C_Grouper.TabGroupInitializations.TabGroupInitialization import *
from application.FrontEnd.C_Grouper.WidgetGroupInitializations.WidgetGroupInitialization import *
from application.FrontEnd.C_Grouper.SpliterGroupInitializations.SpliterGroupInitialization import *
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.FrontEnd.E_combiner.connections import *







def PreviewWindow():
    
    previewWindow.add_widgets_to_window(
        
        
        card_view_area.add_widgets_to_group(
            web_view,
            
        ),
        
        card_nav_area.add_widgets_to_group(
            
            prev_btn,
            next_btn,
            
        ),
        
    )

    if not hasattr(mw, "_card_viewer"):
        mw._card_viewer = previewWindow
    mw._card_viewer.show()
    mw._card_viewer.raise_()
    
    # previewWindow.show()









class CardViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Single Card Viewer")
        self.setMinimumSize(400, 300)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)
        
        self.web_view = AnkiWebView()
        layout.addWidget(self.web_view)
        
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("Previous")
        next_btn = QPushButton("Next")
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(next_btn)
        layout.addLayout(nav_layout)
        
        self.current_card_index = 0
        
        prev_btn.clicked.connect(self.show_previous_card)
        next_btn.clicked.connect(self.show_next_card)

        self.show_current_card()

    def show_current_card(self):
        did = mw.col.decks.current().get('id')
        if did is None:
            return
        
        cards = mw.col.find_cards(f"did:{did}")
        if not cards:
            return

        card = mw.col.get_card(cards[self.current_card_index])
        q = card.question()
        q_av = card.question_av_tags()
        
        a = card.answer()
        a_av = card.answer_av_tags()
        
        html = f"""
            <style>
            .card-container {{
                display: flex;
                flex-direction: column;
                gap: 20px; /* Space between cards */
            }}

            .card {{
                padding: 20px;
                font-size: 16px;
                background-color: #f4f4f4; /* Card background */
                border-radius: 5px;
            }}

            .front {{
                background-color: #fff; /* White background for the front */
                padding: 20px;
                border-radius: 5px;
            }}

            .back {{
                background-color: #fff; /* White background for the back */
                padding: 20px;
                border-radius: 5px;
            }}
            </style>

            <div class="card-container">
                <div class="card">
                    <div class="front">{q}</div>
                </div>
                <div class="card">
                    <div class="back">{a}</div>
                </div>
            </div>
        """
        
        self.web_view.stdHtml(html, css=[])

    def show_previous_card(self):
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.show_current_card()

    def show_next_card(self):
        did = mw.col.decks.current().get('id')
        if did is None:
            return
        
        cards = mw.col.find_cards(f"did:{did}")
        if self.current_card_index < len(cards) - 1:
            self.current_card_index += 1
            self.show_current_card()


# def show_viewer():
#     if not hasattr(mw, "_card_viewer"):
#         mw._card_viewer = CardViewerWindow()
#     mw._card_viewer.show()
#     mw._card_viewer.raise_()
