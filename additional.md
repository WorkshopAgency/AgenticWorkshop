# Additional resources

Further reading and projects to explore after the workshop. These are resources to inspect, not endorsements or automatic installation instructions.

## Where to go after today

| Project | What to explore |
|---|---|
| [OpenCode](https://opencode.ai/) | The workshop harness: [v2 documentation](https://opencode.ai/v2/docs/) and [source code](https://github.com/anomalyco/opencode) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | A map of plugins, themes, agents and projects |
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | An alternative harness with integrated development tools |
| [OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl) | Planning and approval-based agent coordination |
| [python-expert-agent](https://github.com/amrahman90/python-expert-agent) | A compact, domain-specific agent package to inspect |

Read installation scripts and check compatibility before running them.
Popularity is not a security review.

## What is vLLM, and where does it fit?

**vLLM is an inference and serving engine.** It loads supported model weights
and performs the computation that generates responses. It can serve an
OpenAI-compatible API, so clients can request generations without loading the
model themselves. It is not a model, an agent definition or a chat interface.
See the [vLLM documentation](https://docs.vllm.ai/en/latest/) and
[repository](https://github.com/vllm-project/vllm).

In a remotely hosted setup, the roles are:

```text
OpenCode on your laptop → HTTPS endpoint → serving engine → model weights
         ↕
approved tools and project files on your laptop
```

The model proposes a tool call; the harness handles execution and approval.
Running the model remotely does not move your shell commands to that server.
Tool results included in subsequent requests can, however, reach the model server.

vLLM supports techniques such as continuous batching and efficient attention
cache management to serve multiple requests. That does not mean unlimited
concurrency: weights, active contexts and computation still share hardware.
Long inputs and long answers can reduce capacity for other users.

Our deployment commands and actual configured limits belong in
[admin.md](admin.md), not in students' setup instructions. You do not need to
install a serving engine to use the workshop endpoints.

### Other ways to run models

| Project | What it is | When to investigate |
|---|---|---|
| [vLLM](https://github.com/vllm-project/vllm) | Inference engine and API serving system | Shared model serving, batching and accelerator-based deployments |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | C/C++ inference with CPU and GPU backends, quantized models and a server | Local inference, GGUF models and hardware configurations with limited memory |
| [Ollama](https://github.com/ollama/ollama) | Model-running tools with a CLI and API | Getting started with model downloads and local model use; check whether the selected model is local or cloud-hosted |
| [SGLang](https://github.com/sgl-project/sglang) | Serving framework for language and multimodal models | Another option to benchmark for shared inference workloads |
| [Transformers](https://github.com/huggingface/transformers) | Python model library for inference and training across modalities | Research code that needs direct access to model loading and execution |

These are not interchangeable for every model. Check the exact model
architecture, quantization format, tool-call support, hardware and engine version.
An API labelled "OpenAI-compatible" does not guarantee identical parameters or
behaviour. Quantization reduces numerical precision to save resources; evaluate
its effect on your task instead of assuming unchanged quality.

## Scientific tools worth connecting to an agent

These are optional tools to explore, **not extra workshop requirements or
preinstalled OpenCode integrations**. A scientific library is not automatically
an MCP server: use a reviewed script, an appropriate integration, or a narrowly
scoped tool wrapper. Keep the computation inspectable.

| Tool | Why explore it | A useful agent task |
|---|---|---|
| [Mol*](https://github.com/molstar/molstar) | Web-based macromolecular visualization | Build an interactive structure view with explicit chain, ligand and representation choices; check these against the source structure |
| [napari](https://github.com/napari/napari) | Interactive multidimensional image viewing and annotation in Python | Prepare microscopy image layers and measurements for a human to inspect |
| [DuckDB](https://github.com/duckdb/duckdb) | Analytical SQL within a local process | Produce reproducible queries over research tables, with row counts and missing-value checks |

For visual tasks, request both the artifact and the code/settings that produced
it. A model generating a viewer or figure has not necessarily inspected the
rendered result. Image viewing and image understanding are different capabilities.

## When you want more control over coordination

[LangGraph](https://github.com/langchain-ai/langgraph) is a framework for
stateful agent workflows. Explore it if you want to express the flow in code,
with explicit state, persistence and human intervention, rather than relying
only on a coordinator's Markdown instructions. It is a separate development
choice, not an OpenCode plugin you need for Exercise 2.

A small experiment: implement the same audit → analysis → review task with
an OpenCode coordinator and with an explicit workflow. Compare recovery after
a failed step, evidence retained and how much human supervision each needs.
More agents are not automatically a better experiment.

### More agent-building repositories

| Project | What to look at | Keep in mind |
|---|---|---|
| [smolagents](https://github.com/huggingface/smolagents) | A compact Python library, including agents that generate code to perform actions | Generated code needs controlled execution; short implementations are not automatically safe |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Typed Python agents, tools and structured outputs | A validated output schema does not establish that the scientific content is correct |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful workflows and explicit coordination | Start with a small workflow and add branches only when the task needs them |

These are alternatives for writing your own applications, not additional
dependencies for the workshop's Markdown agents. Compare one bounded task
across frameworks before adopting an entire stack.

## Evaluating your own agent

[promptfoo](https://github.com/promptfoo/promptfoo) provides tooling for
testing and comparing prompts and AI applications. It is worth inspecting
when you want repeatable cases rather than a collection of impressive chats.
Check where each configured provider and test sends data before running it.

For a bioinformatics task, keep a small versioned set of public test cases:

- A normal input with independently calculated reference results.
- Missing values, inconsistent units and ambiguous identifiers.
- A deliberately unavailable tool or malformed input.
- A question the evidence cannot answer: does the agent admit that?

Record model and tool versions, settings, costs or runtime, outputs and manual
corrections. Repeat cases: a fixed temperature or seed is not a universal
guarantee of identical end-to-end agent behaviour. Test scientific correctness
separately from whether the code runs or the response has the right format.

## Finding MCP servers and plugins

Start with the [OpenCode MCP guide](https://opencode.ai/v2/docs/mcp-servers/)
and [plugin guide](https://opencode.ai/v2/docs/plugins/), then use
[awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)
as a discovery list, not a trust list. Our own [MCP notes](mcp/README.md)
describe the workshop's configured servers.

Before enabling something, check:

- What it can read, write or execute, and whether it sends data off your machine.
- Who maintains it, which version you are installing and whether it supports your OpenCode version.
- Whether the same task needs only a small script rather than another server.
- How you will verify its output and switch it off afterwards.

Do not paste unreviewed installation commands into an agent with unrestricted
shell access. An MCP connection standardises access; it does not certify a tool.

## Paper2Agent: papers as usable tools

Paper2Agent turns a paper and its associated code into an **MCP server**,
with tools an agent can use to run the paper's methods.

Its workflow executes and tests code rather than relying on a summary of
the manuscript alone. The paper includes collaborating agents that
prioritise a candidate causal gene for psoriasis.

**Why it matters:** a research contribution can become something others
interrogate and reuse. Computational prioritisation still needs biological validation.

[Miao et al., Nature, 16 September 2026](https://www.nature.com/articles/s41586-026-11044-y)

Thank you, Chiao-Yu, for pointing us to this!

## Multimodal agents: beyond text and tables

**Multimodal** means working across data types.
**Multi-agent** means dividing work across agents. A system can do both.

An illustrative research workflow:

1. Inspect microscopy images with an image-capable model or analysis tool.
2. Calculate measurements and relate them to sample metadata.
3. Produce a report that links each conclusion to its evidence.

Generating a plot does not mean the agent has visually inspected it.
Check which data types its model and tools actually support.

## Biomedical agents and their evaluation

**[Biomni](https://biomni.stanford.edu/)** brings biomedical tools and databases
into an agent environment for research tasks across biological domains.

**[BixBench](https://arxiv.org/abs/2503.00096)** evaluates agents on practical
biological analyses requiring multiple steps and interpretation.

Together, they suggest two research questions: what can we connect, and
how do we establish that the resulting system works?

**What evidence would convince you to use an agent's result in your research?**

## Three things to take away

1. **Separate instructions, execution and permissions.** Know what each
   component contributes and what it can access.

2. **Expose the tools the task needs.** Descriptions and results can consume
   context. The overhead depends on the harness and configuration.

3. **Validate the scientific result.** Successful execution does not establish
   correct methods, interpretation or reproducibility.

[github.com/WorkshopAgency/AgenticWorkshop_dbc2026](https://github.com/WorkshopAgency/AgenticWorkshop_dbc2026)

## References: research and further reading

- **Paper2Agent.** Miao et al. (2026). *Reimagining research papers as interactive and reliable AI agents.* Nature. [doi:10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y). [Earlier preprint](https://arxiv.org/abs/2509.06917).
- **Biomni.** *A General-Purpose Biomedical AI Agent.* [Research paper](https://doi.org/10.1101/2025.05.30.656746), [project and current publication links](https://biomni.stanford.edu/).
- **BixBench.** Mitchener et al. (2025). *A Comprehensive Benchmark for LLM-based Agents in Computational Biology.* [arXiv:2503.00096](https://arxiv.org/abs/2503.00096).
- **Protein Data Bank.** Berman et al. (2000). Nucleic Acids Research 28:235–242. [doi:10.1093/nar/28.1.235](https://doi.org/10.1093/nar/28.1.235).
- **The resolution revolution.** Kühlbrandt (2014). Science 343:1443–1444. Background for the cryo-EM discussion. [doi:10.1126/science.1251652](https://doi.org/10.1126/science.1251652).

## References: tools and security

- **OpenCode v2:** [overview](https://opencode.ai/v2/docs/) · [skills](https://opencode.ai/v2/docs/skills/) · [agents](https://opencode.ai/v2/docs/agents/) · [permissions](https://opencode.ai/v2/docs/permissions/).
- **OpenCode extensions:** [MCP servers](https://opencode.ai/v2/docs/mcp-servers/) · [plugins](https://opencode.ai/v2/docs/plugins/).
- **Model Context Protocol:** [documentation](https://modelcontextprotocol.io/docs/getting-started/intro).
- **OWASP:** [MCP Tool Poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning). Further reading on malicious instructions embedded in tool descriptions or responses.

Project links are on “Where to go after today”. Check current documentation,
installation scripts and data-handling terms before trying them.
