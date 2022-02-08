# Function of the Ontology Storing
import pandas as pd
import spacy
import codecs
import os

def ontology(inputPath, outputPath, numFiles, saveMode):
    # Language model
    nlp = spacy.load('en_core_web_lg')
    # Verbs that go with prepositions
    with open('C:/Users/anast/Desktop/Thesis/MachineLearning/verbList.txt') as v:
        verbList = v.read().splitlines()
    for k in range(1, numFiles + 1):
        # Import Dataset
        if numFiles == 1:
            data = pd.read_csv(f"{inputPath}", header=None, sep='\t')
        else:
            data = pd.read_csv(f"{inputPath}/{k}.txt", header=None, sep='\t')
        # print('File: ', k)
        dataTransformed = []
        # For every sentence in the file apply the below algorithm
        for i in range(0, data.__len__()):
            # print(i)
            text = data.iloc[i, 0]
            # print(text)
            doc = nlp(text)

            # Lists Definition
            # Actor
            actors = []
            # Action
            actions = []
            actionsPositions = []
            # Object
            objects = []
            objectsPositions = []
            actionsWithObjects = []
            actionsWithObjectsLemma = []

            # ---- Actors ----
            for j in range(0, doc.__len__()):
                token = doc[j]
                if token.pos_ == "DET":
                    continue
                else:
                    actors.append(token.text)
                    if token.dep_ == "nsubj":
                        firstSubjectPos = j
                        break

            # Check for second actor
            secondActorFlag = False
            for j in range(0, doc.__len__()):
                token = doc[j]
                if token.dep_ == "conj" and token.head.text == doc[firstSubjectPos].text:
                    secondActorFlag = True
                    secondSubjectPos = j
                    break
            if secondActorFlag:
                for j in range(firstSubjectPos + 1, secondSubjectPos):
                    token = doc[j]
                    actors.append(token.text)


            # Make the actors list a string
            actorsString = " ".join(actors)
            actorsString = actorsString.lower()
            # print(actors)

            # Actor Lemma
            txt = nlp(actorsString)
            actorsLemma = []
            for tok in txt:
                actorsLemma.append(tok.lemma_)
            actorsLemmaString = " ".join(actorsLemma)

            # ---- Action ----
            for j in range(0, doc.__len__()):
                token = doc[j]
                if token.pos_ == "VERB" and token.dep_ == "xcomp" and token.head.text == "able":
                    actions.append(token.text)
                    actionsPositions.append(j)
                if token.pos_ == "VERB" and token.dep_ == "acl" and token.head.text == "ability":
                    actions.append(token.text)
                    actionsPositions.append(j)

            # Case: Action detected is the verb have, causative or passive voice
            # probably works for a bunch of cases
            tempObjFlag = False
            for action in actions:
                # if action in ["have", "know"]:
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ in ["ccomp", "xcomp"] and token.head.text == action:
                        actions.append(token.text)
                        actionsPositions.append(j)
                        verbList.append(token.text)
                    if token.dep_ == "dobj" and token.head.text == action:
                        tempObjFlag = True
                        tempObjPos = j
            if tempObjFlag:
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "relcl" and token.head.text == doc[tempObjPos].text:
                        actions.append(token.text)
                        actionsPositions.append(j)
            # Passive voice
            for j in range(0, doc.__len__()):
                token = doc[j]
                if token.dep_ == "auxpass":
                    auxpass = token.head.text
                    if auxpass not in actions:
                        actions.append(auxpass)
                        for m in range(0, doc.__len__()):
                            if doc[m].text == auxpass:
                                actionsPositions.append(m)
            # Find the other actions
            for action in actions:
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.pos_ == "VERB" and token.dep_ == "conj" and token.head.text == action:
                        actions.append(token.text)
                        actionsPositions.append(j)
            # Find actions in subordinating sentences with when/where/which etc
            for action in actions:
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "advcl" and token.head.text == action:
                        actions.append(token.text)
                        actionsPositions.append(j)
            # Find actions that are in this format select/deselect -> finds deselect
            for j in actionsPositions:
                if j + 1 >= doc.__len__() or j + 2 >= doc.__len__() or j - 1 < 0 or j - 2 < 0:
                    continue
                else:
                    if doc[j + 1].text == "/":
                        actions.append(doc[j + 2].text)
                    elif doc[j - 1].text == "/":
                        actions.append(doc[j - 2].text)

            # Special case: log in,log out, sign in, sign up, sign out
            # value -> position of the action in the sentence
            # count -> position of the action in the actions and actionsPositions lists
            for count, value in enumerate(actionsPositions):
                if value - 1 < doc.__len__():
                    if actions[count] in ['log', 'sign'] and doc[value + 1].text in ['in', 'up', 'out']:
                        actions[count] = actions[count] + " " + doc[value + 1].text

            actionsString = ",".join(actions)
            actionsString = actionsString.lower()

            # Lemmatized actions
            actionLemma = []
            for action in actions:
                txt = nlp(action)
                if txt.__len__() > 1:
                    actionLemma.append(txt[0].lemma_ + " " + txt[1].text)
                else:
                    actionLemma.append(txt[0].lemma_)

            actionLemmaString = ",".join(actionLemma)

            # ---- Objects ----

            for j in range(0, doc.__len__()):
                token = doc[j]
                for action in actions:

                    # use the nlp model to extract the action lemma
                    txt = nlp(action)

                    if token.dep_ == "dobj" and token.head.text == action:
                        objects.append(token.text)
                        objectsPositions.append(j)
                        actionsWithObjects.append(action + "/" + token.text)
                        actionsWithObjectsLemma.append(txt[0].lemma_ + "/" + token.lemma_)
            # Special cases
            # verbs that go with prepositions
            prepFlag = False
            for action in actions:
                action = action.lower()

                # use the nlp model to extract the action lemma
                txt = nlp(action)

                if action in verbList or txt[0].lemma_ in verbList:
                    for j in range(0, doc.__len__()):
                        token = doc[j]
                        if token.dep_ == "prep" and token.head.text == action:
                            prepFlag = True
                            prepPos = j
                        if prepFlag == True and token.dep_ == "pobj" and token.head.text == doc[prepPos].text:
                            objects.append(token.text)
                            objectsPositions.append(j)
                            actionsWithObjects.append(action + "/" + token.text)
                            actionsWithObjectsLemma.append(txt[0].lemma_ + "/" + token.lemma_)
            # Save the subject of the subordinating sentence
            for action in actions:

                # use the nlp model to extract the action lemma
                txt = nlp(action)

                for token in doc:
                    if token.dep_ in ["nsubj", "nsubjpass"] and token.head.text == action and token.text not in actors:
                        objects.append(token.text)
                        actionsWithObjects.append(action + "/" + token.text)
                        actionsWithObjectsLemma.append(txt[0].lemma_ + "/" + token.lemma_)
            # Find the other objects
            for foundObject in objects:
                # Find the action that the object is linked to, in order to save the conj objects with the same action too
                for token in doc:
                    if token.text == foundObject:
                        tempAction = token.head.text

                for token in doc:
                    if token.text == tempAction:
                        txt = token.lemma_

                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "conj" and token.head.text == foundObject:
                        objects.append(token.text)
                        objectsPositions.append(j)
                        actionsWithObjects.append(tempAction + "/" + token.text)
                        actionsWithObjectsLemma.append(txt + "/" + token.lemma_)
            # Find objects that are in this format select/deselect -> finds deselect
            for j in objectsPositions:
                # Find the action that the object is linked to, in order to save the conj objects with the same action too
                tempAction = doc[j].head.text

                for token in doc:
                    if token.text == tempAction:
                        txt = token.lemma_

                if j + 1 >= doc.__len__() or j + 2 >= doc.__len__() or j - 1 < 0 or j - 2 < 0:
                    continue
                else:
                    if doc[j + 1].text == "/":
                        objects.append(doc[j + 2].text)
                        actionsWithObjects.append(action + "/" + token.text)
                        actionsWithObjectsLemma.append(txt + "/" + token.lemma_)
                    elif doc[j - 1].text == "/":
                        objects.append(doc[j - 2].text)
                        actionsWithObjects.append(action + "/" + token.text)
                        actionsWithObjectsLemma.append(txt + "/" + token.lemma_)
            # Remove duplicates
            objects = list(dict.fromkeys(objects))

            objectsString = ",".join(objects)
            objectsString = objectsString.lower()
            actionsWithObjectsString = ",".join(actionsWithObjects)
            actionsWithObjectsString = actionsWithObjectsString.lower()
            # print(objects)

            objectLemma = []
            for foundObject in objects:
                txt = nlp(foundObject)
                objectLemma.append(txt[0].lemma_)
            objectLemmaString = ",".join(objectLemma)

            # Find the conj verbs objects if they exist
            # conj case
            # ie:
            conjPos = 0
            hasObject = False
            for action in actions:
                txt = nlp(action)
                for token in doc:
                    if token.head.text == action and token.dep_ == "dobj":
                        hasObject = True
                if not hasObject:
                    for pos, token in enumerate(doc):
                        if token.head.text == action and token.dep_ == "conj":
                            conjPos = pos
                    for token in doc:
                        if token.head.text == doc[conjPos].text and token.dep_ == "dobj":
                            actionsWithObjectsLemma.append(txt[0].lemma_ + "/" + token.lemma_)
            actionsWithObjectsLemmaString = ",".join(actionsWithObjectsLemma)

            # ---- Object Property ----
            objectProperties = []
            for foundObject in objects:
                # Save the object position in the sentence
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.text == foundObject:
                        objPos = j
                # 1st case: save as object property the words between the article (or det dependency) and the object
                # ie: attend some UI / UX lessons -> UI/UX
                # ie: develop an awesome and beautiful features website -> awesome and beautiful features
                detFlag = False
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "det" and token.head.text == foundObject:
                        detPos = j
                        detFlag = True
                if detFlag:
                    for j in range(detPos + 1, objPos):
                        token = doc[j]
                        objectProperties.append(token.text)
                # 2nd case: compound and amod
                if not detFlag:
                    for token in doc:
                        if (token.dep_ == "compound" or token.dep_ == "amod") and token.head.text == foundObject:
                            objectProperties.append(token.text)

                # 3d case: Find prep dependency of the object
                # ie: A Developer must be able to have a jQuery plugin for Core Data Packages .
                # finds: Core Data Packages
                adpFlag = False
                pobjFlag = False
                prepProp = ""
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "prep" and token.head.text == foundObject:
                        adpPos = j
                        adpFlag = True
                        continue
                    if adpFlag:
                        if token.dep_ == "pobj" and token.head.text == doc[adpPos].text:
                            pobjPos = j
                            pobjFlag = True
                if adpFlag and pobjFlag:
                    for j in range(adpPos + 1, pobjPos + 1):
                        token = doc[j]
                        prepProp = prepProp + " " + token.text
                    objectProperties.append(prepProp)
            # 4th case:
            # ie: A user must be able to create a user account by providing a username and a password.
            # finds: username, password
            # ie: A logged in user must be able to mark his bookmarks as public or private
            # finds: public, private
            adpFlag = False
            pcompFlag = False
            dobjFlag = False
            amodFlag = False
            for action in actions:
                for j in range(0, doc.__len__()):
                    token = doc[j]
                    if token.dep_ == "prep" and token.head.text == action:
                        adpPos = j
                        adpFlag = True
                        continue
                    if adpFlag:
                        if token.dep_ == "pcomp" and token.head.text == doc[adpPos].text:
                            pcompPos = j
                            pcompFlag = True
                        # case: mark as public or private
                        elif token.dep_ == "amod" and token.head.text == doc[adpPos].text:
                            objectProperties.append(token.text)
                        elif token.dep_ == "pobj" and token.head.text == doc[adpPos].text:
                            objectProperties.append(token.text)

                if adpFlag and pcompFlag:
                    for j in range(adpPos, doc.__len__()):
                        token = doc[j]
                        if token.dep_ == "dobj" and token.head.text == doc[pcompPos].text:
                            dobjFlag = True
                            dobjPos = j
                            objectProperties.append(token.text)
            # 5th case:
            # country's currency -> finds country
            for foundObject in objects:
                for token in doc:
                    if token.dep_ == "poss" and token.head.text == foundObject and token.pos_ != "PRON":
                        objectProperties.append(token.text)

            # Find the other object properties
            for objectProperty in objectProperties:
                for token in doc:
                    if token.dep_ == "conj" and token.head.text == objectProperty:
                        objectProperties.append(token.text)
            # Remove duplicates
            objectProperties = list(dict.fromkeys(objectProperties))

            for foundObject in objects:
                for objectProperty in objectProperties:
                    if objectProperty == foundObject:
                        objectProperties.remove(objectProperty)
            # print(objectProperties)

            objectPropertiesString = ",".join(objectProperties)
            objectPropertiesString = objectPropertiesString.lower()

            # ----------------------------------------------------------------------
            # Filter the stop words before export
            aoFiltered =[]
            for ao in actionsWithObjectsLemma:
                temp = nlp(ao)
                if temp[-1].is_stop == False and temp[0].text != "be":
                    aoFiltered.append(ao)
            aoFilteredString = ",".join(aoFiltered)
            # ----------------------------------------------------------------------

            # Save the Ontology in different formats
            if saveMode == 'ao-aa':
            # Lemmatized Actions - Objects + Actor - Actions
                actorActionsLemma = []
                for action_Lemma in actionLemma:
                    actorActionsLemma.append(actorsLemmaString + "/" + action_Lemma)
                actorActionsStringLemma = ",".join(actorActionsLemma)
                if numFiles == 1:
                    for l in actorActionsLemma:
                        dataTransformed.append(l)
                    for l in actionsWithObjectsLemma:
                        dataTransformed.append(l)
                    # if actionsWithObjectsLemmaString != '':
                    #     dataTransformed.append(actionsWithObjectsLemmaString)
                else:
                    if actionsWithObjectsLemmaString == '':
                        dataTogetherString = actorActionsStringLemma
                    elif actorActionsStringLemma == '':
                        dataTogetherString = actionsWithObjectsLemmaString
                    else:
                        dataTogether = actionsWithObjectsLemmaString, actorActionsStringLemma
                        dataTogetherString = ",".join(dataTogether)
                    dataTogetherString = dataTogetherString.lower()
                    dataTransformed.append(dataTogetherString)
            elif saveMode == 'ao-aa-f':
            # Lemmatized Actions - Objects + Actor - Actions and FILTERED
                actorActionsLemma = []
                for action_Lemma in actionLemma:
                    temp = nlp(action_Lemma)
                    if temp[-1].text != 'be':
                        actorActionsLemma.append(actorsLemmaString + "/" + action_Lemma)
                actorActionsStringLemma = ",".join(actorActionsLemma)
                if numFiles == 1:
                    for l in actorActionsLemma:
                        dataTransformed.append(l)
                    for l in actionsWithObjectsLemma:
                        dataTransformed.append(l)
                else:
                    if aoFilteredString == '':
                        dataTogetherString = actorActionsStringLemma
                    elif actorActionsStringLemma == '':
                        dataTogetherString = aoFilteredString
                    else:
                        dataTogether = aoFilteredString, actorActionsStringLemma
                        dataTogetherString = ",".join(dataTogether)
                    dataTogetherString = dataTogetherString.lower()
                    dataTransformed.append(dataTogetherString)
            elif saveMode == 'all':
                # All together and Lemmatized
                dataTogether = actorsLemmaString, actionLemmaString, objectLemmaString, objectPropertiesString
                dataTogetherString = ",".join(dataTogether)
                dataTransformed.append(dataTogetherString.lower())
            elif saveMode == 'ao':
                # Lemmatized Actions - Objects
                for l in actionsWithObjectsLemma:
                    dataTransformed.append(l)
            elif saveMode == 'ao-f':
                # Lemmatized Actions - Objects FILTERED
                for l in aoFiltered:
                    dataTransformed.append(l)
        # In case you want every file to be in one row to the final dataset
        if numFiles !=1:
            newData = ",".join(dataTransformed)

        # File
        if numFiles == 1:
            df = pd.DataFrame(dataTransformed, )
            df.to_csv(f"{outputPath}", header=None, index=None)
            # f = codecs.open(f"{outputPath}", "w", "utf-8")
            # f.write(newData)
        else:
            f = codecs.open(f"{outputPath}/{k}.csv", "w", "utf-8")
            f.write(newData)
            f.close()
    # In case you want every file to be in one row to the final dataset
    if numFiles != 1:
        f = codecs.open(f"{outputPath}.txt", "w", "utf-8")
        for k in range(1, numFiles + 1):
            data = pd.read_csv(f"{outputPath}/{k}.csv", header=None, sep='\t')
            f.write(data.iloc[0, 0])
            f.write('\n')
        f.close()
