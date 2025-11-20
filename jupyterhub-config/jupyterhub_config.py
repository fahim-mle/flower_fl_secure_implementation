import logging
import os

from dockerspawner import DockerSpawner
from oauthenticator.generic import GenericOAuthenticator

c = get_config()  # noqa

# ------------------------------
# Logging
# ------------------------------
c.JupyterHub.log_level = "DEBUG"
logging.basicConfig(level=logging.DEBUG)

# ------------------------------
# Basic JupyterHub settings
# ------------------------------
# Proxy listens on 8000 inside the container; hub listens on HUB_INTERNAL_PORT.
c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = int(os.environ.get("HUB_INTERNAL_PORT", 8081))

# Use a file for cookie secret (persisted in fl-jupyterhub-data)
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"
# fallback env secret if you prefer
if os.environ.get("JUPYTERHUB_COOKIE_SECRET"):
    c.JupyterHub.cookie_secret = os.environ["JUPYTERHUB_COOKIE_SECRET"]

# Cookie options for local dev (adjust for prod - SameSite=None + Secure=True behind HTTPS)
c.JupyterHub.cookie_options = {
    "SameSite": None,
    "Secure": False,
}

# ------------------------------
# Authenticator (Keycloak)
# ------------------------------
c.JupyterHub.authenticator_class = GenericOAuthenticator

# PUBLIC_HOSTNAME is the host users will use in browser (nginx will sit on fl-public-network)
PUBLIC_HOSTNAME = os.environ.get("PUBLIC_HOSTNAME", "localhost")
PUBLIC_PORT = os.environ.get("PUBLIC_PORT", "8100")
PUBLIC_BASE = f"http://{PUBLIC_HOSTNAME}:{PUBLIC_PORT}"

# Browser-facing authorize URL (user goes to this)
c.GenericOAuthenticator.authorize_url = f"http://{os.environ.get('PUBLIC_HOSTNAME','localhost')}:{os.environ.get('KEYCLOAK_PORT','8180')}/realms/fl-realm/protocol/openid-connect/auth"
# Callback that Keycloak redirects to (goes to proxy on PUBLIC_HOSTNAME:PUBLIC_PORT)
c.GenericOAuthenticator.oauth_callback_url = f"{PUBLIC_BASE}/hub/oauth_callback"

# Server-to-server: hub -> keycloak inside docker network
c.GenericOAuthenticator.token_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/token"
)
c.GenericOAuthenticator.userdata_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/userinfo"
)

# Client credentials (pick up from env/.env)
c.GenericOAuthenticator.client_id = os.environ.get(
    "OAUTH_CLIENT_ID", "jupyterhub-client"
)
c.GenericOAuthenticator.client_secret = os.environ.get("OAUTH_CLIENT_SECRET", "")

# Scopes
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]

# By default allow all authenticated users (DEV). Toggle to restrict.
c.GenericOAuthenticator.allow_all = True

# ------------------------------
# DockerSpawner settings
# ------------------------------
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = os.environ.get(
    "DOCKER_JUPYTER_IMAGE", "jupyter/datascience-notebook:latest"
)

# network inside docker (single-user containers will attach here)
c.DockerSpawner.network_name = os.environ.get(
    "DOCKER_NETWORK_NAME", "fl-internal-network"
)
# also ensure created containers use the network_mode
c.DockerSpawner.extra_host_config = {"network_mode": c.DockerSpawner.network_name}

# mount a persistent named volume per user (DockerSpawner creates volumes automatically)
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/jovyan"}

# Notebook server should listen on all interfaces
c.DockerSpawner.cmd = [
    "start-notebook.sh",
    "--NotebookApp.ip=0.0.0.0",
    "--NotebookApp.port=8888",
    # do not set token when managed by JupyterHub
]

c.DockerSpawner.notebook_ip = "0.0.0.0"
c.DockerSpawner.port = 8888

# Run as jovyan by default to avoid permission issues
c.DockerSpawner.extra_create_kwargs = {"user": "1000:100"}

# increase timeouts for slower images
c.Spawner.start_timeout = 180
c.Spawner.http_timeout = 120

# prevent built-in healthcheck from killing container too early (optional)
# you can keep or remove this; I've left it commented so you can choose:
# c.DockerSpawner.extra_host_config.update({"healthcheck": {"test": "NONE"}})

# Clean up containers on stop
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# ------------------------------
# Admins / access
# ------------------------------
c.Authenticator.admin_users = set(
    os.environ.get("JUPYTERHUB_ADMINS", "admin").split(",")
)

# ------------------------------
# Admin Users
# ------------------------------
c.Authenticator.admin_users = {"admin", "test_user"}

# Allow **all** authenticated users
c.GenericOAuthenticator.allow_all = True

# ------------------------------
# Optional: allow anyone to log in (if you want to restrict to groups later)
# ------------------------------
c.GenericOAuthenticator.allowed_groups = []
