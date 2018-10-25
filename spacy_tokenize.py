# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 21:29:18 2018

@author: arjunb
"""

import os, sys, spacy


def main():
    
    nlp = spacy.load('en_core_web_sm')
    directory = sys.argv[1]
    if 'traindata' in directory:
        print('You made a mistake. NEVER run this on the training data!!!')
        sys.exit(0)
    
    for filename in os.listdir(directory):
        file = open(directory+'/'+filename, encoding='utf-8')
        lines = [line.strip() for line in file.readlines()]
        file.close()
        
        filepath = os.path.join(directory+'/'+filename)
        file = open(filepath, 'w', encoding='utf-8')
        lines = [nlp(line) for line in lines]
        for line in lines:
            if len(line) > 0:   
                for token in line[:-1]:
                    file.write(token.text+' ')
                file.write(line[-1].text+'\n')
        file.close()
    
    

if __name__ == "__main__":
    main()