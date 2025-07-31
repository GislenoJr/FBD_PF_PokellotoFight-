-- Criar usuários
CREATE USER admin_user WITH PASSWORD 'admin123';
CREATE USER readonly_user WITH PASSWORD 'readonly123';

-- Dar privilégios ao admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_user;

-- Permissões somente leitura
GRANT CONNECT ON DATABASE seu_banco TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- Garantir que novas tabelas também sejam acessíveis:
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO readonly_user;
