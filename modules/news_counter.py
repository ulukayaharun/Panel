from urllib.parse import urlparse
from flask import request
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://remote:BIw883k8@212.31.2.93/monitor",
                        connect_args={"charset": "utf8mb4"}, echo=False)
class NewsCounter:
    #https://www.example.com.tr/blabla ---> www.example.com.tr dönüştürücü
    def get_domain(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    
    def update_df():
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if start_date and end_date:
            # Formdan alınan tarihleri datetime türüne dönüştür ve saat bilgisini ekle
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

            # Veritabanı sorgusu için bitiş tarihine bir gün ekle (veya günün son saatini kullan)
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)

            df = pd.read_sql_table("sitemap_urls", engine)

            # Veritabanındaki 'DATE' sütununu datetime türüne çevir
            df['DATE'] = pd.to_datetime(df['DATE'])

            # Filtreleme işlemini güncellenmiş datetime aralığıyla yap
            filtered_df = df[(df['DATE'] >= start_datetime) & (df['DATE'] <= end_datetime)]

            data = {}
            for _, row in filtered_df.iterrows():
                domain = NewsCounter.get_domain(row["URL"])
                if domain in data:
                    data[domain] += 1
                else:
                    data[domain] = 1
            #büyükten küçüğe sıralar ve listeye dönüşür
            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

            new_df = pd.DataFrame(sorted_data, columns=['Domain', 'Haber Sayilari'])
            return new_df.to_html(index=False)