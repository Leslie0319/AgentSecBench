# Threat Model Template

Every experiment should answer:

1. **Asset** — What are we protecting?
2. **Adversary capability** — What input/control does the attacker have?
3. **Trust boundary** — Which component incorrectly trusts attacker-controlled data?
4. **Attack goal** — Policy bypass, secret leakage, unauthorized tool call, etc.
5. **Success criterion** — A measurable condition, not a subjective impression.
6. **Baseline** — What happens without the attack?
7. **Defense assumptions** — What is the defense allowed to know/change?

## Week-1 scope

Use only synthetic secrets and controlled prompts. No third-party system testing.
