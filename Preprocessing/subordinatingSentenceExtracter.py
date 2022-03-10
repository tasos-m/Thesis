# This is a script for the second dataset transformation
import pandas as pd
import spacy

data = pd.read_csv('C:/Users/anast/Desktop/Thesis/DatasetTransformation/2/g05.csv', header=None)
data = data.iloc[:, 1]

nlp = spacy.load('en_core_web_lg')

dataTransformed = []
for i in range(0, data.__len__()):
    text = data.iloc[i]
    doc = nlp(text)
    firstSentence = []
    secondSentence = []
    firstSentenceString = ""
    secondSentenceString = ""
    soFlag = False
    # Check if the sentence has a subordinating sentence
    for j in range(0, doc.__len__()):
        token = doc[j]
        if (token.text == "so" and token.pos_ == "SCONJ"):
            soFlag = True
            pos = j
            break

    # If yes, split in two sentences
    if (soFlag):
        # Find the actor
        for j in range(0, doc.__len__()):
            token = doc[j]
            if (token.dep_ == "nsubj"):
                posSubject = j
                break
        actor = ""
        for j in range(0, posSubject+1):
            token = doc[j]
            actor = actor + token.text + " "
        # Find the second actor if exists
        # do somehow

        # Save the first sentence
        for j in range(0, pos):
            token = doc[j]
            if (token.pos_ == "PUNCT" and token.text == ","):
                break
            firstSentence.append(token.text)
        firstSentence.append(".")

        # Save the second sentence
        for j in range(pos+1, doc.__len__()):
            token = doc[j]
            if (token.text == "he" and token.dep_ == "nsubj"):
                secondSentence.append(actor)
                continue
            elif (token.dep_ == "nsubj"):
                secondSentence.append((token.text).capitalize())
                continue
            elif (token.text == "that"):
                continue
            elif (token.text == "can"):
                secondSentence.append("must be able to")
                continue
            else:
                secondSentence.append(token.text)
        # Save the two sentences as strings
        for token in firstSentence:
            firstSentenceString = firstSentenceString + token + " "
        for token in secondSentence:
            secondSentenceString = secondSentenceString + token + " "
        # Append them in the new dataset
        dataTransformed.append(firstSentenceString)
        dataTransformed.append(secondSentenceString)
    else:
        firstSentence = text
        dataTransformed.append(firstSentence)

print(dataTransformed)

df = pd.DataFrame(dataTransformed)
print(df)
df.to_csv('C:/Users/anast/Desktop/Thesis/DatasetTransformation/2/g05v2.csv', header=None)