# Persona pool

Select for the actual audience and goal. These are behavioral perspectives, not
fictional biographies or demographic stereotypes. Give each a concrete task and
starting state; adapt their knowledge without weakening the defining behavior.

## The impatient one

**Useful for:** first use, onboarding, navigation and paths competing for attention.

Skips documentation and messages, including README examples, help text and error
explanations. Tries the most obvious available route and expects feedback quickly.
The lead supplies technical launch access, without a recipe for completing the task.
Does not use source knowledge or a hidden operator recipe to recover. Record where visible
controls lead, what feedback gets missed and the first point they abandon or
misunderstand the task. Respect actual loading times; arbitrary instant impatience
is not evidence that a product is broken.

## The skeptic

**Useful for:** strong product claims, trust-sensitive flows and inconsistent states.

Starts from a user-visible promise and attempts the corresponding task. Challenges
contradictions between claims, interface feedback and outcomes. At the first unmet
claim, problem or inconsistency, record what broke trust and why they would stop.
Do not keep treating them as a satisfied adopter; the lead can investigate further
separately. Ordinary preferences need a reason before becoming defects.

## The cautious one

**Useful for:** accounts, personal data, permissions, payments and irreversible actions.

Wants the result but hesitates at unexplained requests or unclear consequences.
Looks for costs, permission scope, cancellation, privacy controls and recovery
before committing. Use only authorized test paths for consequential actions.
Record the decision they cannot make confidently, the information they sought and
whether the product provides it. A justified requirement for authentication is
not itself a bug.

## The distracted one

**Useful for:** multi-step tasks, forms, asynchronous work and return after interruption.

Starts with a real goal, then loses their place or is interrupted at a meaningful
point. Resumes, navigates back, retries an uncertain action or submits twice when
feedback is unclear. Observe progress preservation, duplicate effects, recovery
and whether the next action is understandable. Choose interruptions plausible for
the product rather than random destructive inputs.

## The returning user

**Useful for:** established products, releases, saved work and changed workflows.

Has representative existing data, settings and habits. Attempts a familiar task
and expects their work to remain available. Observe whether changes are discoverable,
state survives and prior choices still make sense. Use a real prior version or
representative seeded state when available; disclose the difference. A first
release without saved state may not earn this persona.

## The power user

**Useful for:** repeated workflows, professional tools, complex inputs and integrations.

Understands the domain and pursues a supported goal efficiently. Tries a realistic
larger input, repeated operation, shortcut or composition with an adjacent feature.
Test whether the product supports its advertised depth without needless repetition.
Keep scale representative; an exploratory journey is not a load benchmark or a
license to demand speculative features.

## The junior practitioner

**Useful for:** OSS projects, developer tools and products requiring technical knowledge.

Has basic relevant skills but limited domain knowledge. Reads the supplied
instructions and follows them literally from a clean starting point. Does not fill
missing steps with maintainer knowledge. Track assumed prerequisites, unexplained
terms, mismatched commands and recovery guidance. Select for the technical audience;
consumer unfamiliarity alone does not make someone a junior practitioner.

## The keyboard user

**Useful for:** interactive web and desktop journeys operated through visible controls.

Completes the task using keyboard navigation and activation. Observe focus order,
visible focus, labels, dialog entry/exit and controls they cannot reach or operate.
Use the actual interface; a static accessibility scan can supplement the journey.
Report specific observed barriers. This pass alone is not a comprehensive
accessibility or screen-reader audit; a CLI-only tool may not earn this perspective.
