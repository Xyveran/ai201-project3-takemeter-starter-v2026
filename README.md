# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This is a classifier trained on posts from r/LetsTalkMusic. The goal is sort posts into one of these categories: fluff, substantive, or derailing.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `label_one`

Fluff

**Definition:** Offers an opinion, reaction, or comment about the dicussion topic without providing supporting reasoning, evidence, context, or a distinct argument, and without changing the subject.

**Example 1:**
> I don't know if anyone has ever described James Blunt or Robbie Williams' material as legitimately great art before.

**Example 2:**
> Totally

### `label_two`

Substantive

**Definition:** Contributes relevant information, personal experience, specific examples, reasoning, or a question that develops the discussion topic or responds to another participant.

**Example 1:**
> Robbie Williams isn't just huge in the UK, he's huge all across Europe. He was actually here in Portugal not too long ago, headlining the MEO Kalorama festival, and it sold out straight away. If I'm not mistaken, he lives in the US because he can keep a low profile over there.

**Example 2:**
> It’s made me pay more attention to albums. There are so many songs that in the past I would’ve only heard on the radio or MTV, and I’d enjoy them but I wouldn’t be intrigued enough to spend like $30 (in today’s dollars) to take a chance on the CD. But now I feel free to explore the rest of the album on Spotify without paying one cent on top of the subscription I’m already paying for.

### `label_three`

Derailing

**Definition:** Shifts attention away from the discussion's central topic or argument by introducing an unrelated subject, targeting a person or group with a dismissive remark, or making a personal attack instead of addressing the topic of discussion.

**Example 1:**
> All I know of Robbie Williams was that banger of a movie they had where he was played by an animated monkey.

**Example 2:**
> For sure. And Facebook getting fined about children’s usage wss a great thing to see. They call it an agreement and take no fault 😂, but we all know whats really going on.

### The hardest boundary

**Which two labels:** Substantive versus Derailing

**Substantive Example:**
> It's funny so many people chiming in saying "well I still listen to albums" yeah no shit you're on the music enthusiast subreddit. I think everyone here does

This post's main purpose is to draw attention to the selection bias present in responses in the topic "Has streaming made listeners less emotionally attached to individual albums?". It presents additional information that should be considered when engaging in the discussion.

**The decision rule I used every time:**
A post is Derailing when its main contribution redirects attention toward an unrelated subject, dismisses or attacks a person or group, or criticizes participants rather than engaging with the topic being discussed. A post is Fluff when it expresses an unsupported or dismissive opinion about the discussion topic without making that redirect or attack. A post that supplies relevant information or develops an argument is Substantive, even if it is brief or strongly worded.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Reddit — r/LetsTalkMusic

**How I labelled them:** A mixture of cold labeling, and AI pre-labelled posts that were reviewed and corrected.<!-- Cold first? Pre-labelled with AI and corrected? Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| substantive | 158 | 0.68 |
| fluff | 60 | 0.26 |
| derailing | 14 | 0.06 |
| **Total** | 232 | 100% |


**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Discogs is how I do my 'crate digging' digitally"
>
> *Could have been:* `Fluff` or `Substantive`
> 
> *I chose, because:* Decided on substantive as its a personal-experience statement, and not just a reaction.

**2.**
> *The post:* "I feel like you missed the point of what they were saying. I could be wrong, though."
>
> *Could have been:* `Fluff` or `Derailing`
>
> *I chose, because:* It responds to another user, but gives no reasoning. Last sentence hedges it to the side of fluff rather than derailing.


**3.**
> *The post:* "For the last few years, for whatever reason, iris has always been on the radio at least twice a day. I hate that song so much, and its not like the goo goo dolls were ever that good to begin with outside of their hardcore albums but i genuinely don't understand how people like that song."
>
> *Could have been:* `Substantive` or `Derailing`
>
> *I chose, because:* This is a rant that mostly says "I hate this song," but it does give context and a reason so I erred toward substantive.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** distilbert-base-uncased

**Settings:** EPOCHS = 3, LEARNING_RATE = 2e-5, BATCH_SIZE = 16, SEED = 42<!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** 
train 162 / val 35 / test 35
                 
| fluff | 42 | 9 | 9 |
| substantive | 110 | 24 | 24 |
| derailing | 10 | 2 | 2 |
<!-- train / val / test, and per-label counts in the test split. If a label had fewer than about 8 in test, say so — it explains a lot of next unit's variance. -->


---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* "organize and label the posts in batch_1 into Fluff, Substantive, or Derailing. Definitions being used are at the top of the file.
Original thread is titled "Streaming gave me every album ever made, and I stopped discovering music. How do you still dig?"'
- *What came back:* 23 labeled posts appended onto labels.csv in the same format as the cold-labeled posts I added beforehand. Reasons for choosing a label for close calls alongside.
- *What I changed:* Nothing here, as I agreed with the verdicts on labelling based on my label definitions.

**Moment 2**

- *What I asked for:* "How solid are the labels, definitions, and examples? I need them to hold up for ambiguous posts that sit on boundaries."
- *What came back:* Constructive criticism of the definitions, and recommendations for rules for deciding between labels.
- *What I changed:* I tighted up the definitions for each of `fluff` `substantive` and `derailing`, and added information to their definitions to more consistently categorize posts sitting on boundaries.

**Pre-labelling disclosure:** Around half of the labeled examples were pre-labeled with the use of AI and indicated with a `pre-labeled` note. These examples were all hand reviewed and corrected.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json` prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.629 | 0.686 | +0.057 |
| Macro F1 | 0.272 | 0.271 | -0.000 |
| F1 — `derailing` | 0.000 | 0.000 | +0.000 |
| F1 — `fluff` | 0.000 | 0.000 | +0.000 |
| F1 — `substantive` | 0.815 | 0.814 | -0.001 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
I expect the trained model to see a significant improvment in fluff prediction accuracy, and a minor improvment for derailing prediction accuracy.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
As it stands, the fine-tuning did not significantly impact accuracy for any label. The overall accuracy improved by 0.057, with a very slight loss to substantive labels of 0.001.


---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

<!-- | Measure | Seed 25 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.714 | 0.686 | 0.686 | 0.029 |
| Macro F1 | 0.343 | 0.271 | 0.271 | 0.071 |
| F1 — `fluff` | 0.200 | 0.000 | 0.000 | 0.200 |
| F1 — `substantive` | 0.828 | 0.814 | 0.814 | 0.014 |
| F1 — `derailing` | 0.000 | 0.000 | 0.000 | 0.000 |
-->

| Criterion | Target | Seed 25 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall Accuracy | ≥ 0.80 | 0.714 | 0.686 | 0.686 | MISSED |
| 2. F1 for Substantive and Fluff | ≥ 0.80; ≥ 0.65 | 0.828; 0.200 | 0.814; 0.000 | 0.814; 0.000 | MISSED |
| 3. Macro F1 | ≥ 0.65 | 0.343 | 0.271 | 0.271 | MISSED |
| 4. Recall and F1 for Derailing | ≥ 0.50; ≥ 0.40 | 0.000; 0.000 | 0.000; 0.000 | 0.000; 0.000 | MISSED |
| 5. No label below 10% of dataset, substantive at most 65% | True | False | False | False | MISSED |


### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | fluff | substantive | derailing |
|---|---|---|---|
| **fluff** | 1 | 8 | 0 |
| **substantive** | 0 | 24 | 0 |
| **derailing** | 0 | 2 | 0 |


**My biggest off-diagonal number, and what it means:**
8 real `fluff` posts were called `substantive`, and 0 real `substantive` posts were called `fluff`. When it comes to choosing between these labels, the model leans heavily toward `substantive`.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1. Overall Accuracy | ≥ 0.80 | MISSED |
| 2. F1 for Substantive and Fluff | ≥ 0.80; ≥ 0.65 | MISSED |
| 3. Macro F1 | ≥ 0.65 | MISSED |
| 4. Recall and F1 for Derailing | ≥ 0.50; ≥ 0.40 | MISSED |
| 5. No label below 10% of dataset, substantive at most 65% | True | MISSED |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 1: Overall accuracy (0.714 / 0.686 / 0.686, target 0.80).**
*Cause: the model collapsed to the majority label.* In seeds 7 and 2024 it predicted `substantive` for all 35 test posts, so accuracy equals the share of `substantive` in the test split (24/35 = 0.686). Seed 25's 0.714 is one extra correct `fluff` post. The model never beat the always-guess-`substantive` baseline (0.629 to 0.686), so fine-tuning added almost nothing. The training set is 68% `substantive` and 162 examples over 3 epochs gave the model little reason to leave that default.

**Criterion 2: F1 for `substantive` and `fluff` (substantive 0.828 / 0.814 / 0.814, fluff 0.200 / 0.000 / 0.000).**
*Cause: too few `fluff` examples to learn from (42 in train), and no pressure to use them.* The `substantive` half of this criterion is met in every seed. The `fluff` half is missed. The confusion matrices show the failure goes one way: 8 or 9 of 9 real `fluff` posts were called `substantive`, and no `substantive` post was ever called `fluff`. Seed 25 got 1 of 9 and the other two seeds got 0. That swing from one post means the model has no stable `fluff` signal. The confidence data agrees: accuracy was 1.0 in the most confident third of predictions and only 0.18 to 0.27 in the least confident third. The model is unsure on exactly the posts it gets wrong.

My agreement report says I apply written rules consistently, but the baseline's per-post predictions (baseline_results.json, same 35 test posts) suggest my `fluff` definition is still too loose. Under the staff taxonomy I matched 29 of 30 (96.7%), and the one disagreement (the shoe-running post, `analysis` vs `hot_take`) is pile (c), a defensible reading of an ambiguous rule. So I found no pile (a) cases: no sign I applied a written boundary two different ways. But the staff set uses a different taxonomy, so it cannot test my `fluff` rule. Reading the 9 test `fluff` posts shows why that matters. Only two are pure reactions ("who?", "Oh man, it would have been monstrous!"). The other seven make claims or take positions: "DMB has no redeeming qualities", "You don't need to break into any market if you're already in the biggest market", "I mean... Rage Against the Machine was huge in the USA", "They know the song. They're not going to recognize him on the street". Next to them, "Dave sells out pretty big places in Europe??" is labelled `substantive`, and "Honest answer is because they are all pretty mediocre" is `derailing`. A model cannot separate those from the text alone, and I'd have trouble doing it from my own definitions. The zero-shot baseline, which was given my definitions, called six of the nine `substantive` and three `derailing`, and got none right. So the `fluff` boundary is a real contributor here, not only the class imbalance.

**Criterion 3: Macro F1 (0.343 / 0.271 / 0.271, target 0.65).**
*Cause: follows from criteria 2 and 4.* Macro F1 averages three labels, and two of them (`fluff` and `derailing`) score at or near 0. With `substantive` at about 0.81, the macro score cannot exceed about 0.34 until at least one minority label becomes learnable. This is a symptom, not a separate problem, so I cam't fix it separately.

**Criterion 4: `derailing` recall and F1 (0.000 / 0.000 in all three seeds, target 0.50 / 0.40).**
*Cause: too few examples.* This is the clearest case, and it supports my hypothesis. There are 14 `derailing` posts in total, giving 10 in train, 2 in val and 2 in test. The model predicted `derailing` zero times in every seed. Recall on a 2-post test set can only be 0, 0.5 or 1.0, so this criterion could not be measured reliably even with a better model. A second, smaller contributor is that `derailing` is a mixed class. My examples include personal attacks ("random internet know-it-all"), topic policing ("You are off topic"), and generalizations about groups ("The same people who whine about..."). With 10 examples the model has no way to find a common pattern, and I haven't shown that one exists.

**Criterion 5: Dataset balance (`derailing` 6%, `substantive` 68%).**
*Cause: too few examples, and I knew this before training.* The counts fail both halves directly: `derailing` is 14/232 (6%, below the 10% floor of 24) and `substantive` is 68% (above the 65% cap). My criteria.md predicted this and planned to add at least 10 more `derailing` posts. This criterion is checked before training, so it is the one miss I can fix with data alone, and it is the likely root of criteria 3 and 4.


---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 29 / 30 = 96.7%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* analysis / hot_take
>
> *My call, and why:* The analysis label requires a specific checkable fact that does the work in the argument. The evidence in this post doesn't support the conclusion. The only fact here is that three runners performed similarly on one day. Three runners having close times cannot differentiate a "shoes don't matter" conclusion from a "three people ran with similar effort" conclusion. The post states all runners finished within 10 seconds of each other. The idea of shoe effect being smaller than this 10-second spread can't be tested from this information.
>
> *Which pile:* (c) the rule is ambiguous here and my reading is defensible

**What the pattern in my disagreements tells me:** The one disagreement came from how I read analysis: staff checked whether a specific fact was present, and I checked whether it supported the conclusion.


---

## The Improvement

**What I changed:** I added 28 posts to the dataset that all belong under the 'derailing' label.

**Which diagnosis pointed at it:** The diagnosis of Criterion 4: `derailing` recall and F1 (0.000 / 0.000 in all three seeds, target 0.50 / 0.40). I believed that there was not enough data on the `derailing` label for the model to learn.


### Run Log — After

| Criterion | Target | Seed 25 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall Accuracy | ≥ 0.80 | 0.615 | 0.615 | 0.615 | MISSED |
| 2. F1 for Substantive and Fluff | ≥ 0.80; ≥ 0.65 | 0.762; 0.000 | 0.762; 0.000 | 0.762; 0.000 | MISSED |
| 3. Macro F1 | ≥ 0.65 | 0.254 | 0.254 | 0.254 | MISSED |
| 4. Recall and F1 for Derailing | ≥ 0.50; ≥ 0.40 | 0.000; 0.000 | 0.000; 0.000 | 0.000; 0.000 | MISSED |
| 5. No label below 10% of dataset, substantive at most 65% | True | False | False | False | MET |

**Did it help, and how do I know:** With the additional labels, the share of `substantive` dropped to ~60.77% and the share of `derailing` rose to 16.15%. Plainly, that means criterion 5 gets to pass. However, it's apparent that the model learned to just go with `substantive` rather than learn any relationships between the posts and their labels. Performance for `derailing` and `fluff` flatlined across each seed, and all the positive metrics are directly tied to how many posts in test had the `substantive` label.

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->
---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

Criteria 1-4 are still missed in all three seeds. Only criterion 5 (dataset balance) is met, and it did not carry over into model performance. The current dataset has 260 posts (158 `substantive`, 60 `fluff`, 42 `derailing`). All three seeds returned identical numbers after the change (0.615 accuracy, 0.254 macro F1), which means the model is collapsing to `substantive` regardless of seed and is not learning anything from the text.

**Criterion 1: Overall accuracy (0.615, target 0.80).**
*What I'd do:* Cut `substantive` down by about 60 posts, from 158 to roughly 98, so it is about 49% of the data and always predicting it no longer wins. Raise epochs from 3 to 5 at the same learning rate so the model has time to move off the majority class. Accuracy should only be trusted once the model predicts more than one label. Right now 0.615 is just 24/39, the `substantive` share of the test split.
*Why I stopped:* The unit asks for one improvement, and I spent it on `derailing` volume because that was my clearest diagnosis. Both of these changes are untested.

**Criterion 2: F1 for `substantive` and `fluff` (0.762 / 0.000, targets 0.80 / 0.65).**
*What I'd do:* Fix the `fluff` definition before adding any data. I would reread all 60 `fluff` posts, relabel or tighten the rule so that `fluff` means only unsupported reactions, then retrain. Substantive F1 fell from about 0.81 to 0.762, which only reflects the larger test split with more non-`substantive` posts and does not mean the model got worse.
*Why I stopped:* Relabeling means rereading the whole dataset and rewriting the definition, and I did not want to change labels and data in the same run, because I would not be able to tell which one moved the numbers.

**Criterion 3: Macro F1 (0.254, target 0.65).**
*What I'd do:* Nothing separate. It is the average of three F1 scores, and two of them are 0.000. It cannot rise until `fluff` or `derailing` becomes learnable, so fixing criteria 2 and 4 fixes this one.
*Why I stopped:* There is nothing to fix on its own.

**Criterion 4: `derailing` recall and F1 (0.000 / 0.000, targets 0.50 / 0.40).**
*What I'd do:* My diagnosis blamed too few examples, and this run weakens that. Training `derailing` went from 10 posts to about 38 and the model still predicted it zero times, with all 6 test `derailing` posts called `substantive`. So volume alone was not the cause. This may still be related to dataset balance though, with the majority representation still being held by `substantive` posts preventing the learning of other labels.
*Why I stopped:* The 28 new posts were the whole improvement for this unit.

**The gap between what I meant my labels to capture and what the model
learned:** I meant for my labels to capture whether a post adds something to the discussion, takes it off topic, or only reacts to it. The model learned to go all-in on `substantive` every time, as the matrix below shows: 9 of 9 `fluff` and 6 of 6 `derailing` posts were called `substantive`.

| true \ predicted | fluff | substantive | derailing |
|---|---|---|---|
| **fluff** | 0 | 9 | 0 |
| **substantive** | 0 | 24 | 0 |
| **derailing** | 0 | 6 | 0 |


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->


## Capstone

**The Shape**
Shape C — Extend one capability. The post classifier originally sought to classify reddit posts into one three labels: `substantive`, `fluff`, or `derailing`. The system before this point only processes the posts in isolation. Accurately determining a `derailing` or `fluff` label needs context, so the goal of this extension is to enable a user to provide this context.  

**What's Out of Scope**:
(1) Automatic context retrieval: the user supplies the context themselves, so I'm not scraping Reddit or looking up the parent post and thread from a URL.
(2) Full thread context: the extension takes one piece of user-provided context per post, not whole reply chains or other comments in the thread.
(3) Changing the labels or relabeling data: the label set stays `substantive`, `fluff`, and `derailing`, and I'm not rebuilding the staff-labeled dataset to include context.

**Instrumentation**
Live entries pulled from the deployed Render service (`sample_posts/live_log.jsonl`, fetched with `pull_logs.py`).
```json
{
     "timestamp": "2026-11-15T02:49:49.384+00:00", "event": "prediction", "request_id": "650b73532c9344f29fe135cf52bac75f", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 202.58, "cold_start": true, "input_text": "I thought they were the best of the pop punk bands from that era. The riffs were way more interesting than their peers, and the second album's production holds up.", "text_hash": "730099dddcb13b8daee278053715ac9e974be914f1c85ce4c119c09a414f6d01", "text_length": 163, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.6424, "margin": 0.4573, "low_confidence": false, "label_confidences": {"fluff": 0.1851, "substantive": 0.6424, "derailing": 0.1725}, "token_count": 43, "truncated": false, "preprocess_ms": 0.43, "inference_ms": 200.09, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:49.604+00:00", "event": "prediction", "request_id": "0f252d3429494eb4bf9c08ddf0bbe231", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 8.78, "cold_start": false, "input_text": "lol same", "text_hash": "b545a3a88f03c01982bfc396ccd0c4b41147a96c4b32f43ac261166c2bcc424a", "text_length": 8, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.4103, "margin": 0.0915, "low_confidence": true, "label_confidences": {"fluff": 0.3188, "substantive": 0.4103, "derailing": 0.2709}, "token_count": 10, "truncated": false, "preprocess_ms": 0.14, "inference_ms": 7.54, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:49.793+00:00", "event": "prediction", "request_id": "cab709e76d5b440584af791b3381b938", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 54.8, "cold_start": false, "input_text": "I have no idea what that lunatic was thinking. With how they responded, you would think they lived in a psych ward.", "text_hash": "e8e9f3286b0c774e030557869b1efc284c6810b2dd9fb148fe4c63cac7f3ab90", "text_length": 115, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.4938, "margin": 0.2289, "low_confidence": true, "label_confidences": {"fluff": 0.2649, "substantive": 0.4938, "derailing": 0.2413}, "token_count": 33, "truncated": false, "preprocess_ms": 0.19, "inference_ms": 53.51, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:49.995+00:00", "event": "prediction", "request_id": "13bce07239014e54b8c600995a41c559", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 87.24, "cold_start": false, "input_text": "Saw them live in 2009 and the sound mix was awful, but the crowd carried the whole set. Has anyone heard if the reunion tour fixed that?", "text_hash": "6f9c941e1370ba547376c38919845bfd8df4f0558f7f872abfa9c781a6245bd6", "text_length": 136, "input_topic": "Reunion tours", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.5918, "margin": 0.3728, "low_confidence": true, "label_confidences": {"fluff": 0.219, "substantive": 0.5918, "derailing": 0.1892}, "token_count": 35, "truncated": false, "preprocess_ms": 0.19, "inference_ms": 85.6, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:50.186+00:00", "event": "prediction", "request_id": "742c72e2acaa44c59411997c5cde929f", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 29.41, "cold_start": false, "input_text": "Honestly this whole thread is a waste of time, none of you know anything about music.", "text_hash": "4e636f64f8dd4bfdbdfe04224f65349b6421d11547d642df5785e4af673061a0", "text_length": 85, "input_topic": "Reunion tours", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.491, "margin": 0.2252, "low_confidence": true, "label_confidences": {"fluff": 0.2658, "substantive": 0.491, "derailing": 0.2432}, "token_count": 23, "truncated": false, "preprocess_ms": 0.19, "inference_ms": 27.98, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:50.325+00:00", "event": "prediction", "request_id": "da1d360a93714ef6a1e63d698de2a105", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 5.66, "cold_start": false, "input_text": "Great song.", "text_hash": "1c122242c1bc443374094aff01a11d381a38039199c1f233282437674dfa7502", "text_length": 11, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.3805, "margin": 0.0461, "low_confidence": true, "label_confidences": {"fluff": 0.3344, "substantive": 0.3805, "derailing": 0.2851}, "token_count": 5, "truncated": false, "preprocess_ms": 0.1, "inference_ms": 4.58, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:50.491+00:00", "event": "prediction", "request_id": "c69e7fbbae7b4674be4407ec18a5ca1e", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 46.56, "cold_start": false, "input_text": "The bridge modulates up a whole step, which is why the last chorus feels so much bigger even though the arrangement barely changes.", "text_hash": "3f86a41bb69ee218992bfc1cbc8ecdbaf6c0c201e3e1ba390303fb6fda029252", "text_length": 131, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.5605, "margin": 0.3315, "low_confidence": true, "label_confidences": {"fluff": 0.229, "substantive": 0.5605, "derailing": 0.2105}, "token_count": 28, "truncated": false, "preprocess_ms": 0.25, "inference_ms": 45.16, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:50.692+00:00", "event": "prediction", "request_id": "2c2842dd25414178b9e64c37cd89ea6b", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 96.81, "cold_start": false, "input_text": "Anyone else here a big fan of that new cooking show? Totally unrelated but I can't stop watching it.", "text_hash": "b480dd37eb23d31133172d0610f6449b5abe46fb586b6ead5855cd80ca350e3d", "text_length": 100, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.5243, "margin": 0.2671, "low_confidence": true, "label_confidences": {"fluff": 0.2572, "substantive": 0.5243, "derailing": 0.2185}, "token_count": 31, "truncated": false, "preprocess_ms": 0.22, "inference_ms": 95.35, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:50.892+00:00", "event": "prediction", "request_id": "616eaea9b6344995bbf019653efc0b79", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 94.18, "cold_start": false, "input_text": "Vinyl sounds warmer mostly because of mastering choices, not the format. The same master on streaming usually measures almost identical.", "text_hash": "764754436bd8084a38025dba98331623246da02d3693cd9ee1593f43a9d83a54", "text_length": 136, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "chosen_label": "substantive", "confidence": 0.63, "margin": 0.4446, "low_confidence": false, "label_confidences": {"fluff": 0.1846, "substantive": 0.63, "derailing": 0.1854}, "token_count": 31, "truncated": false, "preprocess_ms": 0.19, "inference_ms": 92.81, "corrected_label": null, "feedback": null
}
{
     "timestamp": "2026-11-15T02:49:51.010+00:00", "event": "rejected", "request_id": "7546b7d22a6c4be29733b7580a3bd039", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 400, "latency_ms": 1.01, "cold_start": false, "input_text": "   ", "text_hash": "0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4", "text_length": 3, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "a2643a6d0ba8665c19987049b947caee582db2b2", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7c4cff58c9-dl9kq", "error_type": "validation", "reason": "empty text", "stack_trace": null
}
```

**What It Costs**
The classifier is a quantized ONNX model that runs on CPU inside my own Render service, so there is no API spend and nothing is billed per token. The real cost is compute time per request. Every number below comes from the server-side log of the live Render deployment (`latency_ms`, `inference_ms`, `preprocess_ms` and `token_count` in `sample_posts/live_log.jsonl`), not from my own machine.

*Tokens:* 26.6 per request on average (min 5, max 43; 24.5 excluding the cold-start request). This is the number of model input tokens after tokenization, including the topic when one is provided. Input is truncated at 256 tokens, so the worst case is bounded. Tokens are not billed, but they do affect inference time.

*Inference Time:* 68.1 ms per request on average for the model call alone, across the nine processed requests. The first request after the restart was a cold start and took 200.1 ms. Excluding it, inference averaged 51.6 ms (median 49.3 ms, range 4.6 to 95.4 ms). End-to-end server time per request, including tokenization, was 69.6 ms on average (52.9 ms warm).

| Metric (9 processed requests) | Mean | Mean, warm only (8) | Cold start (1) | Min | Max |
|---|---|---|---|---|---|
| Total latency | 69.56 ms | 52.93 ms | 202.58 ms | 5.66 ms | 202.58 ms |
| Inference (`session.run`) | 68.07 ms | 51.57 ms | 200.09 ms | 4.58 ms | 200.09 ms |
| Preprocessing | 0.21 ms | 0.18 ms | 0.43 ms | 0.10 ms | 0.43 ms |
| Input tokens | 26.6 | 24.5 | 43 | 5 | 43 |

*How I measured it:* Each request is timed on the server in the FastAPI middleware with `time.perf_counter()`, and `session.run` is timed separately inside the endpoint. Both are written to the audit log as `latency_ms` and `inference_ms`. After deploying and restarting the service on Render, I sent ten requests to the live URL (mixing posts with and without a topic) and pulled the server's log through a token-protected `/logs` endpoint. Nine were processed and one was rejected (blank text, which returns a 400 before the model runs, in 1.01 ms). The averages cover the nine processed requests. Network time between my machine and Render is not included, because these are server-side timings.

*What the numbers show:* The cold start is about four times slower than the warm average (200 ms against 52 ms for inference), so the first request after a restart pays an extra cost. Inference time only loosely follows token count: 5 tokens took 4.6 ms and 43 tokens took 200 ms, but two requests with 31 tokens took 95.4 ms and 92.8 ms while one with 28 tokens took 45.2 ms. I think that variation comes from Render's free tier sharing CPU with other workloads, but I did not test that.

<!-- 
curl.exe -X POST https://ai201-project3-takemeter-starter-v2026.onrender.com/predict -H "Content-Type: application/json" -d '{\"text\":\"hello\",\"topic\":\"optional\"}' 

curl.exe -X POST https://ai201-project3-takemeter-starter-v2026.onrender.com/predict -H "Content-Type: application/json" -d "@sample_posts/sample1.json"

-->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
