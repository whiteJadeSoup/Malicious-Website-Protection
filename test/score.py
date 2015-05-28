from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble
from sklearn import linear_model
from sklearn import svm
import numpy as np

if __name__ == '__main__':
    train_data = np.loadtxt('feature.txt',dtype=np.int,delimiter=" ")
    train_target = np.loadtxt("target.txt")
    
    
    
    lr = linear_model.LogisticRegression()
    lr_scores = cross_validation.cross_val_score(lr, train_data, train_target, cv=5)
    print("logistic regression accuracy:")
    print(lr_scores)
    
    
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=8, min_samples_split=5)
    clf_scores = cross_validation.cross_val_score(clf, train_data, train_target, cv=5)
    print("decision tree accuracy:")
    print(clf_scores)
    
    
    
    rfc = ensemble.RandomForestClassifier(criterion='entropy', n_estimators=3, max_features=0.5, min_samples_split=5)
    rfc_scores = cross_validation.cross_val_score(rfc, train_data, train_target, cv=5)
    print("random forest accuracy:")
    print(rfc_scores)
    
    
    
    etc = ensemble.ExtraTreesClassifier(criterion='entropy', n_estimators=3, max_features=0.6, min_samples_split=5)
    etc_scores = cross_validation.cross_val_score(etc, train_data, train_target, cv=5)
    print("extra trees accuracy:")
    print(etc_scores)
    
    
    
    gbc = ensemble.GradientBoostingClassifier()
    gbc_scores = cross_validation.cross_val_score(gbc, train_data, train_target, cv=5)
    print("gradient boosting accuracy:")
    print(gbc_scores)
    
    
    
    svc = svm.SVC()
    svc_scores = cross_validation.cross_val_score(svc, train_data, train_target, cv=5)
    print("svm classifier accuracy:")
    print(svc_scores)
