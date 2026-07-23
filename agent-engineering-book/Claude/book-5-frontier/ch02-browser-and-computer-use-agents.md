# Chapter 2 — Browser and Computer-Use Agents

Computer-use agents interact with software through screens, browser pages, keyboard actions and pointer coordinates. They are valuable when APIs are unavailable but are more fragile than structured integrations. This chapter introduces DOM-based and visual interaction, screenshot interpretation and page-state reasoning. Readers build a bounded browser research agent that performs low-risk navigation and preserves evidence of each significant observation.

## 2.1 DOM-Based and Visual Interaction

DOM-based automation uses structured page elements, while visual interaction uses screenshots and coordinates. DOM access is generally more precise, but not every environment exposes stable structure.

Readers will compare the two approaches and design graceful fallback where appropriate. The agent will prefer the most structured interface available.

## 2.2 Screenshots and Visual Grounding

Screenshots provide visual state but may contain dense, dynamic or ambiguous information. Visual grounding links the model's interpretation to specific regions and controls.

The system will preserve screenshots as artifacts and record the basis for selected actions. Sensitive screen regions will be protected from unnecessary capture.

## 2.3 Coordinate-Based Actions

Coordinate actions such as clicking and dragging depend on screen size, scrolling and layout. A small shift can trigger the wrong control.

Readers will use element targeting where possible and coordinates only when necessary. Every consequential click will be followed by state verification.

## 2.4 Page-State Interpretation

The agent must determine whether a page is loading, complete, blocked, authenticated or showing an error. Visual appearance alone may be misleading.

Readers will combine visible evidence, DOM signals and navigation state. Ambiguous state will cause re-observation rather than speculative action.

## 2.5 Scrolling, Modals and Dynamic Content

Important information may be hidden below the viewport, behind expandable sections or inside modal dialogs. Dynamic pages can also change after interaction.

The agent will maintain a record of explored regions and avoid repeated scanning. New content will be verified before extraction.

## 2.6 Building a Browser Research Agent

The lab agent will visit approved public sources, collect account evidence and save citations or screenshots. It will not submit forms, accept terms or authenticate into business systems.

Readers will evaluate navigation success, extraction quality and action count. The computer-use solution will be compared with ordinary web tools.
