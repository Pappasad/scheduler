import pandas as pd

class Scheduler:

    class Day(dict):

        def __init__(self, series, name=None):
            self.date = name
            for idx in range(1, len(series), 2):
                self[series.iloc[idx]] = series.iloc[idx-1] == True or series.iloc[idx-1] == 'True' or series.iloc[idx-1] == 'TRUE'

        def isDone(self):
            return all(self.values())
        
        def setAll(self, val: bool):
            for key in self:
                self[key] = val


    def __init__(self, url):
        self.url = url
        self.sheet_data = pd.read_csv(self.url)
        self.sheet_data = self.sheet_data.rename(columns={self.sheet_data.columns[0]:"Date"})
        self.sheet_data = self.sheet_data.drop(self.sheet_data.columns[self.sheet_data.columns.get_loc('Weekly Due'):], axis=1)
        
    def getCheckboxes(self, date):
        date_idx = self.sheet_data.index[self.sheet_data['Date'] == date][0]
        day = self.sheet_data.iloc[date_idx].tolist()
        to_check = [(int(date_idx) + 1, idx) for idx, val in enumerate(day) if val == True]
        return to_check
              
    def __getitem__(self, date):
        return self.Day(self.sheet_data.loc[self.sheet_data['Date'] == date].drop('Date', axis=1).iloc[0], name=date)
    
    def __setitem__(self, date, day: Day):
        row = self.sheet_data.loc[self.sheet_data['Date'] == date].index[0]
        for key, value in day.items():
            col = self.sheet_data.iloc[row].tolist().index(key)
            self.sheet_data.iloc[row, col-1] = bool(value)

    def __repr__(self):
        s = f'URL: {self.url}\n'
        s += f'Sheet Data: \n {self.sheet_data}'
        return s

    def __str__(self):
        return self.__repr__()
