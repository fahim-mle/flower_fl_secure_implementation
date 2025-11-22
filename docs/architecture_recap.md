# ✅ **SECTION 1 — Target Architecture Recap (Codex Specification)**

**Filename:** `01_architecture_overview.md`

```markdown
# 01 — Architecture Overview for Local Secure Federated Learning Deployment

This document defines the architecture Codex must adhere to when generating the implementation for the secure local FL environment. All following sections will depend on this structure.

---

# 1. System Components (Containers)

Codex will deploy the following containers:

1. **reverse-proxy**
   - Runs Nginx
   - Terminates HTTPS (TLS)
   - Performs OIDC redirects for user authentication
   - Forwards authenticated traffic to SuperLink

2. **auth-provider** (ONLY ONE selected by user)
   - Option A: Keycloak in Docker
   - Option B: GitHub OAuth via `oauth2-proxy`
   - Option C: Dex + GitHub connector
   - Must support OIDC (OpenID Connect)

3. **superlink**
   - Flower Aggregator node
   - Receives user-authenticated requests from reverse-proxy
   - Manages FL rounds
   - Validates mTLS certificates from SuperNodes
   - Maintains a public-key allowlist of valid SuperNodes

4. **supernode-N**
   - Multiple independent Flower client nodes
   - Each with separate dataset volume
   - Each has its own certificate + key
   - Communicates ONLY with SuperLink

---

# 2. Networks

Codex must create the following Docker networks:

| Network Name | Purpose |
|--------------|---------|
| `fl_internal_net` | Private network for SuperLink + SuperNodes |
| `fl_reverse_proxy_net` | Public-facing network for Nginx |
| `fl_auth_net` | Nginx ↔ Auth Provider (if external provider requires it) |

Rules:
- SuperNodes must NOT be reachable from the public network.
- Only reverse-proxy exposes any ports to the host machine.
- SuperLink & SuperNodes remain isolated.

---

# 3. Volumes

Codex must create the following Docker volumes:

## Global Volumes
```

fl_ca_certs
superlink_certs

```

## Per-SuperNode Volumes
```

supernode1_data
supernode1_certs

supernode2_data
supernode2_certs

supernode3_data
supernode3_certs
...

```

Rules:
- `*_data` volumes store SuperNode datasets (never exposed).
- `*_certs` volumes store SuperNode certificates inside containers.
- Certificates originate from the `certificates/` directory on the host.

---

# 4. Certificate Model

Codex must assume:

- Certificates are generated in `project-root/certificates/`
- Docker Compose mounts them **into containers** so that inside:
  - SuperLink certs live under `/etc/flwr/certs/*`
  - SuperNode certs live under `/etc/flwr/certs/*`
  - CA cert is shared and accessible by all nodes

Codex must NOT generate certificate data itself — only scripts/commands to create them.

---

# 5. Security Design Requirements

Codex must enforce the following security rules:

## User Authentication (Frontend)
- Handled at Nginx layer
- Only authenticated requests go to SuperLink
- OIDC is mandatory (provider selectable by user)

## Node Authentication
- All SuperNodes must use mTLS
- Each SuperNode must have:
  - `node.key` (private key)
  - `node.crt` (certificate signed by CA)
  - `ca.crt` (trust anchor)

## Node Authorization
- SuperLink keeps an allowlist file:
```

allowed_supernodes.json

```
- Codex must generate logic (or config patterns) to:
- Extract public key fingerprints
- Register them with SuperLink

## Network-Level Security
- No FL-related ports are exposed publicly
- Only reverse-proxy publishes ports (443/80)
- SuperLink and SuperNodes communicate ONLY on `fl_internal_net`

---

# 6. Expected Routing Path

```

Browser → Nginx → Auth Provider → Nginx → SuperLink → SuperNodes

```

Transport guarantees:
- TLS for browser ↔ Nginx
- mTLS for SuperLink ↔ SuperNodes
- No direct external traffic to SuperNodes

---

# 7. Container Interaction Diagram

```

```
                USER (Browser)
                      │  HTTPS
                      ▼
            ┌────────────────────┐
            │      NGINX         │
            │ TLS + OIDC Gateway │
            └─────────┬──────────┘
                      │ Authenticated HTTP
                      ▼
            ┌────────────────────┐
            │    SUPERLINK       │
            │ Flower Aggregator  │
            └─────────┬──────────┘
                mTLS   │
                      ▼
  ┌────────────────────────────────────────────┐
  │             SUPER NODES (N)                │
  │--------------------------------------------│
  │ supernode-1   supernode-2   ...   supernode-N │
  │ each with its own dataset + certs          │
  └────────────────────────────────────────────┘
```

```

---

# 8. Summary for Codex

Codex must strictly follow this architecture when generating code:
- Docker Compose with 4 component types
- Private + public networks
- mTLS everywhere between FL nodes
- Host-level cert generation scripts
- Nginx as auth gateway

Future sections will define:
1. Docker base layout
2. Certificate generation scripts
3. SuperLink implementation
4. SuperNode client containers
5. Authentication provider integration
6. Nginx reverse proxy
7. Verification & testing steps

Codex should not implement anything outside the scope of this architecture.

```
