# Bem vindo ao **BOT Telegram**!
<p><img height="20" src="https://img.shields.io/badge/Version-v1.0.0-green"/></p>

Um BOT de telegram com um objetivo de facilitar a pesquisa de preços e ter um scraping realizado de maneira mais rápida e fácil, digitando apenas um comando em um CHAT de Telegram.

A Api interna faz requisições para os Sites:
- [Amazon](https://www.amazon.com)
- [Magazine Luiza](https://www.magazineluiza.com.br)
- [Mercado Livre](https://mercadolivre.com)
- [Kabum](https://www.kabum.com.br)

## Redes Sociais
* [Instagram](https://www.instagram.com/claudiogfez/)
* [Linkedin](https://www.linkedin.com/in/clcostaf/)

## Pré requisitos
```
python <=3.9
```

## Instalação

1. É muito simples, você pode clonar este repositório.

```
git clone https://github.com/clcosta/bot-telegram.git
```

## Como utilizar

#### **O BOT já está funcionando, porém não está!**
Neste momento o BOT já poderia ser iniciado, porém é necessário fazer um configuração no Telegram. 

O telegram tem um sistema de BOTs controlados por um [_BOT FATHER_](https://telegram.me/botfather), que é responsável por gerar essa conta BOT e um token. O **Token** precisa ser passado em uma **variável de ambiente `BOT_TOKEN`**.

**OBS: É recomendado criar um arquivo chamado _.env_ e dentro colocar a sua variável com o valor do seu token, o script vai procurar está variável!**


[Como criar um BOT Telegram](https://core.telegram.org/bots)

#### **Agora com sim!**
Com a o `BOT_TOKEN` já setado agora é só rodar o BOT com:

```
python bot.py
```

### **Comandos**

No **CHAT** com o BOT digite `/<COMANDO>`, podendo ser os seguintes:

| Comando | Argumento | Resumo | Resposta |
| --- | --- | --- | --- |
| start | - | Faz um resumo dos comandos | Mensagem |
| help | - | Fornece detalhes e informações sobre o BOT e seu funcionamento | Mensagem |
| produto | PRODUTO | Faz a pesquisa pelo produto passado como argumento e retorna um arquivo *.json* para cada site | Arquivo |
| p | PRODUTO | Faz a pesquisa pelo produto passado como argumento e retorna os 10 primeiros resultados, _você pode escolher de qual site deseja ver_ | Mensagem |



### **Exceções conhecidas**

**O sistema de Scraping não é perfeito, algumas pesquisas podem não funcionar por segurança e proteção dos sites.** 

Na **Magazine Luiza** acontece o redirecionamento para verificar se o responsável pela requisição é humano, sendo necessário concluir um _CAPTCHA_ para liberar futuras requisições.

Na **Kabum** acontece o redirecionamento para filtros específicos do site, sendo redirecionado para promoções e listas especificas de produtos _(url diferente dependendo do produto)_.

**Como vem estes erros?**  
Você recebera a resposta do error contendo a seguinte sintaxe:

1. No arquivo _.json_

```json
"Error": {
    "code": 301,
    "message": "Moved Permanently",
    "redirect_link": "<URL>" // Se existir uma URL de redirecionamento.
}
```

2. Na mensagem do comando `/p`

```
Error: 301(Moved Permanently) - Redirect to :<URL> // Se existir URL de redirecionamento.
```

### **Debugg e personalização.**

O BOT tem um sistema de de **LOGS**, assim que for iniciado será gerado um diretorio chamado _logs/_.  
Com o LOG sem nenhuma modificação será passado somente as informações no nivel Informativo (INFO), as mesmas informações que são mostradas no terminal.

Existe uma variável de ambiente chamada `LOG_LVL` para realizar a mudança no nivél de exibição dos LOGs, os logs serão exibidos no terminal e um detalhamento será colocado no arquivo _log.log_.

Os niveis de LOG são definidos com uma string, e são:

1. CRITICAL
2. ERROR
3. WARNING
4. INFO
5. DEBUG

**Default é: `LOG_LVL=INFO`**

# Autor
| [<img src="https://avatars.githubusercontent.com/u/83929403?v=4" width=120><br><sub>@clcostaf</sub>](https://github.com/clcosta) |
| :---: |
