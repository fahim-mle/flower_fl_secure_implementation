# ✅ **Final Directory Architecture (for Codex + Your Implementation)**

**Filename suggestion:** `00_project_directory_structure.md`

```markdown
# Project Directory Structure for Secure Local Federated Learning

This directory tree defines the foundation for the entire implementation life-cycle.
All instructions, Dockerfiles, compose stacks, certificates, and scripts will adhere
to this exact structure.

```

project-root/
│
├── certificates/                     # All certificates generated on host
│   ├── ca/
│   │   ├── ca.crt
│   │   ├── ca.key
│   │   └── ca.srl
│   │
│   ├── superlink/
│   │   ├── superlink.crt
│   │   ├── superlink.key
│   │   └── superlink.pem
│   │
│   └── supernodes/
│       ├── sn1/
│       │   ├── sn1.crt
│       │   ├── sn1.key
│       │   └── sn1.pem
│       ├── sn2/
│       │   ├── sn2.crt
│       │   ├── sn2.key
│       │   └── sn2.pem
│       └── ...
│
├── nginx/                             # Reverse proxy layer
│   ├── nginx.conf
│   ├── ssl/
│   │   ├── nginx.crt
│   │   └── nginx.key
│   ├── oidc/                          # OIDC integration config
│   │   ├── oauth2_proxy.cfg
│   │   ├── dex.cfg
│   │   └── keycloak.cfg
│   └── docker/
│       └── Dockerfile
│
├── auth-provider/                     # Optional Keycloak / Dex / OAuth2-proxy
│   ├── keycloak/
│   │   ├── realm-export.json
│   │   └── Dockerfile
│   ├── oauth2-proxy/
│   │   ├── oauth2-proxy.cfg
│   │   └── Dockerfile
│   └── dex/
│       ├── config.yaml
│       └── Dockerfile
│
├── docker/                            # All container build contexts
│   ├── docker-compose.yml             # Main orchestrator for local deployment
│   ├── superlink/
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── config/
│   │       ├── flwr_server_config.py
│   │       └── allowed_supernodes.json
│   │
│   └── supernode/
│       ├── Dockerfile
│       ├── entrypoint.sh
│       └── config/
│           ├── flwr_client_config.py
│           └── dataset_loader.py
│
├── supernodes/                         # Host-side logical structure
│   ├── sn1/
│   │   ├── data/                      # Mounted volume
│   │   └── logs/
│   ├── sn2/
│   │   ├── data/
│   │   └── logs/
│   └── ...
│
├── scripts/                            # All automation scripts
│   ├── generate_ca.sh
│   ├── generate_superlink_cert.sh
│   ├── generate_supernode_cert.sh
│   ├── verify_cert.sh
│   ├── create_networks.sh
│   └── cleanup.sh
│
├── docs/                               # All documentation consumed by Codex
│   ├── 01_architecture_overview.md
│   ├── 02_base_compose_stack.md
│   ├── 03_certificate_generation.md
│   ├── 04_superlink_config.md
│   ├── 05_supernode_config.md
│   ├── 06_authentication_layer.md
│   ├── 07_nginx_reverse_proxy.md
│   ├── 08_verification_and_tests.md
│   └── operations_manual_extracted.md
│
├── logs/                               # Unified local logs if you aggregate
│   ├── superlink.log
│   ├── supernode1.log
│   ├── supernode2.log
│   └── reverse-proxy.log
│
└── .env                                # Environment variables for compose

```

---

# 🔐 **Naming Standards (Codex Must Follow)**

### **Networks**
```

fl_internal_net
fl_reverse_proxy_net
fl_auth_net

```

### **SuperNode Container Names**
```

supernode-1
supernode-2
supernode-3
...

```

### **Volumes**
```

superlink_certs
fl_ca_certs

supernode1_data
supernode1_certs

supernode2_data
supernode2_certs

...

```

### **Certificate Locations (inside containers)**

#### SuperLink:
```

/etc/flwr/certs/superlink.crt
/etc/flwr/certs/superlink.key
/etc/flwr/certs/ca.crt

```

#### Each SuperNode:
```

/etc/flwr/certs/node.crt
/etc/flwr/certs/node.key
/etc/flwr/certs/ca.crt

```

### **Nginx TLS**
```

/etc/nginx/ssl/nginx.crt
/etc/nginx/ssl/nginx.key

```

---

# 🔧 **This Directory Architecture Enables**
✔ Clean separation between host-level assets & container configs
✔ Predictable paths for Codex to mount certs into containers
✔ Portable deployment on any Ubuntu machine
✔ Proper isolation between certificates, configs, datasets, and logs
✔ Scalable multi-node FL development
✔ Extensible auth system (Keycloak / GitHub / Dex)

---
