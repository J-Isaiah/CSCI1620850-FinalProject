import csv
from typing import Tuple, Dict, Any
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
        self.__votes = {}

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
        self.__votes = {}

    def add_vote(self, candidate: str, voter_id: int) -> None:
        """
        Adds a vote to the canadate selected in GUI
        :param voter_id:
        :param candidate: Canadate selected
        :return: None
        """
        self.__votes[voter_id] = candidate

    def get_votes(self) -> dict[Any, Any]:
        """
        gets the votes
        :return: Tuple[int, int, int]
        """
        return self.__votes

    def go_vote(self) -> None:
        """
        Redirects to the vote page
        :return:
        """
        self.stackedWidget.setCurrentIndex(0)

    def reset_widgets(self) -> None:
        self.Isaiah.setChecked(False)
        self.Julia.setChecked(False)
        self.Jane.setChecked(False)
        self.VoterID.clear()

    def submit(self) -> None:
        """
        Submits the vote and redirects user to home page
        :return: None
        """
        try:

            voter_id = self.VoterID.toPlainText().strip()
            if voter_id == '':
                raise BLANK_VOTER_ID

            voter_id = int(voter_id)

            if voter_id < 1000:
                raise Voter_ID_Greator_1k

            try:

                if not (self.Isaiah.isChecked() or self.Julia.isChecked() or self.Jane.isChecked()):
                    QMessageBox.warning(self, "Warning", "Please select a candidate before submitting your vote.")
                    return
                if len(str(voter_id)) != 4:
                    raise Incorrect_voter_ID_Len
                elif voter_id in self.__votes.keys():
                    print(self.__votes.keys())
                    raise VoterID_Exists

                voted = ''
                if self.Isaiah.isChecked():
                    self.add_vote('Isaiah', voter_id)
                    voted = 'Isaiah'
                elif self.Julia.isChecked():
                    self.add_vote('Julia', voter_id)
                    voted = 'Julia'
                elif self.Jane.isChecked():
                    self.add_vote('Jane', voter_id)
                    voted = 'Jane'
                QMessageBox.information(self, "Information", f"'Thank you for your vote!' - {voted}")
                self.stackedWidget.setCurrentIndex(2)
                self.reset_widgets()
                self.label_4.setText('Voting Menu')

            except Incorrect_voter_ID_Len:
                self.label_4.setText('Voter ID Needs to Have a Length Of 4')
            except VoterID_Exists:
                self.label_4.setText('Cannot Vote Twice')
        except ValueError:
            self.label_4.setText('Only Numbers Are Allowed as Voter ID')
        except BLANK_VOTER_ID:
            self.label_4.setText('VOTER ID CANNOT BE BLANK')
        except Voter_ID_Greator_1k:
            self.label_4.setText('Voter ID needs to be\nGreater then 1000')

    def total_votes(self) -> None:
        """
        calculates the winner of the election
        :return:
        """

        print(self.__votes)
        self.stackedWidget.setCurrentIndex(1)
        total_votes = {'Isaiah': 0,
                       'Julia': 0,
                       'Jane': 0}
        for vote in self.__votes.values():
            if vote == 'Isaiah':
                total_votes['Isaiah'] += 1
            elif vote == 'Julia':
                total_votes['Julia'] += 1
            elif vote == 'Jane':
                total_votes['Jane'] += 1

        winning_canadate = max(total_votes, key=total_votes.get)
        winning_votes = total_votes[winning_canadate]
        print(winning_canadate, winning_votes)

        if all(count == winning_votes for count in total_votes.values()):
            self.label_5.setText(f'The Election is a tie\n There is no winner\n{winning_votes} Votes')
        else:
            self.label_5.setText(
                f'THE WINNER OF THE ELECTION IS \n{winning_canadate}\n With {winning_votes} votes \n{sum(total_votes.values())} Votes Casted')

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

            total_votes = {'Isaiah': 0, 'Julia': 0, 'Jane': 0}
            for vote in self.__votes.values():
                if vote == 'Isaiah':
                    total_votes['Isaiah'] += 1
                elif vote == 'Julia':
                    total_votes['Julia'] += 1
                elif vote == 'Jane':
                    total_votes['Jane'] += 1

            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Voter ID', 'Candidate'])
                for voter_id, candidate in self.__votes.items():
                    writer.writerow([voter_id, candidate])
                writer.writerow([])
                writer.writerow(['Total Votes: ', sum(total_votes.values())])

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
