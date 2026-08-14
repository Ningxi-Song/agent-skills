# Visual Acceptance Criteria

Inspect every required image at readable zoom. Logs and manifests cannot substitute for inspection.

A target fails for node, label, panel, legend, caption, or annotation overlap; arrows crossing text or unintended objects; hidden arrowheads; clipping; unreadable or cramped text; ambiguous routing; unclear hierarchy; visibly inconsistent scaling or typography; or any required page, frame, or overlay not inspected.

Repair in this order: clipping, semantic ambiguity, overlaps, readability, then alignment and balance. Prefer relative positioning, anchors, text width, node distance, and routed bends over unexplained coordinate nudges.

Record `VISUALLY_VERIFIED` only after every required image passes. Automated checks may reject but cannot award a pass.
