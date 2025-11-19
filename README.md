<!-- LOGO -->
<br />
<p align="center">
  <a href="https://github.com/bereis01/gitruck">
    <img src="./assets/gitruck_logo_no_bg.png" alt="Gitruck" width="250" height="250">
  </a>
  <h3 align="center"><strong>Gitruck</strong></h3>
  <p align="center">
    Uma ferramenta para análise de colaboração em repositórios!
    <br />
    <a href="https://github.com/bereis01/gitruck/issues">Report Bug</a>
    ·
    <a href="#Contato">Send Feedback</a>
  </p>
</p>
<div align="center">
    <img src="https://github.com/bereis01/gitruck/actions/workflows/tests.yml/badge.svg">
</div>

<!-- DESCRIPTION -->
# 🚚 Sobre o Projeto

**Gitruck** é uma ferramenta para análise da colaboração entre os desenvolvedores responsáveis por um repositório do GitHub. A funcionalidade principal da ferramenta é o cálculo do ***truck factor*** do repositório, isto é, *"a quantidade de desenvolvedores que, caso atropelados por um caminhão, levarão à discontinuação do projeto"*. Em outras palavras, a quantidade de desenvolvedores responsável pela maior parte da manutenção do sistema. Além disso, também são apresentadas outras métricas colaborativas relevantes, como os autores com a maior quantidade de arquivos sobre os quais são responsáveis e a evolução da quantidade de pessoas realizando *commits* e, de forma geral, contribuindo ao longo do tempo.

![Web Page](./assets/report.png)

<!-- TECHNOLOGIES -->
# 📟 Tecnologias

A ferramenta foi inteiramente implementada na linguagem de programação Python, em sua versão 3.12.3. Ela é composta de três principais módulos. O primeiro deles é responsável pela interface via linha de comando e, essencialmente, recebe, realiza o *parsing* e retorna internamente à aplicação os parâmetros fornecidos pelo usuário. Sua implementação foi baseada na biblioteca *argparse*, a qual faz parte da biblioteca padrão do Python. O segundo módulo é responsável pelo cálculo das diversas métricas apresentadas, sendo a principal delas o ***truck factor***. Nele, a biblioteca *GitPython* é utilizada para a clonagem local do repositório e para a extração das informações dele, como *commits* em um arquivo. Além disso, um programa, denominado *linguist*, é utilizado para a extração especificamente dos arquivos de código em um repositório, por ele fazer uma filtragem automática de arquivos terceiros ou automaticamente gerados. O módulo acessa esse programa por meio de uma interface da biblioteca *GitPython*, a qual permite a execução de comandos do terminal no contexto do repositório. Por fim, o último módulo é responsável pela geração da visualização dos resultados em formato *.html*. Este módulo não utiliza nenhuma biblioteca em especial. Os gráficos são gerados por meio da *Matplotlib*, enquanto o documento em si é montado manualmente.

<!-- USAGE -->
# ⚙️ Utilização



<!-- CONTACT -->
# ☎️ Contato

Bernardo Reis de Almeida (bera01@ufmg.br)
