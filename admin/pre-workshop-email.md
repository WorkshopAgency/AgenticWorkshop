# Pre-workshop email (send about a week before)

Subject: Agents workshop at the conference: 10 minutes of setup before you come

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

   If you already have OpenCode v2, run `opencode upgrade` instead. Check with
   `opencode --version`.
3. **Install `uv`** (used in Exercise 3 and in an optional extra):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **Get the workshop material:**

   ```bash
   git clone https://github.com/peterwadsackett/AgenticWorkshop.git
   cd AgenticWorkshop
   ```

   No Git? Download https://github.com/peterwadsackett/AgenticWorkshop/archive/refs/heads/main.zip and unzip it.
5. **Run the setup check** from inside that folder:

   ```bash
   scripts/check-setup.sh
   ```

   Every line should show ✅. A ⚠️ about the DTU models is expected before the
   workshop day: they are switched on for the session.

Optional: Exercise 1 ends with an extra in which you run a notebook inside
OpenCode. Its first run downloads about 400 MB of Python packages; to fetch
them at home instead, run this once:

```bash
uv run --no-project --with jupyter_client --with ipykernel --with pandas --with matplotlib python -c "print('ready')"
```

You do not need a paid AI subscription. We provide models hosted at DTU, and
OpenCode offers free models. If you have a subscription (for example Claude
or ChatGPT), you may connect it, but it is not required.

Please bring your charger.

See you there,
Dimitrios S. Kanakoglou and Peter Wad Sackett
