from flask import Flask, render_template, request
from util import ProcessosAnalisador

app = Flask(__name__)
analisador = ProcessosAnalisador('uploads/dados_je_geral_25042025.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    comarca_selecionada = request.form.get('comarca') or analisador.obter_comarcas()[0]
    ano_selecionado = int(request.form.get('ano') or analisador.obter_anos()[0])
    
    tabela = analisador.gerar_analise(comarca_selecionada, ano_selecionado)
    
    return render_template('index.html',
                         tabela=tabela.to_html(classes='table table-striped', index=False),
                         comarcas=analisador.obter_comarcas(),
                         anos=analisador.obter_anos(),
                         comarca_selecionada=comarca_selecionada,
                         ano_selecionado=ano_selecionado)

if __name__ == '__main__':
    app.run(debug=True)