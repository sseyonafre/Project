import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import pickle

df = pd.read_csv(r'/Users/sehee/Section3/Project/Section3/user.csv',index_col = 1)
df.drop(columns=['Unnamed: 0'],inplace=True) 
df.drop_duplicates(keep='first', inplace=True)
df.replace('-',np.nan, inplace=True)
for i in ['jump','situp','crunch','trunkFlexion','IllinoisAgility','standinglongjump','twominwalk','threeMwalk']:
    df[i]= pd.to_numeric(df[i],errors='coerce')

df['certGbn'].replace({'참가증':'4','1등급':'1','2등급':'2','3등급':'3'},inplace=True)
df['certGbn'] = df['certGbn'].astype('category')
df1 = df.query("ageGbn=='노인'")
df2 = df.query("ageGbn=='성인'")
df3 = df.query("ageGbn=='유소년'")
df4 = df.query("ageGbn=='청소년'")

df1.drop(columns=['crunch','jump','IllinoisAgility','situp','standinglongjump'],inplace=True)
df2.drop(columns=['crunch','jump','IllinoisAgility','standsit','twominwalk','threeMwalk'],inplace=True)
df3.drop(columns=['jump','situp','standsit','twominwalk','threeMwalk','IllinoisAgility'],inplace=True)
df4.drop(columns=['crunch','situp','standsit','twominwalk','threeMwalk'],inplace=True)

df['standsit'] = df1['standsit'].replace(np.nan,0)
df2['situp'] = df2['situp'].replace(np.nan,0).round(0).astype(int)
df3['crunch'] = df3['crunch'].replace(np.nan,0).round(0).astype(int)
df4['jump'] = df4['jump'].replace(np.nan,0).round(0).astype(int)

target = 'certGbn'

features1 = df1.drop(columns=['certGbn','exercise','testYm','ageGbn']).columns

X_df1 = df1[features1]
y_df1 = df1[target]


#노년층 모델 #랜덤포레스트
pipe1_rfc = make_pipeline(
    SimpleImputer(), 
    RandomForestClassifier(n_estimators=100, random_state=2, n_jobs=-1)
)


#데이터 수가 많지않아서 fit 할때 전체를 다 fit 해줌.
pipe1_rfc.fit(X_df1,y_df1)  #fit을 꼭 해줘야함.
with open('senior.pickle','wb') as fw:
    pickle.dump(pipe1_rfc, fw)

#성인층 모델

features2 = df2.drop(columns=['certGbn','exercise','testYm','ageGbn']).columns

X_df2 = df2[features2]
y_df2 = df2[target]


pipe2_rfc = make_pipeline(
    SimpleImputer(), 
    RandomForestClassifier(n_estimators=100, random_state=2, n_jobs=-1)
)



pipe2_rfc.fit(X_df2,y_df2)

with open('middle.pickle','wb') as fw:
    pickle.dump(pipe2_rfc, fw)


#유소년 모델링 #xgboost

features3 = df3.drop(columns=['ageClass','certGbn','exercise','testYm','ageGbn']).columns

X_df3 = df3[features3]
y_df3 = df3[target]


pipe3_xg = make_pipeline(
    SimpleImputer(), 
    XGBClassifier(random_state=2, n_jobs=-1)
)


pipe3_xg.fit(X_df3,y_df3)

with open('underaged.pickle','wb') as fw:
    pickle.dump(pipe3_xg, fw)

#청소년 모델링 #랜덤포레스트모델

features4 = df4.drop(columns=['ageClass','certGbn','exercise','testYm','ageGbn']).columns

X_df4 = df[features4]
y_df4 = df[target]


pipe4_rfc = make_pipeline(
    SimpleImputer(), 
    RandomForestClassifier(n_estimators=100, random_state=2, n_jobs=-1)
)


pipe4_rfc.fit(X_df4,y_df4)

with open('youth.pickle','wb') as fw:
    pickle.dump(pipe4_rfc, fw)