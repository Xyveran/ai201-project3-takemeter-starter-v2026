# Running TakeMeter

Everything about how the starter works.

This pair is different from the last two: **you train a model.** It runs on
your own machine, in a notebook, from inside this repo. No accounts, no keys,
nothing hosted.

---

## Before your first class

One setup, one virtual environment, everything in this repo. The
[environment setup page](../pages/ide_setup) has the per-operating-system
commands.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**`python test.py` passing is what you need before your first session.** It
checks your Python version against the pins, your disk, your memory, and
whether the packages import.

**Your disk needs about 9 GB free, up from 2 in the last two pairs.** The baseline model is roughly
1.6 GB and PyTorch is not small.

**Your machine needs about 6 GB of RAM.** Two things here are memory-hungry:
`baseline.py` peaks around 1.8 GB loading the zero-shot model, and the training
run peaks around 2.1 GB. Neither is comfortable beside an editor and a browser
on a 4 GB machine. `test.py` warns you.

You'll see one `[WARN] Baseline model — not downloaded yet`. That's expected in
unit 5. **Clear it before the unit 6 session** by running `python baseline.py`
once — downloading 1.6 GB during class is not how you want to spend a breakout.

> **No API key and no accounts for this pair.** Nothing here calls a hosted
> model. The baseline and the training both run on your own machine.

### What you'll be training on

`test.py` tells you, and so does section 1 of the notebook. There are three
possibilities and all of them work:

| Device | What it means | Speed |
|---|---|---|
| `cuda` | An NVIDIA GPU | Under a minute per seed |
| `mps` | Apple Silicon — M1 and later | Fast; much quicker than the CPU path |
| `cpu` | Everything else | A few minutes per seed. Three seeds is a coffee, not an afternoon |

⚠️ **Write down which one you get.** It is part of your result, not a detail
about your laptop. Two people running the same notebook on the same data with
the same seed can get different numbers, because different hardware does the
arithmetic in a slightly different order. Unit 6 asks you to report it beside
your three seeds, and `results.json` records it for you.

---

## The notebook

`takemeter.ipynb` runs **on your own machine**, from inside this repo.

1. Open it in VS Code (or `jupyter notebook`, if you prefer).
2. **Pick the kernel: the `.venv` inside this project.** In VS Code that's the
   selector in the top right. Getting this wrong is the most common way the
   first cell fails — it will say a package isn't installed when it is,
   because it's looking at a different Python.
3. Fill in the two lines at the top of section 1's second cell — your name and
   email. They only label your results.

> ⚠️ **Open it from your repo, not from a copy.** The notebook writes next to
> your code and expects `labels.csv` to be there. If you open a copy from your
> Downloads folder, it will tell you so rather than failing strangely.

### It reads and writes this folder

There is nothing to upload and nothing to download. `labels.csv` is already
here; `results.json`, `test_split.csv` and `results_three_seeds_*.json` land
here when the notebook writes them.

**Commit them yourself**, the way you commit anything else. Nothing is pushed
for you.

- Section 5 writes `results.json` and `test_split.csv` — **unit 5**
- Section 6 writes `results_three_seeds_<label>.json` — **unit 6**.
  Set `RUN_LABEL = "after"` in that cell before the Milestone 5 re-run, or the
  improvement overwrites the numbers you're comparing against.

> **Add rows to `labels.csv` mid-session?** Re-run section 2, which is what
> reads the file. The notebook holds the data in memory once it has read it.

> **Your edits to the notebook itself are yours to commit too.** `LABELS`, the
> settings and the seed live in the file — if you change them, that's a change
> to your repo like any other.

### What's in it

| Section | When | What it does |
|---|---|---|
| 1. Setup | unit 5 | Reports your device, and confirms it can see your files |
| 2. Your labels | unit 5 | `LABELS`, the settings, and **the seed** |
| 3. Split | unit 5 | 70/15/15, stratified |
| 4. Train | unit 5 | Minutes on a laptop CPU, under one on a GPU |
| 5. Results | unit 5 | Writes `results.json` and `test_split.csv` |
| 6. Three seeds | **unit 6** | Retrains three times in one cell |
| 7. Confusion matrix | **unit 6** | Prints a markdown table to paste |

Sections 6 and 7 are next unit. Nothing in unit 5 needs them.

---

## Your data

`labels.csv` in your repo. Three columns:

| Column | What's in it |
|---|---|
| `text` | The whole post. Don't trim it to fit |
| `label` | One of your labels, spelled **exactly** as in `LABELS` |
| `note` | `cold` for the 20 you labelled unaided, and a note on any you pre-labelled |

`labels_template.csv` shows the shape. `data/practice_labels.csv` is the set
used in class — 60 posts from a fictional running forum, already labelled, so
you can run the whole notebook before you have data of your own.

**One file, unsplit.** Don't split it yourself — the notebook does the 70/15/15
split, and splitting twice is how examples leak between training and test.

### The check before training

Section 2's last cell looks for the things that break a run or quietly ruin it:

| It says | What it means |
|---|---|
| `[FIX ME] Labels in your CSV that aren't in LABELS` | A spelling or capital mismatch. `Hot_take` and `hot_take` are different |
| `[FIX ME] 'x' is 78% of your data` | Over the brief's 70% cap. The model will learn to guess it |
| `[look at] N duplicate posts` | They'll land in different splits and inflate your score. That's leakage |
| `[look at] Only 12 examples of 'x'` | Its test split will be tiny, so its F1 will jump between seeds |
| `[look at] 60 rows` | Under the submission floor. Training still runs — fine for the practice data |

---

## The baseline — unit 6

```bash
python baseline.py
python baseline.py --trained results.json
```

This runs a general model over your posts using **only your label
definitions**, with no training. It's the fair opponent your fine-tuned model
has to beat.

**It scores `test_split.csv`** — the held-out posts the notebook saved in unit 5,
the same ones your trained model was measured on. Two numbers from two different
sets of posts aren't a comparison, which is why it reads that file rather than
picking its own sample. If the file isn't there it says so, falls back to a
random sample of `labels.csv`, and tells you to disclose that in your README.

Runs **on your machine**. No account, no key. A few seconds per post, so 30
posts takes a couple of minutes — that slowness is itself part of the finding.

Put your definitions in `label_definitions.txt`, one per line as
`label: definition`, copied from your README. **The definitions are the prompt** —
they're the entire input the model gets.

Without the file it falls back to bare label names, which is a much weaker
prompt. Worth doing on purpose once: run it both ways and the gap between the
two accuracies is what your definitions were worth, measured instead of assumed.
If you report the bare-names run as your baseline, say so in your README.

The second command adds a Trained column and prints the **Baseline vs.
Trained** table ready to paste.

---

## The agreement check — unit 6

Staff labelled 30 posts under the taxonomy in `data/staff_taxonomy.md`. You
label the same 30 under **those** definitions — not the ones you designed in
unit 5 — and then compare.

```bash
python agreement.py
```

Four files. The posts and the rules ship with the starter; only the answers
come from your TF, and only after yours are done. Posts and labels join on `id`:

| File | Where it comes from |
|---|---|
| `data/staff_taxonomy.md` | **Ships in the starter.** The three definitions and the decision rules staff used. Read it first — you label under *these*, not your own |
| `data/staff_posts.csv` | **Ships in the starter.** The 30 posts, no labels |
| `data/staff_labels.csv` | **Your TF gives you this**, once your own labels are done |
| `my_staff_labels.csv` | You make it: the same posts, labelled by you, with `text` and `label` columns |

**You label the staff set under the staff taxonomy, not the one you designed in
unit 5.** Your own taxonomy was yours to invent; this one is somebody else's to
apply, and whether you can apply a written rule the way its authors did is the
only evidence you have about whether your own 200 labels were consistent.

Put both staff files in `data/` under those names and the bare command finds
them. Anywhere else, point at them:

```bash
python agreement.py --staff-posts posts.csv --staff-labels labels.csv
```

Posts are matched on their text, so **paste it unchanged**. Retype or trim a
post and it won't match — the script tells you which ones didn't.

It works out the rate and lists every disagreement. **It stops there on
purpose.** The rate is arithmetic; the adjudication is the graded part, and your
README has a block to fill in for each one.

> This is the only instrument you have that can tell a labelling problem from a
> model problem. Milestone 4 asks you to use it as exactly that — a label pair
> you disagreed with staff about, and that your matrix also confuses, is a
> finding about your labels rather than about the model.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python baseline.py` | The zero-shot baseline on your held-out posts — **unit 6** |
| `python agreement.py` | Your labels vs. the staff set — **unit 6** |
| `python baseline.py --help` | All the options |
| Notebook: sections 1–5 | Train once, write `results.json` — **unit 5** |
| Notebook: sections 6–7 | Three seeds and the matrix — **unit 6** |

---

## Capstone: the deployed service

The capstone wraps the trained model in a FastAPI web service, deploys it to
Render, logs every request, and tests it with batches of sample posts. The
commands below are in the order they were first run. They are PowerShell; on
macOS/Linux swap the activate line and `$env:X = "..."` for
`source .venv/bin/activate` and `export X=...`.

| Requirements file | Used for |
|---|---|
| `requirements-dev.txt` | Your machine: training, baseline, ONNX export and quantization |
| `requirements.txt` | Render only: `fastapi`, `uvicorn`, `onnxruntime`, `tokenizers`, `numpy`, `pydantic` |

The Python version is pinned in `.python-version`.

### 1. Install and activate

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt     # training + export tooling
pip install -r requirements.txt         # the same packages Render installs
```

### 2. Export and quantize the fine-tuned model

The notebook saves the fine-tuned PyTorch model to `./my-finetuned-distilbert`.
`run_onnx_export.py` converts it to ONNX (`./onnx-temp`), then quantizes it to
INT8 and writes the deployable files to `./render_model`.

```powershell
python run_onnx_export.py
```

Check that `render_model/model_quantized.onnx` is about 65 MB (down from about
256 MB) and that `tokenizer.json` and `config.json` are there. The service
loads those files at start-up.

**Deploying before the real model exists?** `make_temp_model.py` writes a tiny
stand-in model into `render_model/` with the same inputs and outputs, so the
deployment can be tested end to end. Its predictions are meaningless, and
re-running `run_onnx_export.py` overwrites it.

```powershell
python make_temp_model.py
```

### 3. Run the service locally

```powershell
$env:ADMIN_TOKEN = "choose-any-secret"   # enables /logs and the timeout test hook
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000/docs> for the interactive page, or call it directly:

```powershell
curl http://127.0.0.1:8000/                       # health check -> {"status": "ok"}

curl -X POST http://127.0.0.1:8000/predict `
  -H "Content-Type: application/json" `
  -d '{"text": "The bridge modulates up a whole step.", "topic": "Song structure"}'
```

`topic` is the optional user-supplied context (the capstone extension). Omit it
and the post is classified on its own.

Each request is also appended to `logs/use.jsonl` and echoed to stdout.
Optional environment variables:

| Variable | Default | Effect |
|---|---|---|
| `ADMIN_TOKEN` | unset | Unset disables `/logs` (404) and the test-delay hook. Set it to turn them on |
| `LOG_INPUT_TEXT` | `1` | `0` keeps raw post text out of the logs (hash and length are still logged) |
| `LOG_STDOUT` | `1` | `0` stops echoing entries to stdout |
| `LOW_CONFIDENCE_THRESHOLD` | `0.6` | Below this, a prediction is logged as `low_confidence` |

### 4. Deploy to Render

Create a **Web Service** from this GitHub repo, then:

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| Environment variable | `ADMIN_TOKEN` = a secret you choose |

`render_model/` is committed to the repo, so deploying is a push:

```powershell
git add render_model app.py requirements.txt
git commit -m "Deploy"
git push origin main
```

The first request after a spin-down is a **cold start** (the free tier sleeps
when idle) and takes noticeably longer. The live URL is the `DEFAULT_URL` at the
top of `send_batch.py` and `pull_logs.py`.

### 5. Put the admin token in `.env`

`send_batch.py` reads `ADMIN_TOKEN` from a `.env` file in the repo root, so you
don't have to export it each session. `.env` is in `.gitignore`. Never commit it.

```
ADMIN_TOKEN=the-same-value-you-set-on-render
```

`pull_logs.py` does **not** read `.env`. Set the variable in the shell first
(step 7).

### 6. Send the sample posts

`sample_posts/` holds the request sets:

| File | What it holds |
|---|---|
| `sample_requests.json` | Well-formed posts, with and without a `topic`. All expected to succeed |
| `malformed_requests.json` | Bad inputs, each with an `expected_status` (400-class). Tests validation |
| `timeout_requests.json` | Entries with `delay_s` that stall the server to force the 5 s timeout. Needs the admin token |
| `live_log.jsonl` | The audit log pulled from Render (step 7) |

`send_batch.py` posts them to the service and prints one line per request:
`ok`, `FAIL` (5xx or network error) or `MISMATCH` (status differed from
`expected_status`). Exit code is 1 if anything was not `ok`.

```powershell
python send_batch.py                                          # every sample_posts/*.json
python send_batch.py sample_posts/sample_requests.json        # one file
python send_batch.py sample_posts/malformed_requests.json
python send_batch.py sample_posts/timeout_requests.json       # needs ADMIN_TOKEN
python send_batch.py --url http://127.0.0.1:8000              # against your local server
python send_batch.py --delay 0.5 --repeat 5 --out batch.json  # pace, repeat, save results
python send_batch.py --help
```

The Run Log in the README is three runs of each criterion, so run the relevant
file three times.

### 7. Pull the logs

The service exposes the audit log at `/logs`, protected by the admin token.
`pull_logs.py` downloads it and **merges** it into `sample_posts/live_log.jsonl`,
deduplicating, so repeated pulls keep what's already saved.

```powershell
$env:ADMIN_TOKEN = "the-same-value-you-set-on-render"
python pull_logs.py
python pull_logs.py --out other.jsonl --url http://127.0.0.1:8000
```

> **Pull soon after you use the service.** Render's free-tier disk is wiped on
> spin-down or redeploy, and the log goes with it.

| Error | Meaning |
|---|---|
| `HTTP 404` | `ADMIN_TOKEN` isn't set on Render |
| `HTTP 401` | The token doesn't match the one on Render |
| Hangs a minute | The service is waking from a cold start. Wait |

Raw IP addresses are stripped from anything saved to the repo.

### 8. Commit the evidence

```powershell
git add sample_posts/live_log.jsonl README.md RUNNING.md
git commit -m "Capstone: logs and run log"
git push origin main
```

### Capstone commands at a glance

| Command | What it does |
|---|---|
| `python run_onnx_export.py` | Fine-tuned model to quantized ONNX in `render_model/` |
| `python make_temp_model.py` | Stand-in model for testing a deployment |
| `uvicorn app:app --port 8000` | Run the service locally |
| `python send_batch.py [files]` | Send sample posts to the service |
| `python pull_logs.py` | Download the live audit log into `sample_posts/` |

---

## Which piece goes with which milestone

### Unit 5 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Pick a community and read it | Nothing to run. Read for 20 minutes |
| 2 | Design your labels | README, **Label Taxonomy** |
| 3 | Write your criteria | `criteria.md` — all five are yours this time |
| 4 | Collect and label 200 | `labels.csv` |
| 5 | Run the training | Notebook, sections 1–5 |
| 6 | Write it up | README |

### Unit 6 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Run the baseline | `baseline.py` |
| 2 | Retrain three times, read the matrix | Notebook, sections 6–7 |
| 3 | Check yourself against the staff labels | `agreement.py` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | Notebook, section 6 with `RUN_LABEL = "after"` |
| 6 | Say what's still broken | README |

---

## Where everything lives

| File | What it does |
|---|---|
| `takemeter.ipynb` | The training notebook. Runs here, on your machine |
| `baseline.py` | The zero-shot baseline. Runs on your machine |
| `agreement.py` | Your labels against the staff set. **Unit 6** |
| `criteria.md` | Your five criteria. **You write all five** |
| `labels.csv` | Your labelled data. **You create this** |
| `labels_template.csv` | The shape it needs |
| `label_definitions.txt` | Your definitions, for the baseline |
| `data/practice_labels.csv` | The 60-post practice set used in class |
| `data/staff_taxonomy.md` | The staff set's definitions and decision rules. Ships here |
| `data/staff_posts.csv` | The staff set's 30 posts. Ships here |
| `data/staff_labels.csv` | The staff set's labels. **Your TF gives you this** |
| `README.md` | Your submission |
| `results.json` | Written and committed by the notebook |
| `test_split.csv` | Your held-out posts, committed by the notebook. `baseline.py` reads it |
| `results_three_seeds_before.json` | Written and committed in unit 6, section 6 |
| `results_three_seeds_after.json` | The same cell re-run with `RUN_LABEL = "after"`, in Milestone 5 |
| `baseline_results.json` | Written by `baseline.py`. **Commit it** |
| `agreement_results.json` | Written by `agreement.py`. **Commit it** |
| `my_staff_labels.csv` | Your labels on the staff set. **You create this** |

---

## When something goes wrong

| What you see | What it means |
|---|---|
| Section 1 says `cpu` | Correct on most laptops, and fine. A three-seed run is minutes. Nothing to fix |
| `ModuleNotFoundError` in the notebook | Wrong kernel. Pick the `.venv` inside this project, top right in VS Code |
| `FileNotFoundError: labels.csv` | Either you haven't created it yet, or the notebook is open from a copy rather than from your repo. Section 1's second cell says which |
| The machine crawls during training | Close the browser and anything heavy. Training peaks around 2.1 GB |
| `KeyError` during training | A label in your CSV isn't in `LABELS`. Check capitals and spaces |
| Training takes an hour | You're on CPU. See the first row |
| Accuracy swings 15 points between seeds | Your dataset is too small or too lopsided for a stable measure. **That's a diagnosis, not a mistake** — write it down |
| A label's F1 is 0.00 | It probably has almost nothing in the test split. Check the split table |
| `baseline.py` says no `test_split.csv` | Unit 5's results section never finished. Re-run it, or note in your README that your comparison isn't like-for-like |
| `baseline.py` is downloading forever | First run only, ~1.6 GB. Do it before class |
| The baseline is very slow | Expected. A few seconds per post is what no fine-tuning costs at runtime |

The three usual causes when the notebook fails, in order: the kernel is the
system Python rather than this project's `.venv`, the notebook was opened from
a copy outside the repo, or a label in your CSV doesn't match `LABELS` exactly.

If none of those fix it, commit your CSV and criteria and write down the error.
**You have a labelled dataset and a filed standard, which is most of the
unit's grade.**

---

## A note on committing

At least four new commits in unit 5, four more in unit 6. Your commit history is
what shows your criteria existed before your results did.

The `results*.json` files are deliberately **not** in `.gitignore`. They're
evidence the run happened, and so are `test_split.csv` and `labels.csv`. The
notebook writes them; you commit them, along with `criteria.md`,
`baseline_results.json` and your README.

**One machine, one repo.** Everything happens here, so there's nothing to pull
before you push.

**Do not delete and recreate this repository.** You submit the same URL both
units.
