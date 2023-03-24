from flask import Flask, render_template, request
from views import views


import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

@app.route("/data")
def get_data():
    results = []
    
    loginurl=('https://e.csdd.lv/login/?action=doLogin')
    secureurl=('https://e.csdd.lv/')
    searchurl=('https://e.csdd.lv/tadati/')

    payload= {
        #e-pasts un parole
        'email': '*',
        'psw': '*',
    }
    plate= {
        #numurzime
        'rn':"*"
    }

    #Rasena magija
    with requests.session() as s:
        cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(s.cookies))
        s.post(loginurl, data=payload)
        r = s.post(searchurl, data=plate)
        soup = BeautifulSoup(r.content, 'html.parser')
        tabula = soup.find('table', class_ = 'table-list')
    for row in tabula.find_all("tr")[1:]:
        results.append([cell.get_text(strip=True) for cell in row.find_all("td")])
    
    #pagaidam atgriezam pretigu garu stringu
    
    string = ""
    string = string.join(str(results))
    
    #iesprauzam stringu index html faila
    return render_template("index.html" ,name=string)
    


if __name__ == '__main__':
    app.run()
