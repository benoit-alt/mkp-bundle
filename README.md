
# MKPCTL — Modular Knowledge Platform CLI (v1.0.0)

A zero-dependency CLI that validates and loads a **Core** knowledge base plus any number of **Modules** into a unified, query-ready aggregate (CSV + SQLite).

## Key Guarantees
- **Strict Predicate Catalog** (the *Standard 12*): loader rejects unknown verbs.

| Predicate | Meaning |

|---|---|

| IS_A | Hierarchy/type assertion |

| USES | General consumption/usage |

| PROVIDES | Capability/service offering |

| MITIGATES | Defensive control reduces risk |

| EXPLOITS | Uses a vulnerability/CVE |

| TARGETS | Victimology/target class |

| LOCATED_IN | Geography/jurisdiction |

| AFFILIATED_WITH | Group membership/ownership |

| BLOCKS | Technical restriction |

| REQUIRES | Dependency/prerequisite |

| CONFLICTS_WITH | Incompatibility |

| RELATED_TO | Weak/associative link |



- **URN Cheatsheet**

  - Core (3 segments): `urn:entity:<core-category>:<slug>` → e.g., `urn:entity:mfa:fido2`.

  - Module (4 segments): `urn:entity:<module-namespace>:<module-category>:<slug>` → e.g., `urn:entity:darkweb:market:hydra`.

  - Regex: `^urn:entity:([a-z0-9_]+):([a-z0-9_]+)(?::([a-z0-9_]+))?$`



- **Conflict Logic**

  - Resolution chain: **core_immutable → prefer_fresh → prefer_higher_source_confidence → flag**.

  - Human audit: `aggregated/conflict_log.csv` with columns:

    `entity_urn | field | winning_value | losing_value | resolution_rule | winning_source_module`



## Install (wheel)

```bash

pip install mkpctl-*.whl

```



## Quickstart

```bash

# Generate a demo KB (Core + DarkWeb) and build aggregates

mkpctl demo ./my-kb


# Validate your own KB

mkpctl validate ./my-kb/00_Core_System ./my-kb/01_Module_DarkWeb --strict-predicates


# Load & aggregate

mkpctl load ./my-kb/00_Core_System ./my-kb/01_Module_DarkWeb --out ./my-kb/aggregated --strict-predicates


# Merge label lookups

mkpctl build-labels --root ./my-kb --out ./my-kb/aggregated/labels_to_urn_merged.csv

```



## Directory Contract (schemas)

- `graph/entities.csv`: `id,type,name,description`

- `graph/relationships.csv`: `source_id,relation,target_id`

- `evidence/claims.csv`: `claim_id,subject,predicate,object,source_id,observed_at,confidence`

- `conflict_resolution/conflicts.csv` (optional): `dispute_id,urn,aspect,claim_id,stance,source_id,observed_at,last_updated,notes`



## Versioning

This wheel is **v1.0.0** and generates **v1.0** Core-compatible data by default. Upgrade the Core to **v2.x** via a predicate-catalog PR and bump the CLI accordingly.

---

## MKP + Claude + CLI (v1.0.4)

- Specs: see `/specs/SPEC-001 …`, `/specs/SPEC-002 …`, `/specs/SPEC-003 …`
- Claude: `.claude/` is installed; run **/mkp-bootstrap**, **/mkp-audit**, **/mkp-task**
- CLI: use `mkpctl` from the local wheel at repo root
- CI: `.github/workflows/mkp-audit.yml` (strict mode + optional --json-summary gating)

