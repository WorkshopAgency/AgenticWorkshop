# Pre-workshop email (send about a week before)

Subject: Agents workshop at the conference: 10 minutes of setup before you come

Dear participant,

Thank you for signing up for **Building and employing agents for data
analysis and visualization**. The session is 2 h 30 min of hands-on work on
your own laptop, so please do the setup below before you arrive. It takes
about 10 minutes.

1. **Windows only:** install WSL2 and do every step below inside the Ubuntu
   (WSL2) terminal.
2. **Install OpenCode 2.0.16**, the version the material was tested on:

   ```bash
   npm install -g @opencode/cli@2.0.16
   ```

   If you already have OpenCode v2, run `opencode upgrade 2.0.16` instead.
   Check with `opencode --version`.
3. **Install `uv`** (used in one exercise):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **Get the workshop material:**

   ```bash
   git clone -b dkb-2026 https://github.com/peterwadsackett/AgenticWorkshop.git
   cd AgenticWorkshop
   ```

   No Git? Download https://github.com/peterwadsackett/AgenticWorkshop/archive/refs/heads/dkb-2026.zip and unzip it.
5. **Run the setup check** from inside that folder:

   ```bash
   scripts/check-setup.sh
   ```

   Every line should show ✅. A ⚠️ about the DTU models is expected before the
   workshop day: they are switched on for the session.

You do not need a paid AI subscription. We provide models hosted at DTU, and
OpenCode offers free models. If you have a subscription (for example Claude
or ChatGPT), you may connect it, but it is not required.

Please bring your charger.

See you there,
Dimitrios S. Kanakoglou and Peter Wad Sackett
