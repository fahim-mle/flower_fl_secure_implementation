FROM jupyterhub/jupyterhub:5.4.2

RUN pip install --no-cache-dir "oauthenticator==16.2.0" "dockerspawner==14.0.0"

COPY ./jupyterhub-config/jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

WORKDIR /srv/jupyterhub

ENV JUPYTERHUB_LOG_LEVEL=DEBUG

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
