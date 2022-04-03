# Employing Machine Learning and Intelligent Information Management Techniques for efficient Software Requirements Elicitation

## Abstract 
Proper definition of functional requirements is a prerequisite for succesful software project development. Inaccurate and/or missing functional requirements are among the top reasons that lead to failure of the software development process, since incomplete definition of functional requirements results in erroneous scheduling of necessary tasks and subsequently failure in the implementation of the software project.

This dissertation initially builds a dataset of functional requirements of software projects from various sources, which is missing from bibliography. Then an ontology is defined, that captures the static view of a software project. The functional requirements of the dataset are mapped to the defined entities and the data is efficiently stored using the ontology format.

In the next step, machine learning algorithms are employed in order to extract recommendations for better software requirements elicitation.  For the evaluation of their performance the models are fed with take a new software project with incomplete functionality as input and the extracted recommendations are evaluated.

_Anastasios Mouratidis_

_Electrical and Computer Engineering School,_

_Aristotle University of Thessaloniki, Greece_

_February 2022_

## Thesis Report in Greek
You can read the Thesis Report [here](https://ikee.lib.auth.gr/record/337972/files/Thesis_Mouratidis_Anastasios_9040.pdf). 

## Dependencies 
```
pip install pandas
pip install numpy
pip install spacy
python -m spacy download en_core_web_lg
pip install apyori
pip install regex
pip install gensim
pip install pyLDAvis
pip install scikit-learn
pip install matplotlib
pip install scipy
```
## Code Run
### Ontology extraction
* Extract the Ontology from the Functional Requirements Dataset using the /Ontology Extraction/extractOntology.ipynb notebook 
### Associtation Rules
* Extract the Association Rules for the dataset using the /Apriori/apriori.ipynb notebook
* Extraxt the Association Rules for the tesing project using the /Apriori/aprioriTestProject.ipynb notebook
### LDA
* Calculate the Topic Coherence using the /LDA/lda_select_model.ipynb notebook
* Train the LDA models for different number of topics using the /LDA/lda_topics_iterations.ipynb notebook
* Visualize the LDA results using the /LDA/lda_vis.ipynb notebook
### Clustering
* Implement Hierarchical Text Clustering with TFIDF using the /Text Clustering/clustering.ipynb notebook 
