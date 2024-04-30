from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://remote:BIw883k8@212.31.2.93/monitor",
                        connect_args={"charset": "utf8mb4"}, echo=False)

class AddingUrl:
    link_df = pd.DataFrame(columns=["URL", "DATETIME"])  # Linkleri kaydetmek için DataFrame

    def add_link(link):
        timestamp = datetime.now()
        AddingUrl.link_df.loc[len(AddingUrl.link_df)] = [link, timestamp]
        AddingUrl.save_to_database("url")

    def save_to_database(table_name):
        try:
            AddingUrl.link_df.to_sql(table_name, engine, if_exists="append", index=False)
            AddingUrl.link_df = pd.DataFrame(columns=["URL", "DATETIME"])  # DataFrame'i sıfırlar
        except Exception as e:
            print(e)