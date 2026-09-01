# STAT163 Week 1 — setup check

Verifies that Python, `uv` and pandas are installed and working before your first
practice session. **Not graded.** An automatic check marks your commits with a green ✓
or a red ✗.

## Steps

1. Click the green **Use this template** button → **Create a new repository**.
   Owner: your own GitHub account. Name: `week1-setup-check-<your-username>`.
   Visibility: **Public** is fine for this one (there is nothing personal in it beyond
   your name) — but Private also works.
2. Clone your new repository:
    ```
    git clone <your-repository-url>
    cd <repository-folder>
    ```
3. Install [`uv`](https://docs.astral.sh/uv/) if you do not have it:
    - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
4. Install the dependencies:
    ```
    uv sync
    ```
    `uv.lock` is already in the repository — it pins exact versions, so `uv sync`
    installs precisely those. Do not delete or edit it.
    On the university Wi-Fi, `uv sync` can fail with `operation timed out` — the
    fix is in [If `uv sync` fails with a timeout](#if-uv-sync-fails-with-a-timeout)
    below.
5. Open `check.ipynb`:
    - Jupyter Lab: `uv run jupyter lab`, then click `check.ipynb` in the file browser.
    - Positron: open the repository folder (File → Open Folder), then click `check.ipynb`.
6. In the first code cell, replace `_your name_` with your name.
7. Run every cell in order (`Shift+Enter`). Each must finish without errors.
8. Save the notebook, then commit and push:
    ```
    git add check.ipynb
    git commit -m "Setup check"
    git push
    ```
9. Refresh your repository page on GitHub. Within about a minute a green ✓ appears next
   to your commit if the automatic check passed. A red ✗ means something failed — click
   it to see the details, and bring the error message to your practice session.

## If `uv sync` fails with a timeout

The error looks like this:

```
× Failed to download `jupyterlab==4.6.3`
├─▶ Failed to fetch: `https://files.pythonhosted.org/packages/...`
╰─▶ operation timed out
```

The university Wi-Fi blocks a part of the PyPI file server
(`files.pythonhosted.org`). Your computer and your installation are fine.
The fix: use Cloudflare DNS (`1.1.1.1`). Cloudflare DNS returns server
addresses that the university firewall permits.

### Windows 11

1. Open **Settings → Network & internet → Wi-Fi → Hardware properties**.
2. Next to **DNS server assignment**, click **Edit**.
3. Select **Manual** and set the **IPv4** switch to **On**.
4. Enter `1.1.1.1` as **Preferred DNS** and `1.0.0.1` as **Alternate DNS**.
5. Click **Save**.
6. Run `uv sync` again.

### macOS

1. Open **System Settings → Wi-Fi**.
2. Click **Details…** next to the university network.
3. Open the **DNS** tab.
4. Click **+** and add `1.1.1.1`.
5. Add `1.0.0.1` the same way.
6. Click **OK**.
7. Run `uv sync` again.

### Linux

Set DNS to `1.1.1.1, 1.0.0.1` in your network settings (GNOME: **Settings →
Wi-Fi → gear icon → IPv4**). Reconnect to Wi-Fi, then run `uv sync` again.

If a university internal site stops working after this change, remove these
DNS servers again.

### If you cannot change DNS

Add one line to the hosts file, then run `uv sync` again.

- macOS / Linux:
  ```
  echo "151.101.0.223 files.pythonhosted.org" | sudo tee -a /etc/hosts
  ```
- Windows (PowerShell **as Administrator**):
  ```
  Add-Content C:\Windows\System32\drivers\etc\hosts "151.101.0.223 files.pythonhosted.org"
  ipconfig /flushdns
  ```

### Last resort

Connect through a phone hotspot and run `uv sync` one time. uv caches the
downloaded packages, so later commands need no new downloads.

This problem exists only on the university network. At home, `uv sync` works
without changes.

## What this check tests

- Python ≥ 3.10 and pandas ≥ 2.0 are installed and importable
- pandas can create and display a `DataFrame`
- The notebook records your OS, CPU architecture and Python version — saved in the
  repository as proof of completion and as diagnostic context that speeds up
  debugging
- Jupyter can execute the notebook top to bottom (the automatic check re-runs it and
  fails if any cell raises)
- **Every code cell was executed and saved.** The check requires saved output in each
  cell — that proves you ran the notebook on your own machine. A notebook committed
  without running (empty outputs) or with a saved error fails. Run every cell
  (`Shift+Enter`) **and save** before `commit`.
