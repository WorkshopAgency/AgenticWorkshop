# Slides

Each deck here is a plain Markdown file. `---` on its own line starts a new
slide, which is also an ordinary horizontal rule — so **GitHub renders these
files as readable documents**, and [Marp](https://marp.app/) renders the same
file as a presentation. There is one source, not a document and a deck that
drift apart.

| File | Deck | Published |
|---|---|---|
| [`dkb2026.md`](dkb2026.md) | **Conference edition (dkb-2026 branch).** 14 slides: agenda, concepts, where data goes, one slide per module, agent suitability, limitations | Yes |
| [`unoriginalSlop.md`](unoriginalSlop.md) | Harnesses, skills, agents, MCP, plugins, model choices, the three README lessons and HALp, followed by exercise instructions and tips | Yes |
| [`semioriginalSlop.md`](semioriginalSlop.md) | Building and employing agents for data analysis. An earlier deck, kept for reference | No |
| [`originalSlop.md`](originalSlop.md) | Skills, agents and MCP. An earlier draft, kept for reference | No |
| [`themes/dtu.css`](themes/dtu.css) | The workshop theme. Not a deck | — |

Only `unoriginalSlop.md` is published, as HTML. Drafts are listed in `SKIP` in
[the workflow](../.github/workflows/slides.yml); add a name there to keep a
deck in the repository but off the site.

The revised deck is **15 slides**: 14 introductory and exercise slides,
followed by a thank-you slide. Further reading, project links and references
live in [additional.md](../additional.md) as an ordinary Markdown document,
outside this folder so the slide workflow does not turn it into a presentation.
The exercise READMEs retain the detailed instructions. Speaker notes contain
source references. The supplied MCP diagram lives in
`assets/mcp-overview.png`; the publishing workflow copies assets alongside
the HTML. Keep the filename unchanged
so the existing published link stays valid when the revision is approved.

## Reading it

Click the file. That is the whole procedure — GitHub shows it as a document.
Slide directives are HTML comments, so they do not appear.

## Presenting it

**In VS Code** — install the *Marp for VS Code* extension, open the file and
click the preview icon. Live preview, and export to PDF/PPTX/HTML from the
command palette. Nothing else to install.

**From the terminal** — no install needed beyond Node:

```bash
# live preview in a browser, reloads as you edit
npx @marp-team/marp-cli@4.5.1 -s slides --theme-set slides/themes

# one-off exports
npx @marp-team/marp-cli@4.5.1 slides/unoriginalSlop.md --theme-set slides/themes -o unoriginalSlop.html
npx @marp-team/marp-cli@4.5.1 slides/unoriginalSlop.md --theme-set slides/themes --pdf --allow-local-files
npx @marp-team/marp-cli@4.5.1 slides/unoriginalSlop.md --theme-set slides/themes --pptx
```

In the HTML deck: arrow keys to move, <kbd>F</kbd> for fullscreen,
<kbd>P</kbd> for presenter view with the speaker notes.

## Publishing it

[`.github/workflows/slides.yml`](../.github/workflows/slides.yml) builds each
published deck in this folder to HTML on every push to `main` and publishes it
to GitHub Pages. No PDF is produced; export one locally if you need it.

Pages is set to **Settings → Pages → Build and deployment → Source: GitHub
Actions.** If that is ever switched back to a branch, the deploy step fails.

## Writing a new deck

Copy the front matter and go:

```markdown
---
marp: true
theme: dtu
paginate: true
---

# First slide

---

## Second slide
```

Conventions used in the decks:

| You want | Write |
|---|---|
| A title slide | `<!-- _class: lead -->` as the slide's first line |
| A section divider | `<!-- _class: part -->` |
| A dark warning slide | `<!-- _class: warn -->` |
| A slide with a big table | `<!-- _class: tight -->` — drops the body size |
| Small grey aside text | `<span class="note">…</span>` |
| Speaker notes | Any other HTML comment. Hidden on GitHub, shown in presenter view |

`_class` with the leading underscore applies to that one slide. Without the
underscore it applies to that slide and every slide after it, which is almost
never what you want.

**Keep slides short.** Marp does not shrink text to fit; content taller than
the slide is simply clipped. Check the rendered output before presenting —
`npx @marp-team/marp-cli@4.5.1 slides/unoriginalSlop.md --theme-set slides/themes --pdf`
and page through it.
