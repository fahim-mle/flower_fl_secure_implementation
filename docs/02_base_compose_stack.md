# ✅ **SECTION 2 — Base Docker/Compose Layout (INSECURE Validation First)**

**Filename:** `02_base_compose_stack.md`

```markdown
# 02 — Base Docker/Compose Stack (Insecure First for Wiring Validation)

Goal:
Bring up a local multi-container Flower topology:
- 1 SuperLink container
- N SuperNode containers
- Nginx reverse proxy (no auth yet)
- All connected by correct networks + volumes
- NO TLS/mTLS/auth at this step

This stage is purely to validate:
1. container build/run correctness
2. private networking works
3. SuperNodes can register + train with SuperLink
4. you can scale nodes cleanly

---

# 1. Files Codex MUST Create

Codex will create these files (following directory structure Section 0):

```

docker/docker-compose.yml
docker/superlink/Dockerfile
docker/superlink/entrypoint.sh
docker/supernode/Dockerfile
docker/supernode/entrypoint.sh
nginx/nginx.conf
nginx/docker/Dockerfile
.env

````

No certificates used yet.

---

# 2. Compose Requirements (Authoritative)

## 2.1 Services Required

### reverse-proxy
- image built from `nginx/docker/Dockerfile`
- ports:
  - host 80 → container 80
  - host 443 reserved for later (do not enforce TLS yet)
- networks:
  - fl_reverse_proxy_net
  - fl_internal_net
- depends_on: superlink

### superlink
- built from `docker/superlink/Dockerfile`
- runs Flower SuperLink in insecure mode
- exposes NO ports to host
- networks:
  - fl_internal_net
- mounts:
  - superlink config folder (bind mount)
  - superlink_certs volume exists but unused now

### supernode-1..N
- built from `docker/supernode/Dockerfile`
- each node has:
  - its own dataset volume
  - its own cert volume (unused now)
- networks:
  - fl_internal_net
- depends_on: superlink

---

## 2.2 Networks Required

Codex must define:

```yaml
networks:
  fl_internal_net:
    driver: bridge

  fl_reverse_proxy_net:
    driver: bridge
````

Rules:

* Only reverse-proxy attaches to public bridge.
* SuperLink + SuperNodes never expose ports to host.

---

## 2.3 Volumes Required

Codex must define:

```yaml
volumes:
  fl_ca_certs:
  superlink_certs:

  supernode1_data:
  supernode1_certs:

  supernode2_data:
  supernode2_certs:

  ...
```

Rules:

* Each supernode must map the correct volume pair.
* Dataset volumes persist between runs.

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

# 4. Minimal Insecure Runtime Commands

## SuperLink entrypoint.sh

Codex will run SuperLink in insecure mode.
Example intent:

* start Flower server
* listen on internal port
* no TLS flags

## SuperNode entrypoint.sh

Codex will run each node in insecure mode:

* connect to superlink hostname
* train on local synthetic dataset dir mounted from `<supernodeX_data>`
* keep running / retry until connected

Codex should implement basic retry backoff so a node waits if SuperLink isn't ready.

---

# 5. Nginx Behavior (No Auth Yet)

nginx.conf must:

* accept traffic on port 80
* forward everything to SuperLink HTTP endpoint
* preserve headers
* no auth, no TLS enforcement

This is temporary. Section 6 will replace this with full TLS + OIDC config.

---

# 6. Validation & Acceptance Criteria

Codex must include a scripted or documented validation path:

### ✅ A. Compose boots cleanly

* `docker compose up --build`
* all containers healthy
* no restart loops

### ✅ B. SuperNodes connect to SuperLink

* SuperLink logs show node joining
* SuperNodes logs show handshake success
* At least 1 FL round completes

### ✅ C. Multi-node scaling works

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
