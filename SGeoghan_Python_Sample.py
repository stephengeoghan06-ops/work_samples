import pandas as pd
import numpy as np
from pandas import DataFrame
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser
from pathlib import Path

BASE_DIR = Path(__file__).parent
MorningTrades_History: DataFrame = pd.read_excel(BASE_DIR / "sample_Data_SG.xlsx")
MorningTrades_History["Ticker"] = MorningTrades_History["Ticker"].str.upper()
tickers_to_delete = ["ADP","CLX","DIA","MMM","ORI","EXC","STAG"]
MorningTrades_History = MorningTrades_History[~MorningTrades_History["Ticker"].isin(tickers_to_delete)]
MorningTrades_History.columns = MorningTrades_History.columns.str.strip()
MorningTrades_History["Date"] = pd.to_datetime(MorningTrades_History["Date"])
MorningTrades_History.set_index("Date",inplace=True)
MorningTrades_History.drop(columns=["Day of week","Open"],inplace=True)
MorningTrades_History["Low"] = (
    pd.to_numeric(MorningTrades_History["Low"].astype(str).replace(r'[$,]','',regex=True),errors='coerce')
     .fillna(0)
     .astype(float))
MorningTrades_History["Next High"] = (
    pd.to_numeric(MorningTrades_History["Next High"].astype(str).replace(r'[$,]','',regex=True),errors='coerce')
     .fillna(0)
     .astype(float))
First_Low_staged = pd.to_datetime(MorningTrades_History["First low Time"],format='%H:%M:%S')
next_high_staged = pd.to_datetime(MorningTrades_History["Next High Time"],format='%H:%M:%S')
MorningTrades_History["First low Time"] = First_Low_staged.dt.strftime('%H:%M')
MorningTrades_History["Next High Time"] =  next_high_staged.dt.strftime('%H:%M')
MorningTrades_History["Profit_Potential"] = np.where(MorningTrades_History["Low"]>=300,
    ((MorningTrades_History["Next High"]-MorningTrades_History["Low"])*100).round(2),
    ((MorningTrades_History["Next High"]-MorningTrades_History["Low"])*200).round(2))
#below is meant to filter out any anomolies:
MorningTrades_History = MorningTrades_History[(MorningTrades_History["Profit_Potential"]>-1000) &
(MorningTrades_History["Profit_Potential"]<1000)]


SECTOR_LIST = [["AEP","Utilities"],
["AMT","REIT"],
["AMZN","Tech"],
["BX","Financial"],
["CRM","Tech"],
["DLR","REIT"],
["DUK","Utilities"],
["ED","Utilities"],
["ES","Utilities"],
["HD","Consumer Staples"],
["MCD","Consumer Staples"],
["MSFT","Tech"],
["PG","Consumer Staples"],
["TLT","Bonds"],
["VZ","Consumer Staples"],
["PG","Consumer Staples"],
["PLD","REIT"],
["PLTR","Tech"],
["QQQ","Tech"],
["STAG","REIT"],
["TLT","Bonds"],
["TRV","Financial"],
["UNH","Medical"],
["Unknown","Unknown"],
["UNP","Consumer Staples"],
["VDC","Consumer Staples"],
["VZ","Consumer Staples"]]
#naming the columns:
SECTOR_LIST = pd.DataFrame(SECTOR_LIST,columns=['Ticker','Sector'])
MorningTrades_History = MorningTrades_History.merge(SECTOR_LIST[["Ticker","Sector"]],on='Ticker',how='left')
Setting_up_summary_by_ticker = pd.DataFrame(MorningTrades_History)

summary_by_ticker = Setting_up_summary_by_ticker.groupby(["Ticker","Sector"]).agg(
Num_of_Trades =('Ticker','size'),Profit_potential=("Profit_Potential",'sum')).reset_index()

#this is slow so using for illustrative purposes. Else would name conditions then pull them in with np.select
def how_to_rate(row):
    if row['Num_of_Trades']<20:
        return 'not good'
    elif row['Num_of_Trades']>=20 and row['Num_of_Trades'] < 40:
        return 'ok'
    else:
        return 'Solid history'
summary_by_ticker["My_Rating"] = summary_by_ticker.apply(how_to_rate, axis=1)
summary_by_ticker = summary_by_ticker.sort_values(by="Sector",ascending=True)

#all the data is lined up and filtered and calculated and now we're making it into a pop-op box:
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 400, 450, 450)

        self.display = QTextBrowser(self)
        self.setCentralWidget(self.display)
        html_table = summary_by_ticker.to_html(
            index=False, #this is b/c the index # was showing up as a random column
            justify='center',
            formatters={
                'Profit_potential': lambda x: f"${x:,.2f}"
            }
        )
        self.display.setHtml(html_table)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


print(summary_by_ticker)