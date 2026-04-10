# Study Roadmap: YOLOv8, YOLO11, and YOLO26 Adversarial Patches

This roadmap is designed for a capstone-style project where you need something that is both academically grounded and realistically finishable.

## Phase 1: Literature Grounding

Read these first:

1. Brown et al. for the universal patch concept.
2. DPatch for detector-specific attacks.
3. Thys et al. for person-vanishing against YOLO.
4. Hu et al. for naturalistic patch generation.
5. Gala et al. for modern Ultralytics YOLO coverage.

Output from this phase:

- One page of notes per paper using `docs/notes/paper_review_template.md`
- A table of attack assumptions: white-box vs black-box, digital vs physical, classifier vs detector, universal vs per-image

## Phase 2: Reproduce a Baseline

Use the local `create_adv_patch.py` baseline to understand the mechanics:

- confirm you can train a patch
- inspect patch placement and size effects
- compare clean vs patched detection output

This phase is about workflow literacy, not model fidelity. The local script uses YOLOv5 because it is simpler to get running with ART.

## Phase 3: Move to Ultralytics Models

Your main evaluation set should be:

- `yolov8n.pt`
- `yolo11n.pt`
- `yolo26n.pt`

Recommended first comparison:

- same dataset
- same patch scale
- same patch placement policy
- same victim class
- same evaluation metric

Suggested metrics:

- clean mAP or recall
- patched mAP or recall
- attack success rate
- confidence drop for the victim class
- transfer success across model families

## Phase 4: Answer a Real Research Question

Good capstone questions for this repo:

1. Does a patch trained on YOLOv8 transfer to YOLO11 and YOLO26?
2. Are newer Ultralytics models more robust, or just differently fragile?
3. Does end-to-end NMS-free YOLO26 change patch behavior in a measurable way?
4. Are smaller edge-oriented models consistently more vulnerable than medium models?

## Suggested Experimental Matrix

Minimal matrix:

| Train On | Test On | Patch Type | Victim Class | Dataset |
|---|---|---|---|---|
| YOLOv8n | YOLOv8n, YOLO11n, YOLO26n | universal | person | INRIA Person |
| YOLO11n | YOLOv8n, YOLO11n, YOLO26n | universal | person | INRIA Person |
| YOLO26n | YOLOv8n, YOLO11n, YOLO26n | universal | person | INRIA Person |

Then expand by:

- patch scale
- digital vs printed evaluation
- n vs s vs m model size

## Practical Advice

- Start with the `n` models. They are faster and usually easier to attack.
- Keep the first study narrow: one victim class, one dataset, one patch family.
- Do not mix too many patch paradigms at once. First compare model families, then compare attack methods.
- Treat YOLO26 as a likely research-gap target unless you later find stronger patch-specific literature.
