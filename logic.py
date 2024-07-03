import csv
from typing import Tuple
from PyQt5.QtWidgets import QWidget, QMessageBox
from gui.gui import Ui_End
import os as os

from errors import *


class Logic(QWidget, Ui_End):

    def __init__(self) -> None:
        """
        initializes the logic class
        """
        super().__init__()
        self.setupUi(self)
        self.__votes = {'Isaiah': 0, 'Julia': 0, 'Jane': 0}

        # vote menu buttons
        self.vote_button.clicked.connect(self.go_vote)
        self.total_button.clicked.connect(self.total_votes)

        # candidate menu buttons
        self.submit_vote.clicked.connect(self.submit)
        self.back.clicked.connect(self.back_page)

        # Total Votes Menu
        self.reset_election.clicked.connect(self.reset_elections)
        self.export_votes.clicked.connect(self.confirm_exports)

        # Confirm Votes Menu
        self.pushButton.clicked.connect(self.write_file)

    def reset_elections(self) -> None:
        """
        Resets the election state and redirects user to home page
        :return: None
        """
        self.stackedWidget.setCurrentIndex(2)
        self.__votes = {'Isaiah': 0, 'Julia': 0, 'Jane': 0}

    def add_vote(self, candidate: str) -> None:
        """
        Adds a vote to the canadate selected in GUI
        :param candidate: Canadate selected
        :return: None
        """
        if candidate in self.__votes:
            self.__votes[candidate] += 1

    def get_votes(self) -> Tuple[int, int, int]:
        """
        gets the votes
        :return: Tuple[int, int, int]
        """
        return self.__votes['Isaiah'], self.__votes['Julia'], self.__votes['Jane']

    def go_vote(self) -> None:
        """
        Redirects to the vote page
        :return:
        """
        self.stackedWidget.setCurrentIndex(0)

    def submit(self) -> None:
        """
        Submits the vote and redirects user to home page
        :return: None
        """
        if not (self.Isaiah.isChecked() or self.Julia.isChecked() or self.Jane.isChecked()):
            QMessageBox.warning(self, "Warning", "Please select a candidate before submitting your vote.")
            return
        voted = ''
        if self.Isaiah.isChecked():
            self.add_vote('Isaiah')
            voted = 'Isaiah'
        elif self.Julia.isChecked():
            self.add_vote('Julia')
            voted = 'Julia'
        elif self.Jane.isChecked():
            self.add_vote('Jane')
            voted = 'Jane'

        QMessageBox.information(self, "Information", f"'Thank you for your vote!' - {voted}")

        self.stackedWidget.setCurrentIndex(2)

    def total_votes(self) -> None:
        """
        calculates the winner of the election
        :return:
        """
        print(self.__votes)
        self.stackedWidget.setCurrentIndex(1)
        winning_candidate = max(self.__votes, key=self.__votes.get)
        winning_votes = self.__votes[winning_candidate]
        total = sum(self.__votes.values())
        if self.__votes['Isaiah'] == self.__votes['Julia'] == self.__votes['Jane']:
            self.label_5.setText(f'The election is a tie with {total} votes')
        elif winning_votes > 0:
            self.label_5.setText(
                f'THE WINNER OF THE ELECTION IS \n{winning_candidate}\n With {winning_votes} votes \n{total} Votes Casted')

    def back_page(self) -> None:
        """
        goes back a page
        :return: None
        """
        self.stackedWidget.setCurrentIndex(2)

    def confirm_exports(self) -> None:
        """
        When confirm export button is clicked redirects user
        :return: None
        """
        self.stackedWidget.setCurrentIndex(3)

    def write_file(self) -> None:
        """
        Writes The votes to a file and calculates the total votes user picks file name
        :return: None
        """
        try:
            verify = self.lineEdit.text().strip().lower()
            file_name = self.fileNameLineEdit.text().strip().lower()
            print(file_name)
            if verify != 'save':
                raise ValueError
            if file_name == '':
                raise FileEmpty
            if file_name[-4:] not in ['.txt', '.csv']:
                raise WrongEnding
            if os.path.exists(file_name):
                raise FileExistsError
            candidates = self.__votes.keys()
            total_votes = sum(self.__votes.values())
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(candidates)
                writer.writerow(self.get_votes())
                writer.writerow(['Total Votes: ', total_votes])

        except ValueError:
            self.errorlabel.setText('SAVE text does not match')
        except WrongEnding:
            self.errorlabel.setText('Invalid file format')
        except FileExistsError:
            self.errorlabel.setText('File already exists')
        except FileEmpty:
            self.errorlabel.setText('file cannot be NONE')
        except:
            print('e')

        else:
            self.reset_elections()
