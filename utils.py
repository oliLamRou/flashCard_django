import hashlib
from uuid import uuid4
import pandas as pd

def split_and_add_id():
    ##WARINING!!!
    df = pd.read_csv('db.csv')
    # for i in df.index:
    #     df.loc[i, 'id'] = uuid4()
    #     pass
    
    # df[['id', 'created', 'word', 'translation']].to_csv('words.csv', index=False)
    # df[['id', 'last_try', 'fail', 'success']].to_csv('user.csv', index=False)
    # print(df)

if __name__ == '__main__':
    df = pd.read_csv('words.csv')
    df['id'] = df['id'].fillna('')
    for i in df.index:
        if df.loc[i, 'id'] == '':
            df.loc[i, 'id'] = uuid4()

    print(df)
    df.to_csv('words_.csv', index=False)
    