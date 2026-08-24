# Class 02B Build Guide: Multi-Agent Workflows with ADK 2.x

This guide modernizes the supplied `class-02B.zip` starter package for ADK 2.x and builds the solution in small, testable stages. The instructions were compatibility-tested with ADK `2.6.0`:

1. Run the root agent as a single agent.
2. Add parent-to-sub-agent delegation.
3. Share information through session state.
4. Run a deterministic `SequentialAgent` pipeline.
5. Add a bounded `LoopAgent` for iterative improvement.
6. Add `ParallelAgent` branches and gather their results.

The final example produces a movie pitch by combining delegated routing, a sequential workflow, an iterative writers' room, two parallel preproduction branches, and a file-writing gather step.

## 1. Expand the starter ZIP

Place `class-02B.zip` in the directory where you want to work.

### macOS, Linux, or Cloud Shell

```bash
unzip class-02B.zip
cd class-02B
```

If you want a fresh destination directory:

```bash
mkdir class-02B-work
unzip class-02B.zip -d class-02B-work
cd class-02B-work/class-02B
```

### Windows PowerShell

```powershell
Expand-Archive -Path .\class-02B.zip -DestinationPath .
Set-Location .\class-02B
```

Confirm that the package expanded correctly:

```bash
find . -maxdepth 4 -type f | sort
```

Expected structure:

```text
class-02B/
├── adk_multiagent_systems/
│   ├── callback_logging.py
│   ├── parent_and_subagents/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── requirements.txt
│   └── workflow_agents/
│       ├── __init__.py
│       └── agent.py
└── adk_utils/
    ├── __init__.py
    └── plugins.py
```

## 2. Create an isolated ADK 2.x environment

Use a class-local virtual environment so another globally installed ADK version does not change the exercise. This guide pins ADK `2.6.0`, the current ADK 2.x version used for validation.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
PIP_CACHE_DIR=.pip-cache python -m pip install "google-adk[gcp]==2.6.0" \
  -r adk_multiagent_systems/requirements.txt
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

Verify the tools:

```bash
python --version
adk --version
python -c "import importlib.metadata; print('google-adk', importlib.metadata.version('google-adk'))"
```

Expected ADK result:

```text
google-adk 2.6.0
```

The `[gcp]` extra supplies the Google Cloud packages used by the starter's logging and Vertex AI path. If pip reports a read-only cache error, keep `PIP_CACHE_DIR=.pip-cache` in the command as shown.

## 3. Apply the ADK 2.x compatibility updates

The starter was originally written for ADK 1.x. Its core agent definitions, session state, `SequentialAgent`, `LoopAgent`, and `ParallelAgent` remain valid in ADK 2.x. Update the following integration points before running it.

### 3.1 Update the `App` import

In both files:

- `adk_multiagent_systems/parent_and_subagents/agent.py`
- `adk_multiagent_systems/workflow_agents/agent.py`

replace:

```python
from google.adk.apps.app import App
```

with:

```python
from google.adk.apps import App
```

The old path remains an alias in ADK 2.6.0, but the new import is the documented public route.

### 3.2 Update the LangChain integration import

In `adk_multiagent_systems/workflow_agents/agent.py`, replace:

```python
from google.adk.tools.langchain_tool import LangchainTool
```

with:

```python
from google.adk.integrations.langchain import LangchainTool
```

The old import emits a deprecation warning in ADK 2.6.0.

### 3.3 Update the plugin error hook

In `adk_utils/plugins.py`, replace the old `on_model_error` method with ADK 2.x's `on_model_error_callback` hook:

```python
async def on_model_error_callback(
    self,
    *,
    callback_context,
    llm_request,
    error: Exception,
) -> LlmResponse | None:
    """Return a controlled fallback when the model reports quota exhaustion."""
    if "RESOURCE_EXHAUSTED" in str(error) or "429" in str(error):
        print(
            "\n[PLUGIN TRIGGERED] "
            f"Caught 429 error. Returning fallback for {self.name}."
        )
        fallback = self._get_fallback_text(llm_request)
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part.from_text(text=fallback)],
            )
        )
    return None
```

ADK 2.x calls this method with `callback_context`, `llm_request`, and `error`. The previous `on_model_error(agent, model, input, error)` method is not an ADK 2.x plugin hook.

### 3.4 Remove the internal model monkey patch

In both agent files, remove:

```python
graceful_plugin.apply_429_interceptor(root_agent)
```

Keep the plugin registered on the application:

```python
app = App(
    name="parent_and_subagents",  # workflow_agents in the other file
    root_agent=root_agent,
    plugins=[graceful_plugin],
)
```

The application-level ADK 2.x plugin hook now handles the error. Monkey-patching `Gemini.generate_content_async` couples the code to model internals and is unnecessary.

### 3.5 What remains unchanged

These constructs continue to work in ADK 2.x:

```python
from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.models import Gemini
from google.adk.tools import exit_loop
```

The `Agent(..., sub_agents=[...])`, state templating, `ToolContext`, `output_key`, `max_iterations`, callbacks, and workflow-agent composition used in this class remain available.

## 4. Choose one `.env` authentication mode

Create the active `.env` inside `adk_multiagent_systems/parent_and_subagents/`, then copy it to `workflow_agents/`.

Do not combine the two modes in one active file.

### Option A: Vertex AI

Create `adk_multiagent_systems/parent_and_subagents/.env` with:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-2.5-flash
```

Authenticate and select the project:

```bash
gcloud auth application-default login
gcloud config set project your-google-cloud-project-id
gcloud services enable aiplatform.googleapis.com logging.googleapis.com
```

In a managed Cloud Shell lab, the temporary student credentials may already supply the required Google Cloud authentication. Use the lab project, not a personal project.

### Option B: Gemini API key

Create `adk_multiagent_systems/parent_and_subagents/.env` with:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=replace_with_your_google_ai_studio_key
MODEL=gemini-2.5-flash
```

Do not add a real key to Git. Make sure `.gitignore` includes:

```gitignore
.env
*.env
```

### Copy the selected configuration to both agents

```bash
cp adk_multiagent_systems/parent_and_subagents/.env \
   adk_multiagent_systems/workflow_agents/.env
```

Check the mode without printing the API key:

```bash
python - <<'PY'
from pathlib import Path
from dotenv import dotenv_values

for path in [
    Path("adk_multiagent_systems/parent_and_subagents/.env"),
    Path("adk_multiagent_systems/workflow_agents/.env"),
]:
    values = dotenv_values(path)
    print(path)
    print("  vertex:", values.get("GOOGLE_GENAI_USE_VERTEXAI"))
    print("  model:", values.get("MODEL"))
    print("  api key present:", bool(values.get("GOOGLE_API_KEY")))
PY
```

## 5. Make logging work in both authentication modes

Both starter `agent.py` files create a Google Cloud Logging client immediately. That works in Cloud Shell or with Application Default Credentials, but an API-key-only laptop may raise `DefaultCredentialsError` before the agent starts.

In both files:

- `adk_multiagent_systems/parent_and_subagents/agent.py`
- `adk_multiagent_systems/workflow_agents/agent.py`

replace:

```python
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
```

with:

```python
use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"

if use_vertex:
    try:
        cloud_logging_client = google.cloud.logging.Client()
        cloud_logging_client.setup_logging()
    except Exception as exc:
        logging.basicConfig(level=logging.INFO)
        logging.warning("Cloud Logging unavailable; using local logging: %s", exc)
else:
    logging.basicConfig(level=logging.INFO)
```

Important: in `workflow_agents/agent.py`, move `load_dotenv()` above this block so `use_vertex` reads the `.env` file before deciding which logging route to use.

Recommended order:

```python
load_dotenv()

use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
if use_vertex:
    try:
        cloud_logging_client = google.cloud.logging.Client()
        cloud_logging_client.setup_logging()
    except Exception as exc:
        logging.basicConfig(level=logging.INFO)
        logging.warning("Cloud Logging unavailable; using local logging: %s", exc)
else:
    logging.basicConfig(level=logging.INFO)
```

## 6. Validate the ADK 2.x imports before the first run

From the expanded `class-02B` directory, run:

```bash
source .venv/bin/activate
cd adk_multiagent_systems

python - <<'PY'
import importlib.metadata
from parent_and_subagents.agent import app as travel_app
from workflow_agents.agent import app as workflow_app
from adk_utils.plugins import Graceful429Plugin

print("ADK:", importlib.metadata.version("google-adk"))
print("Travel app:", travel_app.name)
print("Workflow app:", workflow_app.name)
print(
    "ADK 2 error hook:",
    callable(getattr(Graceful429Plugin, "on_model_error_callback", None)),
)
PY
```

Expected result:

```text
ADK: 2.6.0
Travel app: parent_and_subagents
Workflow app: workflow_agents
ADK 2 error hook: True
```

This validates imports and application construction without making a model request.

## 7. Milestone 1: Run the root as a single agent

The starter defines specialist objects, but the `root_agent` does not yet list them as sub-agents. Therefore ADK begins with only the `steering` root in the active topology.

From the directory that contains the two agent folders:

```bash
cd adk_multiagent_systems
adk run parent_and_subagents
```

At the prompt, enter:

```text
hello
```

Expected result: the `steering` agent asks whether you already know where you want to travel or need help deciding.

Exit:

```text
exit
```

Checkpoint: the environment, model, package import, and `root_agent` discovery all work before multi-agent routing is introduced.

## 8. Milestone 2: Add parent and sub-agents

Open:

```text
adk_multiagent_systems/parent_and_subagents/agent.py
```

In `root_agent`, add:

```python
sub_agents=[travel_brainstormer, attractions_planner],
```

The completed root definition should look like:

```python
root_agent = Agent(
    name="steering",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    description="Start a user on a travel adventure.",
    instruction="""
        Ask the user if they know where they'd like to travel
        or if they need some help deciding.

        If they need help deciding, send them to travel_brainstormer.
        If they know which country they want, send them to attractions_planner.
        """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    sub_agents=[travel_brainstormer, attractions_planner],
)
```

Run it again:

```bash
adk run parent_and_subagents
```

Test the first route:

```text
hello
I do not know where to go. I want adventure and great food.
```

Expected: control transfers from `[steering]` to `[travel_brainstormer]`.

Start a new run and test the other route:

```text
hello
I know where I want to go: Egypt.
```

Expected: control transfers to `[attractions_planner]`.

Then test peer transfer:

```text
Actually, I do not know which country to choose.
```

Expected: the conversation can move from `attractions_planner` to its peer `travel_brainstormer`.

Checkpoint: the parent uses the specialists' names, descriptions, and instructions to route the conversation.

## 9. Milestone 3: Add shared session state

Under the `# Tools` heading in `parent_and_subagents/agent.py`, add:

```python
def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: List[str],
) -> dict[str, str]:
    """Save selected attractions in session state."""
    existing_attractions = tool_context.state.get("attractions", [])
    tool_context.state["attractions"] = existing_attractions + attractions
    return {"status": "success"}
```

Add the tool to `attractions_planner`:

```python
tools=[save_attractions_to_state],
```

Expand its instruction:

```python
instruction="""
    - Provide the user options for attractions to visit within their selected country.
    - When they reply, use your tool to save their selected attraction and then
      provide more possible attractions.
    - If they ask to view the list, provide a bulleted list of { attractions? }
      and then suggest some more.
    """,
```

Start the development UI from `adk_multiagent_systems/`:

```bash
adk web --port 8000
```

For Cloud Shell, use:

```bash
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```

Open `http://127.0.0.1:8000`, select `parent_and_subagents`, and test:

```text
hello
I would like to go to Egypt.
I will go to the Sphinx.
I will also visit the Egyptian Museum.
What is on my list?
```

Inspect:

1. The agent name on each response.
2. The tool-call event.
3. The event's `state_delta`.
4. The State tab's `attractions` list.

Checkpoint: the tool writes durable session state and the instruction reads it through `{ attractions? }`.

## 10. Milestone 4: Run the starter sequential workflow

Stop ADK Web with `Ctrl+C`, then review:

```text
adk_multiagent_systems/workflow_agents/agent.py
```

The starter already contains:

```python
film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[researcher, screenwriter, file_writer],
)
```

The order is fixed:

```text
researcher -> screenwriter -> file_writer
```

Run the Dev UI again:

```bash
adk web --port 8000
```

Select `workflow_agents` and enter:

```text
hello
Ada Lovelace
```

Expected execution:

1. `greeter` stores the subject in `PROMPT` and transfers to the workflow.
2. `researcher` calls Wikipedia and appends to `research`.
3. `screenwriter` appends the logline and outline to `PLOT_OUTLINE`.
4. `file_writer` saves a text file under `adk_multiagent_systems/movie_pitches/`.

Inspect the result:

```bash
find movie_pitches -maxdepth 1 -type f -print
```

Checkpoint: all three sub-agents execute in list order without waiting for another user message.

## 11. Milestone 5: Add a bounded writers' room loop

At the imports in `workflow_agents/agent.py`, add:

```python
from google.adk.tools import exit_loop
```

Add this critic after the existing `researcher` definition:

```python
critic = Agent(
    name="critic",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Reviews the outline so that it can be improved.",
    instruction="""
    INSTRUCTIONS:
    Consider these questions about the PLOT_OUTLINE:
    - Does it have a satisfying three-act cinematic structure?
    - Are the characters' struggles engaging?
    - Does it feel grounded in a real historical period?
    - Does it incorporate useful historical details from the RESEARCH?

    If the PLOT_OUTLINE does a good job, call the exit_loop tool.
    If significant improvements are possible, use append_to_state to add
    your feedback to CRITICAL_FEEDBACK.

    Explain your decision briefly.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state, exit_loop],
)
```

Create the loop before `film_concept_team`:

```python
writers_room = LoopAgent(
    name="writers_room",
    description="Iterates through research and writing to improve a movie plot outline.",
    sub_agents=[researcher, screenwriter, critic],
    max_iterations=5,
)
```

Replace the sequential workflow's sub-agent list:

```python
film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[writers_room, file_writer],
)
```

In ADK Web, click **New session** and test:

```text
hello
An ancient doctor whose discoveries changed medicine
```

Inspect the events. You should see repeated passes through:

```text
researcher -> screenwriter -> critic
```

The loop ends when `critic` calls `exit_loop` or after five iterations. Then the outer sequence advances to `file_writer`.

Checkpoint: the loop has both a semantic quality gate and a hard safety cap.

## 12. Milestone 6: Add parallel branches

Add these two specialists and the parallel team before `film_concept_team`:

```python
box_office_researcher = Agent(
    name="box_office_researcher",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Considers the box office potential of this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Write a concise report on the box office potential of this movie.
    Compare its premise with the reported performance and audience appeal
    of relevant recent films. State assumptions clearly.
    """,
    output_key="box_office_report",
)

casting_agent = Agent(
    name="casting_agent",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Generates casting ideas for this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Suggest casting ideas for the important characters in PLOT_OUTLINE.
    Explain the fit based on comparable roles and screen presence.
    Treat all suggestions as creative options, not commitments.
    """,
    output_key="casting_report",
)

preproduction_team = ParallelAgent(
    name="preproduction_team",
    sub_agents=[box_office_researcher, casting_agent],
)
```

Update the outer sequence:

```python
film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[writers_room, preproduction_team, file_writer],
)
```

Why this is safe to parallelize:

- Both branches read `PLOT_OUTLINE`.
- Neither branch needs the other branch's result.
- Each writes to a different state key.
- The downstream file writer performs the gather.

## 13. Update the gather step

Replace `file_writer`'s instruction with:

```python
instruction="""
INSTRUCTIONS:
- Create a marketable, contemporary title for the movie in PLOT_OUTLINE.
- Use write_file to create a new text file.
- Write it to the movie_pitches directory.
- Use the movie title as the filename.
- Include:
  - The logline and PLOT_OUTLINE
  - The BOX_OFFICE_REPORT
  - The CASTING_REPORT

PLOT_OUTLINE:
{ PLOT_OUTLINE? }

BOX_OFFICE_REPORT:
{ box_office_report? }

CASTING_REPORT:
{ casting_report? }
""",
```

The final topology is:

```text
greeter
  -> film_concept_team: SequentialAgent
       -> writers_room: LoopAgent
            -> researcher
            -> screenwriter
            -> critic
       -> preproduction_team: ParallelAgent
            -> box_office_researcher
            -> casting_agent
       -> file_writer
```

## 14. Run the completed solution

From `adk_multiagent_systems/`:

```bash
adk web --port 8000
```

Select `workflow_agents`, start a new session, and enter:

```text
hello
Hedy Lamarr and her contribution to wireless communication
```

Expected evidence:

1. `greeter` records `PROMPT` and transfers into the workflow.
2. The writers' room makes one or more passes.
3. The critic either adds `CRITICAL_FEEDBACK` or exits the loop.
4. Box-office and casting branches run after the loop.
5. State contains `box_office_report` and `casting_report`.
6. `file_writer` creates one combined pitch file.

Inspect the final file:

```bash
find movie_pitches -maxdepth 1 -type f -print
```

Open the newest file and verify that it contains:

- A title
- A logline
- A plot outline
- A box-office report
- A casting report

## 15. Quick validation checklist

- [ ] ADK reports version `2.6.0`.
- [ ] Both applications pass the import-validation script.
- [ ] The custom plugin exposes `on_model_error_callback`.
- [ ] No `google.adk.tools.langchain_tool` deprecation warning appears.
- [ ] Only one authentication mode is active.
- [ ] Both agent directories contain a `.env` file.
- [ ] API-key mode starts without Google Cloud ADC.
- [ ] Vertex AI mode uses the intended project and location.
- [ ] The single root agent runs before adding sub-agents.
- [ ] Both travel delegation routes are observed.
- [ ] `attractions` appears in session state.
- [ ] The sequential workflow executes in fixed order.
- [ ] The loop exits on quality or at `max_iterations`.
- [ ] Parallel branches use distinct `output_key` values.
- [ ] The file writer gathers all three final content sections.
- [ ] A pitch file appears under `movie_pitches/`.

## 16. Troubleshooting

### `ModuleNotFoundError: No module named 'google.adk'`

Activate the class virtual environment and reinstall:

```bash
source .venv/bin/activate
PIP_CACHE_DIR=.pip-cache python -m pip install "google-adk[gcp]==2.6.0" \
  -r adk_multiagent_systems/requirements.txt
```

### `DefaultCredentialsError`

- Vertex AI mode: run `gcloud auth application-default login` and confirm the project.
- API-key mode: confirm the logging fallback in Section 5 is present and `GOOGLE_GENAI_USE_VERTEXAI=FALSE`.

### `AttributeError` or the 429 fallback never runs

Confirm the plugin method is named:

```python
on_model_error_callback
```

and remove both calls to:

```python
graceful_plugin.apply_429_interceptor(root_agent)
```

### LangChain import deprecation warning

Use:

```python
from google.adk.integrations.langchain import LangchainTool
```

not the older `google.adk.tools.langchain_tool` path.

### `404 NOT_FOUND` for the model

The model identifier may not be available in the selected backend or location. Confirm the exact model offered by your lab or account, then update only `MODEL` in both `.env` files.

### `429 RESOURCE_EXHAUSTED`

The supplied `Graceful429Plugin` should return a controlled fallback for intercepted quota failures. Also verify quota, billing or lab limits, and reduce repeated test runs.

### ADK Web does not show the agents

Start `adk web` from the parent directory containing both agent folders:

```bash
cd class-02B/adk_multiagent_systems
adk web --port 8000
```

### No output file appears

Run ADK from `adk_multiagent_systems/` and inspect terminal logs for the `write_file` tool call. The relative output directory should be:

```text
adk_multiagent_systems/movie_pitches/
```

### The loop consumes too much time or quota

Reduce the hard cap temporarily:

```python
max_iterations=2
```

Restore the intended cap after the workflow is stable.

## 17. Instructor demonstration order

1. Show the root agent alone and ask students what it cannot do.
2. Add `sub_agents` and visibly trigger each routing path.
3. Save two attractions and inspect `state_delta` plus the State tab.
4. Run the three-step sequential movie workflow.
5. Add the critic and show at least one improvement cycle.
6. Add the two parallel branches and point out their separate state keys.
7. Open the final pitch file and map each section back to the agent that produced it.

## Sources

- Supplied starter package: `class-02B.zip`
- Supplied reference: `Build Multi-Agent Systems with ADK | Google Skills.pdf`
- Google ADK documentation: <https://google.github.io/adk-docs/>
- Sequential workflow: <https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/>
- Loop workflow: <https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/>
- Parallel workflow: <https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/>
- State: <https://google.github.io/adk-docs/sessions/state/>
- Development UI: <https://google.github.io/adk-docs/runtime/web-interface/>
- ADK 2.0 overview and migration notes: <https://google.github.io/adk-docs/2.0/>

> ADK 2.x note: graph-based and dynamic workflows are the forward-looking orchestration model. This class deliberately retains `SequentialAgent`, `LoopAgent`, and `ParallelAgent` because they remain supported, make the three core control patterns explicit, and provide a clear bridge into graph workflows.
