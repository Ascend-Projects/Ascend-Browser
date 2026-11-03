Act as a Principal Software Engineer and Systems Architect. I want to create a hyper-optimized, privacy-centric, low-resource web browser called "Ascend Browser".

Key Specifications:
- Name: Ascend Browser
- Base: Firefox source code / Gecko engine / Mozilla codebase components
- Core Goals: Minimal RAM/CPU footprint, maximum speed, zero telemetry, strict privacy, hardened security, and a ultra-clean UI.

Since writing a modern C++/Rust browser engine directly inside Scratch block coding environment is technically impossible due to Scratch's VM constraints, process limitations, and memory model, I need you to approach this in two distinct ways:

1. THE ARCHITECTURAL ROADMAP (Real-World Implementation):
   - Explain how to fork/build "Ascend Browser" using the Gecko codebase, C++, Rust, and custom compile flags (LTO, jemalloc, PGO).
   - Outline what telemetry, background services, and bloat to strip from the raw Firefox source.
   - Detail low-level `about:config` hardening, memory management tweaks (tab discard policies, process caps), and default security configurations.
   - Show how to bundle and pre-package hardened extensions (like uBlock Origin) directly into the core build.

2. THE "SCRATCH CONCEPT" / PROOF OF CONCEPT:
   - Provide a realistic conceptual design or visual mockup for how an "Ascend Browser" UI/shell prototype or simplified web engine simulation could be visually block-scripted in Scratch or structured modularly.

Please provide a detailed, step-by-step breakdown for building Ascend Browser under these principles.
