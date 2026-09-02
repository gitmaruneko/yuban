---
name: engineering-standards
description: Apply repository-wide engineering standards during implementation, refactoring, and code review. Use when executable behavior, data contracts, dependencies, accessibility, security, testing, or build behavior changes. Skip wording, formatting, and data-entry-only changes unless they alter a contract.
---

# Engineering Standards

Apply these standards in proportion to the risk and scope of the change. Prefer correctness and user safety, then clarity and simplicity, then maintainability and measured optimization.

When a change involves responsibilities, module boundaries, extension points, substitutable implementations, interfaces, or dependency direction, also read and apply [SOLID Development](../solid-development/SKILL.md).

## Design constraints

### KISS and YAGNI

- Choose the simplest design that satisfies the current requirement and remains easy to verify.
- Do not add patterns, configuration, hooks, layers, or extension points without a demonstrated use.
- Remove dead code and obsolete paths rather than preserving them for hypothetical needs.

### DRY with the Rule of Three

- Remove duplication of domain knowledge and business rules, not merely code that happens to look similar.
- Prefer a small amount of duplication over a premature or misleading abstraction.
- Treat a third occurrence or a proven shared change driver as a signal to extract a common unit.

### Separation of concerns

- Keep external I/O, boundary validation, search and filtering policy, data transformation, DOM rendering, and orchestration separable when they change independently.
- Do not create layers solely to satisfy a diagram; each boundary must reduce coupling or improve verification.
- Prefer composition of focused functions and modules over inheritance. Use inheritance only for a genuine substitutable relationship.

### Explicit contracts

- Make inputs, outputs, error behavior, side effects, and invariants evident from names, documentation, schemas, or tests.
- Preserve established JSON fields, URL parameters, and module behavior unless the requirement explicitly changes the contract.
- When a contract must change, update its producers, consumers, validation, tests, and documentation together.

## Boundary validation and Fail Fast

- Treat spreadsheets, JSON, URLs, query parameters, forms, remote responses, and browser storage as untrusted inputs.
- Validate and normalize data once at the boundary, then pass a known-valid representation inward.
- Reject invalid build or import data early with actionable messages. In the UI, provide safe loading, empty, and error states.
- Never expose secrets, raw internal failures, or unescaped user-controlled content.

## Verification and testability

- Keep core search, filtering, sorting, transformation, and validation logic independent from DOM and I/O where practical.
- Test observable behavior rather than implementation details. Add regression coverage when fixing a defect.
- Use shared contract tests for interchangeable implementations or adapters when relevant.
- Run the narrowest relevant checks during development and the complete applicable validation before handoff.
- Do not chase a coverage percentage; prioritize critical flows, boundary cases, and failure behavior.

## User-facing quality

### Accessibility by default

- Use semantic HTML, associated labels, meaningful names, visible focus, keyboard-operable controls, and sufficient contrast.
- Provide text alternatives for meaningful images and do not communicate state by color alone.
- Verify primary flows without relying on a mouse.

### Security and privacy by default

- Prefer safe DOM APIs such as `textContent` for untrusted values; avoid inserting unsanitized HTML.
- Validate allowed URL schemes and protect external links when opening a new browsing context.
- Collect, retain, and transmit only the user data required by the feature.
- Keep dependencies minimal and do not add one when a small, maintainable local implementation is sufficient.

### Progressive enhancement and performance

- Keep core content and navigation usable under slow networks and partial JavaScript failure where the product permits.
- Avoid unnecessary page weight and blocking work, but measure before adding performance complexity.
- Preserve clear feedback for loading, successful actions, empty results, and recoverable failures.

## Change discipline

- Keep changes small, focused, reviewable, and reversible.
- Apply the Boy Scout Rule only to code adjacent to the requested work; avoid unrelated refactors.
- Update relevant documentation and examples in the same change.
- Record durable architectural choices and meaningful tradeoffs in an ADR.
- State any intentional exception to these standards in the handoff, including its scope and rationale.

## Completion check

Before handoff, confirm that the change:

- satisfies the requested behavior without speculative scope;
- has clear responsibilities and contracts;
- validates external data at its boundary;
- covers important behavior and failure paths with proportionate tests;
- meets applicable accessibility, security, privacy, and performance expectations; and
- passes the repository's relevant automated and manual checks.
