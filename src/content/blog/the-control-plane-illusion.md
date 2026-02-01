---
title: "The Control Plane Illusion: Why Your Phone is Always Tracking You"
date: 2026-02-03
author: "Ganesh Pagade"
tags: ["privacy", "security", "networking", "mobile"]
description: "Why mobile privacy settings are largely security theater when the cellular control plane remains a silent, silicon-level tracking layer."
draft: true
---

You've toggled off "Location Services." You've denied app permissions. You've audited your privacy reports. You feel secure.

But beneath the polished UI of your mobile operating system, a silent conversation is happening between your modem silicon and the cellular network. Using protocols like RRLP and LPP, your carrier can ask your device for its precise GNSS coordinates at any time, and your phone will respond—natively, silently, and invisibly. This isn't an "app permission" problem; it's a "control plane" reality.

### The Real Problem: The Hardware/Software Schism

We have been trained to think of privacy as a software setting. If the OS (iOS or Android) says an app isn't accessing your location, we believe it. But your phone is not a single computer; it is a collection of processors with different masters.

The Application Processor (AP) runs the OS you see. The Baseband Processor (BP) runs the modem. In the hierarchy of power, the BP often has direct access to the GNSS (GPS) hardware and bypasses the OS entirely to communicate with the cellular network's **Control Plane**.

```text
The Location Hierarchy:

[ User Interface ]  <-- "Location: OFF" (Comforting lie)
       |
[ Operating System ] <-- Software Gates (App permissions)
       |
[ Control Plane ]   <-- RRLP / LPP Protocols (The Silent Handshake)
       |
[ Modem Silicon ]   <-- Carrier Command: "Send GPS Now"
       |
[ GNSS Hardware ]   <-- Precise Coordinates (lat/long)
```

### Why This Exists: The Regulatory Mandate

This capability isn't a "bug" or a "backdoor" in the traditional sense. It is a core feature of the cellular standard, driven by two primary incentives:

1.  **Emergency Services (E911):** Regulators require carriers to provide precise location data for emergency calls. To ensure this works even when "Location Services" are off, the capability must be baked into the modem at the protocol level.
2.  **Network Optimization:** 5G technologies like beamforming require the network to know exactly where a device is to optimize the radio signal. Precise tracking is the cost of high-bandwidth connectivity.

### The Missing Model: The OS as a Guest

The missing model is that **the OS is just a guest on the modem's hardware**.

We view the phone as a device we own that connects to a network. The network views the phone as a node it manages. Protocols like **LTE Positioning Protocol (LPP)** are natively part of the control plane—the inner workings of the cellular network that are practically invisible to the end user. When the network pings the modem for coordinates, the modem responds. The OS is never even informed that the transaction took place.

### Tradeoffs and Failure Modes

The tradeoff for our high-speed, reliable mobile world is the absolute loss of location sovereignty.

1.  **The Shadow Audit:** Because these protocols happen in the control plane, there is no "Privacy Report" that shows when your carrier (or a state actor with access to the carrier's core) pinged your device.
2.  **The Metadata Leak:** Even if the modem doesn't send GNSS data, the network still knows which cell towers you are connected to. With 5G's dense small-cell architecture, "cell tower triangulation" is becoming nearly as precise as GPS.
3.  **The Trust Boundary:** We trust Apple or Google to manage our privacy, but they are often beholden to the same regulatory requirements that mandate these control-plane features. Apple’s recent move to control its own modem silicon is a step toward closing this gap, but it remains to be seen if they will actually allow users to disable these protocols.

### Second-Order Effects: The Erosion of the Opt-Out

The second-order effect is the **death of the "Opt-Out."**

As society becomes increasingly dependent on mobile connectivity, the ability to truly "go dark" requires opting out of participating in modern life. If you want a phone that works, you must accept a device that can be silently tracked by the network operator.

We are moving toward a world where "privacy" is something we only have relative to third-party app developers, while our relationship with the infrastructure itself is one of total transparency.

If you really want to hide your location, a software toggle won't save you. You need a Faraday bag, not a privacy setting.

---
*Inspired by the discussion on HN: [Mobile carriers can get your GPS location](https://an.dywa.ng/carrier-gnss.html)*
