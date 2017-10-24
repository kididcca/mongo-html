import os, time
from pymongo import MongoClient 

cliente = MongoClient(os.getenv('MONGO_SERVER', 'nuvem.sj.ifsc.edu.br'))
db = cliente[os.getenv('DATABASE', 'estacao')]

while True:
    dados_recebidos = []
    lista_colecoes = []
    lista_colecoes = db.collection_names()

    saida = open("html/dados.js", "w")
    html = open("html/page.html", "w")

    html.write('<!DOCTYPE html>\n')
    html.write('<html>\n')
    html.write('<head>\n')
    html.write('<meta charset="utf-8">\n')
    html.write('<title>Lendo dados com o Arduino</title>\n')
    html.write('<link href="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css" rel="stylesheet" type="text/css" />\n')
    html.write('</head>\n')
    html.write('<body>\n')
    for colecao in lista_colecoes:
        posts = db[colecao]
        dados_recebidos = posts.find()
        saida.write("new Chartist.Line('#" + colecao + "', {\n")
        saida.write("series: [\n")
        html.write('<p align="left">' + colecao + '</p>\n')
        html.write('<div class="ct-chart ct-major-seventh" id="' + colecao + '"></div>\n')
        for sensores in dados_recebidos:
            saida.write("{\n")
            saida.write("name: '" + colecao + "',\n")
            saida.write("data: [\n")
            for linha in dados_recebidos:
                saida.write("{\n")
                saida.write("x: new moment.unix(" + str(linha['data']).split('.')[0] + "),\n")
                saida.write("y: " + linha['valor'] + "\n")
                saida.write("},\n")
            saida.write("]\n")
            saida.write("},\n")
        saida.write("]\n")
        saida.write("},\n")
        saida.write("{\n")
        saida.write("axisX: {\n")
        saida.write("type: Chartist.FixedScaleAxis,\n")
        saida.write("divisor: 5,\n")
        saida.write("labelInterpolationFnc: function (value) {\n")
        saida.write("return moment(value).format('HH:MM-DD/MM');\n")
        saida.write("}\n")
        saida.write("}\n")
        saida.write("});\n")
    html.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.js"></script>\n')
    html.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/locale/pt-br.js"></script>\n')
    html.write('<script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js "></script>\n')
    html.write('<script src="dados.js"></script>\n')
    html.write('</body>\n')
    html.write('</html>\n')
    
    saida.close()
    html.close()
    
    time.sleep(60)
