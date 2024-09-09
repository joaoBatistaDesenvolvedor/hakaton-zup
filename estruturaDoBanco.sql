-- Tabela para armazenar informações dos usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(50) UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela para armazenar informações sobre empreendimentos
CREATE TABLE empreendimentos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo_empreeendimento VARCHAR(50),
    descricao_empreeendimento TEXT,
    objetivo TEXT
    
);

-- Tabela para armazenar áreas de interesse dos empreendimentos
CREATE TABLE areas_interesse (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- Tabela de junção para associar áreas de interesse aos empreendimentos
CREATE TABLE empreendimentos_areas_interesse (
    empreendimento_id INT REFERENCES empreendimentos(id) ON DELETE CASCADE,
    area_interesse_id INT REFERENCES areas_interesse(id) ON DELETE CASCADE,
    PRIMARY KEY (empreendimento_id, area_interesse_id)
);

-- Tabela para armazenar artigos
CREATE TABLE artigos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
    link VARCHAR(255)
);

-- Tabela de junção para associar artigos às áreas de interesse
CREATE TABLE artigos_areas_interesse (
    artigo_id INT REFERENCES artigos(id) ON DELETE CASCADE,
    area_interesse_id INT REFERENCES areas_interesse(id) ON DELETE CASCADE,
    PRIMARY KEY (artigo_id, area_interesse_id)
);
