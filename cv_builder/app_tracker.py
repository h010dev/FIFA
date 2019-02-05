import os
import docx
import datetime
import pandas as pd
from collections import defaultdict


class JobTracker:

    key_words = dict()

    def __init__(self, df=None, document=None):
        self.df = df
        self.document = document

    def load_files(self):

        self.df = pd.read_csv(r'Main\app_tracker.csv')
        self.document = docx.Document(r'Main\cv_template.docx')

    def new_entry(self):

        position = str(input('Enter position name: '))
        organization = str(input('Enter organization name: '))
        location = str(input('Enter location: '))

        self.key_words.clear()
        self.key_words['Job'] = position
        self.key_words['Organization'] = organization
        self.key_words['Location'] = location

    def cover_letter(self):

        for i in range(len(self.document.paragraphs)):
            self.document.paragraphs[i].text = self.document.paragraphs[i].text.replace('JOB', self.key_words['Job'])
            self.document.paragraphs[i].text = self.document.paragraphs[i].text.replace('ORGANIZATION',
                                                                                        self.key_words['Organization'])
            self.document.paragraphs[i].text = self.document.paragraphs[i].text.replace('LOCATION',
                                                                                        self.key_words['Location'])

        file_name = f'Main\\' \
            f'{self.key_words["Organization"].replace(" ", "-")}' \
            f'_CV_{self.key_words["Job"].replace(" ", "-")}' \
            f'_{self.key_words["Location"].replace(" ", "-")}' \
            f'_USA_{datetime.date.today()}.docx'

        self.document.save(file_name)

    def app_tracker(self):

        column_names = list(self.df.columns)
        d = defaultdict(object)

        for i in column_names:
            d[i]

        d['Organization'] = self.key_words['Organization']
        d['Position'] = self.key_words['Job']
        d['Province/State'] = self.key_words['Location']
        d['Country'] = 'USA'
        d['Application Date'] = datetime.datetime.now()
        d['Test'] = False
        d['Contact'] = False
        d['Interview'] = False
        d['Offer'] = False
        d['Notes'] = None

        self.df = self.df.append(d, ignore_index=True)
        self.df.to_csv(r'Main\app_tracker.csv', index=False)

        d.clear()
