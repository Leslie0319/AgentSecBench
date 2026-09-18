# Reproducibility contract

Every benchmark run should be traceable to the code, dataset, and configuration that produced it.

A standard run directory contains:

- `results.jsonl`: per-case model response and evaluation
- `summary.json`: aggregate security and utility metrics
- `config.snapshot.yaml`: byte-for-byte snapshot of the YAML experiment config
- `metadata.json`: provenance metadata and hashes

## metadata.json

The metadata records:

- UTC creation timestamp
- run id
- evaluator, model/backend, temperature, and max tokens
- Git commit SHA and whether the local worktree was dirty
- Python and platform information
- SHA-256 of the input config and dataset
- SHA-256 of the generated config snapshot, results, and summary

API-key values are never persisted. Configs store only the environment-variable name used to load a credential.

## Why hashes matter

A path or filename is not a stable experiment identity: files can be edited in place. SHA-256 lets a later reader verify that the dataset, config, and result artifacts are byte-for-byte the same inputs and outputs as the original run.

## Dirty worktrees

`git.dirty=true` means the run was executed with uncommitted local changes. Such a run can still be useful, but it is weaker evidence for reproducibility because the Git commit alone is insufficient to reconstruct the exact code state.

For research-quality runs, prefer a clean worktree and record the resulting commit SHA.
