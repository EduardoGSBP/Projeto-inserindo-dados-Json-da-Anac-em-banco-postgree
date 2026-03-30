# %%
import pandas as pd
import psycopg2
import os


# %%




caminho_do_arquivo = r"C:\Users\Eduardo\OneDrive\Documentos\Curso\Arquivos\01. Postgree\Origem de dados\V_OCORRENCIA_AMPLA.json"
df = pd.read_json(caminho_do_arquivo, encoding='utf-8-sig')


# %%
colunas = ["Numero_da_Ocorrencia", "Classificacao_da_Ocorrência", "Data_da_Ocorrencia","Municipio","UF","Regiao","Nome_do_Fabricante"]
df = df[colunas]
df.rename( columns={  'Classificacao_da_Ocorrência'   :  'Classificacao_da_Ocorrencia' }, inplace=True)


# %%
# Parâmetros de conexão
dbname   = 'python'
user     = 'postgres'
password =  os.getenv("DB_PASSWORD")
host     = 'localhost'
port     = '5432' 

conexao = psycopg2.connect(dbname=dbname,
                        user=user,
                        password=password,
                        host=host,
                        port=port)


cursor = conexao.cursor()
#delete base antes da carga

cursor.execute( "delete from public.Anac     "      )


#carga de dados
for indice,coluna_df in df.iterrows():
    cursor.execute( """ insert into Anac (       
			Numero_da_Ocorrencia, 
            Classificacao_da_Ocorrencia, 
            Data_da_Ocorrencia, 
            Municipio, 
            UF, 
            Regiao, 
            Nome_do_Fabricante
        ) VALUES (%s,%s,%s,%s,%s,%s,%s)

        """ ,(
            coluna_df["Numero_da_Ocorrencia"],
            coluna_df["Classificacao_da_Ocorrencia"],
            coluna_df["Data_da_Ocorrencia"],
            coluna_df["Municipio"],
            coluna_df["UF"],
            coluna_df["Regiao"],
            coluna_df["Nome_do_Fabricante"],
        
        )
    )

conexao.commit()
cursor.close()
conexao.close()
			


# %%



