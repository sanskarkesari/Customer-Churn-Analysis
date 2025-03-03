
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
# %matplotlib inline

telco_base_data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

telco_base_data.head()

telco_base_data.shape

telco_base_data.dtypes

telco_base_data.describe()

telco_base_data['Churn'].value_counts().plot(kind='barh', figsize=(8, 6))
plt.xlabel("Count", labelpad=14)
plt.ylabel("Target Variable", labelpad=14)
plt.title("Count of TARGET Variable per category", y=1.02);

100*telco_base_data['Churn'].value_counts()/len(telco_base_data['Churn'])

telco_base_data['Churn'].value_counts()

telco_data = telco_base_data.copy()

telco_data.TotalCharges = pd.to_numeric(telco_data.TotalCharges, errors='coerce')
telco_data.isnull().sum()

telco_data.loc[telco_data ['TotalCharges'].isnull() == True]

telco_data.dropna(how = 'any', inplace = True)

print(telco_data['tenure'].max())

labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]

telco_data['tenure_group'] = pd.cut(telco_data.tenure, range(1, 80, 12), right=False, labels=labels)

telco_data['tenure_group'].value_counts()

telco_data.drop(columns= ['customerID','tenure'], axis=1, inplace=True)
telco_data.head()

for i, predictor in enumerate(telco_data.drop(columns=['Churn', 'TotalCharges', 'MonthlyCharges'])):
    plt.figure(i)
    sns.countplot(data=telco_data, x=predictor, hue='Churn')

telco_data['Churn'] = np.where(telco_data.Churn == 'Yes',1,0)

telco_data.head()

telco_data_dummies = pd.get_dummies(telco_data)
telco_data_dummies.head()

sns.lmplot(data=telco_data_dummies, x='MonthlyCharges', y='TotalCharges', fit_reg=False)

Mth = sns.kdeplot(telco_data_dummies.MonthlyCharges[(telco_data_dummies["Churn"] == 0) ],
                color="Red", shade = True)
Mth = sns.kdeplot(telco_data_dummies.MonthlyCharges[(telco_data_dummies["Churn"] == 1) ],
                ax =Mth, color="Blue", shade= True)
Mth.legend(["No Churn","Churn"],loc='upper right')
Mth.set_ylabel('Density')
Mth.set_xlabel('Monthly Charges')
Mth.set_title('Monthly charges by churn')

Tot = sns.kdeplot(telco_data_dummies.TotalCharges[(telco_data_dummies["Churn"] == 0) ],
                color="Red", shade = True)
Tot = sns.kdeplot(telco_data_dummies.TotalCharges[(telco_data_dummies["Churn"] == 1) ],
                ax =Tot, color="Blue", shade= True)
Tot.legend(["No Churn","Churn"],loc='upper right')
Tot.set_ylabel('Density')
Tot.set_xlabel('Total Charges')
Tot.set_title('Total charges by churn')

plt.figure(figsize=(12,12))
sns.heatmap(telco_data_dummies.corr(), cmap="Paired")

telco_data_dummies.to_csv('tel_churn.csv')

import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from imblearn.combine import SMOTEENN

df=pd.read_csv("tel_churn.csv")
df=df.drop('Unnamed: 0',axis=1)

x=df.drop('Churn',axis=1)
x

y=df['Churn']
y

sm = SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(x,y)

xr_train,xr_test,yr_train,yr_test=train_test_split(X_resampled, y_resampled,test_size=0.2)

model_dt_smote=DecisionTreeClassifier(criterion = "gini",random_state = 100,max_depth=6, min_samples_leaf=8)

model_dt_smote.fit(xr_train,yr_train)
yr_predict = model_dt_smote.predict(xr_test)
model_score_r = model_dt_smote.score(xr_test, yr_test)
print(model_score_r)
print(metrics.classification_report(yr_test, yr_predict))

print(metrics.confusion_matrix(yr_test, yr_predict))

import pickle
filename = 'model.sav'
pickle.dump(model_dt_smote, open(filename, 'wb'))

model = pickle.load(open("model.sav", "rb"))

data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7,
             inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12, inputQuery13, inputQuery14,
             inputQuery15, inputQuery16, inputQuery17, inputQuery18, inputQuery19]]

new_df = pd.DataFrame(data, columns = ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender',
                                           'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
                                           'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                           'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                                           'PaymentMethod', 'tenure'])

single = model.predict(new_df__dummies.tail(1))
probablity = model.predict_proba(new_df__dummies.tail(1))[:,1]

if single==1:
    o1 = "This customer is likely to be churned!!"
    o2 = "Confidence: {}".format(probablity*100)
else:
    o1 = "This customer is likely to continue!!"
    o2 = "Confidence: {}".format(probablity*100)
