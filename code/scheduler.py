import pandas as pd

class Scheduler:

    """
    A class to manage and manipulate schedule data from a CSV file.

    """

    class Day(dict):
        """
        A representation of a single day's tasks.

        Provides methods to manipulate task statuses.

        """

        def __init__(self, scheduler, series, name):
            self.scheduler = scheduler
            self.date = name
            # Populate tasks and their statuses from the series.
            for idx in range(1, len(series), 2):
                key = str(series.iloc[idx])
                while key in self:
                    key += 'I'
                self[key] = series.iloc[idx-1] in [True, 'True', 'TRUE']

        def getNotDone(self):
            return [key for key in self.keys() if not self[key]]

        def isDone(self):
            """
            Checks if all tasks for the day are completed.

            """
            return all(self.values())

        def setAll(self, val=True):
            """
            Sets the completion status of all tasks to the specified value.

            """

            for key in self:
                self[key] = val
            self.scheduler[self.date] = self

        def setEmpty(self, val=True):
            """
            Sets the completion status of tasks marked as empty to the specified value.

            """
            for key in (k for k in self.keys() if 'nan' in k):
                self[key] = val
            self.scheduler[self.date] = self

        def __repr__(self):
            """
            Provides a string representation of the day's tasks and statuses.

            """
            s = f"Day: {self.date}\\n"
            for key, value in self.items():
                s += f"\\t{key}: {'DONE' if value else 'Not Done'}\\n"
            return s


    def __init__(self, url):
        self.url = url  # URL of the CSV file containing the schedule data.

        # Load the CSV data into a Pandas DataFrame.
        self.sheet_data = pd.read_csv(self.url)
        self.sheet_data = self.sheet_data.rename(columns={self.sheet_data.columns[0]: "Date"})

        # Drop unnecessary columns starting from 'Weekly Due'.
        self.sheet_data = self.sheet_data.drop(self.sheet_data.columns[self.sheet_data.columns.get_loc('Weekly Due'):], axis=1)

    def getCheckboxes(self, date):
        """
        Retrieves the coordinates of checkboxes to be checked for a given date.
            :param date: Date for which checkboxes are to be fetched.
            :return: List of (row, col) tuples representing checkbox coordinates.

        """

        date_idx = self.sheet_data.index[self.sheet_data['Date'] == date][0]
        day = self.sheet_data.iloc[date_idx].tolist()
        to_check = [(int(date_idx) + 2, idx + 1) for idx, val in enumerate(day) if val in [True, 'True', 'TRUE']]
        return to_check

    def __getitem__(self, date):
        """
        Retrieves a Day object for the specified date.

        """
        return self.Day(self, self.sheet_data.loc[self.sheet_data['Date'] == date].drop('Date', axis=1).iloc[0], name=date)

    def __setitem__(self, date, day: Day):
        """
        Updates the schedule data for a specific date.
            :param date: Date to update.
            :param day: Day object containing updated task statuses.

        """
        row = self.sheet_data.loc[self.sheet_data['Date'] == date].index[0]
        row_list = self.sheet_data.iloc[row].astype(str).tolist()
        seen = set()
        for i in range(len(row_list)):
            if row_list[i] in [True, 'True', 'TRUE']:
                continue

            while row_list[i] in seen:
                row_list[i] += 'I'
            seen.add(row_list[i])

        for key, value in day.items():
            col = row_list.index(key)
            self.sheet_data.iloc[row, col-1] = bool(value)

    def __repr__(self):
        """
        Provides a string representation of the Scheduler's state.

        """
        s = f'URL: {self.url}\\n'
        s += f'Sheet Data: \\n {self.sheet_data}'
        return s

    def __str__(self):
        """
        Provides a string representation (same as __repr__).

        """
        return self.__repr__()
