
import numpy as np
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping
import os

# Parameters
words = 100000
review_len = 128
vec_len = 300
patience = 5
batch_size = 15
epochs = 60
model_name = "mdl_reutersv3.h5"

def main():
    train()
    test()


def train():
    
    # Load data
    X, y = build_dataset(review_len)

    # Build model
    model = build_model(words, vec_len, review_len)

    # Early stopping
    early_stopping_monitor = EarlyStopping(patience=patience, monitor="loss", mode="auto")

    # Fit model
    model.fit(X, y, epochs=epochs, callbacks=[early_stopping_monitor], batch_size=batch_size, verbose=1, validation_split=0.25)

    # Export
    model.save(model_name)
    print("Model successfully exported!")


######
#TEST#
######

from keras.preprocessing import sequence
from keras.models import load_model

def test():

    test_values = pd.read_csv(r"C:\Repos\reddit-capstone\reddit-capstone\reddit-capstone\upliftingnews_senti_testdata.csv")
    titles = test_values["title"]
    # Parameters
    review_len = 128

    # Model
    model = load_model(model_name)

    #titles = [
    #    "Homeless man's selfless act caught on camera",
    #    "'Tree man' Abul Bajandar to get government-funded surgery",
    #    "Dog thought to be dead brought back to life by Vancouver firefighters",
    #    "Rhonda Farley says she's just another mom. But those who know her say she is so much more than that. 'Saint', 'queen', and 'great woman' are all superlatives used to describe her.",
    #    "Canadian Rangers travel more than 100 kilometres in severe weather to rescue fisherman",
    #    "Vet calms a crying puppy after surgery",
    #    "Inspiration for the Teddy Bear taken off threatened species list.",
    #    "Aminah Hart tracked down and married sperm donor",
    #    "College Student, 24, Pays Off Grandparents' Mortgage by Saving Money Eating Microwave Pizza and Skipping Parties",
    #    "78-year-old grandmother goes viral after deadlifting 245lbs",
    #    "World's first Pastafarian wedding takes place in New Zealand",
    #    "Lamborghini grants wish of dying child to drive in a pink Lamborghini Aventador with Richard Hammond from Top Gear",
    #    "No Gray Area: Autistic Artist Shares His World of Vibrant Colors",
    #    "Labrador Helps Save Arizona Man Stranded in Snowstorm",
    #    "Nonverbal boy with autism falls in love with Snow White",
    #    "Police officer rewards young girls for turning in stolen cash",
    #    "Ten years ago, Marlie Casseus had 16-pound facial tumor removed at Jackson Memorial hospital; she returns to thank the team that saved her life",
    #    "Boy who saw world upside down due to rare condition has lifesaving op thanks to kindhearted Brit",
    #    "Happening right meow: New York puts bill before both the Senate and Assembly which would ban declawing of cats making it the first state to do so",
    #    "Lowes hires a man with a brain injury and a service dog, under one condition.",
    #    "Egg Industry Promises to Stop Grinding Up Millions of Living Baby Chickens",
    #    "China fits final piece on world's largest radio telescope",
    #    "Women and children who are victims of domestic violence in NSW will soon be able to flee their homes faster and without penalty for abandoning a rental property.",
    #    "man prevents ISIS suicide bomber from killing more civilians By hugging him.",
    #    "George Zimmerman punched in the face for bragging about killing Trayvon Martin",
    #    "Volunteers help flood survivors restore irreplaceable photos.",
    #    "Millions in U.S. Climb Out of Poverty, at Long Last",
    #    "Mom celebrates 'rainbow baby' with stunning photo shoot after 6 miscarriages",
    #    "The Worldâ€™s First Six-Pack Ring That Fish Can Eat",
    #    "Joyce to the world: Skateboard community celebrates â€˜Grandmother of Hastingsâ€™",
    #    "Green Bay police officer buys food for boy accused of shoplifting",
    #    "High School Cross Country Runner helps his rival with autism to the finish line",
    #    "Penguin Bloom: how a scruffy magpie saved a family",
    #    "New Zealand Gang that makes Children's school sandwiches tells Meth/Ice dealers to leave their town or else.",
    #    "Office Depot to Close for Thanksgiving",
    #    "10 yo becomes the youngest International Master in Chess history",
    #    "Baton Rouge video game store to play 24 hours to raise money for children's hospital",
    #    "Farmer saves cows trapped on tiny patch of turf after earthquake",
    #    "The Guardian view on social media: facts need to be labelled as facts | Editorial | Opinion",
    #    "Virtual reality to aid Auschwitz war trials of concentration camp guards",
    #    "Turkish Construction Workers Rescue A Bear Who Got Itself Trapped Underground. [Video in the comments).",
    #    "'Iron man' bystander saves young boy with seconds to spare after Thames plunge",
    #    "Germany launches World's first crowdfunded train service",
    #    "Viola Davis will inspire you with her moving words on finding confidence at 51",
    #    "Armless teen receives best holiday gift; prosthetic drumsticks made by UF students",
    #    "$125,000+ raised as Children Hospital of Wisconsin mailed donors a rock with every $85 donation. Nordstrom donated $50,000",
    #    "This 'Unsung Hero' was a convicted murderer until Gov. Brown set him free immediately â€” he was approved for parole by Gov. Jerry Brown after he helped a group of civilians to safety during a prison riot",
    #    "Campaign reminds people of rule that everyone is an organ donor unless they say no",
    #    "canadian man spends C$1.5m to help settle 58 families from syria" ]

    results = predict(titles, model)

    results_df = pd.DataFrame({"title":titles, "sentiment_prob": list(results)})
    results_df["sentiment"] = results_df["sentiment_prob"].apply(lambda x: 1 if x>0.5 else 0)
    print(results_df)
    print(sum(results_df["sentiment"])/len(results_df))

def encode_pred(arr):
    result = []
    for sentence in arr:
        result.append(encode_sentence(sentence))
    return sequence.pad_sequences(result, maxlen=review_len)

def predict(values, model):
    values_encode = encode_pred(values)
    result = model.predict(values_encode, batch_size=len(values_encode), verbose=0)
    return result



#######
#MODEL#
#######

from keras.models import Sequential
from keras.layers import MaxPooling1D, Conv1D, Flatten, Dropout, Dense
from keras.layers.embeddings import Embedding


def build_model(words, vec_len, review_len):
    model = Sequential()
    model.add(Embedding(words, vec_len, input_length=review_len))
    model.add(Dropout(0.25))
    model.add(Conv1D(32, 3, padding="same"))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(16, 3, padding="same"))
    model.add(Flatten())
    model.add(Dropout(0.25))
    model.add(Dense(100, activation="sigmoid"))
    model.add(Dropout(0.25))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.summary()
    return model

import pandas as pd
from keras.datasets import reuters
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence

#word_dict = imdb.get_word_index()
word_dict = reuters.get_word_index()

def encode_sentence(text):
    result = []
    arr = text_to_word_sequence(text, lower=True, split=" ")  # returns list of words (like split)
    for word in arr:
        w = encode_word(word)
        if w is not None:
            result.append(w)
    return result


def encode_word(word):
    if word not in word_dict:
        return None
    return word_dict[word]


def build_dataset(max_len):
    # response y = sentiment (1-positive or 0-negative), X = text
    df = pd.read_csv("reddit-capstone/reddit_both_labeled.csv", delimiter=",", names=["X", "y"], usecols=[8,11], header=0, nrows=10000)
    Xts = df["X"].values
    arr = []
    for text in Xts:
        arr.append(encode_sentence(text))
    X = sequence.pad_sequences(arr, maxlen=max_len)
    y = df["y"].values
    return (X, y)


if __name__=="__main__":
    main()