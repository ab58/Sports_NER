Named Entity Recognition Modeling with Sports Articles!

Hi everyone. This is my first dive into Python's spaCy library, which is designed for development ogf powerful industry-grade
Natural Language Processing applications. I am trying out the basic tokenization pre-processing method, and then attempting the much
more complex task of Named Entity Recognition (NER). For NER, pre-processing of text is usually minimal, since the loss of information
such as capital letters, punctuation and stopwords all serve as vital anchors for predicting which words (or word sequences) are likely 
to be named entities, and which ones are not. Therefore, simple tokenization where punctuation is separated from the lexical items is the
only pre-processing I have done on the raw text.

My data consists of game recap articles popularly found in newspapers, on websites, etc. These articles appear in a structured yet highly
variable format, and so are perfect for analysis for named entities and doing tasks in NER and NEE (Named Entity Extraction). The particular 
training data I am using thus far are NFL game recap articles for the 2018 NFL regular season. Each week of the NFL season features 13-16 
games, meaning there are 13-16 game recap articles produced each week during the 17-week season. I have gathered as much of these as I can
get thus far from https://cbssports.com. All of the articles have extensive mentions of named entities of various named entity categories.
According to pre-trained labels that I have made myself, I have trained the data by putting it through an empty spaCy NER model, and displayed 
the results using the displaCy functionality within spaCy.

First, I pre-processed my data by running a precursor script, spacy_tokenize.py. This script takes in a directory containing text files 
that are untokenized (as in, still in normal written form, punctuation not separated from lexical items and things like that), and replaces 
each file with a new file, fully tokenized according to spaCy's built-in tokenization algorithm. This script may take in files that have
already been fully tokenized; in this case, there is no change made once put through the algorithm, and the replacement file will end up
being identical to the file fed into the script.

The fully tokenized files appear in the directory 2018_nfl_reg_season. After I tokenized all the files, I manually copied them over into 
the directory game_recap_traindata. These files at first glance look identical to those in 2018_nfl_reg_season. But they are not. They are
actually in tab-separated format, with 2 columns. The first column (before the tab) is the same as all the lines of text of the corresponding
file in 2018_nfl_reg_season. The second column (after the tab) are my personal annotations of all the Named Entities contained in each line
of the file. I manually did all of these annotations, and tried to make my NER categories as general as possible. The most common categories
are PLAYER and TEAM, while a less common one is BOSS; The BOSS tag is mainly used when a coach is mentioned. However, I could not use COACH
as the tag because I also wanted to capture possible mentions of general managers, team owners and executives, and even referees and official
people in other capacities. Therefore my BOSS tag is sort of a catch-all in this respect. There are other named entities for which these 3
categories cannot match, so I had to invent a few as I went along if there was no appropriate category to place it in. Song titles are 
sometimes mentioned, so there is a category for that. Celebrities and dances and cities, states and countries are mentioned as well, so there
are tags for that. A challenging problem is whether a name of a city is meant ot be a reference to a TEAM or to a CITY. This depends on the
context in which the word is used, so the model needs lots of data points in which city names are tagged as TEAM, and plenty where they're tagged
as CITY as well, in order to accurately disambiguate this.

The NER annotations are in the format that the spaCy NER model accepts. That is, the first index of the NE (inclusive), the last index 
of the NE (exclusive), followed by the named entity category it belongs to. An example annotation is as follows:

Ben Roethlisberger throws 2 TDs to Antonio Brown as the Pittsburgh Steelers defeat the Miami Dolphins .  0,18,PLAYER;35,48,PLAYER;56,75,TEAM;87,101,TEAM

The main script, sports_ner.py, takes in the directory containing the full annotated files (to be used as training data) and another 
directory argument containing un-annotated game recap articles to run the trained model on. I first gather all the training data text and
separate them into the text strings and their corresponding named entity tags, making sure they map onto each other. To train the model,
I first initialize an empty spaCy NER model, and make the necessary configurations before initializing the NER training function. Then 
in a loop, I do a random shuffle of the training data, a hard-coded number of times. For now this is just 1 shuffle, although the spaCy
tutorial recommends at least 20 shuffles. I found this to take a very long time with the amount of data I have though, so I have opted 
for just one shuffle to ease training time and get an idea of a baseline accuracy for my model that will only be improved with more 
iterations of random shuffling. I call the spacy update() function using the separated structures of the training text lines, the parallel
list of the named entities for each line, and put it through the optimized NER trainer. The part of the script consists of going through
the second directory, of the plain text files without annotations, and attempting to predict the named entities. Whatever is in the plain
directory that has been used as an annotated training file, I consider this "seen data", and accuracies from here are counted towards my
"training accuracy. Whatever is in the plain directory that has not been used as an annotated training file, I consider to be "unseen 
data", and accuracies from these files are counted towards "test accuracy" for my model.

I have uploaded an Excel spreadsheet which outlines my baseline accuracies for the model; for this initial file, I only have 5 weeks' 
worth of data from the 2018 NFL season. Weeks 1-4 I have fully annotated, and serve as my training files. Week 5 I have not yet annotated
as of 10/25/18, and at this point these files serve as my test data. This is for only one random shuffling and a single model update of
the training data. The model accuracy should increase with more variation added through more random shuffles and updates, but training would
take a longer time depending on how many shuffles, so I have provided these preliminary results here to give you an idea of how well my 
model is working with only 1/4 of the NFL season to work with as training data, and only one level of variation added to train the model.

I will come up with more updates as I annotate more data for this, and I'm hoping for a bit of transfer learning to occur here where this
can accurately produce NER results for not just football, but ANY sport!
