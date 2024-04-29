from RPA.Excel.Files import Files


class Filer:

    def __init__(self):
        self.filename = 'output/results.xlsx'
        self.sheet_name = 'Sheet1'
        self.headers = [['Title', 'Desc', 'Date', 'Currency within title or desc', 'Phrase Matches', 'Image filename']]
        self.excel = Files()

    def create_excel(self):
        self.excel.create_workbook(self.filename, sheet_name=self.sheet_name)

    def insert_data(self, data, start_row: 1, start_col: 1):
        self.headers.extend(data)
        for row_idx, row_data in enumerate(self.headers, start=start_row):
            for col_idx, value in enumerate(row_data, start=start_col):
                self.excel.set_cell_value(row_idx, col_idx, value)

    def save(self):
        self.excel.save_workbook()
