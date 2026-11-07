---
description: Run a blockchain/Web3 design session , produce a security-first smart-contract
  or protocol design with an audit and deployment path, grounded in the gd-blockchain-engineer
  skill.
---

Design a blockchain/Web3 solution for: **$ARGUMENTS**

All arguments are optional. `blockchain_type` (default `ethereum`; options: `ethereum`, `layer2`,
`solana`, `cosmos`, `multi-chain`); `protocol_type` (default `defi`; options: `defi`, `nft`, `dao`,
`bridge`, `infrastructure`, `enterprise`, `yield-strategy`); `security_level` (default `high`;
options: `standard`, `high`, `critical`, `formal-verification`, `enterprise-grade`); `complexity`
(default `standard`; options: `simple`, `standard`, `complex`, `enterprise`, `cross-chain`). With no
arguments, open by drawing out the protocol's purpose, the value at risk, and the trust model.

## Approach

1. **Load the blockchain knowledge** , Use the `gd-architecture:blockchain-engineer` skill.
2. **Frame the problem** , clarify the protocol's purpose behind `$ARGUMENTS`, the value at risk, the
   trust and threat model, and the target chain and standards.
3. **Design the protocol** , apply the fitting models from the skill (DeFi protocol patterns,
   access-control and emergency systems, Layer 2 scaling, cross-chain bridges, relevant ERC/EIP
   standards) to the chosen `blockchain_type` and `protocol_type`.
4. **Validate and deploy** , at the requested `security_level` and `complexity`, guard against MEV,
   flash-loan, and oracle-manipulation vectors, confirm emergency controls and an upgrade path, and
   deliver the design with an audit-preparation and deployment plan.

## Opening (when no args)

"Let's design a protocol that is secure by construction before it is fast. What is it for, how much
value will it hold, what is the trust model, and which chain and standards are we targeting?"

## Examples

```bash
# DeFi protocol on Ethereum with critical security
/gd-architecture:blockchain-engineer blockchain_type=ethereum protocol_type=defi security_level=critical

# Complex yield strategy on Layer 2
/gd-architecture:blockchain-engineer blockchain_type=layer2 protocol_type=yield-strategy complexity=complex

# Enterprise multi-chain protocol with enterprise-grade security
/gd-architecture:blockchain-engineer blockchain_type=multi-chain protocol_type=enterprise security_level=enterprise-grade
```

---

- Skill: `gd-architecture:blockchain-engineer` (owns the methodologies, patterns, and blockchain
  knowledge)
- Related agent: the proactive `gd-architecture:blockchain-engineer` agent loads the same skill autonomously.
