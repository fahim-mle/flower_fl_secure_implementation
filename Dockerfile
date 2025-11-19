# Dockerfile

# Use a specific version of the JupyterHub image for stability
FROM jupyterhub/jupyterhub:5.4.2

# Install the latest stable, compatible versions of the packages
RUN pip install "oauthenticator==16.2.0" "dockerspawner==14.0.0"

# Copy the configuration file from your host machine into the image
COPY ./jupyterhub-config/jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
