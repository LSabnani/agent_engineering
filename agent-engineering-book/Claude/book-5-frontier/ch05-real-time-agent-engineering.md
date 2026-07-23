# Chapter 5 — Real-Time Agent Engineering

A technically functional voice agent may still feel unusable because of delay, interruption failures or poor recovery. This chapter addresses real-time latency budgets, barge-in, partial transcripts, tool calls during conversation and telephony considerations. Readers evaluate the voice assistant using metrics specific to spoken interaction.

## 5.1 Interruptions and Barge-In

Users expect to interrupt a speaking agent when the response is wrong, too long or no longer needed. The system must stop playback and process the new turn quickly.

Readers will implement interruption handling without losing conversational state. The interrupted response will be marked incomplete rather than treated as delivered.

## 5.2 Partial Transcripts

Partial transcripts can support early intent detection but may misrepresent names, numbers or corrections. Premature actions create unnecessary risk.

The agent may prepare low-risk context while waiting for transcript finalization. External actions remain blocked until the relevant utterance is stable and confirmed.

## 5.3 Tool Calls During Conversation

Research, calendars and business systems may be invoked while the conversation continues. Tool latency must be communicated without creating awkward silence.

The agent will provide concise status, continue gathering clarifying information or offer to complete the task asynchronously. It will not fabricate results to maintain conversational flow.

## 5.4 Real-Time Latency Budgets

Latency budgets allocate time across recognition, reasoning, tools and synthesis. Users perceive delays differently depending on whether the system acknowledges progress.

Readers will measure median and tail latency for each stage. Optimization will preserve safety and factual validation.

## 5.5 Telephony and Communication Channels

Telephony introduces call routing, codecs, recording consent, caller identity and network variability. These concerns extend beyond model capability.

The chapter will discuss architecture and compliance considerations without implementing autonomous outbound calls. Human-approved, inbound or training scenarios are safer learning contexts.

## 5.6 Voice-Specific Evaluation

Voice evaluation includes transcription accuracy, interruption success, turn errors, response latency, task completion and conversational naturalness.

Human evaluation remains important because numerical speech metrics do not fully capture user frustration or trust. The voice agent will be compared with a text-based baseline.
