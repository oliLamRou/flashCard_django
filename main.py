import os
from pathlib import Path
import hashlib
from uuid import uuid4

import pandas as pd
import asyncio
from googletrans import Translator

from _CONSTANT import *

async def translate_text(word):
    translator = Translator()
    return await translator.translate(word, src="fr", dest="ko")
    
path = Path(__file__)
dir = path.parent.absolute()
words_path = os.path.join(dir, 'words.csv')
user_path = os.path.join(dir, 'user.csv')

class FlashCard:
    def __init__(self):
        self.words = None
        self.user = None
        self.stack = None
        self.translator = Translator()
        self._load()

    #DB
    def _load(self):
        #WORDS
        if os.path.isfile(words_path):
            self.words = pd.read_csv(words_path)
        else:
            self.words = pd.DataFrame(columns=WORDS_COLUMNS)

        #USER
        if os.path.isfile(user_path):
            self.user = pd.read_csv(user_path)
            self.user['fail'] = self.user['fail'].astype('int32')
            self.user['success'] = self.user['success'].astype('int32')
        else:
            self.user = pd.DataFrame(columns=USER_COLUMNS)

    def _save(self):
        self.words.sort_values(LANGUAGE_A).to_csv(words_path, index=False)
        self.user.to_csv(user_path, index=False)

    def get(self):
        pass

    def edit(self):
        pass

    def add(self):
        os.system('clear')

        word = input('word: ')
        word = word.lower()
        if word in self.words[LANGUAGE_A].unique():
            print('Attention le mot existe déjà')

        translation = asyncio.run(translate_text(word))
        translation = input(translation.text) or translation.text

        row = pd.Series({
            'id': uuid4(),
            LANGUAGE_A: word,
            LANGUAGE_B: translation,
            'created': pd.Timestamp.now().as_unit('s'),
            }).to_frame().T
        self.words = pd.concat([self.words, row]).reset_index(drop=True)

    def play(self):
        #Add fail and success AB vs BA

        self.user.set_index('id', inplace=True)

        while True:
            os.system('clear')
            '''
                sample all first timer
                get 10% of positive ratio
                get 50% of negative ratio
                random pick one
            '''
            unguessed = self.words[~(self.words['id'].isin(self.user.index))]
            
            positive_id = self.user[(self.user['success'] > self.user['fail'])].sample(frac=0.1).index
            positive = self.words[(self.words['id'].isin(positive_id))]
            
            negative_id = self.user[(self.user['fail'] > self.user['success'])].sample(frac=0.3).index
            negative = self.words[(self.words['id'].isin(negative_id))]

            words = pd.concat([unguessed, positive, negative])            
            
            if words['id'].size < 1:
                words = self.words
                
            row = words.sample(1).iloc[0]

            if row.id in self.user.index:
                # print(self.user.loc[row.id, 'fail'])
                print(f"failed: {self.user.loc[row.id, 'fail']} // success: {self.user.loc[row.id, 'success']}")
            else: 
                print('new word')

            input(f'{row[LANGUAGE_A]} (enter to answer)')

            print(f'{row[LANGUAGE_A]} -> {row[LANGUAGE_B]} \n')
            self.menu(MENU_GUESS)
            answer = input('answer: ')
            
            
            self.user.loc[row.id, 'last_try'] = pd.Timestamp.now().as_unit('s')
            self.user.fillna(0, inplace=True)
            if answer == '1':
                previous = self.user.loc[row.id, 'success']
                self.user.loc[row.id, 'success'] = previous + 1
            elif answer == '2':
                previous = self.user.loc[row.id, 'fail']
                self.user.loc[row.id, 'fail'] = previous + 1
            else:
                break
        
        self.user.reset_index(inplace=True)

    def delete(self):
        pass

    def menu(self, choice):
        for i in range(len(choice)):
            print(f'{i+1}: {choice[i]}')

    def main(self):
        while True:
            os.system('clear')
            print(self.words[[LANGUAGE_A, LANGUAGE_B]].tail(5), '\n')
            self.menu(MENU_HOME)
            input1 = input()

            #Quit
            if input1 == 'q':
                break

            #Only difit from here
            if not input1.isdigit():
                continue

            #MENU
            if MENU_HOME[int(input1) - 1] == 'add':
                self.add()
            elif MENU_HOME[int(input1) - 1] == 'play':
                self.play()
            
        self._save()

if __name__ == '__main__':
    fc = FlashCard()
    fc.main()