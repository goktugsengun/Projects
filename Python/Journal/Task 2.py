import pandas as pd
import sqlite3
from sklearn import tree
from sklearn.model_selection import train_test_split
import datetime
d = datetime.datetime.now()
current_date = d.strftime("%Y-%m-%d")
#from sklearn.metrics import accuracy_score
model = tree.DecisionTreeClassifier()

def predict():
    conn = sqlite3.connect("DATA.sqlite")
    script = "SELECT * FROM Data"
    cursor = conn.cursor()
    cursor.execute(script)
    lists = cursor.fetchall()
    conn.commit()
    df = pd.DataFrame(lists)
    df_new = df.rename(columns = {0:"Date",1: "Went to bed", 2:"Woke up", 3: "Sport", 4:"Cigarettes", 5:"Alcohol", 6:"Sleeping hours",
                                  7:"Weather", 8:"Day Answer"})

    df_new["Went to bed"] = df_new["Went to bed"].astype("datetime64")
    df_new["Woke up"] = df_new["Woke up"].astype("datetime64")
    df_new["Sleeping hours"] = df_new["Sleeping hours"].astype("datetime64")

    df_new["Went to bed_hour"] = df_new["Went to bed"].dt.hour
    df_new["Went to bed_minute"] = df_new["Went to bed"].dt.minute
    df_new["Woke up_hour"] = df_new["Woke up"].dt.hour
    df_new["Woke up_minute"] = df_new["Woke up"].dt.minute
    df_new["Sleeping hours_hour"] = df_new["Sleeping hours"].dt.hour
    df_new["Sleeping hours_minute"] = df_new["Sleeping hours"].dt.minute

    df_new["Alcohol_binary"] = (df_new["Alcohol"] == "Yes").astype("int")
    df_new["Sport_binary"] = (df_new["Sport"] == "Yes").astype("int")


    X = df_new[["Went to bed_hour", "Went to bed_minute", "Woke up_hour", "Woke up_minute", "Sport_binary", "Cigarettes","Alcohol_binary", "Sleeping hours_hour","Sleeping hours_minute", "Weather"]]
    Y = df_new["Day Answer"]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
    model.fit(X_train,Y_train)
    prediction = model.predict(X)

    #VISUALIZATION OF THE DECISION TREE
    #fn = ["Went to bed_hour", "Went to bed_minute", "Woke up_hour", "Woke up_minute", "Sport", "Cigarettes", "Alcohol","Sleeping hours_hour", "Sleeping hours_minute", "Weather"]
    #cn = ["Bad", "Normal", "Good"]
    #fig, ax = plt.subplots(figsize=(15, 10))
    #tree.plot_tree(model, feature_names=fn, class_names=cn, fontsize=10, filled=True)
    #plt.show()

    #fig.savefig('decisiontree.png')

    # plt.figure(figsize=(15,10))
    # tree.plot_tree(clf, filled=True)

    conn.close()

    conn = sqlite3.connect("PREDICTION.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Predictions VALUES (?,?)", (current_date, prediction[-1]))
    conn.commit()
predict()