import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import PCA

# Load the training and evaluation data
train_data = pd.read_csv("TrainOnMe.csv", index_col=0)
eval_data = pd.read_csv("EvaluateOnMe.csv", index_col=0)

# Apply an ordinal encoder to column 7
ordinal_encoder = OrdinalEncoder()
train_data['x7'] = ordinal_encoder.fit_transform(train_data[['x7']])
eval_data['x7'] = ordinal_encoder.transform(eval_data[['x7']])

# Drop column 12 since it's redundant
train_data.drop(columns=['x12'], inplace=True)
eval_data.drop(columns=['x12'], inplace=True)

# Split into X- and y-data separation
X = train_data.drop(columns=['y'])
y = train_data['y']

# Split into training and testing sets; 20% testing and 80% training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Feature scaling before PCA
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply PCA
pca = PCA(n_components=11)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)


# CLASSIFIER 1: RANDOM FOREST
rfclf = RandomForestClassifier()
rfclf.fit(X_train_pca, y_train)
y_pred_rf = rfclf.predict(X_test_pca)
print(f'Random Forest Accuracy: {accuracy_score(y_test, y_pred_rf)}')


# CLASSIFIER 2: ADA BOOST + RANDOM FOREST
ada_clf = AdaBoostClassifier(estimator=rfclf, n_estimators=50)
ada_clf.fit(X_train_pca, y_train)
y_pred_ada = ada_clf.predict(X_test_pca)
print(f'AdaBoost Accuracy: {accuracy_score(y_test, y_pred_ada)}')


# CLASSIFIER 3: GRADIENT BOOSTING (XGBOOST)
gb = GradientBoostingClassifier()
gb.fit(X_train_pca, y_train)
y_pred_gb = gb.predict(X_test_pca)
print(f'Gradient Boosting Accuracy: {accuracy_score(y_test, y_pred_gb)}')


# CLASSIFIER 4: VOTING CLASSIFIER
voting_clf = VotingClassifier(estimators=[
    ('rf', rfclf),
    ('ada', ada_clf),
    ('gb', GradientBoostingClassifier()),
], voting='soft')

# Train and evaluate the voting classifier
voting_clf.fit(X_train_pca, y_train)
y_pred_voting = voting_clf.predict(X_test_pca)
print(f'Voting Classifier Accuracy Test: {accuracy_score(y_test, y_pred_voting)}')


# Cross-val
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=11)
X_pca = pca.fit_transform(X_scaled)

# Perform cross-validation on RandomForestClassifier
cv_scores_rf = cross_val_score(rfclf, X_pca, y, cv=10, scoring='accuracy')
print(f'Random Forest Cross-Validation Accuracy: {np.mean(cv_scores_rf)}')

# Perform cross-validation on AdaBoostClassifier
cv_scores_ada = cross_val_score(ada_clf, X_pca, y, cv=10, scoring='accuracy')
print(f'AdaBoost Cross-Validation Accuracy: {np.mean(cv_scores_ada)}')

# Perform cross-validation on GradientBoostingClassifier
cv_scores_gb = cross_val_score(gb, X_pca, y, cv=10, scoring='accuracy')
print(f'Gradient Boosting Cross-Validation Accuracy: {np.mean(cv_scores_gb)}')

# Perform cross-validation on VotingClassifier
cv_scores_voting = cross_val_score(voting_clf, X_pca, y, cv=10, scoring='accuracy')
print(f'Voting Classifier Cross-Validation Accuracy: {np.mean(cv_scores_voting)}')