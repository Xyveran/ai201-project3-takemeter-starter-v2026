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

**Run Log**

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Requests with malformed inputs return a 400-class error code instead of reaching the model in 10/10 calls. |  10 of 10 | 1/10 | 1/10 | 1/10 | MISSED |
| 2. Successful service calls log a timestamp, client_id, input_text, chosen_label, and confidence in 10/10 calls. | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 3. The deployed `/predict` endpoint responds in under 1 second in 9 of 10 calls. | 9 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 4. When a request exceeds the time limit, the service returns an error message and stays up in 5 of 5 forced timeouts. | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Each prediction costs less than $0.01 in 10 of 10 calls. | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

**Criterion 1: Requests with malformed inputs return a 400-class error code instead of reaching the model in 10/10 calls.**
Multiple issues with this miss. Most of the malformed inputs are not currently being marked as errors and subsequently aren't returning error codes for these malformed inputs. Most notably, two requests from the `malformed_requests.json` set don't even appear in the logs. Case #4 `lone_surrogate_escape` contains `\\ud83d` parsing into an unencodable string which caused an Internal Server Error, and case #10 `markup_and_json_payload_as_text` which got its return body overridden with html. The amendment to resolve this miss is in `app.py` input validation, and adjusting the error logging to capture the additional edge cases.

Logs From a Single Run

*Success Test Set*
```json
     {"timestamp": "2026-11-15T22:05:33.312+00:00", "event": "prediction", "request_id": "7ca7861d67a74aacb9f83821293ba47f", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 133.04, "cold_start": true, "input_text": "I thought they were the best of the pop punk bands from that era. The riffs were way more interesting than their peers, and the second album's production holds up.", "text_hash": "730099dddcb13b8daee278053715ac9e974be914f1c85ce4c119c09a414f6d01", "text_length": 163, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.6424, "margin": 0.4573, "low_confidence": false, "label_confidences": {"fluff": 0.1851, "substantive": 0.6424, "derailing": 0.1725}, "token_count": 43, "truncated": false, "preprocess_ms": 0.64, "inference_ms": 129.79, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:33.513+00:00", "event": "prediction", "request_id": "0287d58619af47d1b37021ff45b6e191", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 8.87, "cold_start": false, "input_text": "lol same", "text_hash": "b545a3a88f03c01982bfc396ccd0c4b41147a96c4b32f43ac261166c2bcc424a", "text_length": 8, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.4103, "margin": 0.0915, "low_confidence": true, "label_confidences": {"fluff": 0.3188, "substantive": 0.4103, "derailing": 0.2709}, "token_count": 10, "truncated": false, "preprocess_ms": 0.12, "inference_ms": 7.62, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:33.716+00:00", "event": "prediction", "request_id": "b823411304a743bfa3781b966781a13f", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 75.92, "cold_start": false, "input_text": "I have no idea what that lunatic was thinking. With how they responded, you would think they lived in a psych ward.", "text_hash": "e8e9f3286b0c774e030557869b1efc284c6810b2dd9fb148fe4c63cac7f3ab90", "text_length": 115, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.4938, "margin": 0.2289, "low_confidence": true, "label_confidences": {"fluff": 0.2649, "substantive": 0.4938, "derailing": 0.2413}, "token_count": 33, "truncated": false, "preprocess_ms": 0.21, "inference_ms": 74.54, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:33.915+00:00", "event": "prediction", "request_id": "ad8d772fd7384d9a9f7a8c1742d8ca0e", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 125.5, "cold_start": false, "input_text": "Saw them live in 2009 and the sound mix was awful, but the crowd carried the whole set. Has anyone heard if the reunion tour fixed that?", "text_hash": "6f9c941e1370ba547376c38919845bfd8df4f0558f7f872abfa9c781a6245bd6", "text_length": 136, "input_topic": "Reunion tours", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.5918, "margin": 0.3728, "low_confidence": true, "label_confidences": {"fluff": 0.219, "substantive": 0.5918, "derailing": 0.1892}, "token_count": 35, "truncated": false, "preprocess_ms": 0.18, "inference_ms": 123.48, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.113+00:00", "event": "prediction", "request_id": "55b7174253ba485799fd70f9aad2e6f2", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 63.07, "cold_start": false, "input_text": "Honestly this whole thread is a waste of time, none of you know anything about music.", "text_hash": "4e636f64f8dd4bfdbdfe04224f65349b6421d11547d642df5785e4af673061a0", "text_length": 85, "input_topic": "Reunion tours", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.491, "margin": 0.2252, "low_confidence": true, "label_confidences": {"fluff": 0.2658, "substantive": 0.491, "derailing": 0.2432}, "token_count": 23, "truncated": false, "preprocess_ms": 0.21, "inference_ms": 61.5, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.223+00:00", "event": "prediction", "request_id": "de30499eee5949f7a500875b9d8fb0b9", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 5.89, "cold_start": false, "input_text": "Great song.", "text_hash": "1c122242c1bc443374094aff01a11d381a38039199c1f233282437674dfa7502", "text_length": 11, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.3805, "margin": 0.0461, "low_confidence": true, "label_confidences": {"fluff": 0.3344, "substantive": 0.3805, "derailing": 0.2851}, "token_count": 5, "truncated": false, "preprocess_ms": 0.12, "inference_ms": 4.54, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.413+00:00", "event": "prediction", "request_id": "b03068b030ee4b8690f2d82ad7f9b188", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 51.4, "cold_start": false, "input_text": "The bridge modulates up a whole step, which is why the last chorus feels so much bigger even though the arrangement barely changes.", "text_hash": "3f86a41bb69ee218992bfc1cbc8ecdbaf6c0c201e3e1ba390303fb6fda029252", "text_length": 131, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.5605, "margin": 0.3315, "low_confidence": true, "label_confidences": {"fluff": 0.229, "substantive": 0.5605, "derailing": 0.2105}, "token_count": 28, "truncated": false, "preprocess_ms": 0.21, "inference_ms": 49.97, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.617+00:00", "event": "prediction", "request_id": "01220985713c42c4a411ff7d1ceb303a", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 91.71, "cold_start": false, "input_text": "Anyone else here a big fan of that new cooking show? Totally unrelated but I can't stop watching it.", "text_hash": "b480dd37eb23d31133172d0610f6449b5abe46fb586b6ead5855cd80ca350e3d", "text_length": 100, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.5243, "margin": 0.2671, "low_confidence": true, "label_confidences": {"fluff": 0.2572, "substantive": 0.5243, "derailing": 0.2185}, "token_count": 31, "truncated": false, "preprocess_ms": 0.24, "inference_ms": 90.3, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.812+00:00", "event": "prediction", "request_id": "77899205b46740f3a7dfdc7e2c2f3230", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 127.57, "cold_start": false, "input_text": "Vinyl sounds warmer mostly because of mastering choices, not the format. The same master on streaming usually measures almost identical.", "text_hash": "764754436bd8084a38025dba98331623246da02d3693cd9ee1593f43a9d83a54", "text_length": 136, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.63, "margin": 0.4446, "low_confidence": false, "label_confidences": {"fluff": 0.1846, "substantive": 0.63, "derailing": 0.1854}, "token_count": 31, "truncated": false, "preprocess_ms": 0.19, "inference_ms": 126.13, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:34.914+00:00", "event": "prediction", "request_id": "8c3f66afcb7f420a9f7c6ee3a03f90da", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 29.46, "cold_start": false, "input_text": "UB Star Trek should've been a few commander deck boxes instead of a premier set.", "text_hash": "08e05f0d4458e7ee64db69c2084139b4a7d2054f12e0bab94060ad8aec8eb2e2", "text_length": 80, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.5439, "margin": 0.3054, "low_confidence": true, "label_confidences": {"fluff": 0.2385, "substantive": 0.5439, "derailing": 0.2175}, "token_count": 21, "truncated": false, "preprocess_ms": 0.15, "inference_ms": 28.23, "corrected_label": null, "feedback": null}
```

*Malformed Input Test Set*
```json
     {"timestamp": "2026-11-15T22:05:48.145+00:00", "event": "prediction", "request_id": "33beb980874047088dfc0cfaa44198bd", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 9.25, "cold_start": false, "input_text": "​​​​", "text_hash": "153c9ccaf588eee6fdd24ff667ce64c1bf7f432cbd0eff0efbebc5245b8dc10b", "text_length": 4, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.4174, "margin": 0.1025, "low_confidence": true, "label_confidences": {"fluff": 0.3149, "substantive": 0.4174, "derailing": 0.2677}, "token_count": 8, "truncated": false, "preprocess_ms": 0.14, "inference_ms": 7.66, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:48.244+00:00", "event": "prediction", "request_id": "9efd0a4ce11f4d3e9aceb92e25941a4e", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 5.73, "cold_start": false, "input_text": "ㅤ⠀⁠ㅤ", "text_hash": "50a6c57e77ebf94ee16c216f747ebdbe4c3425d3b8d3bdbe23838e65485eaf55", "text_length": 4, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.3556, "margin": 0.0011, "low_confidence": true, "label_confidences": {"fluff": 0.3545, "substantive": 0.3556, "derailing": 0.2899}, "token_count": 3, "truncated": false, "preprocess_ms": 0.11, "inference_ms": 4.24, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:48.326+00:00", "event": "prediction", "request_id": "4464c41c3fe0418d98143a4a8d2b54ba", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 9.14, "cold_start": false, "input_text": "\u0000\u0007\u001b[31mgreat\u001b[0m\u0000", "text_hash": "ab385e9314f7b7747674c0b5c237ed280b9e23dd403084fbd5952130642b504b", "text_length": 17, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.4166, "margin": 0.098, "low_confidence": true, "label_confidences": {"fluff": 0.3186, "substantive": 0.4166, "derailing": 0.2648}, "token_count": 10, "truncated": false, "preprocess_ms": 0.14, "inference_ms": 7.85, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:48.510+00:00", "event": "prediction", "request_id": "766d640636e942dfb028fb7fa378d5f3", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 20.95, "cold_start": false, "input_text": "Vinyl sounds warmer mostly because of mastering choices.", "text_hash": "3a3a687ca0a70158ba4990ba9d8c78a6ad241f4a38151c8ceddbcc4c4c9bf4f0", "text_length": 56, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.5705, "margin": 0.3542, "low_confidence": true, "label_confidences": {"fluff": 0.2163, "substantive": 0.5705, "derailing": 0.2132}, "token_count": 11, "truncated": false, "preprocess_ms": 0.12, "inference_ms": 19.48, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:48.615+00:00", "event": "prediction", "request_id": "10c50c63d11f4c0ba19ee54e68fe0b69", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 6.17, "cold_start": false, "input_text": "Great song.", "text_hash": "1c122242c1bc443374094aff01a11d381a38039199c1f233282437674dfa7502", "text_length": 11, "input_topic": null, "topic_provided": false, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.3805, "margin": 0.0461, "low_confidence": true, "label_confidences": {"fluff": 0.3344, "substantive": 0.3805, "derailing": 0.2851}, "token_count": 5, "truncated": false, "preprocess_ms": 0.1, "inference_ms": 4.78, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:50.121+00:00", "event": "prediction", "request_id": "ecc8378d0e3c41a48eaa01bff37d083d", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 1427.25, "cold_start": false, "input_text": "The mix on this record buries the bass under the guitars, which is a choice, not an accident... ", "text_hash": "c2e742e539bb413051eb553e2a4e349629dcbbb992f4778f94d000e244cfca7c", "text_length": 65800, "input_topic": "Reunion tours", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.671, "margin": 0.5053, "low_confidence": false, "label_confidences": {"fluff": 0.1657, "substantive": 0.671, "derailing": 0.1633}, "token_count": 256, "truncated": true, "preprocess_ms": 200.16, "inference_ms": 1207.14, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:51.421+00:00", "event": "prediction", "request_id": "504b2958f8c7470fae98504deda8506a", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 1200.99, "cold_start": false, "input_text": "lol same", "text_hash": "b545a3a88f03c01982bfc396ccd0c4b41147a96c4b32f43ac261166c2bcc424a", "text_length": 8, "input_topic": "Early 2000s pop punk reunion tours and vinyl pressings. Early 2000s pop punk reunion tours and vinyl pressings...", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.6129, "margin": 0.4126, "low_confidence": false, "label_confidences": {"fluff": 0.2003, "substantive": 0.6129, "derailing": 0.1868}, "token_count": 256, "truncated": true, "preprocess_ms": 7.96, "inference_ms": 1191.17, "corrected_label": null, "feedback": null}
     {"timestamp": "2026-11-15T22:05:51.609+00:00", "event": "prediction", "request_id": "e18f74ae976e4954b26c923595e53ff8", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 100.02, "cold_start": false, "input_text": "🔥🔥🔥 ??? !!! ... 💀💀", "text_hash": "072dc37dd80384075a626538b6648f53ea6ae989221d1258dd7c187f8f4e88e7", "text_length": 18, "input_topic": "Early 2000s pop punk", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "42a14c03678f2f9aa63939992a981168d27e4b69", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-5dcd7cc6b8-g2mm5", "chosen_label": "substantive", "confidence": 0.4786, "margin": 0.1981, "low_confidence": true, "label_confidences": {"fluff": 0.2805, "substantive": 0.4786, "derailing": 0.2409}, "token_count": 18, "truncated": false, "preprocess_ms": 0.2, "inference_ms": 13.77, "corrected_label": null, "feedback": null}
```

*Request Timeout Test Set*
```json
     {"timestamp": "2026-11-15T22:37:18.223+00:00", "event": "rejected", "request_id": "aafbe873869a4e6ea6cc16239d89909d", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 504, "latency_ms": 5001.09, "cold_start": true, "input_text": "Honestly the second album is better than the debut.", "text_hash": "963c947b0e870832b052eddf3ac9049b58b9ec9e3879991a4170c201e61c80fb", "text_length": 51, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "error_type": "timeout", "reason": "exceeded 5s limit", "stack_trace": null}
     {"timestamp": "2026-11-15T22:37:23.355+00:00", "event": "rejected", "request_id": "42aed292e33543cebc3922d835e3abe9", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 504, "latency_ms": 5000.47, "cold_start": false, "input_text": "lol this thread is wild", "text_hash": "95f920b90b81170f467eec889435fdc7cd4ea3240f5ce1b684c38a946fbeb531", "text_length": 23, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "error_type": "timeout", "reason": "exceeded 5s limit", "stack_trace": null}
     {"timestamp": "2026-11-15T22:37:28.465+00:00", "event": "rejected", "request_id": "414e285af813493a8209075ac2e29566", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 504, "latency_ms": 5002.13, "cold_start": false, "input_text": "Lossless streaming is indistinguishable from vinyl in blind tests.", "text_hash": "534348e0162b7bb59057cce19dac46d2565c497f44fb0855916453fa3005510f", "text_length": 66, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "error_type": "timeout", "reason": "exceeded 5s limit", "stack_trace": null}
     {"timestamp": "2026-11-15T22:37:33.572+00:00", "event": "rejected", "request_id": "ad97cf653aac4d06a9602c79421d1196", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 504, "latency_ms": 5000.6, "cold_start": false, "input_text": "You all just argue about nothing.", "text_hash": "7f8ec86e0f31633dcc6fbce4e590612e51ca60b89a83ca78447f3e45056b8332", "text_length": 33, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "error_type": "timeout", "reason": "exceeded 5s limit", "stack_trace": null}
     {"timestamp": "2026-11-15T22:37:38.685+00:00", "event": "rejected", "request_id": "a2af82e970824e08988c2a944e948097", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 504, "latency_ms": 5000.78, "cold_start": false, "input_text": "Mastering matters more than the format.", "text_hash": "d5a5769ec2b2fec38230bdc44edbb04079ffee58ff178f144c042b7475ca441d", "text_length": 39, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "error_type": "timeout", "reason": "exceeded 5s limit", "stack_trace": null}
     {"timestamp": "2026-11-15T22:37:38.767+00:00", "event": "prediction", "request_id": "44de4d7ac6344d19b4424aa44c4e703c", "endpoint": "/predict", "method": "POST", "client_id": "b458a9d7684e55af", "status_code": 200, "latency_ms": 12.57, "cold_start": false, "input_text": "Mastering matters more than the format.", "text_hash": "d5a5769ec2b2fec38230bdc44edbb04079ffee58ff178f144c042b7475ca441d", "text_length": 39, "input_topic": "Vinyl vs streaming sound quality", "topic_provided": true, "model_name": "takemeter-onnx", "model_version": "047d8a6239be", "model_quantized": true, "app_version": "e7fa2bbbe6195ba12fdc5ff773b82b1353bbff5e", "instance_id": "srv-dbsbhbjl550s7380o200-hibernate-7cb7c986b5-wt6f8", "chosen_label": "substantive", "confidence": 0.5512, "margin": 0.3218, "low_confidence": true, "label_confidences": {"fluff": 0.2294, "substantive": 0.5512, "derailing": 0.2194}, "token_count": 15, "truncated": false, "preprocess_ms": 0.17, "inference_ms": 11.19, "corrected_label": null, "feedback": null}
```


<!-- 
curl.exe -X POST https://ai201-project3-takemeter-starter-v2026.onrender.com/predict -H "Content-Type: application/json" -d '{\"text\":\"hello\",\"topic\":\"optional\"}' 

curl.exe -X POST https://ai201-project3-takemeter-starter-v2026.onrender.com/predict -H "Content-Type: application/json" -d "@sample_posts/sample1.json"

-->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
