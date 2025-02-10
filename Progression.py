# # import the main window object (mw) from aqt
# from aqt import mw
# # import the "show info" tool from utils.py
# from aqt.utils import showInfo, qconnect
# # import all of the Qt GUI library
# from aqt.qt import *
# # import hooks from Anki's hooks module
# from anki.hooks import wrap

# # Dictionary to track counts of "Good" and "Again" clicks
# review_counts = {"good": 0, "again": 0}

# def increment_review_count(button: int) -> None:
#     """
#     Increment the count for "Good" or "Again" based on the button pressed.
#     :param button: The review button pressed (1=Again, 3=Good).
#     """
#     global review_counts
#     if button == 1:  # "Again" button
#         review_counts["again"] += 1
#     elif button == 3:  # "Good" button
#         review_counts["good"] += 1

# # Hook into the "review card answered" event
# from aqt.reviewer import Reviewer
# old_answerCard = Reviewer._answerCard

# def new_answerCard(self, ease):
#     increment_review_count(ease)
#     old_answerCard(self, ease)

# Reviewer._answerCard = new_answerCard

# def show_review_counts() -> None:
#     """Display the counts for "Good" and "Again" clicks."""
#     global review_counts
#     message = f"Good: {review_counts['good']}\nAgain: {review_counts['again']}"
#     print("Menu item clicked, showing counts...")
#     showInfo(message)

# # Create a new menu item to show counts
# def add_menu_item():
#     action = QAction("Show Review Counts", mw)
#     action.triggered.connect(show_review_counts)  # Connect the action directly to the function
#     mw.form.menuTools.addAction(action)
    
# add_menu_item()

# from aqt import mw
# from aqt.utils import showInfo, qconnect
# from aqt.qt import *
# from anki.hooks import wrap
# from aqt.reviewer import Reviewer

# # Dictionary to track review history (all presses for the current card)
# review_history = []

# def increment_review_history(button: int) -> None:
#     """
#     Track all button presses for the current card.
#     :param button: The review button pressed (1=Again, 3=Good, 2=Easy).
#     """
#     global review_history
#     if button == 1:
#         review_history.append("Again")
#     elif button == 2:
#         review_history.append("Easy")
#     elif button == 3:
#         review_history.append("Good")

# # Hook into the "review card answered" event
# old_answerCard = Reviewer._answerCard

# def new_answerCard(self, ease):
#     increment_review_history(ease)
#     old_answerCard(self, ease)

# Reviewer._answerCard = new_answerCard

# def show_review_history() -> None:
#     """Display a window showing all button presses for the current card."""
#     global review_history
    
#     # Create the dialog
#     dialog = QDialog(mw)
#     dialog.setWindowTitle("Review History")

#     # Layout for the dialog
#     layout = QVBoxLayout()

#     # Add a label showing the review history
#     history_label = QLabel("Review History:")
#     layout.addWidget(history_label)

#     # Add each review action as a new label
#     for action in review_history:
#         action_label = QLabel(action)
#         layout.addWidget(action_label)

#     # Set the dialog layout
#     dialog.setLayout(layout)

#     # Show the dialog
#     dialog.exec_()

# # Create a new menu item to show review history
# def add_menu_item():
#     action = QAction("Show Review History", mw)
#     action.triggered.connect(show_review_history)  # Connect the action to the function
#     mw.form.menuTools.addAction(action)

# # Add the menu item when Anki starts
# add_menu_item()


# # import the main window object (mw) from aqt
# from aqt import mw
# # import the "show info" tool from utils.py
# from aqt.utils import showInfo, qconnect
# # import all of the Qt GUI library
# from aqt.qt import *

# # We're going to add a menu item below. First we want to create a function to
# # be called when the menu item is activated.

# def testFunction() -> None:
#     # get the number of cards in the current collection, which is stored in
#     # the main window
#     cardCount = mw.col.cardCount()
#     # show a message box
#     showInfo("Card count: %d" % cardCount)

# # create a new menu item, "test"
# action = QAction("test", mw)
# # set it to call testFunction when it's clicked
# qconnect(action.triggered, testFunction)
# # and add it to the tools menu
# mw.form.menuTools.addAction(action)