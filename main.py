import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import cx_Oracle
from conexao_oracle import conectar_oracle

def enviar_email(destinatario, assunto, mensagem, bcc=None):
    smtp_server = 'email@dominio.com'
    porta = 587
    email_rem = 'email@teste.com'
    senha = 'senhaemail'

    msg = MIMEMultipart('related')
    msg['From'] = email_rem
    msg['To'] = destinatario
    msg['Subject'] = assunto

    if bcc:
        msg['Bcc'] = bcc

    caminho_imagem = r''

    if not os.path.isfile(caminho_imagem):
        print(f"Erro: A imagem de assinatura não foi encontrada no caminho: {caminho_imagem}")
        return

    try:
        # Verifica se a mensagem está no formato singular ou plural
        if 'o PDV' in mensagem:
            # Formato singular
            pdv = mensagem.split('o PDV ')[1].split(' está desligado')[0].strip()
            pdvs = pdv
            texto_alerta = f"o PDV <strong style='color: #e74c3c;'>{pdv}</strong> está desligado ou desconectado"
        else:
            # Formato plural
            pdvs_lista = mensagem.split('os PDVs ')[1].split(' estão desligados')[0].strip()
            pdvs = pdvs_lista
            texto_alerta = f"os PDVs <strong style='color: #e74c3c;'>{pdvs_lista}</strong> estão desligados ou desconectados"

    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        return

    mensagem_html = f"""<html>
<body style="font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px;">
    <!-- Card principal -->
    <table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
            <td align="center">
                <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <!-- Cabeçalho do card -->
                    <tr>
                        <td style="background-color: #e74c3c; padding: 15px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h2 style="color: white; margin: 0;">ALERTA DE PDV DESLIGADO OU DESCONECTADO</h2>
                        </td>
                    </tr>
                    
                    <!-- Corpo do card -->
                    <tr>
                        <td style="padding: 20px;">
                            <p style="font-size: 16px; color: #333;">Identificamos que {texto_alerta}.</p>
                            
                            <div style="background-color: #f9f9f9; border-left: 4px solid #e74c3c; padding: 10px 15px; margin: 15px 0;">
                                <p style="margin: 0; font-size: 15px; color: #555;">
                                    Favor verificar o cabo de rede. Caso o problema não seja resolvido, entre em contato com a equipe de Infraestrutura.
                                </p>
                            </div>
                            
                            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; margin-top: 15px;">
                                <p style="margin: 0; font-size: 14px; color: #666;">
                                    <strong>Detalhes:</strong> PDV(s) afetado(s): {pdvs}
                                </p>
                            </div>
                            
                            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-top: 20px;">
                                <tr>
                                    <td style="text-align: center; padding: 10px 0; border-top: 1px solid #eee;">
                                        <img src="cid:assinatura" alt="Assinatura" style="max-width: 200px;">
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""

    msg_alternativa = MIMEMultipart('alternative')
    msg_alternativa.attach(MIMEText(mensagem, 'plain'))
    msg_alternativa.attach(MIMEText(mensagem_html, 'html'))
    msg.attach(msg_alternativa)

    try:
        with open(caminho_imagem, 'rb') as img:
            assinatura_img = MIMEImage(img.read())
            assinatura_img.add_header('Content-ID', '<assinatura>')
            msg.attach(assinatura_img)

        server = smtplib.SMTP(smtp_server, porta)
        server.starttls()
        server.login(email_rem, senha)
        texto = msg.as_string()
        server.sendmail(email_rem, [destinatario] + (bcc.split(",") if bcc else []), texto)
        server.quit()
        print(f"E-mail enviado com sucesso para {destinatario}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")

# Conectar ao banco de dados Oracle
conexao = conectar_oracle()

# Query SQL
query = """
SELECT mensagem, destinatario FROM tabela_alertas WHERE status = 'PDV_OFF'
"""
#INSERT PARA TABELA DE LOG
insert_query = """
UPDATE tabela_alertas SET enviado = 1 WHERE status = 'PDV_OFF'
"""
try:
    cursor = conexao.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.execute(insert_query)
    conexao.commit()
    for row in resultados:
        mensagem = row[0]
        destinatario = row[1]
        assunto = 'PDV DESLIGADO OU DESCONECTADO'
        bcc = 'EMAIL@COPIA.COM' #EMAIL EM COPIA
        enviar_email(destinatario, assunto, mensagem, bcc=bcc)

    cursor.close()
    conexao.close()

except cx_Oracle.DatabaseError as e:
    print(f"Erro ao conectar ou consultar o banco de dados: {str(e)}")
