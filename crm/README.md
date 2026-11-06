# CRM de Leads · Amper Energia

Página única (`index.html`) para qualificar leads de energia solar e serviços elétricos.

- **Importa CSV e Excel (.xlsx)**, incluindo a exportação de leads do Meta Ads (Instagram/Facebook).
  As colunas são reconhecidas pelo cabeçalho e você confere o mapeamento antes de importar.
  Faixas de valor da conta (ex.: `de_501_a_800`) viram o ponto médio.
- **Pontuação de 0 a 100**: consumo (35), perfil do cliente (15), decisor (15), prazo (15),
  pagamento (10) e área de instalação (10). Quente ≥ 70, morno 40–69, frio < 40.
- **Estimativa** de kWp, número de módulos, investimento e economia mensal (parâmetros editáveis).
- **Funil** com arrastar e soltar, lista ordenável, follow-ups atrasados, histórico de anotações,
  atalho para o WhatsApp e exportação para CSV (padrão Excel BR, com `;`).

Publicado como Artifact no claude.ai, os leads ficam salvos na nuvem. Aberto direto no navegador,
os dados ficam no `localStorage` daquele navegador.
