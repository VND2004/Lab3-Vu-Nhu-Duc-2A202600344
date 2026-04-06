# Flowchart & Insight

This document captures the visual logic of our chatbot-to-agent workflow and the key learning points from the lab.

## 1. Visual Logic Diagram

```mermaid
flowchart TD
    US[User Input] --> ModelChoice{Execute As?}
    
    %% Chatbot Flow
    subgraph Baseline Chatbot
    ModelChoice -->|Chatbot| CB1[Build System & User Prompts]
    CB1 --> CB2[Call LLM API]
    CB2 --> CB3[Stream Output]
    CB3 --> CB4[Print Content & Reasoning]
    end
    
    %% ReAct Agent Flow
    subgraph ReAct Agent
    ModelChoice -->|Agent| RE1[Log AGENT_START & Init Context]
    RE1 --> RE2{while steps < max_steps?}
    RE2 -->|Yes| RE3[Call LLM generate]
    RE3 --> RE4{Has 'Final Answer:'?}
    
    RE4 -->|Yes| RE5[Extract Answer & Log AGENT_END]
    
    RE4 -->|No| RE6{Has 'Action:'?}
    RE6 -->|Yes| RE7[Extract Tool Name & Args]
    RE7 --> RE8[Execute Tool]
    RE8 --> RE9[Get Observation]
    RE9 --> RE10[Append Observation to Context]
    RE10 --> RE2
    
    RE6 -->|No| RE11[Append Invalid Action Observation]
    RE11 --> RE2
    
    RE2 -->|No| RE12[Log max_steps_exceeded & Return Error]
    end

    %% Telemetry Subsystem
    subgraph Telemetry & Metrics
    RE1 -.-> TM1[(Logger)]
    RE3 -.-> TM1
    RE7 -.-> TM1
    RE8 -.-> TM1
    RE5 -.-> TM1
    RE12 -.-> TM1
    RE3 -.-> TM2[(Tracker: Usage & Latency)]
    end
```

## 2. Group Insights

- The **baseline chatbot** (`src/chatbot.py`) uses a simple direct API call. It is very fast and handles streaming out of the box, but lacks external interactions, meaning it hallucinate facts (especially current weather or real-time costs).
- The **ReAct loop** (`src/agent/agent.py`) heavily mitigates hallucination by executing tools and appending the *Observation* back to the context. 
- **Parsing logic is critical**: The loop relies on regular expressions matching `Final Answer:` and `Action:`. If the LLM produces a slightly different pattern, the code forces an `[Không tìm thấy Action hợp lệ]` observation.
- **Guardrails & Limits**: `max_steps` prevents the agent from infinitely looping when tool execution continuously fails (as seen in some `max_steps_exceeded` scenarios).
- **Comprehensive Telemetry**: The agent architecture integrates explicit hooks for logging events (`AGENT_START`, `LLM_RESPONSE`, `TOOL_CALL`, `TOOL_RESULT`) and tracking metric usages (`latency_ms`, `total_tokens`), making finding root causes of looped logic or error much easier compared to the baseline chatbot.