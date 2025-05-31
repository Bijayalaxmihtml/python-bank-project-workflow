from datetime import datetime
import  pandas as pd


df=pd.read_csv(r"C:\Users\israd\Downloads\Datakvalitet\transactions.csv")
print("orginal data")
print(df["timestamp"].head())

df["timestamp"]= pd.to_datetime(df["timestamp"], errors="coerce", format= "%Y-%m-%d %H:%M:%S")

print(df["timestamp"].head())

df.to_csv("clean_transaction.csv" , index= False)

clean_df = pd.read_csv('clean_transaction.csv')
print(df["timestamp"].head())

