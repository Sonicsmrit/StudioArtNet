# Studio Art Net

A fine-tuned ResNet-50 classifier that predicts which anime studio produced a given frame, based on visual rendering style rather than character or content recognition. Built as part of a self-directed 30-week ML curriculum project (transfer learning + explainability module).

## Motivation

I wanted to see if it's possible to separate anime studios by art style. So I tried it!

## Classes

Seven major anime studios, each represented by 3–4 shows chosen to control for era (roughly 2013–2023) and to avoid over-indexing on a single show's specific characters or color palette:

| Studio | Shows |
|---|---|
| MAPPA | Jujutsu Kaisen, Chainsaw Man, Attack on Titan: The Final Season |
| ufotable | Demon Slayer, Fate/Stay Night: Unlimited Blade Works, Fate/Zero (+ S2) |
| Trigger | Kill la Kill, Little Witch Academia (TV), Cyberpunk: Edgerunners |
| Wit Studio | Attack on Titan (S1–2), Vinland Saga, Ranking of Kings |
| Bones | My Hero Academia, Mob Psycho 100 (+ II), Fullmetal Alchemist: Brotherhood |
| Madhouse | One Punch Man, Hunter x Hunter (2011), Overlord (+ II) |
| Kyoto Animation | Violet Evergarden, Hyouka, Miss Kobayashi's Dragon Maid (+ S), Sound! Euphonium, Free! |

## Dataset

- **Source**: screencap frames scraped per-episode from a screenshot archive site, ~4 images per episode across all available episodes per show.
- **Deduplication**: perceptual hashing (`imagededup`, PHash, distance threshold 10) to remove near-identical sequential frames, since raw scraping pulled consecutive frames from the same scene.
- **Balancing**: post-dedup counts varied significantly by studio (185–736 images). Thinner classes (Kyoto Animation, Trigger) were supplemented with additional same-era, same-genre-lane shows; all classes were then randomly downsampled to a common target of **320 images per studio** (2,240 images total) to avoid class-imbalance bias.
- **Split**: 70/15/15 train/val/test, applied independently per class (224 / 48 / 48 per studio), split before any augmentation.

## Model & Training

Two-stage transfer learning on a pretrained ResNet-50:

**Stage 1 — head-only.** All layers frozen except a newly initialized FC layer (2048 → 7). Trained 5 epochs at `lr=1e-3` (Adam), only on the FC head. Ends around 66% train / 55% val accuracy — confirms the head is learning real signal before touching the backbone.

**Stage 2 — partial unfreeze.** `layer3` and `layer4` unfrozen alongside the FC head, trained at `lr=1e-4` (10x lower than stage 1) for up to 10 epochs. Val loss consistently bottoms out around **epoch 3** across repeated runs (val loss ≈0.96, val accuracy ≈66%), after which train accuracy keeps climbing to ~99–100% while val loss climbs — a clear, reproducible overfitting signal given the small per-class dataset. The epoch-3 checkpoint (lowest val loss) is used as the final model rather than the final epoch.

## Explainability — Grad-CAM findings

Grad-CAM (`pytorch-grad-cam`, hooked on `layer4[-1]`) was run across correctly and incorrectly classified test images from all 7 classes to inspect *what* the model actually learned to key on. This produced the project's most interesting result: **the model's real learned signal varies significantly by studio, and is often not "art style" in the intended sense.**

- **Kyoto Animation, Bones, MAPPA, Madhouse** — activation consistently concentrates on faces and character features. Plausibly legitimate (facial rendering is part of studio style) but also plausibly confounded with specific recurring character designs.
- **Wit Studio** — activation consistently concentrates on stone/brick/architectural textures and backgrounds, confirmed across both correct and incorrect predictions. This is a genre/setting confound: all three source shows (AoT, Vinland Saga, Ranking of Kings) are architecture/ruins-heavy, so the model appears to have learned "stone texture → Wit Studio" rather than Wit Studio's actual line/shading style. This shortcut was directly observed causing misclassifications of Bones and Trigger images that happened to contain similar architectural/rocky content.
- **Trigger** — the most mixed class: some images show attention tracing dynamic linework/action silhouettes (a genuinely style-relevant signal), others show face/expression fixation, and one misclassification (Trigger → Wit Studio) was driven by rocky terrain in the background.
- **ufotable** — Background and Character faces driven.

**Takeaway**: aggregate accuracy alone understates how much of the model's behavior is driven by genre/setting overlap between shows rather than by the intended target (studio rendering style).

## Notes on limitations

- Class sizes are small (224 train images/class) by deep learning standards, a meaningful factor in both the overfitting pattern seen in stage 2 and the genre/content confounds surfaced by Grad-CAM.
- Only trained/raw model weights and code are published in this repository. No scraped image dataset is redistributed.

## This is not good enough!

Change the entire dataset, from test, val, and train getting the same anime to now, test getting the 320 images from the shows that already exist, and test and val getting new shows entirely!!
