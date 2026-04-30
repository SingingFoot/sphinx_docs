.. SphinxDocs documentation master file
   Redesigned by Oleh Shynkarenko — Senior Technical Writer
   Showcasing Sphinx + reStructuredText mastery

.. raw:: html

   <style>
   /* ── Feature card grid ── */
   .feature-grid {
     display: grid;
     grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
     gap: 1.2rem;
     margin: 2rem 0;
   }
   .feature-card {
     background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
     border: 1px solid #0f3460;
     border-radius: 8px;
     padding: 1.4rem 1.6rem;
     color: #e0e0e0;
     transition: transform .2s ease, box-shadow .2s ease;
   }
   .feature-card:hover {
     transform: translateY(-4px);
     box-shadow: 0 8px 24px rgba(15,52,96,.55);
   }
   .feature-card .card-icon { font-size: 2rem; margin-bottom: .5rem; }
   .feature-card h3 { color: #4ecca3; margin: .3rem 0 .6rem; font-size: 1.05rem; }
   .feature-card p  { font-size: .88rem; line-height: 1.55; margin: 0; color: #b0b8c8; }

   /* ── Comparison table ── */
   .cmp-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: .9rem; }
   .cmp-table thead tr { background: #0f3460; color: #4ecca3; }
   .cmp-table th, .cmp-table td { padding: .75rem 1rem; border: 1px solid #2a3a5c; text-align: left; }
   .cmp-table tbody tr:nth-child(even) { background: #12192b; }
   .cmp-table tbody tr:hover { background: #1a2a45; }
   .badge { display: inline-block; padding: .15rem .55rem; border-radius: 12px; font-size: .78rem; font-weight: 600; }
   .badge-yes  { background: #1a4731; color: #4ecca3; }
   .badge-no   { background: #4a1a1a; color: #e06c75; }
   .badge-part { background: #3a3010; color: #e5c07b; }

   /* ── Directive anatomy block ── */
   .directive-anatomy {
     font-family: 'SFMono-Regular', Consolas, 'Courier New', monospace;
     background: #0d1117;
     border: 1px solid #30363d;
     border-radius: 6px;
     padding: 1.2rem 1.6rem;
     margin: 1.2rem 0;
     line-height: 1.9;
     font-size: .87rem;
   }
   .da-kw  { color: #ff79c6; }
   .da-name{ color: #8be9fd; }
   .da-opt { color: #f1fa8c; }
   .da-val { color: #50fa7b; }
   .da-arg { color: #ffb86c; }
   .da-body{ color: #e0e0e0; }
   .da-cmt { color: #6272a4; font-style: italic; }
   </style>

.. _home:

==========================================
Sphinx & reStructuredText Reference Portal
==========================================

.. rst-class:: lead

   A living demonstration of **Sphinx** capabilities and **reStructuredText** mastery —
   from directives and roles to extensions, theming, and Docs-as-Code automation.

   *Authored by* **Oleh Shynkarenko**, *Senior Technical Writer*

----

.. contents:: On This Page
   :depth: 2
   :local:
   :backlinks: none

----

Overview
--------

**Sphinx** is the industry-standard documentation engine for Python projects and increasingly
adopted across the wider software engineering world. Paired with **reStructuredText** (reST),
it provides a highly expressive, semantic markup language that compiles to HTML, PDF (via LaTeX),
ePub, man pages, and more — all from a single plain-text source tree.

.. note::

   reST predates Markdown and was designed specifically for *technical documentation*,
   with first-class support for cross-referencing, auto-generated indices, typed roles,
   and domain-specific markup that Markdown cannot match without heavy plugin ecosystems.

.. raw:: html

   <div class="feature-grid">
     <div class="feature-card">
       <div class="card-icon">📄</div>
       <h3>Semantic Markup</h3>
       <p>reST encodes <em>meaning</em>, not just appearance. Roles like
       <code>:py:class:</code>, <code>:ref:</code>, and <code>:term:</code>
       make content machine-readable and automatically cross-referenceable.</p>
     </div>
     <div class="feature-card">
       <div class="card-icon">🔌</div>
       <h3>Extension Ecosystem</h3>
       <p>Over 200 first- and third-party Sphinx extensions — autodoc, napoleon,
       mermaid, OpenAPI, nbsphinx — let you automate entire documentation
       pipelines from source code to published site.</p>
     </div>
     <div class="feature-card">
       <div class="card-icon">🔀</div>
       <h3>Multi-Format Output</h3>
       <p>Build HTML, PDF, ePub, man pages, and texinfo from the same source tree
       using Sphinx builders — no extra conversion tools required.</p>
     </div>
     <div class="feature-card">
       <div class="card-icon">⚙️</div>
       <h3>Docs-as-Code</h3>
       <p>Plain-text reST files live alongside code in Git. CI/CD pipelines
       (GitHub Actions, GitLab CI) build and publish docs automatically on
       every commit — no CMS needed.</p>
     </div>
   </div>

reST Syntax Quick Reference
---------------------------

Inline Roles
~~~~~~~~~~~~

reStructuredText expresses semantics through **roles** — inline markup prefixed with a colon.
Unlike Markdown's visual-only emphasis, reST roles carry *type information* that Sphinx uses
to generate a fully cross-referenced index:

.. code-block:: rst

   :strong:`bold text`           →  **bold text**
   :emphasis:`italic text`       →  *italic text*
   :code:`inline_code()`         →  inline_code()
   :command:`sphinx-build`       →  sphinx-build   (shell command)
   :file:`/path/to/file.py`      →  /path/to/file.py
   :guilabel:`OK`                →  OK             (UI label)
   :kbd:`Ctrl+Shift+P`           →  Ctrl+Shift+P   (keyboard shortcut)
   :menuselection:`File --> New`
   :doc:`sdk/getting_started`    →  link to another page in this project
   :ref:`home`                   →  link to a labelled anchor (any .rst file)
   :py:class:`MyClass`           →  cross-reference to a Python class
   :py:func:`my_module.helper`   →  cross-reference to a Python function
   :envvar:`SPHINX_BUILD_DIR`    →  an environment variable
   :rfc:`7519`                   →  link to RFC 7519 (JWT)
   :pep:`517`                    →  link to PEP 517

Admonitions
~~~~~~~~~~~

Sphinx ships with a full palette of admonitions for callouts and alerts:

.. code-block:: rst

   .. note::         General information worth highlighting
   .. tip::          A helpful hint or shortcut
   .. important::    Must-know information
   .. warning::      Potential issues the reader should watch for
   .. danger::       Destructive or irreversible consequences
   .. caution::      Proceed with care
   .. seealso::      Links to related topics
   .. deprecated::   x.y  Feature removed in version x.y
   .. versionadded:: x.y  Feature introduced in version x.y
   .. versionchanged:: x.y Behaviour changed in version x.y

.. tip::

   Combine admonitions with the ``.. only::`` directive to show different callouts
   per builder — for example, a PDF-specific warning that would not apply to HTML readers.

Section Heading Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~

reST headings are determined by underline (and optional overline) characters.
The Python documentation convention, adopted by most Sphinx projects, is:

.. code-block:: rst

   ########
   Part
   ########

   ========
   Chapter
   ========

   Section
   -------

   Subsection
   ~~~~~~~~~~

   Sub-subsection
   ^^^^^^^^^^^^^^

   Paragraph
   """""""""

.. important::

   The *character* used is not fixed by the spec — Sphinx assigns levels based on
   **first-occurrence order** within each file.  Consistency across a project is
   enforced by convention (or a linter such as ``rstcheck``), not the parser.

Directives Deep-Dive
--------------------

Anatomy of a Directive
~~~~~~~~~~~~~~~~~~~~~~~

Every Sphinx directive follows the same grammar. Understanding this structure is the key
to reading and writing any directive — including custom ones:

.. raw:: html

   <div class="directive-anatomy">
     <span class="da-cmt"># Anatomy of a reStructuredText directive</span><br>
     <br>
     <span class="da-kw">..</span> <span class="da-name">directive-name</span><span class="da-kw">::</span>
     <span class="da-arg">optional-argument</span><br>
     <span class="da-opt">&nbsp;&nbsp;&nbsp;:option-name:</span>
     <span class="da-val">option-value</span><br>
     <span class="da-opt">&nbsp;&nbsp;&nbsp;:another-option:</span>
     <span class="da-val">value</span><br>
     <span class="da-opt">&nbsp;&nbsp;&nbsp;:flag-option:</span>
     <span class="da-cmt">&nbsp; ← boolean flag, no value needed</span><br>
     <br>
     <span class="da-body">&nbsp;&nbsp;&nbsp;Body content — indented by 3 spaces (or 1 tab).</span><br>
     <span class="da-body">&nbsp;&nbsp;&nbsp;This is the directive's content block. It may contain</span><br>
     <span class="da-body">&nbsp;&nbsp;&nbsp;nested reST markup, including other directives.</span>
   </div>

Code Blocks
~~~~~~~~~~~

The ``.. code-block::`` directive supports syntax highlighting via **Pygments**, which
covers over 500 languages. Key options include ``:linenos:``, ``:emphasize-lines:``,
``:caption:``, and ``:dedent:``:

.. code-block:: python
   :caption: conf.py — Sphinx project configuration
   :linenos:
   :emphasize-lines: 3,4,5,6,7,8

   # conf.py
   project = "SphinxDocs"
   extensions = [
       "sphinx.ext.autodoc",       # Pull docstrings from Python source
       "sphinx.ext.napoleon",      # Google / NumPy docstring styles
       "sphinx.ext.viewcode",      # Add [source] links to API pages
       "sphinx.ext.intersphinx",   # Cross-project cross-references
       "sphinxcontrib.mermaid",    # Mermaid diagram support
       "sphinxcontrib.httpdomain", # HTTP API documentation
   ]
   html_theme = "sphinx_rtd_theme"
   html_static_path = ["_static"]
   html_logo = "_static/logo.png"
   html_favicon = "_static/favicon.ico"

.. code-block:: bash
   :caption: Sphinx build commands cheat-sheet

   # Build HTML output
   sphinx-build -b html source/ build/html

   # Build PDF via LaTeX
   sphinx-build -b latex source/ build/latex && make -C build/latex

   # Auto-rebuild on save with live reload (requires sphinx-autobuild)
   sphinx-autobuild source/ build/html --port 8080

   # Check for broken external links
   sphinx-build -b linkcheck source/ build/linkcheck

   # Rebuild cleanly (ignore cached environment)
   sphinx-build -E -b html source/ build/html

   # Treat warnings as errors (for CI pipelines)
   sphinx-build -W -b html source/ build/html

Includes and Substitutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

reST supports file includes and text substitutions — two powerful tools for maintaining
a *single source of truth* across large documentation sets:

.. code-block:: rst

   .. |product| replace:: SphinxDocs
   .. |version| replace:: 2.4.1

   The current version of |product| is |version|.

   .. include:: shared/warning_banner.rst

   .. literalinclude:: ../../src/my_module.py
      :language: python
      :lines: 10-35
      :caption: Source: my_module.py (lines 10–35)

Sphinx Extensions Comparison
------------------------------

.. raw:: html

   <table class="cmp-table">
     <thead>
       <tr>
         <th>Extension</th>
         <th>Purpose</th>
         <th>HTML</th>
         <th>PDF</th>
         <th>Complexity</th>
       </tr>
     </thead>
     <tbody>
       <tr>
         <td><code>sphinx.ext.autodoc</code></td>
         <td>Import &amp; render Python docstrings automatically</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td>Low</td>
       </tr>
       <tr>
         <td><code>sphinx.ext.napoleon</code></td>
         <td>Google / NumPy docstring styles</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td>Low</td>
       </tr>
       <tr>
         <td><code>sphinx.ext.viewcode</code></td>
         <td>Add [source] links to API documentation pages</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-no">✗ No</span></td>
         <td>Low</td>
       </tr>
       <tr>
         <td><code>sphinx.ext.intersphinx</code></td>
         <td>Cross-project cross-references (e.g., link to Python stdlib)</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td>Medium</td>
       </tr>
       <tr>
         <td><code>sphinxcontrib.mermaid</code></td>
         <td>Embed Mermaid diagrams as plain-text source</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-part">~ Partial</span></td>
         <td>Low</td>
       </tr>
       <tr>
         <td><code>sphinxcontrib.httpdomain</code></td>
         <td>Semantic markup for REST HTTP APIs</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td>Medium</td>
       </tr>
       <tr>
         <td><code>nbsphinx</code></td>
         <td>Embed Jupyter Notebooks with live output</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-part">~ Partial</span></td>
         <td>High</td>
       </tr>
       <tr>
         <td><code>sphinx_rtd_theme</code></td>
         <td>Read the Docs HTML theme</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-no">✗ No</span></td>
         <td>Low</td>
       </tr>
       <tr>
         <td><code>sphinx.ext.coverage</code></td>
         <td>Report which Python symbols lack documentation</td>
         <td><span class="badge badge-yes">✓ Yes</span></td>
         <td><span class="badge badge-no">✗ No</span></td>
         <td>Low</td>
       </tr>
     </tbody>
   </table>

Tables in reStructuredText
---------------------------

reST provides three table syntaxes. The ``.. list-table::`` directive is the most
maintainable for Docs-as-Code workflows because it does not require manual ASCII
alignment:

.. list-table:: reST Table Syntax Comparison
   :header-rows: 1
   :widths: 20 20 35 25
   :stub-columns: 1

   * - Syntax
     - Readability
     - Best for
     - Tooling support
   * - Grid table
     - Low (ASCII art)
     - Simple, narrow content
     - All editors; alignment tedious
   * - Simple table
     - Medium
     - Column-aligned numeric data
     - All editors; no multi-line cells
   * - ``list-table``
     - High
     - Complex / multi-line cell content
     - Excellent — no manual alignment
   * - ``csv-table``
     - High
     - Data sourced from external CSV files
     - Excellent — reads live ``.csv`` files

.. rubric:: Grid table example (ASCII art syntax)

.. code-block:: rst

   +------------------+------------+---------------------+
   | Header A         | Header B   | Header C            |
   +==================+============+=====================+
   | Row 1, Cell 1    | Cell 2     | Cell 3              |
   +------------------+------------+---------------------+
   | Row 2            | Cell 5     | Cell 6              |
   +------------------+------------+---------------------+

Diagrams as Code with Mermaid
-------------------------------

With ``sphinxcontrib-mermaid``, diagrams live in version control as plain text —
they are diff-able, reviewable, and never go stale because they live next to the
content they describe.

.. rubric:: Sphinx Build Pipeline

.. mermaid::

   flowchart LR
     A["Author writes .rst"] --> B{"sphinx-build"}
     B --> C["HTML output"]
     B --> D["PDF via LaTeX"]
     B --> E["ePub output"]
     C --> F["Read the Docs"]
     C --> G["GitHub Pages"]
     D --> H["Print / Download"]

.. rubric:: Docs-as-Code CI/CD Sequence

.. mermaid::

   sequenceDiagram
     participant Dev as Developer
     participant Git as Git / GitHub
     participant CI  as GitHub Actions
     participant RTD as Read the Docs

     Dev->>Git: git push
     Git->>CI: Trigger workflow
     CI->>CI: sphinx-build -W -b html
     CI->>CI: sphinx-build -b linkcheck
     CI->>RTD: Deploy on success
     RTD-->>Dev: Build notification

Autodoc: Python API Documentation
-----------------------------------

``sphinx.ext.autodoc`` pulls docstrings directly from Python source, keeping docs
and code in sync automatically. Combine it with ``napoleon`` to support Google-style
and NumPy-style docstrings:

.. code-block:: python
   :caption: src/auth.py — Python module with full Google-style docstring

   class TokenManager:
       """Manage API authentication tokens.

       Supports Bearer token, API-key, and OAuth 2.0 client-credentials flows.
       Tokens are cached in-memory and refreshed automatically before expiry.

       Args:
           base_url (str): Root URL of the target API.
           timeout (int): Request timeout in seconds. Defaults to ``30``.

       Raises:
           AuthError: When credentials are invalid or have expired.

       Example:
           >>> mgr = TokenManager("https://api.example.com")
           >>> mgr.authenticate(client_id="abc", client_secret="xyz")
           >>> mgr.get_token()
           'eyJhbGciOiJSUzI1NiIs...'
       """

       def authenticate(self, client_id: str, client_secret: str) -> None:
           """Exchange client credentials for an access token (OAuth 2.0).

           Args:
               client_id (str): OAuth 2.0 client identifier.
               client_secret (str): OAuth 2.0 client secret.
           """

.. code-block:: rst
   :caption: api/auth.rst — Rendering the class automatically with autodoc

   .. autoclass:: auth.TokenManager
      :members:
      :undoc-members:
      :show-inheritance:
      :special-members: __init__

HTTP API Documentation
-----------------------

The ``sphinxcontrib-httpdomain`` extension adds a semantic HTTP domain so REST
endpoints are documented with typed parameters, status codes, and request headers
that Sphinx can cross-reference and index:

.. code-block:: rst
   :caption: api/get_users.rst — Documenting a REST endpoint

   .. http:get:: /api/v1/users/{user_id}

      Retrieve a single user by their unique identifier.

      :param user_id: Unique UUID of the user record.
      :type  user_id: uuid

      :reqheader Authorization: ``Bearer <token>``
      :reqheader Accept:        ``application/json``

      :statuscode 200: User record returned successfully.
      :statuscode 401: Missing or invalid authentication token.
      :statuscode 404: User not found.

      **Example response:**

      .. code-block:: json

         {
           "id":         "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
           "name":       "Oleh Shynkarenko",
           "role":       "admin",
           "created_at": "2026-04-30T09:00:00Z"
         }

Docs-as-Code Workflow
----------------------

The following CI/CD workflow integrates Sphinx into a GitHub Actions pipeline —
building, link-checking, and deploying documentation automatically on every
merge to ``main``:

.. code-block:: yaml
   :caption: .github/workflows/docs.yml — Production-grade GitHub Actions pipeline
   :linenos:

   name: Build & Deploy Docs

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python 3.12
           uses: actions/setup-python@v5
           with:
             python-version: "3.12"

         - name: Install dependencies
           run: pip install -r requirements.txt

         - name: Build HTML (warnings = errors)
           run: sphinx-build -W -b html source/ build/html

         - name: Check for broken links
           run: sphinx-build -b linkcheck source/ build/linkcheck

         - name: Deploy to GitHub Pages
           if: github.ref == 'refs/heads/main'
           uses: peaceiris/actions-gh-pages@v4
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./build/html

Writing a Custom Sphinx Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom Python extensions unlock unlimited possibilities — from version badges to
glossary auto-generators. Every extension follows the same ``setup(app)`` contract:

.. code-block:: python
   :caption: _extensions/version_badge.py — Custom Sphinx directive

   from docutils import nodes
   from docutils.parsers.rst import Directive, directives


   class VersionBadge(Directive):
       """Renders a coloured version badge inline in HTML output."""

       required_arguments = 1
       option_spec = {"color": directives.unchanged}

       def run(self):
           version = self.arguments[0]
           color   = self.options.get("color", "#0f3460")
           html    = (
               f'<span class="badge" style="background:{color};'
               f'color:#fff;padding:.2rem .7rem;border-radius:12px;">'
               f'v{version}</span>'
           )
           return [nodes.raw("", html, format="html")]


   def setup(app):
       app.add_directive("version-badge", VersionBadge)
       return {"version": "0.1", "parallel_read_safe": True}

.. code-block:: rst
   :caption: Using the custom directive anywhere in the project

   .. version-badge:: 2.4.1
      :color: #4ecca3

----

.. seealso::

   * :doc:`sdk/getting_started` — Step-by-step SDK setup guide
   * :doc:`api/oauth` — OAuth 2.0 authentication flow
   * :doc:`diagrams/architecture` — System architecture diagrams
   * `Sphinx Documentation <https://www.sphinx-doc.org/>`_
   * `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
   * `Docutils Reference <https://docutils.sourceforge.io/rst.html>`_
   * `sphinxcontrib-httpdomain <https://sphinxcontrib-httpdomain.readthedocs.io/>`_
   * `Mermaid Diagram Syntax <https://mermaid.js.org/intro/>`_

.. toctree::
   :maxdepth: 2
   :caption: SDK Documentation
   :hidden:

   sdk/getting_started
   sdk/authentication
   sdk/api_endpoints

.. toctree::
   :maxdepth: 2
   :caption: API Documentation
   :hidden:

   api/about
   api/oauth
   api/get_users

.. toctree::
   :maxdepth: 2
   :caption: AI for TechWriters
   :hidden:

   ai/chatgpt
   ai/grammarly

.. toctree::
   :maxdepth: 2
   :caption: Diagrams and Charts
   :hidden:

   diagrams/architecture
   diagrams/flowcharts

.. toctree::
   :maxdepth: 2
   :caption: Books and Research
   :hidden:

   books/literary_works
   books/phd_research
