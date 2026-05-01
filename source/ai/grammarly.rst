.. _ai-grammarly:

Grammarly for Technical Documentation
=======================================

**Grammarly** is an AI-powered writing assistant that enforces prose quality,
grammatical correctness, and style-guide consistency across all documentation.
While Sphinx handles structure and ChatGPT accelerates drafting, Grammarly acts
as the final quality gate before content reaches readers.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Where Grammarly Fits in the TW Workflow
-----------------------------------------

.. mermaid::

   flowchart LR
     Draft["RST draft\n(written or AI-generated)"]
     Grammarly["Grammarly\nQuality Gate"]
     StyleGuide["Internal\nStyle Guide"]
     Approved["Clean draft\nready for peer review"]

     Draft --> Grammarly
     StyleGuide -.->|"Rules configured\nin Grammarly profile"| Grammarly
     Grammarly --> Approved

     subgraph Grammarly["Grammarly checks"]
       direction TB
       G1["Grammar &\nspelling"]
       G2["Passive voice\ndetection"]
       G3["Wordiness\n& clarity"]
       G4["Tone\nconsistency"]
       G5["Plagiarism\ncheck"]
     end

Feature Breakdown
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Feature
     - Plan required
     - How technical writers use it
   * - **Grammar & spelling**
     - Free
     - Catches typos and grammatical errors in RST prose blocks.
   * - **Clarity suggestions**
     - Premium
     - Flags overly complex sentences; suggests shorter alternatives.
   * - **Passive-voice detection**
     - Premium
     - Highlights passive constructions; prompts conversion to active voice.
   * - **Wordiness reduction**
     - Premium
     - Removes filler phrases (*"in order to"* → *"to"*).
   * - **Tone detector**
     - Premium
     - Flags tone as Formal / Neutral / Informal — useful for audience targeting.
   * - **Consistency check**
     - Business
     - Enforces custom word lists (e.g., "API key" not "api-key").
   * - **Style guide integration**
     - Business
     - Imports rules from APA, Chicago, AP, or a custom style guide.
   * - **Plagiarism detection**
     - Premium / Business
     - Ensures original phrasing — relevant when adapting vendor content.
   * - **Goals panel**
     - Free
     - Set audience, formality, domain, and intent before each review.

Maintaining the Documentation Tone of Voice
--------------------------------------------

Our documentation follows a **helpful, direct, and objective** style:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Principle
     - Example (before)
     - Example (after)
   * - **Active voice**
     - *"The token is refreshed by the SDK."*
     - *"The SDK refreshes the token."*
   * - **Concise language**
     - *"In order to be able to make use of the API…"*
     - *"To use the API…"*
   * - **Second person**
     - *"The developer should configure…"*
     - *"Configure the client with…"*
   * - **Present tense**
     - *"The function will return a list."*
     - *"The function returns a list."*
   * - **Specific over vague**
     - *"An error may occur."*
     - *"The request returns ``401`` if the token is missing."*

.. important::
   Grammarly is a **supplement**, not a replacement, for human review. It
   does not understand domain-specific jargon (e.g., ``idempotent``,
   ``TTL``, ``PKCE``) and may incorrectly flag technical terms as errors.
   Add your glossary terms to a custom dictionary in the Grammarly Business
   profile to suppress false positives.

Integration Patterns
--------------------

Browser Extension (Recommended for RST drafts in web editors)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Grammarly browser extension activates automatically in web-based
editors such as Confluence, Notion, and GitHub's PR description editor.

.. code-block:: text
   :caption: Supported browsers

   Chrome · Firefox · Safari · Edge

VS Code + Grammarly Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Docs-as-Code teams editing ``.rst`` files directly in VS Code, the
official Grammarly extension provides inline suggestions inside the editor.

.. code-block:: bash
   :caption: Install the VS Code extension via CLI

   code --install-extension znck.grammarly

After installing, add the following to :file:`.vscode/settings.json` to
enable Grammarly checks on RST files:

.. code-block:: json
   :caption: .vscode/settings.json

   {
     "grammarly.files.include": ["**/*.rst", "**/*.md", "**/*.txt"],
     "grammarly.files.exclude": ["**/build/**", "**/.venv/**"],
     "grammarly.config.documentDomain": "technical"
   }

.. tip::
   Set ``"grammarly.config.documentDomain": "technical"`` to reduce
   false positives on code-adjacent terminology in RST files.

Desktop App (Recommended for long-form reviews)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Paste full RST sections into the Grammarly desktop editor for a
comprehensive review before raising a PR. The Goals panel lets you
specify audience (expert), formality (formal), and domain (technical)
for each document type.

Grammarly API (CI integration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Grammarly Text Editor SDK can be embedded in custom internal tools
or documentation platforms to enforce quality rules programmatically.

.. code-block:: javascript
   :caption: Node.js — inline Grammarly check via Text Editor SDK

   import { GrammarlyEditorPlugin } from "@grammarly/editor-sdk";

   const plugin = await GrammarlyEditorPlugin.init("CLIENT_ID");
   plugin.addPlugin(document.querySelector("#doc-textarea"));

Recommended Documentation Workflow
------------------------------------

.. mermaid::

   sequenceDiagram
     participant TW   as Technical Writer
     participant VSC  as VS Code + Grammarly ext.
     participant GPT  as ChatGPT (optional)
     participant Git  as Git / GitHub PR
     participant Peer as Peer Reviewer

     TW->>VSC:   Write or paste RST draft
     VSC-->>TW:  Inline grammar / clarity suggestions
     TW->>TW:    Accept or reject suggestions
     TW->>GPT:   Optional — "Rewrite for tone consistency"
     GPT-->>TW:  Revised paragraph
     TW->>VSC:   Paste revised text → re-check
     TW->>Git:   Push RST to docs branch
     Git-->>Peer: PR notification
     Peer->>Git: Review + approve
     Git->>Git:  Merge → CI build → publish

.. list-table:: Workflow stage and Grammarly touchpoint
   :header-rows: 1
   :widths: 25 35 40

   * - Stage
     - Tool
     - What to check
   * - Live editing
     - VS Code extension
     - Grammar, spelling, passive voice inline.
   * - Pre-PR polish
     - Desktop App
     - Tone, wordiness, consistency — Goals panel active.
   * - PR description
     - Browser extension
     - Clarity of change summary for reviewers.
   * - Translated content
     - Desktop App (paste)
     - Verify fluency and preserved technical meaning.

AI Tools Comparison for Technical Writers
------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Capability
     - Grammarly
     - ChatGPT
     - Claude
   * - Grammar & spelling
     - ✅ Best-in-class
     - ⚠️ Adequate
     - ⚠️ Adequate
   * - Content generation
     - ❌ Not supported
     - ✅ Excellent
     - ✅ Excellent
   * - Code documentation
     - ❌ Not supported
     - ✅ Good
     - ✅ Excellent
   * - Style-guide enforcement
     - ✅ Custom rules
     - ⚠️ Prompt-dependent
     - ⚠️ Prompt-dependent
   * - Tone consistency
     - ✅ Tone detector
     - ⚠️ Inconsistent
     - ✅ Consistent
   * - IDE integration
     - ✅ VS Code plugin
     - ⚠️ Via Copilot chat
     - ✅ Claude Code (CLI)
   * - File / repo access
     - ❌ No
     - ❌ No (without plugins)
     - ✅ Yes (Cowork / Code)
   * - Pricing model
     - Freemium
     - Subscription / API
     - Subscription / API

.. seealso::

   * :doc:`chatgpt` — Content generation and prompt engineering for TW.
   * :doc:`claude` — Claude Cowork and Claude Code workflows.
   * :doc:`/books/literary_works` — Recommended books on technical style.
