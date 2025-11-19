# === IMPORT THE AUTHENTICATOR CLASS ===
# This is the modern, correct way to configure the authenticator.

from oauthenticator.generic import GenericOAuthenticator

# jupyterhub-config/jupyterhub_config.py
print("Loading JupyterHub configuration...")
# jupyterhub-config/jupyterhub_config.py


# === Basic JupyterHub Configuration ===
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/cookie_secret"
c.JupyterHub.bind_url = "http://localhost:8000/"

# === OAuthenticator Configuration for Keycloak ===
# Assign the imported class directly, not as a string.
c.JupyterHub.authenticator_class = GenericOAuthenticator

# --- Keycloak OAuth URLs ---
c.GenericOAuthenticator.authorize_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/auth"
)
c.GenericOAuthenticator.token_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/token"
)
c.GenericOAuthenticator.userdata_url = (
    "http://keycloak:8080/realms/fl-realm/protocol/openid-connect/userinfo"
)
c.GenericOAuthenticator.oauth_callback_url = "http://localhost:8000/hub/oauth_callback"

# --- Keycloak Client Configuration ---
c.GenericOAuthenticator.client_id = "jupyterhub-client"
c.GenericOAuthenticator.client_secret = ""

# --- User Data Mapping ---
c.GenericOAuthenticator.username_key = "preferred_username"

# === DockerSpawner Configuration ===
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = "jupyter/datascience-notebook:latest"
c.DockerSpawner.remove = True
c.DockerSpawner.network_name = "flower_fl_secure_implementation_fl-internal-network"

# === Admin Users ===
c.Authenticator.admin_users = {"admin"}
print("JupyterHub configuration loaded successfully.")
