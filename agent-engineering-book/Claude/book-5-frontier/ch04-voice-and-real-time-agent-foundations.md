# Chapter 4 — Voice and Real-Time Agent Foundations

Voice agents operate under time pressure while processing partial, noisy and interruptible input. They must determine when a user has finished speaking, maintain conversational state and respond with acceptable latency. This chapter introduces the real-time voice pipeline from speech recognition through reasoning and synthesis. Readers build a simple voice-based account-briefing assistant without telephony or autonomous outbound calling.

## 4.1 The Real-Time Voice Pipeline

A voice system includes audio capture, speech recognition, turn detection, agent reasoning, tool calls and speech synthesis. Each stage contributes latency and potential error.

Readers will trace information and timing across the pipeline. The architecture will keep transcript, audio and workflow state distinct.

## 4.2 Streaming Speech Recognition

Streaming recognition provides partial transcripts before an utterance is complete. These early results improve responsiveness but may change as additional audio arrives.

The agent will avoid acting on unstable transcript fragments for consequential requests. Finalized text will be marked separately from provisional text.

## 4.3 Voice Activity Detection

Voice activity detection distinguishes speech from silence and background sound. Incorrect detection can cut off users or create false turns.

Readers will tune silence thresholds and examine noisy conditions. The system will allow user correction when speech is missed.

## 4.4 Turn Detection and Turn Taking

A conversational agent must infer when it should respond, wait or continue listening. Natural pauses do not always indicate the end of a turn.

Turn logic will combine acoustic signals, language completion and conversational context. Users must be able to interrupt or extend their thought naturally.

## 4.5 Speech Synthesis

Speech synthesis converts agent output into audio with appropriate pacing, pronunciation and tone. Long textual responses may be unsuitable for spoken delivery.

Readers will design concise voice responses and provide optional visual detail separately. Evidence-heavy material may be summarized aloud and displayed for inspection.

## 4.6 Conversational State

Voice conversations contain references, corrections and interruptions that depend on prior turns. Conversational state must remain synchronized with workflow and tool state.

The assistant will track the current account, question and pending action explicitly. A conversational acknowledgment will not be mistaken for formal approval.
