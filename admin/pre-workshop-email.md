# Pre-workshop email (send about a week before)

Subject: Agents workshop: 10 minutes of setup before you come

Dear participant,

Thank you for signing up for **Building and employing agents for data
analysis and visualization**. The session is hands-on work on your own
laptop, so please do the setup below before you arrive. It takes
about 10 minutes.

1. **Install the dependencies** (OpenCode, Git, uv and Python 3.10 or later)
   by following step 1 of the Quick start, which has one block for macOS and
   one for Windows (WSL2) and Linux:
   https://github.com/WorkshopAgency/AgenticWorkshop#quick-start--install-download-and-open

   If you already have OpenCode v2, run `opencode upgrade`.

2. **Get the workshop material:**

   ```bash
   git clone https://github.com/WorkshopAgency/AgenticWorkshop.git
   cd AgenticWorkshop
   ```

   No Git? Download https://github.com/WorkshopAgency/AgenticWorkshop/archive/refs/heads/main.zip and unzip it.
3. **Run the setup check** from inside that folder:

   ```bash
   scripts/check-setup.sh
   ```

   Every line of the shared setup should show ✅. The workshop key and the
   plugins come at the start of the session.

Some exercises run notebooks inside OpenCode. The first one downloads Python
packages, up to about 400 MB; to fetch them at home instead, run this once:

```bash
uv run --no-project --with jupyter_client --with ipykernel --with pandas --with matplotlib python -c "print('ready')"
```

You do not need a paid AI subscription. The chat uses OpenCode's free
models, and we give you a key for two small models used in two exercises. If you have a subscription (for example Claude
or ChatGPT), you may connect it, but it is not required.

Please bring your charger.

See you there,
Dimitrios S. Kanakoglou and Peter Wad Sackett
