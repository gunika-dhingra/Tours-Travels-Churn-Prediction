# -*- coding: utf-8 -*-
"""customer_churn_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YfF-AIQXzTD6zVi5JIj3FkTuAcVidvks

## Churn Prediction for Tours and Travels industry

Customer churn, also known as customer attrition, refers to the phenomenon where customers cease their relationship with a business or discontinue using its products or services. It is a critical concern for businesses across industries, as the loss of customers can have a substantial impact on revenue and long-term sustainability. y analyzing patterns and identifying early warning signs, businesses can proactively implement retention strategies, reduce churn rates, and ultimately improve customer satisfaction and loyalty.

### Importing libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.layers import BatchNormalization

data = pd.read_csv("/content/Customertravel.csv")
data.head()

data.columns    #display the columns present in the dataset/dataframe

data.info()     #display information relevant to our dataframe

data.isnull().sum()       #checking the presence of any null values

data.shape

#renaming the column 'Target' to 'Status' just for the ease of interpretation
data.rename(columns={'Target': 'Status'}, inplace=True)

#in the given dataset 0 represents that the customer hasn't churned i.e., the customer has retained. We are hence renaming it as such for better readability
data['Status'] = data['Status'].map({0: 'retained', 1 : 'dropped'})

print(data['Status'].value_counts())   #counting the number of customers reatined and dropped

data.head()

"""### Data Visualization"""

retained_count = data[data['Status'] == 'retained'].shape[0]
dropped_count = data[data['Status'] == 'dropped'].shape[0]
labels = ['Retained', 'Dropped']
explode = (0,0.1)
sizes = [retained_count, dropped_count]
plt.pie(sizes, labels=labels, colors=['blue','orange'], autopct='%1.1f%%', shadow = True, explode = explode)

plt.axis('equal')
plt.title('Customer Retention')

# Displaying the chart
plt.show()

fig, axes = plt.subplots(2,3, figsize=(14,8), sharey=True)
sns.countplot(x='FrequentFlyer', data=data, ax=axes[0,0])
sns.countplot(x='AccountSyncedToSocialMedia', data=data, ax=axes[0,1])
sns.countplot(x='BookedHotelOrNot',data=data, ax=axes[0,2])
sns.countplot(x='Age',data=data, ax=axes[1,0])
sns.countplot(x='AnnualIncomeClass',data=data, ax=axes[1,1])
sns.countplot(x='ServicesOpted',data=data, ax=axes[1,2])

data.dtypes

"""### Data Preprocessing"""

encoded_data = data.copy()

#converting to categorical variables
encoded_data['FrequentFlyer'] = encoded_data['FrequentFlyer'].astype('category')
encoded_data['AnnualIncomeClass'] = encoded_data['AnnualIncomeClass'].astype('category')
encoded_data['AccountSyncedToSocialMedia'] = encoded_data['AccountSyncedToSocialMedia'].astype('category')
encoded_data['BookedHotelOrNot'] = encoded_data['BookedHotelOrNot'].astype('category')

encoded_data.dtypes

encoded_data.head()

#encoding the categorical variables
encoded_data['FrequentFlyer'] = encoded_data['FrequentFlyer'].cat.codes
encoded_data['AnnualIncomeClass'] = encoded_data['AnnualIncomeClass'].cat.codes
encoded_data['AccountSyncedToSocialMedia'] = encoded_data['AccountSyncedToSocialMedia'].cat.codes
encoded_data['BookedHotelOrNot'] = encoded_data['BookedHotelOrNot'].cat.codes

encoded_data.dtypes

encoded_data['Status'] = encoded_data['Status'].map({'retained': 0, 'dropped' : 1})

encoded_data.head()

encoded_data.to_csv('encoded_data.csv', index=False)
files.download('encoded_data.csv')

x = encoded_data.drop('Status',axis=1)
y = encoded_data['Status']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2,random_state=40)

"""### Model/Algorithm Application

There are a lot of alogorithms that can be applied for churn prediction namely XGBoost, Logistic Regression, DecisionTree, SVMs and other neural networks. It is for us to decide after looking and working with the data, which one to use.

Here we will be using multiple algorithms/models and compare the same using their accuracy to judge what fits the best for our chosen dataset.

#### XGBoost
"""

model1 = XGBClassifier()

model1.fit(x_train,y_train)
y_pred1 = model1.predict(x_test)

print("Accuracy Score :", accuracy_score(y_test, y_pred1)*100, "%")

"""#### Linear Support Vector Classifier"""

model2 = LinearSVC()

model2.fit(x_train,y_train)
y_pred2 = model2.predict(x_test)
print("Accuracy Score :", accuracy_score(y_test, y_pred2)*100, "%")

"""#### Random Forest"""

model3 = RandomForestClassifier()

model3.fit(x_train,y_train)
y_pred3 = model3.predict(x_test)
print("Accuracy Score :", accuracy_score(y_test, y_pred3)*100, "%")

"""#### Artificial Neural Network"""

model_4 = Sequential([Dense(64, activation='relu', input_shape=(6,)),
                      BatchNormalization(),
                      Dense(32, activation='relu'),
                      BatchNormalization(),
                      Dense(16, activation='relu'),
                      BatchNormalization(),
                      Dense(8, activation='relu'),
                      BatchNormalization(),
                      Dense(1, activation='sigmoid')
                      ])

model_4.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

model_4.fit(x_train, y_train, epochs=25)

loss, accuracy = model_4.evaluate(x_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

"""Upon comparing we notice that for our data, XGBoost yields the highest accuracy of ~92%

To know more about Customer Churn Prediction and its practical applications in businesses, refer this: https://medium.com/@12gunika/unlocking-customer-loyalty-the-power-of-data-science-in-churn-prediction-26b529b8fcf0
"""

