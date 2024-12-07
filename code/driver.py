import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetDriver:
    """
    A class to interact with Google Sheets using the gspread library.

    Provides methods to manage checkboxes and navigate sheets.

    """
    def __init__(self, credential_path):
        # Authenticate using service account credentials.
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path)
        self.client = gspread.authorize(self.credentials)
        self.spreadsheet = None  # Reference to the spreadsheet.
        self.active_sheet = None  # Currently active sheet.

    def checkBoxes(self, boxes):
        """
        Marks the specified checkboxes as checked in the active sheet.
            :param boxes: List of tuples (row, col) representing checkbox coordinates.

        """
        print("Checking boxes...")
        for row, col in boxes:
            if self.active_sheet.cell(row, col).value == "FALSE":
                print(f"\tChecked box at [{row}, {col}]")
                self.active_sheet.update_cell(row, col, "TRUE")
        print("Done checking boxes.")

    def uncheckBoxes(self, boxes):
        """
        Marks the specified checkboxes as unchecked in the active sheet.
            :param boxes: List of tuples (row, col) representing checkbox coordinates.

        """
        print("Unchecking boxes...")
        for row, col in boxes:
            if self.active_sheet.cell(row, col).value == "TRUE":
                print(f"\tUnchecked box at [{row}, {col}]")
                self.active_sheet.update_cell(row, col, "FALSE")
        print("Done unchecking boxes.")

    def openSheet(self, sheet_name, sheet_number=0):
        """
        Opens a Google Sheet by name and selects the specified worksheet.
            :param sheet_name: Name of the Google Sheet.
            :param sheet_number: Index of the worksheet (default is 0).

        """
        self.spreadsheet = self.client.open(sheet_name)
        self.active_sheet = self.spreadsheet.get_worksheet(sheet_number)

    def changeSheet(self, number):
        """
        Changes the active worksheet by index.
            :param number: Index of the worksheet to activate.
        """
        if self.spreadsheet is None:
            print("No Spreasheet")
            return

        self.active_sheet = self.spreadsheet.get_worksheet(number)

    def getActive(self):
        """
        Retrieves all values from the active worksheet.

        """

        if self.spreadsheet is None:
            print("No Spreasheet")
            return

        return self.active_sheet.get_all_values()



    def __repr__(self):
        """
        Provides a string representation of the SheetDriver's state.

        """

        if self.spreadsheet is None or self.active_sheet is None:
            return "Inactive SheetDriver"

        return "SheetDriver with Active Sheet: '" + self.active_sheet.title + "'"
    

