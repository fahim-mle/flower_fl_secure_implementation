import os

from oauthenticator.generic import GenericOAuthenticator

# Basic JupyterHub Configuration
c.JupyterHub.cookie_secret = os.environ["JUPYTERHUB_COOKIE_SECRET"]
c.JupyterHub.bind_url = "http://localhost:8000/"

# THIS IS THE LINE TO FIX THE CONNECTION
c.ConfigurableHTTPProxy.ip = "0.0.0.0"

# OAuthenticator Configuration
c.JupyterHub.authenticator_class = GenericOAuthenticator
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
c.GenericOAuthenticator.client_id = "jupyterhub-client"
c.GenericOAuthenticator.client_secret = ""
c.GenericOAuthenticator.username_claim = "preferred_username"

# DockerSpawner Configuration
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = "jupyter/datascience-notebook:latest"
c.DockerSpawner.remove = True
c.DockerSpawner.network_name = "flower_fl_secure_implementation_fl-internal-network"

# Admin Users
c.Authenticator.admin_users = {"admin"}
