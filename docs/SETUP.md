# Setup guide: please do this BEFORE the workshop

Allow about 45 minutes with a good internet connection. If you get stuck, come 30 minutes early on Friday and a facilitator will help.

## 1. Install the tools

| Tool | Download | Notes |
|---|---|---|
| **Python 3.12** (3.11 or newer is fine) | https://www.python.org/downloads/ | **Windows:** on the first installer screen, tick ✅ **"Add python.exe to PATH"** |
| **VS Code** | https://code.visualstudio.com/ | |
| **Git** | https://git-scm.com/downloads | Accept the default options |
| **GitHub account** | https://github.com/signup | Use an email you check. Your username will appear on your research profile, so choose a professional one |

### VS Code extensions
Open VS Code → Extensions (**Ctrl + Shift + X**) → install:
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **GitHub Copilot** *(optional)*: sign in with GitHub. The free plan is enough for the workshop.

### Tell Git who you are (once per computer)
Open a terminal (in VS Code: **Ctrl + `**) and run, with your own details:
```bash
git config --global user.name "Firstname Lastname"
git config --global user.email "the-email-you-used-for-github@example.com"
```

## 2. Get your own copy of the workshop repository

1. Open the workshop repository link (shared in your registration email / WhatsApp group).
2. Click the green **Use this template** button → **Create a new repository**. Give it a name, choose **Public** or **Private**, and click **Create**.
3. In VS Code: **Ctrl + Shift + P** → type **Git: Clone** → **Clone from GitHub** → sign in → pick your new repository.
4. ⚠️ **Choose a SHORT folder** such as `C:\Users\<you>\code` or `C:\research`. Windows has a 260-character path limit, and very deep folders cause installation errors.
5. Click **Open** when VS Code asks.

## 3. Create the project environment

In the VS Code terminal, inside the project folder:

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

When activated, your terminal prompt starts with `(.venv)`.

## 4. Test it

```bash
python scripts/make_sample_data.py
streamlit run app/streamlit_app.py
```
A browser tab should open with the app. Click **Train default model**. If you see the predictor, you are ready. 🎉
Press **Ctrl + C** in the terminal to stop the app.

Then open `notebooks/01_day1_clean_and_explore.ipynb`, click **Select Kernel** (top right) → **Python Environments** → **.venv**, and run the first code cell.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python is not recognized` | Python is not on PATH. Re-run the installer → **Modify** → tick "Add Python to environment variables", **or** use `py` instead of `python` |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer **Y**, then activate again |
| `The filename or extension is too long` during `pip install` | Move the project to a shorter folder (see step 2.4) |
| VS Code can't find the `.venv` kernel | **Ctrl + Shift + P** → **Python: Select Interpreter** → choose `.venv`. Then reload the window |
| `ModuleNotFoundError: No module named 'src'` | Open the **project folder** in VS Code (File → Open Folder), not just the notebook file |
| Git asks for a password | Use the browser sign-in window that pops up. GitHub no longer accepts account passwords on the command line |
| Slow or no internet | Ask a facilitator for the offline installers / package folder on the flash drive |
