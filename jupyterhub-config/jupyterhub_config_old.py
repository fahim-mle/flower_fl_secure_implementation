import logging
import os

from dockerspawner import DockerSpawner
from oauthenticator.generic import GenericOAuthenticator

# ------------------------------
# Logging
# ------------------------------
c.JupyterHub.log_level = "DEBUG"
logging.basicConfig(level=logging.DEBUG)

# ------------------------------
# Basic JupyterHub Settings
# ------------------------------
c.JupyterHub.cookie_secret = os.environ.get("JUPYTERHUB_COOKIE_SECRET")
c.JupyterHub.bind_url = (
    "http://0.0.0.0:8000"  # listen on all interfaces inside container
)
c.JupyterHub.hub_ip = "0.0.0.0"

# Fix cookies for local dev (avoid SameSite issues)
c.JupyterHub.cookie_options = {
    "SameSite": None,  # allows OAuth to work cross-site locally
    "Secure": False,  # HTTP only for local dev
}

# ------------------------------
# Authenticator (Keycloak)
# ------------------------------
c.JupyterHub.authenticator_class = GenericOAuthenticator

# OAuth URLs (browser-facing must use localhost)
c.GenericOAuthenticator.authorize_url = (
    "http://localhost:8080/realms/fl-realm/protocol/openid-connect/auth"
)
c.GenericOAuthenticator.oauth_callback_url = "http://localhost:8000/hub/oauth_callback"

# OAuth server-to-server URLs (use container hostnames)
c.GenericOAuthenticator.token_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/token"
)
c.GenericOAuthenticator.userdata_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/userinfo"
)

# OAuth client config
c.GenericOAuthenticator.client_id = "jupyterhub-client"
c.GenericOAuthenticator.client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
c.GenericOAuthenticator.username_claim = "preferred_username"  # standard Keycloak field
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]
c.GenericOAuthenticator.enable_pkce = False

# ------------------------------
# DockerSpawner
# ------------------------------
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = "jupyter/datascience-notebook:latest"
c.DockerSpawner.remove = True

# Internal Docker network
c.DockerSpawner.network_name = "fl-internal-network"

# Mount each user's home
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/jovyan"}

# Port configuration
c.DockerSpawner.notebook_ip = "0.0.0.0"
c.DockerSpawner.port = 8888

# Run as jovyan (UID 1000) to avoid permissions issues
c.DockerSpawner.extra_create_kwargs = {"user": "1000:100"}

# Give container enough time to start
c.Spawner.start_timeout = 180

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
