# Fundamentos de Segurança (base para o agente)

Guia curto para o agente conduzir análises como um profissional de segurança, sem atacar sistemas de terceiros. Todo teste é só em código e ambientes de laboratório próprios.

## Vulnerabilidade, ameaça, risco

- **Vulnerabilidade:** falha ou fraqueza em sistema, código ou configuração que pode ser explorada. Ex.: concatenação de entrada do usuário em consulta SQL.
- **Ameaça:** quem ou o que pode explorar a vulnerabilidade (pessoa, malware, condição). Ameaça sem vulnerabilidade não vira incidente.
- **Risco:** combinação de vulnerabilidade, ameaça e impacto. Risco = probabilidade de exploração × impacto se explorar. Por isso analisamos os três juntos.

## Tríade CIA

- **Confidencialidade:** guardar segredo. Ex.: senha não deve vazar em logs ou em consulta insegura.
- **Integridade:** nada é alterado sem autorização. Ex.: um atacante não deve mudar dados de outro usuário via SQL Injection.
- **Disponibilidade:** sistema acessível quando precisa. Ex.: um ataque não deve deixar o serviço fora do ar.

Toda vulnerabilidade fere pelo menos um dos três. Na análise, diga qual.

## Boas práticas defensivas

1. Nunca monte SQL concatenando entrada do usuário — use consulta parametrizada.
2. Valide e normalize entrada na borda, mas não confie só nisso.
3. Princípio do menor privilégio: código e usuários só com o acesso necessário.
4. Não exponha erro interno para quem usa o sistema.
5. Guarde senha com hash forte (ex.: bcrypt/argon2) — nunca texto puro.
6. Atualize dependências, tire serviços desnecessários da internet e revise logs.
7. Faça backup e teste restauração.
8. Documente a correção e rode nova varredura para confirmar a mitigação.

## Limites do laboratório

- Teste apenas código e servidores seus, em ambiente isolado (ex.: SQLite em memória, máquina virtual de lab).
- Nada de varrer IP, rede ou banco de terceiros.
- Exploração explicada aqui é conceitual, para entender e corrigir — não é guia de ataque.

## Links conceituais

- MITRE ATT&CK e OWASP Top 10 são referências públicas para nomear a técnica (ex.: Injection). Cite a técnica para organizar o estudo, não para reproduzir dano.
