# Dockerfile

# Use a specific version of the JupyterHub image for stability
FROM jupyterhub/jupyterhub:5.4.2

# Install the latest stable, compatible versions of the packages
RUN pip install "oauthenticator==16.2.0" "dockerspawner==14.0.0"

# Generate the cookie secret file directly inside the image
RUN openssl rand -hex 32 > /srv/jupyterhub/cookie_secret

# Set the correct ownership and permissions for the secret file
# The official image runs as the 'jovyan' user, so we give it ownership.
RUN chown jovyan:users /srv/jupyterhub/cookie_secret && \
    chmod 600 /srv/jupyterhub/cookie_secret

# Copy the configuration file from your host machine into the image
COPY ./jupyterhub-config/jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
