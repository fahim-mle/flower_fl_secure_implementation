# ✅ **SECTION 2 — Base Docker/Compose Layout (INSECURE Validation First)**

**Filename:** `02_base_compose_stack.md`

```markdown
# 02 — Base Docker/Compose Stack (Insecure First for Wiring Validation)

Goal complete ✅ — The base stack now spins up:
- 1 SuperLink container (`docker/superlink`)
- 2 SuperNode containers (`docker/supernode`, scalable)
- Nginx reverse proxy (insecure, no auth)
- `docker-compose` wiring with correct networks/volumes

---

# 1. Files Added / Updated

- `docker/docker-compose.yml` — Defines `reverse-proxy`, `superlink`, `supernode-1`, `supernode-2`, networks, volumes, and scaling-friendly env vars.
- `docker/superlink/Dockerfile` & `entrypoint.sh` — Python 3.11 / Flower 1.7 image that runs `config/flwr_server_config.py`.
- `docker/superlink/config/flwr_server_config.py` — FedAvg strategy with env-driven host/port/rounds (insecure).
- `docker/supernode/Dockerfile` & `entrypoint.sh` — Flower NumPy client container with env-configurable server address.
- `docker/supernode/config/{flwr_client_config.py,dataset_loader.py}` — Synthetic dataset generation, retry loop, and simple linear regression client.
- `nginx/nginx.conf` & `nginx/docker/Dockerfile` — Plain HTTP reverse proxy forwarding `/:80 -> superlink:9091`.
- `.env` — Compose project name + defaults for future overrides (optional).

---

# 2. Compose Requirements (Authoritative)

## 2.1 Services Implemented

- **reverse-proxy**
  - Build context `../nginx` w/ `docker/Dockerfile`.
  - Publishes `80:80`, attaches to `fl_reverse_proxy_net` + `fl_internal_net`.
  - Static config `nginx/nginx.conf` proxies everything to `http://superlink:9091`.
- **superlink**
  - Build context `docker/superlink`.
  - Environment variables drive host/port/rounds (`SUPERLINK_HOST`, `SUPERLINK_PORT`, `SUPERLINK_ROUNDS`).
  - Mounts config folder read-only plus placeholder `superlink_certs` volume for future TLS.
- **supernode-1`, `supernode-2`**
  - Build context `docker/supernode`.
  - Each mounts shared config, dedicated `supernodeX_data`, and `supernodeX_certs` volumes.
  - `CLIENT_ID` + `SUPERLINK_ADDRESS` env vars differentiate nodes.
  - Retry logic in Python client reconnects until SuperLink is up.

---

## 2.2 Networks

Implemented exactly as required:

```yaml
networks:
  fl_internal_net:
    driver: bridge
  fl_reverse_proxy_net:
    driver: bridge
```

Reverse proxy is the only service with access to both.

---

## 2.3 Volumes

`docker/docker-compose.yml` declares:

```yaml
volumes:
  fl_ca_certs:
  superlink_certs:
  supernode1_data:
  supernode1_certs:
  supernode2_data:
  supernode2_certs:
```

Data volumes persist synthetic datasets, cert volumes remain reserved for Section 3+.

---

# 3. Binding & Internal Hostnames

Inside Docker:

* SuperLink must be reachable by hostname:
  `superlink`

Each SuperNode uses:

* `superlink:9091` (or chosen Flower insecure port)

Reverse proxy routes:

* `superlink:PORT` internally
* Host browsers access:
  `http://<your-local-domain>` (even if mapped in /etc/hosts)

Codex must not hardcode localhost for internal service calls.
Use Docker DNS names.

---

# 4. Runtime Behavior

- `docker/superlink/entrypoint.sh` exports env defaults and runs `python -u config/flwr_server_config.py`, which launches a FedAvg server on `0.0.0.0:9091`.
- `docker/supernode/entrypoint.sh` propagates `SUPERLINK_ADDRESS`, selects a dataset dir (`/data`), and starts the NumPy client script.
- `flwr_client_config.py` performs:
  - Synthetic dataset generation via `dataset_loader.load_local_dataset`.
  - Local linear regression training for 5 epochs per round.
  - Retry loop with exponential backoff until Flower handshake succeeds.

---

# 5. Nginx Behavior (No Auth Yet)

`nginx/nginx.conf` listens on port 80 and proxies all traffic to `superlink_backend` (Docker DNS `superlink:9091`) while preserving headers. No TLS or auth is enforced yet, satisfying the validation scope.

---

# 6. Validation & Acceptance Criteria

1. **Bring up stack**
   ```bash
   cd docker
   docker compose up --build
   ```
   Containers should transition to `running` without restarts.
2. **Verify joins**
   - `docker logs superlink` → shows Flower rounds progressing with `supernode-1`/`2`.
   - `docker logs supernode-1` → logs `Starting client supernode-1 targeting superlink:9091`.
3. **Scale nodes**
   - Duplicate the `supernode-2` stanza (rename to `supernode-3`, etc.), assign new `CLIENT_ID`, `supernode3_data`, `supernode3_certs` volumes, and re-run `docker compose up -d --build`.
   - Each additional client automatically generates its own dataset under the mapped `/data`.

* Add a new node by copy/paste service block
* New node joins without modifying others
* Dataset volumes remain isolated

### ✅ D. No exposed federated ports

* Only reverse-proxy is visible on host
* SuperLink/SuperNodes are not accessible from host network

---

# 7. Output of Section 2

When Section 2 is finished, project must support this:

```
docker compose up --build
# opens browser → http://<local-domain>
# triggers FL job
# supernodes connect + train
```

NO TLS, NO auth, NO cert enforcement yet.

---

# 8. STOP POINT

After successful Section 2 validation,
Codex must NOT proceed to TLS/auth changes.

Next phase (Section 3) adds:

* local CA generation
* mTLS between SuperLink/SuperNodes
* certificate mounts + enforcement

```

---

I’m stopping here per your rules.

Say **“Proceed to Section 3”** when you’re ready, or tell me what you want adjusted in Section 2 before we move on.
```
