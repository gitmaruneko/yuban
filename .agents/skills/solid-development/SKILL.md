---
name: solid-development
description: Apply SOLID engineering principles when designing, implementing, refactoring, or reviewing code in this repository. Use for changes involving responsibilities, module boundaries, extension points, interchangeable implementations, public interfaces, or external dependencies. Skip content-only, data-entry, and formatting-only changes.
---

# SOLID Development

Apply SOLID to functions, modules, components, and data pipelines as well as classes. Optimize for cohesive code, explicit contracts, low coupling, and testability. Do not introduce classes, interfaces, dependency-injection containers, or extension points without a concrete need.

## Working method

1. Identify the behavior being changed, its consumers, its external boundaries, and the distinct reasons it may change.
2. Preserve existing observable contracts unless the requirement explicitly changes them.
3. Implement the simplest cohesive design that satisfies the current requirement.
4. Refactor adjacent code only when needed to make the requested change safe; avoid unrelated architecture rewrites.
5. Verify changed behavior and important contracts with proportionate tests.

## Principles

### SRP — Single Responsibility Principle

- Give each unit one primary responsibility and one coherent reason to change.
- Separate policy from I/O concerns such as fetching, storage, DOM rendering, logging, and file access when they vary independently.
- Split code because it serves different actors or change drivers, not merely because a file or function is long.
- Avoid modules that coordinate a workflow while also validating, transforming, persisting, and presenting its data.

### OCP — Open/Closed Principle

- Prefer extending a stable seam over repeatedly editing unrelated working code.
- When variation is established, use focused strategies, handlers, registries, or data-driven mappings instead of growing conditional chains.
- Keep extension contracts small and explicit.
- Do not add speculative abstractions for hypothetical future variants; refactor when a real second case reveals the seam.

### LSP — Liskov Substitution Principle

- Any interchangeable implementation must preserve the documented observable contract: accepted inputs, outputs, errors, side effects, and invariants.
- Do not strengthen preconditions, weaken postconditions, silently discard supported behavior, or require callers to detect a special implementation.
- Prefer composition when an implementation cannot honestly honor the full contract.
- Run the same contract tests against every interchangeable implementation where practical.

### ISP — Interface Segregation Principle

- Make consumers depend only on the capabilities they use.
- Prefer focused parameters, collaborators, and module exports over broad service objects, configuration bags, or catch-all interfaces.
- Split interfaces by consumer need when implementations or callers are forced to ignore fields, methods, or flags.
- Avoid placeholder methods and unsupported-operation errors; they signal that the contract is too broad.

### DIP — Dependency Inversion Principle

- Keep domain and application policy independent of concrete browser, network, filesystem, persistence, and vendor details.
- Put concrete integrations at system boundaries and provide them through narrow functions, callbacks, ports, or collaborators when substitution or testing requires it.
- Let high-level policy define the contract it needs; adapters conform to that contract.
- Compose dependencies at entry points. Do not add indirection when a direct dependency is stable, local, and has no useful testing or replacement seam.

## Review gates

Before considering a code change complete, confirm:

- Every changed unit has a clear, cohesive responsibility.
- Adding the next known variant would not require scattered edits across unrelated modules.
- Interchangeable implementations honor the same contract.
- Consumers receive only the surface area they need.
- Core policy does not directly depend on replaceable infrastructure details.
- Tests cover the changed behavior and shared contracts at the appropriate level.

Flag these common warning signs during review: mixed I/O and policy, repeated type-based conditionals, special-case subtype checks, unused interface members, domain logic importing infrastructure directly, circular dependencies, and mutable global state.

If a requirement justifies an exception, keep it local and record the tradeoff in the change summary. Use an ADR when the exception creates a durable architectural constraint.
