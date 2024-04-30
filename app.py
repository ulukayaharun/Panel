from flask import Flask, request, render_template,flash
from modules.indexing_api import IndexAPI
from modules.adding_url import AddingUrl
from modules.news_counter import NewsCounter
from modules.word_frequencies import WordFrequencies
from modules.sitemap_api import SitemapAPI

app = Flask(__name__)
app.secret_key = "cokgizlisifre"

#Anasayfa
@app.route("/")
def homepage():
    return render_template("homepage.html")

#StatusChecker Sayfası
@app.route("/addurltodatabase", methods=["GET", "POST"])
def add_url_to_database():

    if request.method == "POST":
        link = request.form.get("link")
        if link:
            AddingUrl.add_link(link)
            flash(f'<a href="{link}" target="_blank">{link}</a> Status Kontrolü için Veritabanına Eklendi')

    return render_template("addurltodatabase.html")

#Keşfet Sayfası
@app.route("/wordfrequenties", methods=["GET", "POST"])
def find_most_frequent_word():
    table_html = ""
    if request.method == "POST":
        n = request.form.get("n", type=int)
        WordFrequencies.gsc_auth(['https://www.googleapis.com/auth/webmasters'])
        df_address = WordFrequencies.calculate_word_frequencies(n)
        table_html = df_address.to_html(index=False)
    return render_template("wordfrequenties.html", table_html=table_html)

#Haber Sayisi Sayfasi
@app.route("/countnews", methods=["GET", "POST"])
def make_table():
    table_html = ""
    if request.method == "POST":
        table_html = NewsCounter.update_df()
    return render_template("newscounter.html", table_html=table_html)

#Indexing API sayfası
@app.route("/indexapi",methods=["GET","POST"])
def index():
    if request.method=="POST":
       api_url=request.form.get("api_link")
       IndexAPI.run_api(api_url)
       if request.form["api_link"] ==api_url :
        flash(f'<a href="{api_url}" target="_blank">{api_url}</a> Güncellendi')
    return render_template("indexapi.html")

@app.route("/sitemapapi",methods=["GET","POST"])
def sitemap():
    if request.method=="POST":
        sitemap=request.form.get("sitemap")
        if request.form["sitemap"] ==sitemap :
            flash(f'<a href="{sitemap}" target="_blank">{sitemap}</a> Site Haritası Gönderildi')
        SitemapAPI.run_api(sitemap)
    return render_template("sitemapapi.html")

if __name__ == "__main__":
    app.run(debug=True)
