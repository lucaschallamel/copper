---
description: Run an edge/IoT design session , produce an edge architecture with connectivity,
  firmware, and edge-AI choices plus a deployment plan, grounded in the gd-edge-computing-specialist
  skill.
---

Design an edge/IoT solution for: **$ARGUMENTS**

All arguments are optional. `deployment_type` (default `industrial-iot`; options: `industrial-iot`,
`smart-city`, `autonomous`, `healthcare-iot`, `agriculture`); `connectivity` (default `wifi-mqtt`;
options: `wifi-mqtt`, `lora-wan`, `nb-iot`, `zigbee`, `bluetooth-mesh`, `ethernet-opcua`);
`power_profile` (default `battery-optimized`; options: `ultra-low-power`, `battery-optimized`,
`mains-powered`, `energy-harvesting`); `scale` (default `medium`; options: `prototype`, `small`,
`medium`, `large`, `massive-iot`); `hardware_platform` (default `esp32`; options: `esp32`, `stm32`,
`nrf52`, `raspberry-pi`, `jetson-nano`, `custom-mcu`). With no arguments, open by drawing out the
deployment environment, the connectivity constraints, and the power budget.

## Approach

1. **Load the edge/IoT knowledge** , Use the `gd-architecture:edge-computing-specialist` skill.
2. **Frame the problem** , clarify the deployment behind `$ARGUMENTS`, the environmental and
   connectivity constraints, the power budget, and any real-time or edge-AI requirements.
3. **Design the architecture** , apply the fitting models from the skill (MCU and RTOS selection,
   connectivity-protocol trade-offs, TinyML edge inference, fleet and OTA management) to the chosen
   `deployment_type`, `connectivity`, and `hardware_platform`.
4. **Validate and deploy** , at the chosen `power_profile` and `scale`, check inference latency,
   battery life, OTA reliability, and security provisioning, then deliver an architecture with
   benchmarks and a deployment plan.

## Opening (when no args)

"Let's design an edge solution that meets your latency and power budget at scale. Where is it
deployed, what connectivity and environmental constraints apply, and do you need on-device AI or
real-time response?"

## Examples

```bash
# Large industrial-IoT deployment over OPC-UA
/gd-architecture:edge-computing-specialist deployment_type=industrial-iot connectivity=ethernet-opcua scale=large

# Battery-optimised smart-city deployment over LoRaWAN
/gd-architecture:edge-computing-specialist deployment_type=smart-city connectivity=lora-wan power_profile=battery-optimized

# Autonomous deployment on Jetson Nano at massive IoT scale
/gd-architecture:edge-computing-specialist deployment_type=autonomous hardware_platform=jetson-nano scale=massive-iot
```

---

- Skill: `gd-architecture:edge-computing-specialist` (owns the methodologies, patterns, and edge/IoT
  knowledge)
- Related agent: the proactive `gd-architecture:edge-computing-specialist` agent loads the same skill
  autonomously.
