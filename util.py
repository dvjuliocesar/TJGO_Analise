import pandas as pd

class ProcessosAnalisador:
    def __init__(self, arquivo_csv):
        self.df = self._carregar_dados(arquivo_csv)
    
    def _carregar_dados(self, arquivo_csv):
        df = pd.read_csv(arquivo_csv, sep=',', encoding='utf-8', parse_dates=['data_distribuicao', 'data_baixa'])
        return df

    def obter_comarcas(self):
        return sorted(self.df['comarca'].dropna().unique())

    def obter_anos(self):
        return sorted(self.df['data_distribuicao'].dt.year.dropna().unique())

    def gerar_analise(self, comarca, ano):
        # Filtros iniciais
        filtro_comarca = self.df['comarca'] == comarca
        filtro_ano = self.df['data_distribuicao'].dt.year == ano
        df_filtrado = self.df[filtro_comarca & filtro_ano].copy()
        
        # Cálculo das métricas
        analise = df_filtrado.groupby(['nome_area_acao', 'nome_assunto']).agg(
            Distribuídos=('data_distribuicao', 'count'),
            Baixados=('data_baixa', lambda x: x.notna().sum()),
            Pendentes=('data_baixa', lambda x: x.isna().sum())
        ).reset_index()
        
        # Adicionar totais
        totais = {
            'nome_area_acao': 'TOTAL',
            'nome_assunto': '',
            'Distribuídos': analise['Distribuídos'].sum(),
            'Baixados': analise['Baixados'].sum(),
            'Pendentes': analise['Pendentes'].sum()
        }
        
        return pd.concat([analise, pd.DataFrame([totais])], ignore_index=True)