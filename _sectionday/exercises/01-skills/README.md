# Preface to Skills Exercises
Create a skill through conversation, improve it after testing, and reuse it
on another input. The examples below use protein structures, but the same
process applies to other data-analysis tasks.

Open the extracted workshop folder in OpenCode. In the terminal, start
`opencode` from that folder. Keep your exercise files inside the project.

Select **Plan** mode to discuss the task
before implementation. Select **Build** mode when you are ready to create/manipulate files.
In Desktop, use the agent selector. Review requested file changes and shell
commands in either mode; planning is not a substitute for checking permissions.
Type `/` in the terminal interface to see the available commands.

The basic pattern is: **describe → discuss → build → test → improve**.
Ask for an explanation whenever a proposed step is unclear.
The exercise set is about creating and improving skills.

# Exercise 1a — Download a PDB file

Start in **Plan** mode with a simple request:

> Create a skill that downloads a pdb file

The more precise and detailed you frame your request, the better. While a conversation will likely
reveal ambiguities and lack of detail, then having a good starting point is valuable.
Think of the AI as a real assistant you need to explain a task to.

> Create a project skill called pdb-download that downloads a PDB file
> given its entry ID. Ask me about any choices we need to make before
> implementing it.

Discuss the download source, file format, destination, and what should happen
when an ID is invalid or a file already exists. The skill should work both
when you request it directly and when an agent needs it during another task.
You will see a lot of AI feedback and you can not simply ignore it, so read it carefully.

When the proposal is clear, switch to **Build** mode:

You can write "Build it", "Proceed", "Implement" or any words to that effect - or be more precise

> Implement the agreed pdb-download skill in
> .opencode/skills/pdb-download/SKILL.md. Keep supporting files in that
> skill's folder and ask before overwriting existing work.

The standard action after skill creation is to exit and reopen OpenCode, which makes it discover the new skill. Try it:

The simple

>Download pdb 4HHB

will successfully download the entry in the main workshop folder. If dissatisfied with that, be precise

> Use the pdb-download skill to download 4HHB into outputs/skills/pdb.

Inspect the saved file. A successful HTTP request alone does not tell you
whether the response is the expected structure file rather than an error page.
It is important to note that only **Build** allows for pdb downloading, as that is file manipulation.

Return to **Plan** and improve the skill:

> Review pdb-download. Propose checks that the downloaded file can be
> parsed, contains atomic coordinates, and corresponds to the requested
> entry. If the source publishes a checksum for that exact file, compare
> against it. Otherwise say that source-checksum verification is unavailable;
> do not invent a checksum. Explain the changes before implementing them.

Approve the changes in **Build**, then test again. Try a different valid ID
and an invalid input.<br>
You can also create a text file containing several IDs
and ask the skill to download those entries.

> Download the pdb entries mentioned in the file pdb_to_download.txt

**What to notice:** Useful checks emerge from discussing and testing the task.
A locally computed hash is a file fingerprint, not proof that it matches the
source. Keep unrelated tasks in separate skills rather than growing one skill
to cover everything.

# Exercise 1b — Download an existing structure image

Start another conversation in **Plan**:

> Create a project skill that downloads an existing rendered image of a
> PDB entry from its repository. This should retrieve an image, not render
> new atomic coordinates. Discuss the source, output format, and how to
> handle a missing image before building it.

Once you agree on the behavior, switch to **Build** and implement it. Try
4HHB, open the downloaded image, and check that it shows the requested entry.
Ask the skill to record the source URL and explain what view it retrieved.
Test how it handles an entry with no available image instead of silently
substituting another image.

**What to notice:** Downloading someone else's rendering and generating a
new rendering are different tasks. The skill description should make that clear.

# Exercise 1c — Locate and copy a skill

Open the skill files you created. Project and global locations are:

```text
<project>/.opencode/skills/<skill-name>/SKILL.md
~/.config/opencode/skills/<skill-name>/SKILL.md
```

Each skill has its own subfolder. The `SKILL.md` starts with a YAML header
containing `name` and `description`, followed by Markdown instructions.
The name should match its folder. Supporting scripts or references travel
with the folder; copying only `SKILL.md` can leave a skill incomplete.

Project skills belong to that project. Global skills are available across
your projects. Start locally for these exercises, and promote a skill to
the global location only when you want that wider availability.

In **Plan**, ask:

> Design a skill that copies an existing skill from this project into
> another project, or into my global skills folder when I explicitly ask.
> Copy the whole skill folder, preserve the original, and ask before
> overwriting a destination. Show me the source and destination first.

Review the proposal, build it, and test a copy in a second project. Check
that the original remains intact and that OpenCode discovers the copied skill.
Access outside the current project may require approval. Do not share embedded
credentials or private example data with a copied skill.

To request a skill unambiguously, say **"Use the pdb-download skill to…"**.
For a loading check, type `/skills` in the chat. It lists discovered skills,
but does not prove they work.

# Exercise 1d — Render a structure from coordinates

This time, create an image rather than downloading an existing one. In **Plan**:

> Create a project skill to render a protein backbone from the atomic
> coordinates in a PDB file. Discuss the rendering approach and dependencies
> with me before implementing it.

Discuss whether the output should be a static PNG or an interactive HTML
viewer. What would a molecular viewer provide? Would Python and Matplotlib
be sufficient? For a browser-based result, can it work with the software
already on your laptop? Do not approve an installation without understanding
why it is needed.

Build the agreed version and try it on the downloaded structure. Compare
with the repository image, accounting for different orientations, selected
chains, or assemblies. Check chain breaks, colors, labels, and whether the
backbone comes from the actual coordinates. For an interactive result, open
it and test the controls.

**What to notice:** producing an image is not the same as producing a useful
or scientifically faithful image. Improve the skill based on the problems
you can observe, then try another structure.

OpenCode reference: [skill locations and file format](https://opencode.ai/v2/docs/skills/),
and [Plan and Build agents](https://opencode.ai/v2/docs/agents/).

# Exercise 1e — A skill that helps make skills

Inspect [skill-builder](../../../.opencode/skills/skill-builder/SKILL.md).
It helps an agent clarify a skill's purpose, write useful instructions,
choose supporting files, and check the result. It is itself a skill, not
a separate agent or a newly trained model.

Example request in OpenCode **Plan** mode:

> Use skill-builder to review the skill I just created. Explain which
> instructions are useful, what is missing, and how we could test it.
> Propose changes before implementing them.

Finalize the improved skill in the usual way, if there is anything to improve.

# Exercise 1f — Make and test your own skill

Choose a small task you want to repeat. Use skill-builder to define its
inputs, outputs, and checks. Review the proposal before switching to Build
mode and authorizing implementation.

The skill belongs in `.opencode/skills/<skill-name>/SKILL.md`. Give each skill
its own subfolder. Add scripts, references, or assets only when they help.

Test one successful request, one invalid or incomplete input, and a different
valid input. Inspect the outputs yourself. Record what passed and what you
have not tested, then revise the skill in response to actual failures.

# Epilogue
Read the `SKILL.md` file with a text editor to see what the skill contains.
You can add/modify instructions directly yourself if you prefer to do it without the AI.
This can be done both at very simple and very complex levels.<br>
Source: [https://www.skillsdirectory.com/docs/skill-md-format](https://www.skillsdirectory.com/docs/skill-md-format)

Next: [Exercise 2 — Agents](../02-agents/README.md).
