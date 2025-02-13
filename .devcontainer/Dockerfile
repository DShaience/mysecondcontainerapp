FROM mambaorg/micromamba:0.15.3
USER root

RUN apt update -y
RUN apt upgrade -y
RUN apt-get install -y curl
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | /bin/bash

RUN  mkdir /app
RUN chmod -R 777 /app

WORKDIR /app
USER micromamba
COPY ./src/app_conda_env.yml /opt/demo_azure/app_conda_env.yml

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

COPY ./src/app_conda_env.yml .

RUN micromamba install -y -n base -f app_conda_env.yml && micromamba clean --all --yes
RUN pip install streamlit-aggrid~=1.0.5  

COPY ./src ./src

WORKDIR /app/src
USER root

RUN chmod a+x run.py
RUN chmod a+x run_app.sh

CMD ["streamlit", "run", "webapp/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableWebsocketCompression=false"]

