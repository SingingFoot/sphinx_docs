.. _ai-chatgpt:

ChatGPT for Technical Documentation
=====================================

**ChatGPT** (GPT-4o and later models) accelerates every phase of the
documentation lifecycle — from first-draft generation to terminology
harmonisation and localisation review. This page covers practical use
cases, a ready-to-use prompt library, integration patterns, and the
limitations every technical writer must keep in mind.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Where ChatGPT Fits in the TW Workflow
--------------------------------------

.. mermaid::

   flowchart LR
     subgraph Input["Inputs"]
       Code["Source code\n/ PR diff"]
       Notes["SME notes\n/ meeting transcript"]
       Draft["Existing draft\n/ legacy doc"]
     end

     subgraph ChatGPT["ChatGPT Tasks"]
       direction TB
       Outline["Generate outline\nor first draft"]
       Explain["Explain complex\nlogic in plain English"]
       Rewrite["Rewrite for audience\n(dev / end-user / exec)"]
       Translate["Translate /\nLocalise"]
       Troubleshoot["Generate\ntroubleshooting FAQs"]
     end

     subgraph Output["TW Review Gate"]
       Review["Technical writer\nreviews & validates"]
       Publish["Approved content\npublished in Sphinx"]
     end

     Input --> ChatGPT --> Output

.. important::
   ChatGPT output **always** passes through a human review gate before
   publication. AI-generated content can contain plausible-sounding but
   incorrect technical claims — validate every statement against source
   code, test environments, or SME sign-off.

Core Use Cases
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Activity
     - What to ask ChatGPT
     - Expected gain
   * - **First-draft generation**
     - Paste a function signature and docstring; ask for an RST description
       with parameters, return type, and a usage example.
     - Saves 60–80 % of initial drafting time.
   * - **Code explanation**
     - Paste a complex block; ask for a plain-English explanation suitable
       for a developer audience unfamiliar with the codebase.
     - Reduces SME interview time.
   * - **Terminology audit**
     - Paste 10 page excerpts; ask for a table of inconsistent terms and
       recommended canonical forms.
     - Catches naming drift across large doc sets.
   * - **Audience rewrite**
     - Paste a technical section; ask to rewrite it for a non-technical
       executive audience without losing accuracy.
     - Enables single-source multi-audience publishing.
   * - **Troubleshooting FAQs**
     - Describe a feature; ask *"What are the 10 most likely points of
       failure a developer would encounter during setup?"*
     - Surfaces edge cases before they reach support.
   * - **Release notes**
     - Paste a git diff or JIRA ticket list; ask for a user-facing
       changelog in plain English.
     - Speeds up release cycle documentation.
   * - **Localisation review**
     - Paste a translated section; ask to verify that technical meaning
       is preserved and idioms are appropriate.
     - Reduces back-and-forth with translation vendors.

Prompt Library
--------------

Copy, adapt, and store these prompts in your team's prompt repository.

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Purpose
     - Prompt template
   * - **Document a function**
     - *"Act as a Senior Technical Writer. Analyse the Python function below
       and generate a reStructuredText description that includes: a one-line
       summary, parameter table (:param: / :type:), return value, raised
       exceptions, and a concise usage example. Function: [PASTE CODE]"*
   * - **Explain an error code**
     - *"Explain the error code ``[ERROR_CODE]`` returned by a REST API to
       a developer audience. Include: what caused it, how to reproduce it,
       and three specific remediation steps."*
   * - **Simplify for end users**
     - *"Rewrite the following technical paragraph for a non-technical
       business user. Remove jargon, use active voice, and keep it under
       80 words. Paragraph: [PASTE TEXT]"*
   * - **Generate a troubleshooting section**
     - *"List the 8 most common problems a developer encounters when
       integrating [FEATURE] for the first time. For each problem, provide:
       symptom, root cause, and exact fix."*
   * - **Audit terminology**
     - *"Read the following 5 doc excerpts and produce a table with three
       columns: Term found, Frequency, Recommended canonical form.
       Excerpts: [PASTE]"*
   * - **Write a release note**
     - *"Convert the following JIRA tickets into user-facing release notes.
       Group by: New Features, Improvements, Bug Fixes. Use present tense.
       Tickets: [PASTE]"*
   * - **Peer-review a draft**
     - *"Review this draft section for: technical accuracy (flag any claims
       you cannot verify), clarity, active voice, and compliance with
       Microsoft Writing Style Guide principles. Draft: [PASTE]"*

.. tip::
   Prefix every prompt with a **persona** (*"Act as a Senior Technical Writer
   with 10 years of API documentation experience"*) to anchor tone and
   expertise level consistently.

Workflow Integration
--------------------

ChatGPT integrates into a Sphinx Docs-as-Code workflow at two natural
checkpoints: during drafting and during review.

.. mermaid::

   sequenceDiagram
     participant Dev  as Developer
     participant TW   as Technical Writer
     participant GPT  as ChatGPT
     participant Git  as Git / GitHub
     participant CI   as Sphinx CI Build

     Dev->>TW:  PR merged — new feature ready to document
     TW->>GPT:  "Draft RST for this function: [paste PR diff]"
     GPT-->>TW: Draft RST content
     TW->>TW:   Validate accuracy against test environment
     TW->>GPT:  "Review this draft for clarity and MSSG compliance"
     GPT-->>TW: Suggested edits
     TW->>Git:  Push .rst file to docs branch
     Git->>CI:  Trigger sphinx-build -W
     CI-->>TW:  ✅ Build passed / ❌ Warnings to fix

.. list-table:: Recommended integration checkpoints
   :header-rows: 1
   :widths: 30 35 35

   * - Checkpoint
     - ChatGPT task
     - Human task
   * - Feature merged → docs ticket
     - Generate first-draft RST from PR diff
     - Validate claims; add diagrams
   * - Draft complete
     - Audit for terminology consistency
     - Apply approved changes
   * - Pre-publish review
     - Rewrite for audience; check tone
     - Final approval and merge

Limitations
-----------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Mitigation
   * - **Hallucination** — plausible but wrong technical details
     - Always validate against source code or a running environment.
   * - **Knowledge cutoff** — unaware of recent API changes
     - Provide the current API spec or changelog in the prompt context.
   * - **No access to private repos**
     - Paste relevant code snippets; never paste secrets or credentials.
   * - **Inconsistent output** — same prompt may yield different results
     - Use a fixed system prompt; pin the model version via the API.
   * - **Verbose output** — tends to over-explain
     - Include a word limit in the prompt: *"Keep under 100 words."*
   * - **Tone drift** — may not match your style guide**
     - Append style rules to the system prompt or use a pre-review prompt.

.. seealso::

   * :doc:`claude` — Claude Cowork and Claude Code for technical writers.
   * :doc:`grammarly` — Prose quality and style-guide enforcement.
   * :doc:`/diagrams/flowcharts` — Docs-as-Code CI/CD pipeline flowchart.
