# Related Projects
## Interoperability and framework enhancements
### Data formats
* sklearn_pandas
* sklearn_xarray
### Auto-ML
* auto_ml
* auto_sklearn
* TPOT
* scikit-optimize
### Experimentation frameworks
* REP
* ML Frontend
* Scikit-Learn Laboratory
* Xcessiv
### Model inspection and Visualization
* eli5
* mlxtend
* scikit-plot
* yellowbrick
### Model export for production
* onnxmltools
* sklearn3pmml
* sklearn-porter
* sklearn-compiledtrees
## Other estimators and tasks
### Structured learning
* Seqlearn
* HMMLearn
* PyStruct
* pomegranate
* sklearn-crfsuite
### Deep neural networks etc.
* pylearn2
* sklearn_theano
* nolearn
* keras
* lasagne
* skorch
### Broad scope
* mlxtend
* sparkit-learn
### Other regression and classification
* xgboost
* ML-Ensemble
* lightning
* py-earth
* Kernel Regression
* gplearn
* multiisotonic
* scikit-multilearn
* seglearn
### Decomposition and clustering
* lda (Latent Dirichlet Allocation in Cython)
* Sparse Filtering
* kmodes
* hdbscan
* spherecluster
### Pre-processing
* categorical-encoding
* imbalanced-learn
## Statistical learning with Python
* Pandas
* theano
* statsmodels Estimating and analyzing statistical models.
* PyMC Bayesian statistical models and fitting algorithms.
* Sacred Tool to help you configure, organize, log and reproduce experiments
* Seaborn Visualization library based on matplotlib
* Deep Learning A curated list of deep learning software libraries
## Domain Specific Packages
* scikit-image Image processing and computer vision in python
* Natural language toolkit (nltk)
* gensim A library for topic modelling, document indexing and similarity retrieval
* NiLearn Machine learning for neuro-imaging
* AstroML Machine learning for astronomy
* MSMBuilder Machine learning for protein conformational dynamics time series.
* scikit-surprise A scikit for building and evaluating recommender systems.
# Learning and predicting
    In scikit-learn, an estimator for classification is a python object that implements
    the methods fit(X,y) and predict(T).
    An example is the class sklearn.svm.SVC which implements __support vector
    classification__.
    ```python
    from sklearn import svm
    clf=svm.SVC(gamma=0.001,C=100.)
    digits=sklearn.datasets.load_digits()
    clf.fit(digits.data[:-1],digits.target[:-1])
    clf.predict(digits.data[-1:])
    ```
## Model persistence
```python
from sklearn import svm
from sklearn import datasets
clf=svm.SVC(gamma='scale')
iris=datasets.load_iris()
X,y=iris.data,iris.target
clf.fit(X,y)
import pickle
s=pickle.dumps(clf)
clf2=pickle.loads(s)
clf2.predict(X[0:1])
print(y[0])
# using joblib to pickle to disk and not strings for big data
from joblib import dump,load
dump(clf,'filename.joblib')
clf=load('filename.joblib')
# joblib.dump and joblib.load as accept file like objects instead of filenames.
```
