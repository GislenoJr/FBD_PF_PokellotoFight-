---------Ver quantidades de Pokemon por treinador----
CREATE OR REPLACE VIEW vw_qtd_pokemons_por_treinador AS
SELECT
    u.id_usuario,
    u.nome AS treinador,
    COUNT(tp.id_pokemon) AS qtd_pokemons
FROM usuario u
JOIN time t ON u.id_usuario = t.id_usuario
JOIN time_pokemon tp ON t.id_time = tp.id_time
GROUP BY u.id_usuario, u.nome;


CREATE OR REPLACE VIEW vw_qtd_pokemons_por_tipo AS
SELECT 
    pt.nome_tipo,
    COUNT(*) AS qtd_pokemons
FROM 
    pokemon_tipo pt
GROUP BY pt.nome_tipo
ORDER BY qtd_pokemons DESC;
----------pokémons com sua raridade e tipo-----------
CREATE OR REPLACE VIEW vw_pokemon_com_tipo AS
SELECT
    p.id_pokemon,
    p.nome,
    p.raridade,
    pt.nome_tipo
FROM pokemon p
JOIN pokemon_tipo pt ON p.id_pokemon = pt.id_pokemon;
