import numpy as np
from sklearn import svm
from sklearn.externals import joblib


if __name__ == '__main__':
  f = np.loadtxt('feature.txt',dtype=np.int,delimiter=" ")
  t = np.loadtxt("target.txt")

  clf = svm.SVC(gamma=0.001,C=100)
  clf.fit(f,t)
  joblib.dump(clf,'model/clf.model')
  print clf.predict([1,0,0,0,0])




