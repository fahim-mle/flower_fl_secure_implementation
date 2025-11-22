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

# Optional override via env
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

# PUBLIC_HOSTNAME is the host users will use in browser (e.g. localhost or your domain)
PUBLIC_HOSTNAME = os.environ.get("PUBLIC_HOSTNAME", "localhost")
PUBLIC_PORT = os.environ.get("PUBLIC_PORT", "8100")
PUBLIC_BASE = f"http://{PUBLIC_HOSTNAME}:{PUBLIC_PORT}"

# External (browser-facing) Keycloak port.
# IMPORTANT: this should match the HOST port in docker-compose, typically 8180:8080
KEYCLOAK_EXTERNAL_PORT = os.environ.get("KEYCLOAK_PORT", "8180")

# Browser-facing authorize URL (user's browser goes here)
c.GenericOAuthenticator.authorize_url = (
    f"http://{PUBLIC_HOSTNAME}:{KEYCLOAK_EXTERNAL_PORT}"
    "/realms/fl-realm/protocol/openid-connect/auth"
)

# Callback that Keycloak redirects to (goes to hub via proxy on PUBLIC_HOSTNAME:PUBLIC_PORT)
c.GenericOAuthenticator.oauth_callback_url = f"{PUBLIC_BASE}/hub/oauth_callback"

# Server-to-server: hub -> keycloak inside docker network
# This uses the internal container name and internal port (usually 8080).
c.GenericOAuthenticator.token_url = (
    "http://keycloak:8180/realms/fl-realm/protocol/openid-connect/token"
)
c.GenericOAuthenticator.userdata_url = (
    "http://keycloak:8180/realms/fl-realm/protocol/openid-connect/userinfo"
)

c.GenericOAuthenticator.userdata_token_method = "access"
c.GenericOAuthenticator.username_claim = "preferred_username"

# Client credentials (pick up from env/.env)
c.GenericOAuthenticator.client_id = os.environ.get(
    "OAUTH_CLIENT_ID", "jupyterhub-client"
)

client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
if not client_secret:
    raise RuntimeError(
        "OAUTH_CLIENT_SECRET is not set. "
        "Set it in your .env to match the Keycloak client secret."
    )
c.GenericOAuthenticator.client_secret = client_secret

# Scopes
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]

# Allow all authenticated users (DEV)
c.GenericOAuthenticator.allowed_users = ["test_user", "admin"]

# Optionally restrict by groups later if desired
c.GenericOAuthenticator.allowed_groups = []

# ------------------------------
# DockerSpawner settings
# ------------------------------
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = os.environ.get(
    "DOCKER_JUPYTER_IMAGE", "jupyter/datascience-notebook:latest"
)

# Network inside docker (single-user containers will attach here)
c.DockerSpawner.network_name = os.environ.get(
    "DOCKER_NETWORK_NAME", "fl-internal-network"
)

# Also ensure created containers use the desired network_mode
c.DockerSpawner.extra_host_config = {"network_mode": c.DockerSpawner.network_name}

# Mount a persistent named volume per user (DockerSpawner creates volumes automatically)
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

# Increase timeouts for slower images
c.Spawner.start_timeout = 180
c.Spawner.http_timeout = 120

# Clean up containers on stop
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# ------------------------------
# Admins / access
# ------------------------------
# Read from env, default to "admin". You can set JUPYTERHUB_ADMINS in .env, e.g. "admin,test_user"
admin_env = os.environ.get("JUPYTERHUB_ADMINS", "admin")
admin_users = {u.strip() for u in admin_env.split(",") if u.strip()}
c.Authenticator.admin_users = admin_users
