# This is a script for the second dataset
import pandas as pd
import spacy

data = pd.read_csv("C:/Users/anast/Desktop/Thesis/Datasets/Searching/2/g28.txt", header=None, sep="\t")

nlp = spacy.load('en_core_web_lg')

# Save Dependency Parsing in svg for better visualization
# for i in range(0, data.__len__()):
#     text = data.iloc[i, 0]
#     doc = nlp(text)
#     svg = displacy.render(doc, style="dep", jupyter=False)
#     saveParserAsSVG.save_svg(svg, f"C:/Users/anast/Desktop/Thesis/Experiments/2/g28/parse{i}.svg")

dataTransformed = []

for i in range(0, data.__len__()):
    text = data.iloc[i, 0]
    doc = nlp(text)
    newSentence = []
    newSentence.append((doc[1].text).capitalize())

    iFlag = False
    commaFlag = False
    toFlag = False
    nounFlag = False
    beFlag = False

    for j in range(2, doc.__len__()):
        prevToken = doc[j-1]
        token = doc[j]
        if (token.pos_ == "PUNCT" and commaFlag == False):
            commaFlag = True
            continue
        elif (token.text == "I" and iFlag == False):
            iFlag = True
            continue
        elif (token.text == "I"):
            newSentence.append("he")
            continue
        elif (token.text == "my"):
            newSentence.append("his")
            continue
        elif (token.text == "myself"):
            newSentence.append("himself")
            continue
        elif (token.text == "me"):
            newSentence.append("him")
            continue
        elif (token.text == "am" or token.text == "'m"):
            newSentence.append("is")
            continue
        elif (token.text == "don't"):
            newSentence.append("doesn't")
            continue
        elif (token.text == "have" and (prevToken.pos_ != "AUX" and prevToken.text != "to" )):
            newSentence.append("has")
            continue
        elif (token.text == "want" or token.text == "need"):
            if (doc[j+1].text == "to" and doc[j+2].text == "be" and doc[j+3].text == "able"):
                toFlag = True
                newSentence.append("must")
                continue
            elif (doc[j+1].text == "to" and doc[j+2].text == "have" and doc[j+3].text == "the" and doc[j+4].text == "ability"):
                toFlag = True
                newSentence.append("must") # edw exw provlima me to to
                continue
            elif (doc[j+1].text != "to"):
                newSentence.append("must be able to have")
                nounFlag = True
                continue
            else:
                newSentence.append("must be able")
            continue
        elif(newSentence[newSentence.__len__() - 1] == "he" and token.pos_ == "VERB"):
            verb = token.text + "s"
            newSentence.append(verb)
            continue
        elif (toFlag == True):
            toFlag = False
            continue
        elif (token.text == "to" and nounFlag == True and (prevToken.pos_ == "NOUN" or prevToken.pos_ == "PROPN") ):
            if (doc[j+1].text == "be"):
                beFlag = True
            if (prevToken.text == "access"):
                newSentence.append(token.text)
                continue
            else:
                continue
        elif (beFlag == True):
            beFlag = False
            continue
        else:
            newSentence.append(token.text)
    print(newSentence)
    newString = ""
    for token in newSentence:
        newString = newString + token + " "
    dataTransformed.append(newString)

print(dataTransformed)

df = pd.DataFrame(dataTransformed)
print(df)
df.to_csv('C:/Users/anast/Desktop/Thesis/DatasetTransformation/2/g28.csv', header=None)