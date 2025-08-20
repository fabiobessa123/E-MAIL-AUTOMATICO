# 📧 Alerta de PDV Desligado ou Desconectado

Este projeto envia **alertas por e-mail** sempre que um **PDV (Ponto de Venda)** for identificado como **desligado ou desconectado**.  
O sistema se conecta a um banco de dados **Oracle**, consulta os PDVs com problemas, e envia um e-mail formatado em **HTML**, incluindo **assinatura com imagem** e destaque visual para facilitar a identificação do problema.

---

## 🚀 Funcionalidades
- Conexão com banco de dados **Oracle** via `cx_Oracle`.
- Consulta registros de PDVs desligados/desconectados.
- Geração automática de mensagem personalizada (singular/plural).
- Envio de **e-mail HTML estilizado** com:
  - Cabeçalho em destaque.
  - Detalhes do(s) PDV(s) afetado(s).
  - Orientações de suporte.
  - Assinatura em imagem.
- Suporte a cópia oculta (**BCC**) para múltiplos destinatários.


