from RPA.Excel.Files import Files


class Filer:

    # Initializing document with requested inputs
    def __init__(self):
        self.filename = 'output/results.xlsx'
        self.sheet_name = 'Sheet1'
        self.headers = [['Title', 'Desc', 'Date', 'Phrase Matches', 'Currency within title or desc', 'Image filename']]
        self.excel = Files()

    # To create a file with given parameters
    def create_excel(self):
        self.excel.create_workbook(self.filename, sheet_name=self.sheet_name)

    # To insert information within Excel file
    def insert_data(self, data, start_row: 1, start_col: 1):
        self.headers.extend(data)
        for row_idx, row_data in enumerate(self.headers, start=start_row):
            for col_idx, value in enumerate(row_data, start=start_col):
                self.excel.set_cell_value(row_idx, col_idx, value)

    # To save Excel file
    def save(self):
        self.excel.save_workbook()
