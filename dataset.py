import pandas as pd
import torch
import re
import string
from torch.utils.data import DataLoader, Dataset

from google.cloud import bigquery
from google.oauth2 import service_account


class DatasetSQL():
    '''
    Class object to connect and retrieve data from DB in GCP
    '''
    def __init__(self,client):
        self.client = client

    def get_result_query(self,query_sql):
        '''
        Returns the google.cloud.bigquery.table.RowIterator given a query
        @Input: query in SQL syntax
        @Output: returns google.cloud.bigquery.table.RowIterator
        '''
        query_job = self.client.query(query_sql)
        return query_job.result()

    @classmethod
    def connect_to_DB_GCP(cls,key):
        '''
        Establish connection with DB in GCP.
        @Input: path to the key file
        @Output: initializates the class object reutrning the google.cloud.bigquery.client.Client
        '''
        credentials = service_account.Credentials.from_service_account_file(key)
        project_id = 'nwo-sample'
        client = bigquery.Client(credentials= credentials,project=project_id)
        return cls(client)

class DatasetPandas2Torch(Dataset):
    '''
    Class object Dataset to pass data from pandas to Pytorch Dataloader
    @Input: Pandas dataframe
    @Output: DataLoader calls with method __getitem__ to retrieve samples of the dataframe
    '''
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return (len(self.data))

    def remove_emoji(self,string):
        '''
        Method to remove all emojis in one tweet
        @Input: tweet in string format
        @Output: returns string without emojis
        '''
        emoji_pattern = re.compile("["
                                  u"\U0001F600-\U0001F64F"  # emoticons
                                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                  u"\U00002500-\U00002BEF"  # chinese char
                                  u"\U00002702-\U000027B0"
                                  u"\U00002702-\U000027B0"
                                  u"\U000024C2-\U0001F251"
                                  u"\U0001f926-\U0001f937"
                                  u"\U00010000-\U0010ffff"
                                  u"\u2640-\u2642"
                                  u"\u2600-\u2B55"
                                  u"\u200d"
                                  u"\u23cf"
                                  u"\u23e9"
                                  u"\u231a"
                                  u"\ufe0f"  # dingbats
                                  u"\u3030"
                                  "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def preprocess(self,tweet):
        '''
        Method with a set of commands to clean tweets
        '''
        # Convert all text to lowercase
        #data['tweet'] = data['tweet'].apply(lambda sentence: sentence.lower())
        # remove symbols, exclamation marks... --> '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        #data['tweet'] = data['tweet'].apply(lambda sentence: re.sub('[%s]' % re.escape(string.punctuation), '', sentence))
        # remove line breaks special characters
        tweet = re.sub('[\t\n\r\f\v]' , '', tweet)
        tweet = tweet.replace(u'\xa0', u' ')
        # Remove URL from tweets
        tweet = re.sub(r"http\S+", "", tweet)
        # Remove hashtags
        tweet = re.sub(r"#\S+", "", tweet)
        # Remove pic links
        tweet = re.sub(r'pic.twitter.com/[\w]*',"", tweet)
        # Remove emojis
        tweet = self.remove_emoji(tweet)
        # Substitute multiple white spaces characters for one
        tweet = re.sub(' +' , ' ', tweet)
        return tweet.strip()

    def __getitem__(self,idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        return self.preprocess(self.data['tweet'][idx]), self.data['tweet_id'][idx]
