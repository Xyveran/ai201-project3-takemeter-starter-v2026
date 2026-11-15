# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

**Overall accuracy is at least 0.80 on the held-out set, in every one of the three seeds.**

**Why this target:** About 0.68 of the data (158 of 232) is marked `substantive`, so a model that always guessed `substantive` would score about 0.68 despite not learning anything. A score of 0.80 is a twelve point gain and would make the classifier useful.

---

## 2. Per-label F1 for the common labels

**`substantive` has an F1 of at least 0.80 and `fluff` has an F1 of at least 0.65, in every seed.**

**Why this target:** `substantive` is 68% of my data, so it should be the easiest label and gets the strictest number. `fluff` has 60 examples, so 0.65 is looser: one or two misclassified posts move its F1 several points, and I don't want to miss a target on noise.

---

## 3. Balanced performance

**Macro-averaged F1 is at least 0.65 on the held-out set, in every seed.**

**Why this target:** Accuracy hides the lopsidedness of the data. A model can hit 0.78 by being great on `substantive` and ignoring the other two. Macro-F1 weights `fluff` and `derailing` equally with `substantive`, so it can't be passed that way. It is lower than my accuracy target because `derailing` will drag the average down.

---

## 4. Rare label: `derailing`

**`derailing` has a recall of at least 0.50 and an F1 of at least 0.40, in every seed.**

**Why this target:** I only have 14 `derailing` examples, and each one is worth a third of recall, which means its F1 will jump between seeds however good the model is. That is why this target is the loosest of the five. I picked recall alongside F1 because for a take-quality tool, missing a derailing post matters more than flagging a post that turns out to be fine. 0.40 F1 is still above what a model that never predicts `derailing` gets, which is 0.

---

## 5. Dataset balance

**Before training, no label is below 10% of the dataset (at least 24 of 232 examples), and `substantive` is no more than 65%.**

**Why this target:** Right now this fails: `derailing` is 14 of 232 (6%) and `substantive` is 68%. 14 examples is the root cause of the unstable `derailing` score in criterion 4. I'd rather add at least 10 more `derailing` examples, targeted at the posts I found hardest to label, than lower a number later.

---

# Capstone Criteria

## 1. Malformed Inputs 

**Requests with malformed inputs return a 400-class error code instead of reaching the model in 10/10 calls.**

**Why this target:** A malformed request (empty or whitespace-only text, missing fields, wrong types) is a failure that a caller can cause on purpose, so it can be tested every time and anything below 10/10 means a gap in validation. If bad input reaches the model it produces a confident label for text that isn't a post, which is a waste of resources. A 400 also tells the caller the fault is theirs, where a 500 would look like a bug in the service.

## 2. Logged Results

**Successful service calls log a timestamp, client_id, input_text, chosen_label, and confidence in 10/10 calls.**

**Why this target:** The log is the only way I can see what the classifier did after deployment, such as which labels it picks and how confident it is, so a successful call missing any of these fields leaves an irreparable hole. Each field answers a question I'll have later: client_id for who, input_text for what, and chosen_label and confidence for how the model behaved. It has to be 10/10 because a call that goes unlogged leaves no trace to find afterward.

## 3. Response Latency

**The deployed `/predict` endpoint responds in under 1 second in 9 of 10 calls.**

**Why this target:** The service runs on a Render instance that hibernates when idle, so the first call after some time needs to endure a cold-start. I've chosen one slow call in ten because a take-quality check that regularly takes longer than 1 second could deter someone from using the service.

## 4. Timeout Handling

**When a request exceeds the time limit, the service returns an error message and stays up in 5 of 5 forced timeouts.**

**Why this target:** A timeout is a failure I can trigger on purpose, so it can be tested every time and 5 of 5 is a fair bar. A cold-starting instance is the most likely place for a real timeout, and a crash there would take the endpoint down for the next caller too. I want a readable message with the service still answering afterward.

## 5. Cost per Run

**Each prediction costs less than $0.01 in 10 of 10 calls.**

**Why this target:** The model is a quantized ONNX file served from my own instance, so a prediction has no per-call API charge and its cost is only a small slice of compute time. If a call ever approaches a cent, something's gone wrong. 10 of 10 is therefore the right bar, because I expect this criterion to hold every time.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

