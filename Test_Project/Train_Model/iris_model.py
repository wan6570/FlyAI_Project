from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

# load the iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# standardize the features
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# train a k-nearest neighbors model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# save the model and scaler to file
dump(model, 'iris_model.joblib')
dump(sc, 'scaler.joblib')

print(accuracy)

