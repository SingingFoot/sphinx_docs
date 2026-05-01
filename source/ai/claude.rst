.. _ai-claude:

Claude for Technical Writers
==============================

**Claude** is Anthropic's AI assistant, available in two purpose-built
forms for technical writers: **Claude Cowork** — a desktop tool for
non-developers to automate file and documentation workflows — and
**Claude Code** — a command-line agent for developers and advanced TW
practitioners who want Claude embedded directly in their terminal and
editor.

Together they cover the full TW spectrum: from polishing prose and
regenerating a page in Cowork to running a full Sphinx build, refactoring
50 RST files, or wiring up a CI/CD pipeline in Claude Code.

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Claude Products at a Glance
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Product
     - Best for
     - How to access
   * - **Claude.ai** (web / mobile)
     - Conversational drafting, research, quick reviews.
     - `claude.ai <https://claude.ai>`_
   * - **Claude Cowork**
     - File-level automation, folder management, PPTX/DOCX generation.
     - Claude desktop app → Cowork mode
   * - **Claude Code**
     - Terminal-based coding, Sphinx builds, multi-file refactors, CI.
     - ``npm install -g @anthropic-ai/claude-code`` then ``claude``

.. note::
   Both Cowork and Claude Code use the same underlying Claude models
   (Sonnet, Opus, Haiku). The difference is **access surface** —
   desktop GUI with file system access vs. terminal with shell execution.

----

Claude Cowork for Technical Writers
-------------------------------------

Claude Cowork gives technical writers a **natural-language interface to
their file system**. You describe what you want in plain English and
Claude reads, edits, creates, and organises files in the folder you select —
no command line required.

Cowork Capabilities for TW
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Task
     - What you say / type
   * - **Create a new RST page**
     - *"Create a new RST file called ``rate_limits.rst`` in the api folder
       with a full reference page covering headers, limits per plan, and a
       retry example."*
   * - **Improve an existing page**
     - *"Read ``oauth.rst`` and add a Mermaid sequence diagram showing the
       full token refresh flow, a scopes table, and curl examples."*
   * - **Bulk-refactor a folder**
     - *"Audit all RST files in the sdk/ folder and add a ``.. seealso::``
       block to each one linking to the related api/ pages."*
   * - **Generate a Word document**
     - *"Convert the api/about.rst content into a formatted .docx report
       with a cover page, table of contents, and branded heading styles."*
   * - **Create a presentation**
     - *"Build a 10-slide PowerPoint from our architecture.rst page for a
       stakeholder demo. Include diagrams and speaker notes."*
   * - **Audit for consistency**
     - *"Read every RST file in source/ and produce a table of all
       inconsistently used terms with a recommended canonical form."*
   * - **Update version numbers**
     - *"Find every occurrence of ``v1.1.0`` across all RST files and
       replace it with ``v1.2.0``."*
   * - **Build the Sphinx project**
     - *"Run sphinx-build and show me any warnings."*

Cowork Workflow: From Idea to Published Page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
     participant TW   as Technical Writer
     participant CW   as Claude Cowork
     participant FS   as File System\n(sphinx_docs/)
     participant Git  as Git / GitHub
     participant CI   as Sphinx CI Build

     TW->>CW:  "Add a new errors.rst to api/ with\nfull error code table and retry guidance"
     CW->>FS:  Read existing api/about.rst for context
     FS-->>CW: File contents
     CW->>FS:  Write api/errors.rst (new file)
     CW->>FS:  Edit index.rst → add api/errors to toctree
     CW-->>TW: "Done — errors.rst created and added to toctree"
     TW->>CW:  "Run sphinx-build and fix any warnings"
     CW->>FS:  Execute sphinx-build -W
     FS-->>CW: Build output (2 warnings)
     CW->>FS:  Fix 2 files → re-run build
     FS-->>CW: Build succeeded
     CW-->>TW: "Clean build — 0 warnings ✅"
     TW->>Git: Commit & push
     Git->>CI: Trigger publish pipeline

.. tip::
   Start every Cowork session by pointing it at your ``sphinx_docs/``
   folder. Claude reads the folder structure and ``conf.py`` automatically,
   giving it the context to make changes that are consistent with your
   existing project.

Cowork Use-Case Matrix
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Documentation task
     - Time without AI
     - Time with Cowork
     - Notes
   * - Write a new API reference page (500 words)
     - 2–3 hours
     - 15–30 min
     - TW reviews and validates; Claude drafts.
   * - Add Mermaid diagrams to 5 existing pages
     - 3–4 hours
     - 20–40 min
     - Cowork reads each page and inserts contextually correct diagrams.
   * - Bulk version-number update (50 files)
     - 30–60 min
     - 2–5 min
     - Find-and-replace with context awareness.
   * - Generate PPTX from RST source
     - 2–4 hours
     - 10–20 min
     - Uses the pptx skill for branded output.
   * - Terminology audit across a docset
     - 4–8 hours
     - 15–30 min
     - Returns a canonical-term table and suggested fixes.
   * - Convert RST pages to Word report
     - 1–2 hours
     - 5–10 min
     - Uses the docx skill with ToC and heading styles.

----

Claude Code for Technical Writers
-----------------------------------

**Claude Code** is a terminal-based AI agent. It reads your entire
repository, writes and edits files, runs shell commands, and integrates
with your editor (VS Code, JetBrains, Neovim). For technical writers
with developer backgrounds or those working closely with engineering teams,
Claude Code provides capabilities that go beyond file editing — including
running builds, running tests, and making large-scale, multi-file changes
with surgical precision.

Installing Claude Code
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :caption: Install Claude Code globally

   npm install -g @anthropic-ai/claude-code

.. code-block:: bash
   :caption: Launch Claude Code in your Sphinx project root

   cd sphinx_docs/
   claude

Claude Code understands your project on first launch by reading the
directory tree, ``conf.py``, and any ``CLAUDE.md`` file at the root.
Create a ``CLAUDE.md`` to give Claude project-specific context:

.. code-block:: markdown
   :caption: CLAUDE.md — project context for Claude Code

   # BlueRound Docs

   ## Project structure
   - source/api/      — REST API reference (sphinxcontrib-httpdomain)
   - source/sdk/      — SDK guides (Python, Node.js, Go, Java)
   - source/diagrams/ — Mermaid architecture diagrams
   - source/ai/       — AI tools for technical writers

   ## Style rules
   - Use list-table for all tables (never grid/simple tables)
   - All code blocks must have :caption: set
   - Every page needs a .. contents:: directive
   - Mermaid diagrams preferred over static images

   ## Build command
   sphinx-build -W -b html source/ build/html

Claude Code Capabilities for TW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Task
     - Example Claude Code command
   * - **Sphinx build + fix warnings**
     - *"Run sphinx-build and fix all warnings automatically."*
   * - **Multi-file refactor**
     - *"Add a :ref: label to every RST page that is missing one."*
   * - **Generate from code**
     - *"Read src/auth.py and generate a complete RST API reference page
       using sphinxcontrib-httpdomain markup."*
   * - **Cross-reference audit**
     - *"Find all :doc: and :ref: links across the docs and report any
       that point to non-existent targets."*
   * - **CI pipeline setup**
     - *"Create a GitHub Actions workflow that builds Sphinx with
       ``-W``, checks links, and deploys to GitHub Pages on merge to main."*
   * - **Diff-based docs update**
     - *"Read the git diff since the last tag and update CHANGELOG.rst and
       any API pages affected by the changes."*
   * - **Custom Sphinx extension**
     - *"Write a Sphinx extension that generates a :versionadded: tag
       automatically from the git blame date of each rst file."*

Claude Code Workflow: Terminal-Driven Docs-as-Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
     A(["TW opens terminal\nin sphinx_docs/"]) --> B["claude"]
     B --> C["Claude reads project:\nconf.py · index.rst · CLAUDE.md"]
     C --> D["TW: 'Audit all SDK pages and\nadd missing seealso blocks'"]
     D --> E["Claude reads sdk/*.rst\n(3 files)"]
     E --> F["Claude writes edits\nto 3 files"]
     F --> G["Claude runs sphinx-build -W"]
     G --> H{"Warnings?"}
     H -- Yes --> I["Claude self-corrects\nand rebuilds"]
     I --> H
     H -- No --> J["TW reviews diff\n(git diff)"]
     J --> K{"Approved?"}
     K -- No --> D
     K -- Yes --> L["git commit && git push"]
     L --> M(["CI pipeline publishes\ndocs ✅"])

Slash Commands for TW Productivity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Claude Code supports slash commands for common operations:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - What it does
   * - ``/init``
     - Scans the project and generates a ``CLAUDE.md`` with structure,
       conventions, and build commands.
   * - ``/review``
     - Reviews the current git diff or PR for content quality,
       broken cross-references, and style-guide compliance.
   * - ``/clear``
     - Resets Claude's context window (use when switching between
       unrelated tasks in the same session).

----

Cowork vs. Claude Code: Choosing the Right Tool
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 32 33

   * - Scenario
     - Use Cowork
     - Use Claude Code
   * - Writing a new RST page from scratch
     - ✅ Natural language request
     - ✅ ``claude`` in terminal
   * - Editing files with no coding background
     - ✅ GUI-first, no CLI needed
     - ❌ Requires terminal comfort
   * - Running ``sphinx-build`` after edits
     - ✅ Ask Cowork to run it
     - ✅ Native shell execution
   * - Creating PPTX / DOCX from RST
     - ✅ Built-in skills
     - ⚠️ Possible but manual
   * - Large multi-file refactor (20+ files)
     - ✅ With folder context
     - ✅ Superior — reads full repo
   * - Setting up GitHub Actions CI/CD
     - ⚠️ Can draft YAML files
     - ✅ Best — writes, tests, pushes
   * - Generating from source code (``autodoc``)
     - ⚠️ Needs code pasted in
     - ✅ Reads repo directly
   * - Integrating with VS Code / JetBrains
     - ❌ Desktop app only
     - ✅ Native IDE extension
   * - PR-based review workflow
     - ⚠️ Via file output
     - ✅ ``/review`` command

----

Prompt Library for Claude (TW Edition)
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Goal
     - Prompt
   * - **New RST page**
     - *"Create a new RST file ``source/api/webhooks.rst``. It should cover:
       event types (table), payload schema (JSON example), signature
       verification (code), and a Mermaid delivery-retry sequence diagram.
       Follow the style of the existing api/get_users.rst."*
   * - **Improve an existing page**
     - *"Read source/sdk/authentication.rst. Add: (1) a comparison table of
       all three auth methods, (2) curl examples for each, (3) a Mermaid
       OAuth2 flow diagram. Keep all existing content."*
   * - **Consistency audit**
     - *"Read every RST file in source/. List all pages that are missing:
       a .. contents:: directive, a :ref: label, or a .. seealso:: block.
       Then add the missing elements to each file."*
   * - **Build and validate**
     - *"Run sphinx-build -W -b html source/ build/html. If there are
       warnings, read the relevant files, fix all issues, and rebuild until
       the output is clean."*
   * - **Docs from PR diff**
     - *"Read the git diff: [PASTE DIFF]. Identify which API or SDK pages
       need updating. Draft the minimal changes required and apply them."*
   * - **Generate CI workflow**
     - *"Create .github/workflows/docs.yml that: installs dependencies,
       runs sphinx-build -W, runs linkcheck, and deploys to GitHub Pages
       on push to main. Use the project's existing requirements.txt."*

----

Best Practices
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Practice
     - Why it matters
   * - **Always maintain a CLAUDE.md**
     - Gives Claude project-specific style rules, file structure, and build
       commands so it makes consistent, context-aware edits across sessions.
   * - **Review every diff before committing**
     - Claude edits many files at once. Use ``git diff`` to verify changes
       match intent and no unrelated files were touched.
   * - **Use ``sphinx-build -W`` as the acceptance criterion**
     - Tell Claude *"The task is complete only when sphinx-build -W passes
       with zero warnings."* This drives self-correction loops.
   * - **Provide example pages as style anchors**
     - *"Follow the structure of api/oauth.rst"* gives Claude a concrete
       target to match rather than inferring style from scratch.
   * - **Iterate in small steps**
     - For large refactors, ask Claude to work one folder at a time and
       rebuild after each batch — easier to review and revert.
   * - **Validate technical accuracy yourself**
     - Claude can generate plausible but incorrect API behaviour. Always
       cross-check generated content against source code or test environments.

.. seealso::

   * :doc:`chatgpt` — Content generation and prompt engineering with ChatGPT.
   * :doc:`grammarly` — Prose quality and style-guide enforcement.
   * :doc:`/diagrams/flowcharts` — Docs-as-Code CI/CD pipeline flowchart.
   * :doc:`/sdk/getting_started` — SDK setup guide (example of AI-assisted doc output).
   * `Claude Code documentation <https://docs.anthropic.com/en/docs/claude-code>`_
   * `Anthropic documentation <https://docs.anthropic.com>`_
