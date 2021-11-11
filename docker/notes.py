# 1 O QUE É CONTAINER
import "fmt"
-CONTAINER NO SENTIDO DE ISOLAMENTO(DE PROCESSOS, NETWORK, USUARIOS) - na  forma logica - NAMESPACE
-NA PARTE FISICA - CGROUPS
-NÃO É MAQUINA VIRTUAL
# PRIMEIRAS SOLUCOES DE CONTAINER
-LXC = LINUX CONTAINER(CHROOT, NAMESPACE, CGROUPS)
-VPS = CONTAINER DA PARALELLS(OPEN VZ)

-DOCKER-2013-BASEADO EM LXC, NA DOTCLOUND COM SOLLOMON HIGHT

# 2-O QUE É DOCKER
-IMAGEM - PODE CONTER VARIAS CAMADAS(APACHE, PHP)
*** NÃO É RECOMENDADO TER VARIAS CAMADAS POIS SOMENTE A ULTIMA CAMADA É DE LEITURA/ESCRITA, LOGO SE PRECISAR DE UMA ARQUIVO QUE ESTA NA ULTIMA CAMADA, ELE FARA UMA COPIA DA CAMADA DESTA CAMADA PARA A CAMADA DE ESCRITA--LOGO ELE IRA ESCREVE NA CAMADA COPIA E NÃO NA ORIGINAL ** * NÃO É PPOSSIVEL ALTERAR NA IMAGEM ORIGINAL ** * A ULTIMA CAMADA(arquivos de log, etc) É EM TEMPO DE EXECULSÃO

-AS OUTRAS CAMADA SÃO SOMENTE DE ESCRITA-READ ONLY
-EXEMPLO 10 CONTAINER APACHE AMBOS EMBOS ESTARAM USANDO A MESMA IMAGENS

# 3-AINDA SOBRE O DOCKER
-USO DO KERNEL DO LINUX  DO PROPRIO HOST-PARA O MELHOR GERENCIAMENTO DE RECURSO
-MODOS PRA SE COMUNICAR - NETFILTER, IPTABLES(REDIRECT, DS-NAT)
***PIP NAMESPACE - ISOLAMENTO DE PROCESSOS
***NET NAMESPACE - ISOLAMENTO DE REDES
***MNT NAMESPACE - RESPONSAVEL PELOS PONTO DE MONTAGEM

***CGROUPS - RESPONSAVEL PELO GERENCIAMENTO DE MEMORIA, DISCO, ETC

# 4-INSTALAÇÃO DOCKER CE (STABLE -RELEASES) OU DOCKER EE
curl - fsSl https: // get.docker.com | bash
-INSTALARÁ O CLIENT(CLI)E O DOCKER ENGINE(QUE IRA GERENCIAR OS CONTAINER)
-PARA O USUARIO DA MAQUINA PODER GERANCIAR OS CONTAINER -> sudo usermod - aG docker srvia

To run Docker as a non-privileged user, consider setting up the
Docker daemon in rootless mode for your user:

    dockerd-rootless-setuptool.sh install

# Executando e administrando containers Docker
VERSÃO ANTIGA(LISTAR CONTAINER) docker ps
VERSÃO NOVA(ANTIGA AINDA FUNCIONA) docker container ls
docker image ls
docker network ls

# antigo docker run
EXECULTAR UM CONTAINER docker container run - ti hello-word(SE NÃO TIVER A IMAGE ELE IRA BAIXAR)

'''passos ao baixar a images
To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

'''
docker container ls - a(LISTA TDS OS CONATINERS PARADOS OU NÃO)
USO DE - ti TERA UM TERMINAL E INTERATIVIDADE
docker container run - ti ubuntu (JA ESTARA DENTRO DO CONTAINER APOS FINALIZAR A EXECULÇÃO root@276afe13f1d6: )
ps - ef(MOSTRA OS PROCESSOS EM EXECULÇÃO DENTRO DO CONTAINER)
cat / etc/issue(MOSTRA A VERSÃO DO KERNEL NO CONTAINER)
exit(SAI DO CONTAINER ATUAL) OU ctrl+p+q(SAI SEM MATAR O CONTAINER) OU ctrl+d(SAIR DO CONTAINER POREM ENCERRA A EXECULSÃO DELE)

# O PRINCIPAL PROCESSO DO CONTAINER É O ENTRYPOINT SE ENCERRADO, ENCERRA O CONTAINER (AQUI NO CASO É /BIN/BASH)

cat / etc/redhat-release(MOSTRA VERSÃO DO CONTAINER REDHAT)

docker container attach 95087986fbdb(AQUI É O CONTAINER ID OU O NOME DO CONTAINER)
OUTRO EXEMPLO: docker container run - ti nginx(PARECERÁ TRAVADO POREM É O ENTRYPOINT DO NGINX - ELE NÃO TERÁ O BASH, SOMENTE O PROPRIO PROCESSO)

# TODO PROCESSO DE UM CONTAINER TEM DE ESTAR RODANDO EM FOREGROUND-PRIMEIRO PLANO- (NÃO EM BACKGROUG COMO SERIA EM UMA INSTALAÇÃO NORMAL DO LINUX)
PARA ESSES CASOS:
docker container run - d nginx(O - d FARÁ O CONTAINER SER EXECULTADO COMO DAEMOM) -> NA MAIORIA DAS VEZES SERÁ CRIA UM CONTAINER EM MODO DAEMON

# SE ATACCHAR O CONTAINER NGINX NOVAMENTE E TECLAR CTRL+C O CONTAINER MORRERÁ NOVAMENTE
# PARA SE CONECTAR NESTE CONTAINER DE FORMA CORRETA:
docker container exec - ti 'container id sem aspas' 'comando sem desejado sem aspas'
- -> >>docker container exec - ti 93479ad7498d bash -> NESTE CASO SE TECLAR CTRL+D NÃO MATARÁ O CONTAINER POIS O PRINCIPAL PROCESSO DO NGINX NÃO É O BASH

TESTE: echo "saida do nginx teste" > /usr/share/nginx/html/index.html

# Executando e administrando containers Docker - parte2

docker container stop 93479ad7498d ( < -idcontainer)
docker container start 93479ad7498d(startar o container)
docker container restart 93479ad7498d


docker container inspect 7bbf0c26b021(MOSTRA TODAS AS INFORMAÇÕES DO CONTAINER COMO: CMD, MOUNTS, NETWORK, MEMORIA E CPU SENDO UTILIZADAS)
PAUSANDO E DESPAUSANDO
docker container pause 7bbf0c26b021(MOSTRAR EM STATUS PAUSED)
docker container unpause 7bbf0c26b021

docker container logs - f 93479ad7498d(MOSTRA A SAIDA DO CONTAINER - no exemplo nginx) ** *OS LOGS DO CONTAINER  TAMBEM DEVEM ESTAR EM PRIMEIRO PLANO

# O CONTEUDO ALTERADO EM UM CONTAINER É PERDIDO CASO O CONTAINER FOR ENCERRADO -CASO NÃO TENHA SIDO FEITO EM NENHUM VOLUME

docker container rm 93479ad7498d NÃO É POSSIVEL REMOVER O CONTAINER CASO ESTEJA EM EXECULÇÃO - O COMANDO SO FUNCIONARÁ CASO ESTEJA PARADO

docker container rm - f 93479ad7498d FORÇA A REMOÇÃO DO CONTAINER

# Configurando CPU e memória para os meus containers

docker container stats 93479ad7498d - MOSTRA O QUANTO ESTA SENDO UTILIZADO DE RECURSOS

TESTES DENTRO DO DOCKER -> stress - -cpu 1 - -vm-bytes 128M - -vm 1 - TESTE DE STRESS

docker container top 93479ad7498d = > MOSTRA OS PROCESSO DO CONTAINER
# LIMITANDO MEMORIA
docker container run - d - m 128M nginx == SETA O CONTAINER PRA USAR NO MAXIMO 128M DE MEMORIA(ou - -memory)

stress - -vm1 - -vm-bytes 120M -> TESTE DE STRESS NA MEMORIA(DENTRO DO CONTAINER)
# LIMITANDO CPUS
apt-get install & & apt-get - y stress

docker container run - d - m 128M - -cpus 0.5 nginx(USARÁ  50 % DE UM CORE)

TESTE DE STRESS -> stress - -cpu 1 - -vm 1 - -vm-bytes 64M
CAT / PROC/CPUINFO

docker container updade - -cpu idcontainer(ATUALIZA O RECURSO DE UM CONTAINER)


# Meu primeiro e tosko Dockerfile

docker images = LISTA TODAS AS IMAGENS(ANTIGO)
docker image ls = LISTA TODAS AS IMAGENS

Arquivo dockerfile precisa chamar: Dockerfile

"""
FROM debian

LABEL app="giropops"

ENV DIA="hoje"

RUN apt-get update && apt-get install -y stress && apt-get clean (RODA ENQUANTO ESTIVER BUILDANDO A IMAGEM)

CMD stress --cpu 1 --vm-bytes 64M --vm 1 (SOMENTE UM CMD POR IMAGEM )

"""
# PARA BUILDAR A IMAGE
docker image build - t tosko: 1.0 .  (-t "nomedaTag sem aspas:versão" .- O PONTO É PARA PEGAR A PARTIR DO DIRETORIO)

APOS BUILDADO PARA EXECULTA-LO:
docker container run - d tosko: 1.0


# ===============DIA 2===========
Obs: GitLab ja contem registry

# USO DE VOLUMES POIS SEMPRE QUE O CONTAINER ENCERRA OS DADOS SÃO PERDIDOS ***
EM USO DE VOLUMES NO DOCKER SE TEM 2 OPÇÕES: DO TIPO BIND(***QUANDO SE TEM UM DIRETORIO E SE QUER MONTAR DENTRO DO CONTAINER)
docker container run - ti - -mount type = bind, src = /opt/giropops, dst = /giropops, ro debian
(
    ro-ready only
    type-tipo do volume
    - -mount - monta um volume
    src=ponto de montagem do host
    dst=ponto de montagem do container
)

E DO TIPO VOLUME


# SE NÃO FOR FEITO A GESTÃO DE VOLUMES IRA CRIA UM NOME ALEATORIO

# Volumes - Tipo Volume

docker volume ls(MOSTRA OS VOLUMES ATUAIS)
docker volume create giropops(CRIA UM VOLUME)
docker volume inspect 'nome volume sem aspas'(INSPECIONA UM VOLUME)
{
    "CreatedAt": "2021-08-02T16:38:07-03:00",
    "Driver": "local",
    "Labels": {},
    "Mountpoint": "/var/lib/docker/volumes/giropops/_data", (TODO VOLUME NO DOCKER ESTARÁ NESTA PASTA)
    "Name": "giropops",
    "Options": {},
    "Scope": "local"
}

# PARA ADICIONAR O VOLUME CRIADO EM UM NOVO CONTAINER :
docker container run - ti - -mount type = volume, src = giropops, dst = /giropops debian

POSSIBILIDADE DE USAR "DOCKER PLUGINS" PRA USAR PLUGINS NOS VOLUMES

O MESMO VOLUME PODE SER COMPARTILHADO POR VARIOS CONTAINER

docker volume rm giropops(REMOVER O VOLUME CASO NENHUM CONTAINER ESTEJA USANDO ELE - MESMO SE O CONTAINER ESTIVER PARADO NÃO DEIXARÁ REMOVER SE ESTIVER USANDO)

docker volume rm - f giropops(TAMBEM REMOVE O CONTAINER)

# Volumes - Data-Only e Prune

docker volume prune(APAGA TODOS OS VOLUMES QUE NÃO ESTÃO SENDO UTILIZADOS-CUIDADO!!! - O MESMO SERVE PARA CONTAINERS)
docker container prune(APAGA TODOS OS CONTAINERS PARADOS)

docker container create(SOMENTE CRIA O CONTAINER, NÃO COLOCA ELE EM EXECULÇÃO)

EXEMPLO: SINTAXE ANTIGA
1 - docker container create - v / opt/giropops/: / data - -name dbdados centos
(postgresql cria diretorio / data)
2 - docker run - d - p 5432: 5432 - -name pgsql1 - -volumes-from dbdados - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql

3 - docker run - d - p 5433: 5432 - -name pgsql2 - -volumes-from dbdados - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql

4 - docker logs - f "idcontainer sem aspas" (VERIFICA LOGS DE UM CONTAINER)

(DOS PASSOS 1-4 OCORRERÁ PROBLEMAS QUANTO A PERMISSÕES DO VOLUME E OS CONTAINERS NÃO SUBIRAM)

SOLUÇÃO:
docker container create - v / data - -name dbdados centos
2 - docker run - d - p 5432: 5432 - -name pgsql1 - -volumes-from dbdados - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql

3 - docker run - d - p 5433: 5432 - -name pgsql2 - -volumes-from dbdados - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql

VOLUMES ESTARAM NA MAQUINA HOSTS EM:  cd / var/lib/docker/volumes/_data(DADOS DO POST ESTARAM AQUI)

#Volumes - Desafio

docker volume create dbdados
docker run - d - p 5432: 5432 - -name pgsql1 - -mount type = volume, src = dbdados, dst = /data - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql
docker run - d - p 5433: 5432 - -name pgsql2 - -mount type = volume, src = dbdados, dst = /data - e POSTGRESQL_USER = docker - e POSTGRESQL_PASS = docker - e POSTGRESQL_DB = docker kamui/postgresql

OBS: QUANDO FUI TENTAR CRIEI COM TYPE = BIND

# Volume - Exemplo Backup
CRIANDO O BACKUP ATRAVES DE UM CONTAINER:
mkdir / opt/backup
# uso do bind quando se usa um diretorio ja criado
docker container run - ti - -mount type = volume, src = dbdados, dst = /data - -mount type = bind, src = /opt/backup, dst = /backup debian tar - cvf / backup/bkp-banco.tar / data

# Volumes - Exemplo de comandos

# docker container run -ti --mount type=bind,src=/volume,dst=/volume ubuntu
# docker container run -ti --mount type=bind,src=/root/primeiro_container,dst=/volume ubuntu
# docker container run -ti --mount type=bind,src=/root/primeiro_container,dst=/volume,ro ubuntu
# docker volume create giropops
# docker volume rm giropops
# docker volume inspect giropops
# docker volume prune
# docker container run -d --mount type=volume,source=giropops,destination=/var/opa  nginx
# docker container create -v /data --name dbdados centos
# docker run -d -p 5432:5432 --name pgsql1 --volumes-from dbdados -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
# docker run -d -p 5433:5432 --name pgsql2 --volumes-from dbdados -e  POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker kamui/postgresql
# docker run -ti --volumes-from dbdados -v $(pwd):/backup debian tar -cvf /backup/backup.tar /data

# Dockerfile - Parte 01
IMAGEM EQUIVALE A UM CONTAINER PARADO
-> CUIDADO AO EXECULTAR UMA IMAGEM DE TERCEIROS(DOCKERHUB), POR CONTA DE VUNERABILIDADES
-> OPÇÃO POR USO DO ALPINE(CONTEM GERENCIADOR DE PACOTES)
Exemplo:
FROM debian

RUN apt-get update & & apt-get install - y apache2 & & apt-get clean(ATUALMENTE DESNECESSARIO O CLEAN - SEM / VAR/LIB/CACHE NO CONTAINER - .DEB REMOVIDO AUTOMATICAMENTE)

ENV APACHE_LOCKE_DIR = "/var/lock"
ENV APACHE_PID_FILE = "/var/run/apache2.pid"
ENV APACHE_RUN_USER = "www-data"
ENV APACHE_RUN_GROUP ='www-data"
ENV APACHE_LOG_DIR = "/var/log/apache2"

LABEL description = "webserver"
LABEL  version = "1.0.0"

# onde o volume do container será montado (SOMENTE EM VISÃO DE CONTAINER )
VOLUME / var/www/html/

EXPOSE 80
# OUTRAS OPÇÕES LINHA DE COMANDO :
docker container run - ti - P(O - P BINDA O CONTAINER COM UMA PORTA ALEATORIA)
docker container run - ti - p 8080: 80

***O CONTAINER IRA EXECULTAR POREM O SERVIÇO DO APACHE NÃO ESTARÁ RODANDO POIS ESTE DOCKERFILE NÃO CONTEM ENTRYPOINT OU CMD

# NO DOCKERFILE É MAIS DESVINCULADO AO HOST (DOCKER -COMPOSE TEM MAIOR INTERAÇÃO COM O HOST)
[
    run - execultado no momento do build
    & & -para instalar  varias coisas na mesma camada(somente a ultima camada é de leitura e escrita)
]
# PARA EXECULTAR O ARQUIVO DOCKERFILE E CRIAR A IMAGEM :
docker image build - t minhaimagem: 1.0.0 . (COLOCADO TAG PARA NÃO SUBIR SEM NOME)

docker image ls(MOSTRA AS IMAGENS BUILDADAS/BAIXADAS)

docker container run - ti minhaimagem: 1.0.0 (EXECULTA A IMAGEM BUILDADA)

#  Dockerfile - Parte 02
ENTRYPOINT - É O PRINCIPAL PROCESSO DO CONTAINER(equivalente ao init do linux)

CMD - CASO O ENTRYPOINT NÃO EXITA PODE SER PASSADO NO CMD -> PASSA PARAMETROS PARA O BASH

# CASO EXISTA OS DOIS NO DOCKERFILE : O CMD NÃO PODERÁ CHAMAR QUALQUER COMANDO
******** O CMD SOMENTE PASSA PARAMENTO PARA O PRINCIPAL PROCESSO DO CONTAINER, LOGO SE EXISTI O ENTRYPOINT ELES ESTARÁ PASSANDO PARAMENTOS PARA ELE(COMPLEMENTANDO)
SEM O ENTRYPOINT NAO EXISTIR O CMD ESTARÁ PASSANDO PARAMENTROS PARA O BASH(NO LINUX) QUE SERÁ O PRINCIPAL PROCESSO

EXEMPLO:
"""
FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean (ATUALMENTE DESNECESSARIO O CLEAN -SEM /VAR/LIB/CACHE NO CONTAINER -.DEB REMOVIDO AUTOMATICAMENTE )

ENV APACHE_LOCKE_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_GROUP='www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

LABEL description="webserver"
LABEL  version="1.0.0"

VOLUME /var/www/html/  #onde o volume do container será montado (SOMENTE EM VISÃO DE CONTAINER )

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apachectl"] #PROCESSO RODARÁ EM PRIMEIRO PLANO 

CMD ["-D", "FOREGROUND"]
"""
Execultando novamente
-- -> docker image build - t minhaimagem: 2.0.0 .

# PARA BUILDAR A IMAGEM SEM USA O CACHE DE IMAGENS ANTERIORES
-- -> docker image build - t minhaimagem: 2.0.0 . --no-cache
EXECULTANDO NOVAMENTE A IMAGEM
- -> docker container run - d - p 8080: 80 apachesss: 2.0.0


# Dockerfile - Parte 04
O COMANDO COPY: COPIA UM ARQUIVO OU DIRETORIO ATUAL EM QUE ESTA O DOCKERFILE NO HOST PARA DENTRO DE UM DIRETORIO NO CONTAINER
"""

FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean (ATUALMENTE DESNECESSARIO O CLEAN -SEM /VAR/LIB/CACHE NO CONTAINER -.DEB REMOVIDO AUTOMATICAMENTE )

ENV APACHE_LOCKE_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_GROUP='www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

COPY index.html /var/www/html/ #COPIA O QUE ESTA NO DIRETORIO ATUAL DO DOCKERFILE PARA A PASTA /VAR/WWW/HTML/ DO CONTAINER

LABEL description="webserver"
LABEL  version="1.0.0"

VOLUME /var/www/html/  #onde o volume do container será montado (SOMENTE EM VISÃO DE CONTAINER )

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apachectl"] #PROCESSO RODARÁ EM PRIMEIRO PLANO 

CMD ["-D", "FOREGROUND"]

"""
EXECULTANDO NOVAMENTE A IMAGEM
- -> docker container run - d - p 8000: 80 apachesss: 3.0.0

O COMANDO ADD: TEM A MESMA FUNÇÃO DO COPY POREM NO ADD CASO EXISTA ARQUIVOS .TAR(COMPACTADOS) ELE COPIARÁ PARA O CONTAINER O CONTEUDO JA EXTRAIDO(DESCOMPACTADO). CASO SEJA NECESSARIO BAIXAR ALGUM ARQUIVO NA WEB, O ADD JÁ FARÁ O DOWNLOAD DO ARQUIVO PARA DENTRO DO CONTAINER

ADD index.html / var/www/html/

"""

FROM debian

RUN apt-get update && apt-get install -y apache2 && apt-get clean (ATUALMENTE DESNECESSARIO O CLEAN -SEM /VAR/LIB/CACHE NO CONTAINER -.DEB REMOVIDO AUTOMATICAMENTE )

ENV APACHE_LOCKE_DIR="/var/lock"
ENV APACHE_PID_FILE="/var/run/apache2.pid"
ENV APACHE_RUN_USER="www-data"
ENV APACHE_RUN_GROUP='www-data"
ENV APACHE_LOG_DIR="/var/log/apache2"

ADD index.html /var/www/html/ #COPIA O QUE ESTA NO DIRETORIO ATUAL DO DOCKERFILE PARA A PASTA /VAR/WWW/HTML/ DO CONTAINER

LABEL description="webserver"
LABEL  version="1.0.0"

USER www-data #EXECULTARÁ O CONTAINER COMO O USUARIO WWW-DATA -->>> AO EXECULTAR,O CONTAINER NÃO SUBIU POR CONTA DO USUARIO QUE TERIA QUE SER O ROOT 

WORKDIR /var/www/html/  #FAZ COM QUE O DIRETORIO DEFAULT APOS SER STARTADO, SEJA TAL DIRETORIO 

VOLUME /var/www/html/  #onde o volume do container será montado (SOMENTE EM VISÃO DE CONTAINER )

EXPOSE 80

ENTRYPOINT ["/usr/sbin/apachectl"] #PROCESSO RODARÁ EM PRIMEIRO PLANO 

CMD ["-D", "FOREGROUND"]

"""
- -> >> AO EXECULTAR, O CONTAINER NÃO SUBIU POR CONTA DO USUARIO QUE TERIA QUE SER O ROOT  E POR CONTA DA PORTA BAIXA(80) ONDE SOMENTE O ROOT PODE BINDAR

docker container logs - f idcontainer

'''PARA CORRIGIR : 
RUN chown www-data:www-data /var/lock && chown www-data:www-data /var/run/ && chown www-data:www-data /var/log

'''

#Dockerfile - MultiStage
Exemplo:
FROM golang

WORKDIR / app

ADD . / app

RUN go build - o app_go

ENTRYPOINT ./app_go

BUILDANDO:
docker image build - t appgo: 1.0 .
NO EXEMPLO DEU ERRO DE BUILD go.mod  file not found

# TRABALHANDO EM MULTSTAGE (SIMILAR AO PIPELINE)

FROM golang AS buildando

WORKDIR / app

ADD . / app

RUN go build - o appgo

FROM alpine

WORKDIR / giropops

# PEGARA OS DADOS DA CAMADA DE CIMA (BUILDANDO) E COPIA PRA /GIROPOPS
COPY - -from = buildando / app/appgo / giropops/

ENTRYPOINT ./appgo

== == == == == == == == == == == = SO EXECULTOU QUANDO ALTERADO O RUN PAR CMD
FROM golang AS buildando

WORKDIR / app

ADD . / app

CMD go build - o app_go

FROM alpine

WORKDIR / giropops

COPY - -from = buildando / app/app_go.go / giropops/

ENTRYPOINT ./app_go.go


docker container run - ti meugo: 3.0 (PARA EXECULTAR ESTA COM PERMISSION DENIED)

- -> AO USAR A IMAGEM DO ALPINE O IMAGEM É REDUZIDA PRA 1 % DO IMAGEM SOMENTE COM O GOLANG


# Palestra Images Deep Dive, Healthcheck e Docker commit
->EXECULÇÃO EM MULTI-LINE
RUN apt-get update & & \
    apt-get install - y apache2 & & \
    apt-get clean

->OU ->
RUN apt-get update & & \
    apt-get install - y apache2 \
    apt-get clean

->QUANDO PRECISO ENTRA EM PASTA USAR O RUN CD "DIRETORIO"
[
    .DOCKERIGNORE
    MODO SHELL E MODO EXEC9(OBRIGATORIO SE TIVER ENTRYPOINT E CMD)
    ARG
    VARIAVEIS
    IMUTAVEL E EFEMERAL
    MODO EXEC E MODO SHELL
    ADD X CMD
    HEALTHCHECK
    MULTISTAGE
    | |= OR
]
docker ps - q(MOSTRA SOMENTE O ID DOS CONTINER)

docker container rm - f $(docker ps - q)(EXCLUI OS CONTAINERS)

docker commit - m "ubuntu com vim e curl " idcontainer(TRANSFORMA O CONTAINER EM UMA IMAGEM)

docker image tag idimage nomedatag(TAGEANDO UMA IMAGEM)

== == == == == == == == == == == == == = EXEMPLOS == == == == == == == == == == == == == == == == == == == == == == ==
FROM debian

RUN apt-get update & & apt-get install - y apache2 & & apt-get clean
ENV APACHE_LOCK_DIR = "/var/lock"
ENV APACHE_PID_FILE = "/var/run/apache2.pid"
ENV APACHE_RUN_USER = "www-data"
ENV APACHE_RUN_GROUP = "www-data"
ENV APACHE_LOG_DIR = "/var/log/apache2"

LABEL description = "Webserver"

VOLUME / var/www/html/
EXPOSE 80
-----------------------------------------------------------------------------------
FROM debian

RUN apt-get update & & apt-get install - y apache2 & & apt-get clean
ENV APACHE_LOCK_DIR = "/var/lock"
ENV APACHE_PID_FILE = "/var/run/apache2/apache2.pid"
ENV APACHE_RUN_USER = "www-data"
ENV APACHE_RUN_DIR = "/var/run/apache2"
ENV APACHE_RUN_GROUP = "www-data"
ENV APACHE_LOG_DIR = "/var/log/apache2"

LABEL description = "Webserver"

VOLUME / var/www/html/
EXPOSE 80

ENTRYPOINT["/usr/sbin/apachectl"]
CMD["-D", "FOREGROUND"]
-----------------------------------------------------------------------------------
package main

func main() {
    fmt.Println("GIROPOPS STRIGUS GIRUS - LINUXTIPS")
}

---------------------------------------------------------------------------------
FROM golang

WORKDIR / app
ADD . / app
RUN go build - o goapp
ENTRYPOINT ./goapp

-----------------------------------------------------------------------------------
FROM golang AS buildando

ADD . / src
WORKDIR / src
RUN go build - o goapp


FROM alpine: 3.1

WORKDIR / app
COPY - -from = buildando / src/goapp / app
ENTRYPOINT ./goapp
----------------------------------------------------------------------------------
ADD = > Copia novos arquivos, diretórios, arquivos TAR ou arquivos remotos e os adicionam ao filesystem do container

CMD = > Executa um comando, diferente do RUN que executa o comando no momento em que está "buildando" a imagem, o CMD executa no início da execução do container

LABEL = > Adiciona metadados a imagem como versão, descrição e fabricante

COPY = > Copia novos arquivos e diretórios e os adicionam ao filesystem do container

ENTRYPOINT = > Permite você configurar um container para rodar um executável, e quando esse executável for finalizado, o container também será

ENV = > Informa variáveis de ambiente ao container

EXPOSE = > Informa qual porta o container estará ouvindo

FROM = > Indica qual imagem será utilizada como base, ela precisa ser a primeira linha do Dockerfile

MAINTAINER = > Autor da imagem

RUN = > Executa qualquer comando em uma nova camada no topo da imagem e "commita" as alterações. Essas alterações você poderá utilizar nas próximas instruções de seu Dockerfile

USER = > Determina qual o usuário será utilizado na imagem. Por default é o root

VOLUME = > Permite a criação de um ponto de montagem no container

WORKDIR = > Responsável por mudar do diretório / (raiz) para o especificado nele


== == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

# Dockerhub - Parte 01

docker image tag 68edcbed14fb phhiilliippss/meugo: 5.0 (FORMA DE SUBIR UMA IMAGEM PARA O DOCKER HUB)

docker login(LOGAR PELO TERMINAL NA CONTA DO DOCKERHUB)

docker push phhiilliippss/meugo: 5.0  (FAZ O PUSH-UPLOAD - PARA O DOCKER HUB)

# Dockerhub - Parte 02
docker pull phhiilliippss/meugo(BAIXA A IMAGEM DO REPOSITORIO)

OU

docker container run - d  phhiilliippss/meugo: 5.0 (BAIXA E EXECULTA A IMAGEM)

# Docker Registry
É O REPOSITORIO - REMOTO OU LOCAL - ONDE ESTA SALVO AS IMAGENS

docker container run - d - p 5000: 5000 - -restart = always - -name registry registry: 2 (SOBE O DOCKER REGISTRY NA MAQUINA)

docker logout(DESLOGA DO DOCKER HUB)
(FAZ O UPLOAD DA IMAGE PARA O REGISTRY CRIADO):
->NECESSARIO RETAGUEAR A IMAGE PARA O HOST LOCAL
docker image tag 68edcbed14fb localhost: 5000/meugo: 5.0

EM SEGUIDA PODERÁ FAZER O PUSH PARA O REGISTRY LOCAL
docker push localhost: 5000/meugo: 3.0

EM SEGUIDA PODERÁ EXCLUIR A IMAGE CASO QUEIRA POIS ELA JA ESTA NO REGISTRY

docker image rm - f 68edcbed14fb ec4f11c8ea56

# Registry - Parte 02 e Banho de cerveja

curl localhost: 5000/v2/_catalog(PARA VISUALIZAR AS IMAGENS DO REPOSITORIO LOCAL)

curl localhost: 5000/v2/meugo/tags/list(MOSTRA AS VERSÕES E TAGS DAS IMAGENS NO REGISTRY)

LOCAL NO REGISTRY ONDE FICAM AS IMAGENS -> cd/var/lib/docker/registry/v2/repositories


# DockerHub e Registry - Exemplo comandos

# docker image inspect debian
# docker history linuxtips/apache:1.0
# docker login
# docker login registry.suaempresa.com
# docker push linuxtips/apache:1.0
# docker pull linuxtips/apache:1.0
# docker image ls
# docker container run -d -p 5000:5000 --restart=always --name registry registry:2
# docker tag IMAGEMID localhost:5000/apache

# =========================== DIA 3 =========================================
# Docker Machine - Parte 1
***DOCKER MACHINNE É PARA QUE SE OPERE MAQUINAS VIRTUAIS RODANDO O DOCKER ** *= > NECESSARIO USAR A PROPRIA MAQUINA OU SERVER(Não é em vm é no desktop)
-ELE FARÁ O PROVISIONAMENTO DE UMA MAQUINA COM DOCKER

DOCKER SWARM -> É UM ORQUESTRADOR DE CONTAINERS NATIVO DO DOCKER - É UM CLUSTER COM ALTA DISPONIBILIDADE

KUBERNETS É UM OUTRO ORQUESTRADOR DE CONTAINER

INSTALAÇÃO: https: // docs.docker.com/machine/install-machine/

# Docker Machine - Parte 2

docker-machine create - -driver virtualbox nomedamaquina(USANDO O DRIVE DO VIRTUALBOX)

-> QUANDO LISTAR OS CONTAINERS LISTARÁ ONDE ESTÃO REMOTAMENTE:
docker-machine ls(LISTA OS DOCKERMAQUINE INSTALADOS)

docker-machine ip nomedocontainer

docker-machine ssh nomedocontainer(SE CONECTA VIA SSH NO DOCKER MACHINE)
|
- -> logout(SAI DO DOCKER MACHINE)

docker-machine env giropops(MOSTRARÁ AS VARIAVEIS DE AMBIENTE)

-> SE EXECULTAR AS VARIAVEIS DE AMIENTE NO TERMINAL JA ESTARÁ DENTRO DA DOCKER-MACHINE REMOTA

{
    export DOCKER_TLS_VERIFY = "1"
    export DOCKER_HOST = "tcp://192.168.99.100:2376"
    export DOCKER_CERT_PATH = "C:\Users\Adapter\.docker\machine\machines\giropops"
    export DOCKER_MACHINE_NAME = "giropops"
    export COMPOSE_CONVERT_WINDOWS_PATHS = "true"

} OU NO WINDOWS -> eval $("C:\Users\Adapter\bin\docker-machine.exe" env giropops)

EM TESTES: IP = 192.168.99.100: 8080

docke-machine inspect giropops(MOSTRA DETALHES DA DOCKERMACHINE)

docker-machine stop giropops(PARA O DOCKER MACHINE)
docker-machine start giropops
docker-machine status giropops

docker-machine env - u(REMOVE AS VARIAVEIS DE AMBIENTE QUE FAZEM SE CONECTAR DIRETO NO DOCKER MACHINE)

docker-machine rm giropops(EXCLUI O DOCKER MACHINE)

# Qual o comando utilizado para visualizar as variáveis de ambiente responsáveis por desfazer a configuração que fazia o seu docker client apontar para um docker daemon de um host criado pelo docker-machine?


== == == == COMANDOS == == == =  Docker Machine - Comandos
Para fazer a instalação do Docker Machine no Linux, faça:

    # curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine -`uname - s`-`uname - m` > /tmp/docker-machine
# chmod +x /tmp/docker-machine
# sudo cp /tmp/docker-machine /usr/local/bin/docker-machine


Para seguir com a instalação no macOS:

    # curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine -`uname - s`-`uname - m` > /usr/local/bin/docker-machine
# chmod +x /usr/local/bin/docker-machine

Para seguir com a instalação no Windows caso esteja usando o Git bash:

    # if [[ ! -d "$HOME/bin" ]]; then mkdir -p "$HOME/bin"; fi
    # curl -L https://github.com/docker/machine/releases/download/v0.16.1
/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe"
# chmod +x "$HOME/bin/docker-machine.exe"


Para verificar se ele foi instalado e qual a sua versão, faça:

    # docker-machine version

    # docker-machine create --driver virtualbox linuxtips

    # docker-machine ls

    # docker-machine env linuxtips

    # eval "$(docker-machine env linuxtips)"

    # docker container ls

    # docker container run busybox echo "LINUXTIPS, VAIIII"

    # docker-machine ip linuxtips

    # docker-machine ssh linuxtips

    # docker-machine inspect linuxtips

    # docker-machine stop linuxtips

    # docker-machine ls

    # docker-machine start linuxtips

    # docker-machine rm linuxtips

    # eval $(docker-machine env -u)

== == == == == == == == == == == == == ==

# Docker Swarm - Parte 1
->ORQUESTRADOR DE CONTAINER(quando necessario integrar com outras ferramentas, balanceamento de carga)
- -> NECESSARIO QUANDO SE DESEJA USAR CLUSTERS, TER ALTA DISPONIBILIDADE
-- -> WORKER(MANTER OS CONTAINER EM EXECUÇÃO) E MANAGER(PARA ADMINISTRAÇÃO DO CLUSTER-CONTAINER DE TODOS OS SERVIÇOS - TODA A INFORMAÇÃO SENSIVEL DO CLUSTER - MAS TBEM PODE SER RESPONSAVEL PELA EXECUÇÃO) - DENTRO DO SWARM PARA O GERENCIAMENTO

--- -> PARA MANTER O CLUSTER SWARM EM EXECULSÃO É NECESSARIO MANTER NO MINIMO 51 % DO DOS NODES COM PAPEL DE MANAGER FUNCIONANDO -> LOGO É BOM TER SEMPRE UM NUMERO IMPAR DE NODES
----- -> NÃO É RECOMENDADO MANTER TODOS OS NODES COM PAPEL DE MANAGER POR CONTA DE DOWNTIME(ELEIÇÃO DE PROXIMO MANAGE ATIVO)-DEMORA PARA ESCOLHER OS CLUSTER

docker swarm - -help

docker swarm init(INICIA O SWARM NA MAQUINA HOST)

# CASO TENHA MAIS DE UMA INTERFACE DE REDE NA MAQUINA É NECESSARIO ESPECIFICAR QUAL SERÁ UTILIZADAS
docker swarm init - -advertise-addr 192.168.0.1

docker swarm join - -token SWMTKN-1-4qq5u5x0kl5xd5cnuvryrp78q44xde40s333byawk1r403m1y5-5ir7s8eccp1vldtbdnp5lzp3i 192.168.0.10: 2377 (NECESSARIO RODAR O SWARM JOIN NAS OUTRAS MAQUINAS HOSTS QUE FARAM PARTE DO SWARM)

# VERIFICAR FIREWALL firewall-cmd --add-port=2377/tcp
# Docker Swarm - Parte 2
docker swarn leave(SAI DO CLUSTER)

# NAS OUTRAS MAQUINA QUE FARAM PARTE DO CLUSTER:
->NECESSARIO INSTALAR O DOCKER
curl - fsSL https: // get.docker.com | bash

docker node ls(MOSTRA OS NODES(CONTAINERS) QUE FAZEM PARTE DO SWARM-MONSTRANDO QUEM É O LEADER)
docker node promote hostname(PROMOVE O NODE A LEADER-PREENCHE O STATUS - QUE SERA O MANAGER)
docker node demote hostname(REMOVE O NODE DE MANAGER)

# SE UM DOS NODES FOR MANAGER
docker swarm leave - f(-F PARA FORÇAR A SAIDA)

# Docker Swarm - Node
# CASO PERCAR O TOKEN DO DOCKER SWARM (TOKEN DE WORKER E MANAGER SÃO DIFERENTES)
docker swarm join-token worker(MOSTRARÁ O TOKEN DO SWARM ATIVO)
docker swarm join-token manager

docker node rm hostname(DELETA O NODE)

docker swarm join-token - -rotate worker(atualiza a chave token - necessario ao adicionar novos hosts ao cluster)

docker note inspect nomedonode(MOSTRA INFORMAÇÕES SOBRE O NODE)
# OPÇÕES (drain-limpa os container do nó-DESLIGARÁ OS CONTAINER DA MAQUINA E IRA SUBIR EM OUTRO HOST DO CLUSTER ,pause-não receberá novos containers,active-aceita novos containers )
docker node update - -availability pause eliote-02

# PARA MONITORAR OS NODES PODE-SE ADICIONAR O PROMETHEUS

# Docker Swarm - Services
-É UMA FORMA DE SE TER RESILIENCIA EM RELAÇÃO AOS NOS ONDE SERAM EXECULTADOS OS CONTAINER
-QUANDO SE CRIA UM UM SERVIÇO PODE SE CRIAR VARIAS REPRICAS DO CONTAINER E SE DISTRIBUIR AS REPLICAS ENTRE OS HOSTS DO CLUSTERS
-TENDO UM CLUSTER MONTADO É POSSIVEL BINDAR UMA PORTA DO CLUSTER PARA O MESMO IR REALIZANDO UM BALANCEAMENTO(ROAD ROBBING) DE CARGA ENTRE OS CONTAINER DO CLUSTER
# -> NO SERVICE CRIA -SE UMA DETERMINADA QUANTIDADE DE CONTAINER PARA SUPORTA DETERMINADO SERVIÇO (PARA A APLICAÇÃO SOMENTE SERA IMPORTANTE O NOME DO SERVIÇO)

docker service create - -name giropops - -replicas 3 - p 8080: 80 nginx(ou publisher)
# NO CLUSTER TODOS OS NODES CONHECEM CADA REPLICA DE CADA SERVIÇO EM EXECULÇÃO (LOGO EM QUALQUER DOS HOSTS DO CLUSTER ESTARÁ DISPONIVEL A PORTA/SERVIÇO BINDADO)
docker service ls
SAIDA:
phh3drrxooth   giropops   replicated   3/3(SIGNIFICA QUE DE 3 REPLICAS AS 3 ESTÃO DISPONIVEIS)        nginx: latest   *: 8080 -> 80/tcp

docker service ps giropops(VERIFICA OS CONTAINERS E ONDE ESTÃO RODANDO)

docker service inspect giropops(VERIFICA INFORMAÇÕES DO SERVIÇO)

docker service inspect giropops - -pretty(SAIDA FORMATADA DE FORMA DIFERENTE)

docker service scale giropops = 10 (ESCALA O CONTAINER PRA 10)

docker service logs - f giropops(MOSTRARA O LOGS DE TODOS OS CONTAINER DO SERVIÇO)


# Docker Swarm - Services e Volume

docker service - -help

docker service rm giropops(REMOVE O SERVIÇO)

# usando o volume (docker volume create giropops)-OS DADOS DO VOLUME NO SWARM NÃO SÃO REPLICADOS POR PADRÃO
docker service create - -name giropops - -replicas 3 - p 8080: 80 - -mount type = volume, src = giropops, dst = /usr/share/nginx/html nginx

-> > EXEMPLO DE SYNC DE ARQUIVO COM O NFS.SERVER(apt-get install nfs-server)

''' 
vim /etc/exports (ONDE COLOCA O QUE SERÁ EXPORTADO)
exportfs -ar (PUBLICA A EXPORTAÇÃO )
apt-get install nfs-common (INSTALAR NO CLIENT)
'''

-> > USO RECOMENDADO -> GLUSTERFS, CEF,

showmount - e ip_maquina_nfs_server(MONTA O DIRETORIO COMPARTILHADO)

->NECESSARIO EXISTIR O DIRETORIO EM TODAS AS MAQUINAS QUE FAZEM PARTE DO SWARM CLUSTER

# Docker Swarm - Service e Volume - Desenho
...

# Docker Swarm - Service e Network

docker service update - -help(MOSTRA TODOS OS UPDATES POSSIVEL EM RELAÇÃO AO SERVICE)
(ADICIONANDO OÇÕES NA CRIAÇÃO DE UM SERVICE):
docker service create - -name giro - -replicas 3 - p 8090: 80 - -mount type = volume, src = giropops, dst = /usr/share/nginx/html - -hostname meuhost - -limit-cpu 0.25 - -limit-memory 64M - -env minhavariavel = ehessa - -dns 8.8.8.8 nginx

docker service ps giro(MONSTRANDO NOVAMENTE ONDE ESTÃO OS CONTAINERS)

-> ENTRANDO EM QUALQUER CONTAINER -> docker container exec - ti idcontainer bash

# -> AS INFORMAÇÕES DE MEMORIA,CPU,ETC ESTARAM NO SERVICE INSPECT E NÃO MAIS NO CONTAINER INSPECT
docker inspect giro OU docker service inspect giro

CRIANDO UMA REDE:
docker network create - d overlay giropops(OVERLAY-É UMA REDE PARA O SWARM, PARA TDS OS CONTAINER DO SWARM SE ENXERGAREM)

docker service create - -name giro - -replicas 3 - p 8090: 80 - -network giropops nginx

curl nomeservice -> (CASO TENHA ALGUM ARQUIVO DE CONFIGURAÇÃO DO SERVIÇO, NÃO SERÁ NECESSARIO O USO DO IP-ISSO SE ESTIVER COMPARTILHANDO DA MESMA NETWORK)

MESMO ESCALANDO OS CONTAINER  AINDA SERÁ POSSIVEL

docker service scale giro = 10

***REDES OVERLAY DIFERENTES NÃO IRAM SE COMUNICAR
docker service update - -network-add rede2 nginx(ATUALIZAR UM SERVIÇO EM UMA REDE - O MSM SERVIÇO PODE ESTAR EM MAIS DE UMA REDE)
->>> QUANDO É ATUALIZADO COM UMA NOVA NETWORK, O CONTAINER É ENCERRADO E CRIADO UM OUTRO NO LUGAR

# Docker Swarm - Comandos
# docker swarm init

# docker swarm join --token \ SWMTKN-1-100_SEU_TOKEN SEU_IP_MASTER:2377

# docker node ls

# docker swarm join-token manager

# docker swarm join-token worker

# docker node inspect LINUXtips-02

# docker node promote LINUXtips-03

# docker node ls

# docker node demote LINUXtips-03

# docker swarm leave

# docker swarm leave --force

# docker node rm LINUXtips-03

# docker service create --name webserver --replicas 5 -p 8080:80  nginx

# curl QUALQUER_IP_NODES_CLUSTER:8080

# docker service ls

# docker service ps webserver

# docker service inspect webserver

# docker service logs -f webserver

# docker service rm webserver

# docker service create --name webserver --replicas 5 -p 8080:80 --mount type=volume,src=teste,dst=/app  nginx

# docker network create -d overlay giropops

# docker network ls

# docker network inspect giropops

# docker service scale giropops=5

# docker network rm giropops

# docker service create --name webserver --network giropops --replicas 5 -p 8080:80 --mount type=volume,src=teste,dst=/app  nginx

# docker service update <OPCOES> <Nome_Service>

# =============Final do Day 3
docker network inspect nome_network

# Introdução Day 4 - Aula ao vivo... Informações sobre curso e certificados

SECRETS -> USADO QUANDO NECESSARIO ENVIAR INFORMAÇÕES SENSIVEIS PARA O CONTAINER EX: PASSWORD, CERTIFICADOS -> É ADICIONADO COMO UM ARQUIVO
...NETWORK ATTACHABLE...
EXEMPLO CRIAÇÃO SECRET: echo - n "giropops strigus girus" | docker secret create phteste - (A SAIDA DE ECHO ESTARA NO ARQUIVO SECRET) - n pra evitar quebra de linha

docker secret ls
docker secret inspect nomesecret

PARA COLOCAR UM ARQUIVO NA SECRET:
docker secret create phteste-arquivo pass.txt
docker secret rm(APAGA A SECRET)

docker create service - -name nginx - p 7070: 80 - -secret phteste-arquivo nginx(ADICIONA O SECRET NO SERVIÇO)
\->entrando no container do service -> docker container exec - ti idcontainer bash
(O ARQUIVO DE SECRET FICARÁ EM: / RUN/SECRET)

ADICIONAR A SECRET A UM SERVICE QUE JA ESTEJA RODANDO: docker service update - -secret-add nomesecret nomeserviceparaadicionar
PODE INTEGRAR COM OUTRAS FERRAMENTAS EX: ANSIBLE

OUTRA FORMA:
docker service create - -name nginx2 - p 8181: 80 - -secret-add src = nomesecret, target = meu-secret, uid = 200, gid = 200, mode = 0400 nginx/html

# --->>>A ULTILIZAÇÃO DE SECRET NÃO É POSSIVEL FORA DE UM CLUSTER SWARM
== = SECRETS COMANDOS
echo 'minha secret' | docker secret create
docker secret create minha_secret minha_secret.txt
docker secret inspect minha_secret
docker secret ls
docker secret rm minha_secret(EXCLUI CASO NÃO ESTEJA SENDO UTILIZADA)
docker service create - -name app - -detach = false - -secret db_pass  minha_app: 1.0
docker service create - -detach = false - -name app - -secret source = db_pass, target = password, uid = 2000, gid = 3000, mode = 0400 minha_app: 1.0
ls - lhart / run/secrets/
docker service update - -secret-rm db_pass - -detach = false - -secret-add source = db_pass_1, target = password app

#  Compose, Stack e Services
->COM O DOCKER COMPOSE VOCE ESPECIFICAR PRAR O DOCKER COMO DESEJA QUE A APLICAÇÃO SUBA(INTEGRAÇÃO COM SERVICES A PARTIR DA VERSÃO 3)
->APOS SUBIR OS SERVIÇOS SERÁ POSSIVEL FAZER O GERENCIAMENO DE FORMA INDIVIDUAL(PODENDO POR EXEMPLO ESCALA A APLICAÇÃO WEB)
->ESTRUTURA DE UM docker-compose.yml:

frutas:
    banana
    morango
    manga
cervejas:
    ipa:
        - new
        - double
        - session
    apa
    pillsen
    larger

EXEMPLO 1:
version: "3.7"
services:
    web:
        image: nginx
        deploy:
            replicas: 5
            resources:
                limits:
                    cpus: "0.1"
                    memory: 50M
            restart_policy:
                condition: on-failure  # OPÇÃO PARA RESTARTAR O SERVICE EM CASO DE FALHA
        ports:
        - "8080:80"
        networks:
        - webserver(POR QUE O HIPEN???)
networks:
    webserver:  # NECESSARIO CRIAR A REDE ESPECIFICADA NO SERVIÇO

        # DOCKER STACK É USADO PAA REALIZAR O DEPLOY DO DOCKER-COMPOSE

docker stach - -help

docker stack deploy - c docker-compose.yml giropops(O - C PARA ESPECIFICAR QUE É O DEPLOY DE UM COMPOSE-FILE)

Creating network giropops_webserver(NA CRIAÇÃO NOME_STACK_NOME_REDE)
Creating service giropops_web(NOME_STACK_NOME_SERVIÇO)

docker stack ls

docker stack ps giropops(MOSTRARÁ ONDE AS MAQUINAS ONDE CONTER AS REPLICAS CLIADAS)

docker stack services giropops(MOSTRA OS SERVICOS RODANDO NA STACK)

docker stack rm giropops(REMOVERÁ O SERVICE E A REDE - O STACK COMPLETO)

# DOCKER FILES -QUANDO ESTA CRIANDO A IMAGEM
# DOCKER-COMPOSES- A IMAGEM JA ESTARÁ PRONTA PARA USO

#  Compose, Stack e Services - parte 2
-> NA STACK ENTENDE-SE EM COLOCAR TODOS OS COMPONENTES DA APLICAÇÃO(SE A APLICAÇÃO TIVER 2 SERVICES TERIA QUE CRIA OS DOIS SEPARADOS)
# UMA STACK É A REUNIAO DE VARIOS SERVICES-1 OU MAIS
# UM SERVICE É A REUNIAO DE VARIOS CONTAINERS-1 OU MAIS

version: '3.7'
services:
    db:
        image: mysql: 5.7
        volumes:
            - db_data: / var/lib/mysql
        environment:
            MYSQL_ROOT_PASSWORD: somewordpress
            MYSQL_DATABASE: wordpress
            MYSQL_USER: wordpress
            MYSQL_PASSWORD: wordpress

    wordpress:
        depends_on:  # DEPENDENCIA DE SERVICOS PARA FUNCIONAR
        - db
        image: wordpress: latest
        ports:
        - "8000:80"
        environment:
            # PASSANDO UM SERVICO LOGO TEM-SE UM DNS -SEM NECESSIDADO DO IP
            WORDPRESS_DB_HOST: db: 3306
            WORDPRESS_DB_USER: wordpress
            WORDPRESS_DB_PASSWORD: wordpress

volumes:
    db_data:

-> docker stack deploy - c docker-compose.yml wp(em teste servico não subir via web)
SERÁ CRIADO:
Creating network wp_default
Creating service wp_db
Creating service wp_wordpress

-> docker service ls
-> docker stack ls
-> docker stack ps wp(MONSTRANDO ONDE ESTAM RODANDO OS CONTAINER--todos services de um stack)
-> docker service logs - f wp_wordpress

OBS: FUNCIONOU DEPOIS QUE ESCALEI O SERVICO PRA 3 E FIZ UMA MAQUNA NO HOST

docker service ps wp_wordpress != docker stack ps wp(MOSTRA TDS OS SERVIÇOS DA STACK ONDE ESTÃO RODANDO)

# Compose, Stack e Services - parte 3

version: "3.7"
services:
    web:
        image: nginx
        deploy:
            placement:  # ATRAVES DE UMA CONSTRAINTS ELE ESCOLHERÁ ONDE O NGINX SERÁ POSTO-> SO SUBIRÁ ONDE TEM UM NODE.LABEL.DC
                constraints:
                - node.labels.dc == UK
            replicas: 5
            resources:
                limits:
                    cpus: "0.1"
                    memory: 50M
            restart_policy:
                condition: on-failure
        ports:
        - "8080:80"
        networks:
        - webserver

    visualizer:
        image: dockersamples/visualizer: stable
        ports:
        - "8888:8080"
        volumes:
            # REFERENCIA AO SOCKET DO DOCKER-POI SERÁ NECESSARIO VIZUALIZAR ONDE ESTÃO TODOS SEUS CONTAINER -DE FORMA VISUAL
        - "/var/run/docker.sock:/var/run/docker.sock"
        deploy:
            placement:
                # O NODE DO SWARM PRECISA SER UM MANAGER, SE NÃO NÃO RODARÁ-POIS PRECISARÁ SABER A SITUAÇÃO TOTAL DO CLUSTER
                constraints: [node.role == manager]
        networks:
        - webserver

networks:
    webserver:

docker stack deploy - c docker-compose.yml giros
# PARA SUBIR TERÁ QUE ATUALIZAR O'S NÓS
-- -> docker node update - -label-add dc = UK nome_do_nó

->docker stack ps giros(VERIFICANDO)
# DUVIDA QUANDO ESPEFICICAR E QUANDO NÃO ESPECIFICAR OS LIMITES DOS SERVIÇOS/CONTAINERS


# Compose, Stack e Services - parte 4

version: "3.7"
services:
    redis:
        imagem: redis: alpine
        ports:
        - "6379"  # (SEM BINDAR A PORTA, SOMENTE COM ACESSO INTERNO DO NODE )
        networks:
        - frontend
        deploy:
            replicas: 2
            update_config:
                # (NO CASO DE UPDATE DO SERVIÇO SERÁ FEITO DE 1 EM 1 NAS REPLICAS, COM UM DELAY ENTRE ELAS DE 10SEG)
                parallelism: 1
                delay: 10s
                order: start-first
            rollback_config:    # SE DER ALGUM PROBLEMA NO SERVIÇO/APLICAÇÃO FARÁ O ROLLBACK DE 1 EM 1 REPLICA E DELAY DE 10SEG ->> OPÇÃO A PARTIR DA VERSÃO 3.7
                parallelism: 1
                delay: 10s
                # (CASO O ROLLBACK DÊ PROBLEMA CONTINUA OU PAUSE)
                failure_action: continue
                monitor: 60s  # MONITORA O ROLLBACK
                order: stop-first  # ESTABELECE ORDEM DE STOP E START DOS CONTAINER
            restart_policy:
                condition: on-failure
    db:
        image: postgres: 9.4
        volumes:
        - db-data: / var/lib/postgresql/data
        networks:
        - backend
        deploy:
            placement:
                constraints: [node.role == manager]
    vote:
        image: dockersamples/examplevotingapp_vote: before
        ports:
            - 5000: 80  # (SEM ASPAS TAMBEM FUNCIONA)
        networks:
        - frontend
        depends_on:
        - redis
        deploy:
            replicas: 2
            update_config:
                parallelism: 2
            restart_policy:
                condition: on-failure
    result:
        image: dockersamples/examplevotingapp_result: before
        ports:
        - "5001:80"
        networks:
        - backend
        depends_on:
        - db
        deploy:
            replicas: 1
            update_config:
                parallelism: 1
                delay: 10s
            restart_policy:
                condition: on-failure
    worker:
        image: dockersamples/examplevotingapp_worker
        networks:
            - frontend
            - backend
        deploy:
            # (QUANDO SE ESCOLHE A QUANTIDADE DE REPLICAS DE DETERMINADOS SERVIÇOS- SE FOR GLOBAL ELE CRIARÁ UMA REPLICA POR NÓ-NÕ SERÁ ESCALAVEL -1 REPLICA POR NÓ)
            mode: replicated
            replicas: 1
            labels: [APP = VOTING]
            restart_policy:
                condition: on-failure
                # (EM CASO DE FALHA DELAY DE 10SEG ENTRE UM RESTART E OUTRO, NESTE CASO NO MAXIMO DE 3 TENTATIVAS EM UMA JANELA DE 120 SEG)
                delay: 10s
                max_attempts: 3
                window: 120s
            placement:
                constraints: [node.role == manager]
    visualizer:
        image: dockersamples/visualizer: stable
        ports:
            - "8080:8080"
        # (ESPERA 90SEG PARA O SERVIÇO PARA/MORRER, CASO NÃO IRA PARAR MANUALMENTE KILL -9)
        stop_grace_period: 1m30s
        volumes:
            - "/var/run/docker.sock:/var/run/docker.sock"
        deploy:
            placement:
                constraints: [node.role == manager]
networks:
    frontend:
    backend:
volumes:
    db-data:

OBS: APRESENTANDO ERRO: services.redis Additional property imagem is not allowed

docker stack deploy - c docker-compose.yml giros

# Compose, Stack e Services - parte 5

version: "3.7"
services:
    prometheus:
        image: linuxtips/prometheus_alpine
        volumes:
            # VOLUME NO NIVEL DA PASTA DO DOCKER-COMPOSE  TIPO BIND
            - ./conf/prometheus/: / etc/prometheus/
            - prometheus_data: / var/lib/prometheus  # TIPO VOLUME
        networks:
            - backend
        ports:
            - 9090: 9090
    node-exporter:  # COMO UMA AGENTE DO PROMETHEUS-PEGANDO AS METRICAS
        image: linuxtips/node-exporter_alpine
        hostname: '{{.Node.ID}}'
        volumes:
            - / proc: / usr/proc
            - / sys: / usr/sys
            - / : / rootfs  # POR SER MONITORAÇÃO DE HOST BASEADO EM CONTAINER
        deploy:
            mode: global
        networks:
            - backend
        ports:
            - 9100: 9100
    alertmanager:  # PARA NOTIFICAÇÕES EM E-MAILS/CHAT ,ETC
        image: linuxtips/alertmanager_alpine
        volumes:
            - ./conf/alertmanager/: / etc/alertmanager/
        networks:
            - backend
        ports:
            - 9093: 9093
    cadvisor:  # (PARA METRICAS DOS CONTAINERS)
        image: google/cadvisor
        # PARA SABER QUAL O NODE QUE ESTA SENDO MONITORADO/ESTATISTICAS
        hostname: '{{.Node.ID}}'
        volumes:
            - / : / rootfs: ro
            - / var/run: / var/run: rw
            - / sys: / sys: ro
            - / var/lib/docker/: / var/lib/docker: ro
            - / var/run/docker.sock: / var/run/docker.sock: ro
        networks:
            - backend
        deploy:
            mode: global
        ports:
            - 8080: 8080
    grafana:  # CAPTURA METRICAS NO PROMETHEUS E USA NO GRAFANA
        image: nopp/grafana_alpine
        depends_on:
            - prometheus
        volumes:
            - ./conf/grafana/grafana.db: / grafana/data/grafana.db
        env_file:
            - grafana.config
        networks:
            - backend
            - frontend
        ports:
            - 3000: 3000
networks:
    frontend:
    backend:
volumes:
    prometheus_data:
    grafana_data:

        # Compose - Continuação aula ao vivo

->>>git do projeto: https: // github.com/badtuxx/giropops-monitoring
# SUGESTÃO PROXY-REVERSO -> TRAEFIC-NGINX / METAL LB

# ROCKETCHAT-SEMELHANTE AO SLACK COMUNICADOR


# NÃO CRIAR REDE DE CONTAINER NA MESMA REDE QUE O HOST
# PARA O FUNCIONAMENTO EM REDES OVERLAY LIBERA PORTAS NO FIREWALL
firewall-cmd - -zone = public - -permanent - -add-port = 7946/tcp
firewall-cmd - -zone = public - -permanent - -add-port = 7946/udp
firewall-cmd - -zone = public - -permanent - -add-port = 2377/tcp
firewall-cmd - -zone = public - -permanent - -add-port = 4789/tcp


CRIADO UM WEBHOOK(GMAIL) -> https: // hooks.slack.com/services/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

# ALTERADO LOCAL VOLUME TIPO BIND 30MIN-PARA FUNCIONAR INDEPENDENTE DE EM QUAL NO IRA SUBIR

# BUSCA DE DASHBOARD NO GRAFANA.COM PELO ID

docker contaner stats  # (ACOMPANHAR O USO DE RECURSOS EM TEMPO REAL)

->opcoes -> datadog, dinatrace

#  Compose - Comandos (movido para o arquivo compose_comands)

# AVALIAÇÃO
Qual a diferença entre o 'docker service scale' e o 'docker service update'?:
Qual a diferença entre um modo replicado e o modo global no docker swarm?
Qual comando utilizado para adicionar um volume em determinado service existente? -> --mount type = volume, src = giropops, dst = /usr/share/nginx/html nginx -  # O CORRETO ERA --MOUNT -ADD

# DOCKER SERVICE UPDATE --REPLICAS E DOCKER SERVICE SCALE
Qual comando é utilizado para aumentar o número de réplicas de um determinado service? Cite duas formas. ->

Qual distribuição ideal quando você possui 07 nodes manager em um cluster swarm, utilizando 03 regiões ou datacenter diferentes? 3-2-2 (ok) e 2-2-3 ?

Qual o arquivo onde eu posso especificar que gostaria de utilizar a versão experimental do Docker? / etc/docker/daemon.json

Qual o comando para verificar os services em meu cluster swarm? docker service ls

Qual namespace não vem habilitado por default? users, mas pensei ser o de rede

Qual comando me permite abrir um porta no host e redirecionar todo o tráfego para determinada porta do container quando estou criando um service? docker service create - -publish 8080: 80
Qual o parâmetro utilizado para limitar a quantidade de CPU para determinado container? - -cpus
Qual o parâmetro utilizado para limitar a quantidade de CPU para todos os containers de determinado service? - -limite-cpu

Qual comando eu consigo visualizar qual o driver para logs que determinado container esta sendo utilizado? docker container inspect

Qual o formato default de logs do container ?  json file

Qual comando me permite estabelecer que o meu driver de logs será o 'syslog', no momento da criação de um container?

Qual arquivo eu posso estabelecer qual será o meu storage driver padrão? / etc/docker/daemon.json
{
    "storage-driver": "overlay2"
}

# DUVIDA TEM COMO RODAR O DOCKER STACK SEM INICIAR O SWARM -SO RODANDO O DOCKER COMPOSE FILE ??

Qual o diretório estão os volumes do Docker? / var/lib/docker/volumes/
Qual o comando utilizado para realizar o deploy de um service do apache com quatro replicas? create - -replicas N

== == == == == == == == == == ==ssh == == == == ==

== == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
# CERTIFICADO DCA -CERTIFICAÇÃO DOCKER

...
# TRAEFIC-COMO OPÇÃO FORA DO NGINX
https: // doc.traefik.io/traefik/
-> A IDEIA É SER UM PROXY REVERSO, AINDA COM POSIBILIDADE DE DASHBOARD

docker network create - -driver = overlay traefik-public


version: "3.7"
services:
    reverse-proxy:
        image:  traefik: v2.0.2
        command:
            # COMANDOS NA EXECULÇÃO DO SERVICE ->1º ONDE O DOCKER ESTA EM EXECULÇÃO -> ELE SERÁ MONTADO DENTRO DO CONTAINER
            - "--providers.docke.endpoint=unix:///var/run/docker.sock"
            - "--providers.docker.swarmMode=true"  # MODO SWARM OU NÃO
            - "--providers.docker.exposedbydefault=false"
            - "--providers.docker.network-traefik-public"
            - "--entrypoints.web.address=:80"  # PARA FAZER O REDIRECIONAMENTO DOS SERVICOS
        ports:
            - 80: 80
        volumes
        - / var/run/docker.sock: / var/run/docker.sock: ro
        networks:
            -traefik-public
        deploy:
            placement:
                constraints:
                    - node.role == manager

networks:
    traefik-public:
        external: true  # POIS A REDE JA HAVIA SIDO CRIADA

# execultando
docker stack deploy - c docker-compose.yml traefik
ou
docker stack deploy traefik - c traefik_deploy.yaml

== == == == =
version: "3.7"
services:
    loja:
        image:  linuxtips/nginx-prometheus-exporter: 1.0.0
        labels:  # passando informação para ser coletada pelo traefik
            - "traefik.enable=true"  # para expor o serviço
            # necessario ter um router redireciona url
            - "traefik.http.routers.loja.rule=Host('loja.biqueiranerd.com.br')"
            # entrypoint usado referencia a command de traefik.yaml
            - "traefik.http.routers.loja.entrypoints=web"
            - "traefik.http.service.loja.loadbalancer.server.port=80"
        networks:
            -traefik-public

networks:
    traefik-public:
        external: true


== == == == =APP2
version: "3.7"
services:
    loja:
        image:  linuxtips/nginx-prometheus-exporter: 1.0.0
        labels:  # passando informação para ser coletada pelo traefik
            - "traefik.enable=true"  # para expor o serviço
            # necessario ter um router redireciona url
            - "traefik.http.routers.loja.rule=Host('loja.biqueiranerd.com.br')"
            # entrypoint usado referencia a command de traefik.yaml
            - "traefik.http.routers.loja.entrypoints=web"
            - "traefik.http.service.loja.loadbalancer.server.port=80"
        networks:
            -traefik-public

networks:
    traefik-public:
        external: true

== == == == == == == == == == == == == =
Traefik - Arquivos
HTML
# cat app_example.yaml
version: '3'
services:
    loja:
        image: linuxtips/nginx-prometheus-exporter: 1.0.0
        networks:
            - traefik-public
        deploy:
            labels:
                - "traefik.enable=true"
                - "traefik.http.routers.loja.rule=Host(`loja.biqueiranerd.com.br`)"
                - "traefik.http.routers.loja.entrypoints=websecure"
                - "traefik.http.routers.loja.tls.certresolver=letsencryptresolver"
                - "traefik.http.services.loja.loadbalancer.server.port=80"
networks:
    traefik-public:
        external: true
HTML
# cat traefik_deploy_https.yaml
version: '3'

services:
    reverse-proxy:
        image: traefik: v2.0.2
        labels:
        - "traefik.enable=true"
        - "traefik.http.routers.http-catchall.rule=hostregexp(`{host:.+}`)"
        - "traefik.http.routers.http-catchall.entrypoints=web"
        - "traefik.http.routers.http-catchall.middlewares=redirect-to-https@docker"
        - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
        command:
            - "--providers.docker.endpoint=unix:///var/run/docker.sock"
            - "--providers.docker.swarmMode=true"
            - "--providers.docker.exposedbydefault=false"
            - "--providers.docker.network=traefik-public"
            - "--entrypoints.web.address=:80"
            - "--entrypoints.websecure.address=:443"
            - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge=true"
            - "--certificatesresolvers.letsencryptresolver.acme.httpchallenge.entrypoint=web"
            - "--certificatesresolvers.letsencryptresolver.acme.email=jeferson@linuxtips.com.br"
            - "--certificatesresolvers.letsencryptresolver.acme.storage=/letsencrypt/acme.json"
            - "--api.insecure"
            - "--api.dashboard=true"
        ports:
            - 80: 80
            - 443: 443
            - 8080: 8080
        volumes:
            # So that Traefik can listen to the Docker events
            - / var/run/docker.sock: / var/run/docker.sock: ro
            - traefik-certificates: / letsencrypt
        networks:
            - traefik-public
        deploy:
            placement:
                constraints:
                    - node.role == manager

volumes:
    traefik-certificates:

networks:
    traefik-public:
        external: true
