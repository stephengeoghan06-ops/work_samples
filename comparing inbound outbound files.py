
import pandas as pd
import glob

folder_path = r"C:\Users\steph\OneDrive\Desktop\Power BI PL-300\files_to_compare\Outbound\*.xlsx"
Excel_files = glob.glob(folder_path)
bills_combined = []
for file in Excel_files:
     df = pd.read_excel(file)
     bills_combined.append(df)

combined_outbound_df = pd.concat(bills_combined, ignore_index=True)
output_file = "combined_output.xlsx"
combined_outbound_df.to_excel(output_file, index=False)

#print(combined_outbound_df)

inbound_file_path = r"C:\Users\steph\OneDrive\Desktop\Power BI PL-300\files_to_compare\Inbound\inbound_responses.xlsx"
columns=["Account_#","Bill_Date","Bill_Number","Amount","Tracking_Number","File_Type"]

try:
    inbound_responses = pd.read_excel(inbound_file_path)
    inbound_responses = pd.DataFrame(inbound_responses,columns=columns)
    inbound_responses = inbound_responses.rename(columns={'Bill_Date':'Response_Date','Amount':'Response_Amount'})


except(ValueError, Exception) as e:
    print(col:=f"Folder was empty or file unreadable ({e})")
    inbound_responses = pd.DataFrame(columns=columns)
    inbound_responses = inbound_responses.rename(columns={'Bill_Date': 'Response_Date','Amount': 'Response_Amount'})


combined_outbound_df['Bill_Number'] = combined_outbound_df['Bill_Number'].astype(str).str.strip().str.upper()
inbound_responses['Bill_Number'] = inbound_responses['Bill_Number'].astype(str).str.strip().str.upper()

Outboundbills_vs_Inbound = combined_outbound_df.merge(inbound_responses[['Bill_Number','Response_Amount','Response_Date']],on='Bill_Number',how='left')
Outboundbills_vs_Inbound['Response_Amount'] = Outboundbills_vs_Inbound['Response_Amount'].fillna('No Response')
Outboundbills_vs_Inbound['Response_Date'] = Outboundbills_vs_Inbound['Response_Date'].fillna('None yet')
#Outboundbills_vs_Inbound['Response_Amount'] = inbound_responses['Response_Amount']
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',2000)
print(Outboundbills_vs_Inbound)
