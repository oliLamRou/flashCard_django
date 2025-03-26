import os
from pathlib import Path
import hashlib

import pandas as pd
import asyncio
from googletrans import Translator

from _CONSTANT import *

async def translate_text(word):
    translator = Translator()
    return await translator.translate(word, src="fr", dest="ko")
    
path = Path(__file__)
dir = path.parent.absolute()
db = os.path.join(dir, 'db.csv')

class FlashCard:
    def __init__(self):
        self.df = None
        self.stack = None
        self.translator = Translator()
        self._load()

    #DB
    def _load(self):
        if os.path.isfile(db):
            self.df = pd.read_csv(db)
        else:
            self.df = pd.DataFrame(columns=COLUMNS)

    def _save(self):
        self.df.sort_values(LANGUAGE_A).to_csv(db, index=False)

    def get(self):
        pass

    def edit(self):
        pass

    def add(self):
        #check if not empty
        #check if already exist
        
        os.system('clear')

        word = input('word: ')
        word = word.lower()
        if word in self.df[LANGUAGE_A].unique():
            print('Attention le mot existe déjà')

        translation = asyncio.run(translate_text(word))
        translation = input(translation.text) or translation.text

        row = pd.Series({
            LANGUAGE_A: word,
            LANGUAGE_B: translation,
            'created': pd.Timestamp.now().as_unit('s'),
            'success': 0,
            'fail': 0,
            }).to_frame().T
        self.df = pd.concat([self.df, row]).reset_index(drop=True)

    def play(self):
        while True:
            os.system('clear')
            row = self.df.sample(1).iloc[0]
            
            input(f'{row.LANGUAGE_A} (enter to see answer)')

            print(f'{row.LANGUAGE_A} -> {row.translation} \n')
            self.menu(MENU_GUESS)
            answer = input('answer: ')
            
            self.df.loc[row.name, 'last_try'] = pd.Timestamp.now().as_unit('s')
            if answer == '1':
                self.df.loc[row.name, 'success'] += 1
                break
            elif answer == '2':
                self.df.loc[row.name, 'fail'] = 1
                break

    def delete(self):
        pass

    def menu(self, choice):
        for i in range(len(choice)):
            print(f'{i+1}: {choice[i]}')

    def main(self):
        while True:
            os.system('clear')
            print(self.df[[LANGUAGE_A, LANGUAGE_B]], '\n')
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