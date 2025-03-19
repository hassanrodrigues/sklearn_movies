# Sistema de Recomendação de Filmes

Este é um sistema de recomendação de filmes que utiliza técnicas de processamento de linguagem natural e similaridade de cosseno para sugerir filmes baseados em gêneros e tags.

## Funcionalidades

- Busca de filmes no banco de dados SQLite
- Recomendação de filmes baseada em similaridade de conteúdo
- Processamento de texto usando TF-IDF (Term Frequency-Inverse Document Frequency)
- Cálculo de similaridade usando similaridade de cosseno
- Tratamento e transformação de dados de filmes
- Carregamento paralelo de dados

## Tecnologias Utilizadas

- Python
- scikit-learn (sklearn)
- SQLite
- SQLAlchemy
- TfidfVectorizer para processamento de texto
- Cosine Similarity para cálculo de similaridade
- ThreadPoolExecutor para processamento paralelo

## Estrutura do Projeto

- `main.py`: Contém a lógica principal do sistema de recomendação
- `models/models.py`: Define as classes de modelo de dados
- `movies.db`: Banco de dados SQLite com informações dos filmes
- `services/`: Diretório contendo os serviços de processamento de dados
  - `extract_data.py`: Responsável pela extração de dados dos arquivos CSV
  - `transform_data.py`: Realiza transformações nos dados dos filmes
  - `load_data.py`: Gerencia o carregamento dos dados no banco SQLite
  - `recomendations.py`: Implementa a lógica de recomendação

## Tratamento de Dados

O sistema possui um pipeline completo de tratamento de dados:

1. **Extração de Dados** (`extract_data.py`):
   - Leitura paralela de múltiplos arquivos CSV (filmes, tags, avaliações e links)
   - Processamento eficiente usando ThreadPoolExecutor
   - Tratamento de erros e validação de dados

2. **Transformação de Dados** (`transform_data.py`):
   - Extração do ano do título do filme
   - Normalização de títulos
   - Organização de gêneros e tags
   - Estruturação de avaliações e IDs externos (IMDB, TMDB)

3. **Carregamento de Dados** (`load_data.py`):
   - Persistência dos dados no banco SQLite usando SQLAlchemy
   - Inserção em lote para melhor performance
   - Controle de transações e tratamento de erros
   - Barra de progresso para acompanhamento do carregamento

## Como Usar

1. Certifique-se de ter as dependências instaladas:
```bash
pip install scikit-learn sqlalchemy tqdm
```

2. Execute o script principal:
```python
from main import recommend_movies_func_by_titles

# Exemplo de uso
movie_titles = ["Toy Story", "Jumanji"]
recommended = recommend_movies_func_by_titles(movie_titles, "movies.db")

# Imprimir filmes recomendados
for movie in recommended:
    print(movie.title)
```

## Como Funciona

1. O sistema busca todos os filmes no banco de dados
2. Para cada filme, combina seus gêneros e tags em um único texto
3. Utiliza TF-IDF para transformar o texto em vetores numéricos
4. Calcula a similaridade de cosseno entre todos os filmes
5. Para cada filme de entrada, encontra os 10 filmes mais similares
6. Retorna uma lista única dos filmes mais recomendados

## Requisitos

- Python 3.x
- scikit-learn
- SQLite3
- SQLAlchemy
- tqdm
