import sys
import os.path
from email.parser import Parser
from email.parser import BytesParser
import re
import pandas as pd

def main():
    """Launches the script as a standalone"""
    if not (os.path.isdir('./maildir')):
        print("The required folder seems to be missing from the working folder!")
        print("Download it from https://www.cs.cmu.edu/~./enron/")
        sys.exit()
    if not (os.path.isdir('./output')):
        print('You need to have and empty folder named "output" in the root of the project!')
        sys.exit()
    filenames = find_filenames('./maildir', simplified1=True)
    sender_to_recipient(filenames)
    filenames = find_filenames('./maildir', simplified2=False)
    average_per_weekday(filenames)

def sender_to_recipient(filenames):
    """Calculates how many emails were sent from one adress to another, and saves a csv file from it."""
    dictionary = {}
    print('Parsing emails to calculate how many emails were sent from each sender address to each recipient...')
    for f in filenames:
        content = parse_email(f)
        recipients = [str(content['Cc']), str(content['To']), str(content['Bcc'])]
        recipients =    [x for x in recipients if x is not None]
        recipients = ' '.join(recipients).replace(',', '')
        recipients = list(set(re.findall(r'\S+@\S+', recipients)))
        sender = content['From']
        for r in recipients:
            dictionary[(sender, r)] = dictionary.get((sender, r), 0) + 1
    df = pd.DataFrame(list(dictionary.items()), columns=['sender', 'count'])
    df[['sender', 'recipient']] = pd.DataFrame(df['sender'].tolist(), index=df.index)
    df = df[['sender', 'recipient', 'count']]
    df.to_csv(r'./output/emails_sent_totals.csv', index = None, header=True)
    print('Saved results to ./output/emails_sent_totals.csv')

def average_per_weekday(filenames):
    """Calculates the average of how many mails does employee receive per weekday"""
    print("Calculating the average emails received per employee per weekday...")
    maps = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}
    dictionary = {}
    for f in filenames:
        employee = re.search(r'/maildir/(.+?)/', f)
        if not employee:
            break
        employee = employee.group(1)
        content = parse_email(f)
        if content['Date'] is None:
            break
        day = re.search(r'(.+?),', content['Date'])
        day = day.group(1).lower()
        date = re.search(r',(.+?):', content['Date'])
        date = date.group(1)[:-3]
        dictionary[(employee, maps[day], date)] = dictionary.get((employee, maps[day], date), 0) + 1
        
    df = pd.DataFrame(list(dictionary.items()), columns=['e', 'avg_count'])
    df[['employee', 'day_of_week', 'date']] = pd.DataFrame(df['e'].tolist(), index=df.index)
    df = df[['employee', 'day_of_week', 'date', 'avg_count']]
    df.sort_values(by=['employee', 'day_of_week'], inplace=True)
    df['avg_count'] = pd.to_numeric(df['avg_count']) 
    df = df.groupby(['employee', 'day_of_week']).agg(avg_count=('avg_count', 'mean')).reset_index()
    df.to_csv(r'./output/emails_sent_average_per_weekday.csv', index = None, header=True)
    print('Saved results to ./output/emails_sent_average_per_weekday.csv')


def find_filenames(dir, simplified1 = False, simplified2 = False):
    """finds the filenames from the maildir folder. Two special cases for the requested simplified cases."""
    file_paths = [] 
    print(f'Finding Filenames from path "{dir}"...')
    for root, directories, files in os.walk(dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    if simplified1:
        print('For simplicity, considering only files in folders (sent / sent items).')
        file_paths = [fp for fp in file_paths if 'sent' in fp]
    if simplified2:
        print('For Simplicity, considering only files in folders that feature "inbox".')
        file_paths = [fp for fp in file_paths if '/inbox/' in fp]
    print('Filenames found!')
    return file_paths

def parse_email(filename):
    """Parses email content, works both for utf-8 encoded and byte encoded files."""
    with open(filename, "rb") as email:
        data = email.read()
    if isinstance(data, bytes):
        content = BytesParser().parsebytes(data)
    else:
        content = Parser().parsestr(data)
    return content

if __name__ == '__main__':
    sys.exit(main())
