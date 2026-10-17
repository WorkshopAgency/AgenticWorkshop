# Pre-workshop email (send about a week before)

Subject: Agents workshop: 10 minutes of setup before you come

Dear participant,

Thank you for signing up for **Building and employing agents for data
analysis and visualization**. The session is 2 h 30 min of hands-on work on
your own laptop, so please do the setup below before you arrive. It takes
about 10 minutes.

1. **Windows only:** install WSL2 and do every step below inside the Ubuntu
   (WSL2) terminal.
2. **Install the latest OpenCode:**

   ```bash
   npm install -g @opencode/cli
   ```

   If you already have OpenCode v2, run `opencode upgrade` instead.
3. **Install `uv` and Python 3.10 or later** (uv starts the notebooks' Python
   and a database server in one exercise; Python runs the exercise scripts):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   If you have no Python, or one older than 3.10 (Macs come with 3.9; the
   setup check in step 5 tells you), run `uv python install 3.12 --default`
   and open a new terminal. If the setup check still reports the old Python,
   run `uv python update-shell` and open one more terminal.

4. **Get the workshop material:**

   ```bash
   git clone https://github.com/WorkshopAgency/AgenticWorkshop_dbc2026.git
   cd AgenticWorkshop
   ```

   No Git? Download https://github.com/WorkshopAgency/AgenticWorkshop_dbc2026/archive/refs/heads/main.zip and unzip it.
5. **Run the setup check** from inside that folder:

   ```bash
   scripts/check-setup.sh
   ```

   Every line should show ✅. A ⚠️ about the DTU models is expected beforehand:
   they are switched on for the session.

Some exercises run notebooks inside OpenCode. The first one downloads Python
packages, up to about 400 MB; to fetch them at home instead, run this once:

```bash
uv run --no-project --with jupyter_client --with ipykernel --with pandas --with matplotlib python -c "print('ready')"
```

You do not need a paid AI subscription. We provide models hosted at DTU, and
OpenCode offers free models. If you have a subscription (for example Claude
or ChatGPT), you may connect it, but it is not required.

Please bring your charger.

See you there,
Dimitrios S. Kanakoglou and Peter Wad Sackett
