import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("data/Fights.csv")

# preparar lutador 1
df1 = df[[
"STR_1","TD_1","KD_1","Sub. Att_1",
"Sig. Str. %_1",
"Distance_%_1","Clinch_%_1","Ground_%_1",
"Result_1"
]].copy()

df1.columns = [
"STR","TD","KD","SUB",
"ACCURACY",
"DISTANCE","CLINCH","GROUND",
"RESULT"
]

# preparar lutador 2
df2 = df[[
"STR_2","TD_2","KD_2","Sub. Att_2",
"Sig. Str. %_2",
"Distance_%_2","Clinch_%_2","Ground_%_2",
"Result_2"
]].copy()

df2.columns = df1.columns

df_all = pd.concat([df1, df2])

# transformar resultado
df_all["RESULT"] = df_all["RESULT"].map({"W":1,"L":0})

df_all = df_all.dropna()

X = df_all.drop("RESULT", axis=1)
y = df_all["RESULT"]

X_train, X_test, y_train, y_test = train_test_split(
X,y,test_size=0.2,random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train,y_train)

print("Model accuracy:", model.score(X_test,y_test))

joblib.dump(model,"model/ufc_model.pkl")