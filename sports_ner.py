# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 17:09:25 2018

@author: arjunb
"""

import sys, os, spacy, random, time
from spacy import displacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer


def evaluate(ner_model, examples):
    
    scorer = Scorer()
    for sents, ents in examples:
        doc_gold = ner_model.make_doc(sents)
        gold = GoldParse(doc_gold, entities=ents['entities'])
        pred_value = ner_model(sents)
        scorer.score(pred_value, gold)
    return scorer.scores


def main():
    
    train_dir = sys.argv[1]
    training_data = []
    ner_labels = set([])
    
    for article in os.listdir(train_dir):
        #print("training with file "+article)
        f = open(train_dir+'/'+article, encoding='utf-8')
        lines = [line.rstrip() for line in f.readlines()]
        
        for line in lines:
            line_split = line.split('\t')
            sentence = line_split[0] #a string
            print(sentence)
            entities = []
            if len(line_split) > 1:
                entities = line.split('\t')[1].split(';') #a list of strings of format
            #start_index,end_index,label
            #print(entities)
            
            ent_tuples = []
            for ent in entities:
                ent_components = ent.split(',')
                start_index = int(ent_components[0])
                end_index = int(ent_components[1])
                label = ent_components[2]
                ner_labels.add(label)
                #now we need to put start_index, end_index, and label into a tuple
                ent_tuple = (start_index, end_index, label)
                #print(ent_tuple)
                ent_tuples.append(ent_tuple)
            
            #print(ent_tuples)
            
            #now we convert entities into a dict with one k-v pair;
            #the key will be the string literal 'entities', the value 
            #will be the tuple list ent_tuples
            entities = {'entities' : ent_tuples}
            
            #finally, we combine sentence and entities into a tuple,
            #and append this to the training data
            training_data.append((sentence, entities))
            
            f.close()
            
        
        #for training_instance in training_data:
        #    print(training_instance)
        
        print("TOTAL TRAINING EXAMPLES: "+str(len(training_data)))
            
        
    #we have the training data in the correct format to train a spacy
    #NER model; train it as per the spacy tutorial
        
    nlp = spacy.blank('en')
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
        
    for label in ner_labels:
        ner.add_label(label)

    print('training spacy model')
    optimizer = nlp.begin_training()
    
    tic = time.time()
    for i in range(1):
        random.shuffle(training_data)
        for sentence, entities in training_data:
            print('UPDATE SHUFFLE '+str(i+1))
            print(sentence)
            nlp.update([sentence], [entities], sgd=optimizer)
    
    toc = time.time()
    running_time = toc - tic
    hours = running_time // 3600
    running_time %= 3600
    minutes = running_time // 60
    running_time %= 60
    seconds = int(running_time)
    print("Total Training Time: %d hours, %d minutes, %d seconds." % (hours, minutes, seconds))    
    
    results = evaluate(nlp, training_data)
    print(results)
        
    test_dir = sys.argv[2]
    for filename in os.listdir(test_dir):
        with open(test_dir+'/'+filename) as test_file:        
            test = nlp(test_file.read())
            test_list = []
            for token in test:
                test_list.append(token.text)
                test = ' '.join(test_list)
        
        doc = nlp(test)
        displacy.serve(doc, style='ent')
        
            
            
        
    
    
if __name__ == "__main__":
    main()