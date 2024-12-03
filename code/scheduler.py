import pandas as pd

DAYS = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}

class Scheduler:

    class Day(dict):

        def __init__(self, series):
            for idx in range(0, len(series) - 1, 2):
                self[series.iloc[idx]] = bool(series.iloc[idx+1])

        def isDone(self):
            return all(self.values())



    def __init__(self, url):
        self.url = url
        self.sheet_data = pd.read_csv(self.url)
        self.sheet_data = self.sheet_data.rename(columns={self.sheet_data.columns[0]:"Date"})
        self.sheet_data = self.sheet_data.drop(self.sheet_data.columns[self.sheet_data.columns.get_loc('Weekly Due'):], axis=1)
        
    def __getitem__(self, date):
        return self.Day(self.sheet_data.loc[self.sheet_data['Date'] == date].iloc[0])
    
    def __setitem__(self, )

    def __repr__(self):
        s = f'URL: {self.url}\n'
        s += f'Sheet Data: \n {self.sheet_data}'
        return s

    def __str__(self):
        return self.__repr__()
