# ꧁⎝StudioArtNet⎠꧂
ResNet-50 classifier that predicts which anime studio produced a given frame, based on visual style rather than character content.

## Classes

| Studio | Training shows |
|---|---|
| MAPPA | Jujutsu Kaisen, Chainsaw Man, Attack on Titan: The Final Season |
| ufotable | Demon Slayer, Fate/Stay Night: Unlimited Blade Works, Fate/Zero (+ S2) |
| Trigger | Kill la Kill, Little Witch Academia (TV), Cyberpunk: Edgerunners, SSSS.Gridman, SSSS.Dynazenon, Kiznaiver |
| Wit Studio | Attack on Titan (S1–2), Vinland Saga, Ranking of Kings |
| Bones | My Hero Academia, Mob Psycho 100 (+ II), Fullmetal Alchemist: Brotherhood |
| Madhouse | One Punch Man, Hunter x Hunter (2011), Overlord (+ II) |
| Kyoto Animation | Violet Evergarden, Hyouka, Miss Kobayashi's Dragon Maid (+ S), Sound! Euphonium (2, 3), Free! (+ Eternal Summer) |

## Dataset

- Frames scraped per-episode from a screencap archive, ~4 images/episode.
- Deduplicated with `imagededup` (PHash, threshold 10).
- Train: 320 images/studio, randomly balanced across classes (2,240 total).
- Val/test: separate, unseen shows per studio — no overlap with training shows.

| Studio | Val show | Test show |
|---|---|---|
| MAPPA | Dorohedoro | Banana Fish |
| ufotable | God Eater | Tales of Zestiria the X |
| Trigger | Space Patrol Luluco | BNA: Brand New Animal |
| Wit Studio | Kabaneri of the Iron Fortress | Vivy: Fluorite Eye's Song |
| Bones | Noragami | Bungo Stray Dogs |
| Madhouse | Parasyte -the maxim- | Death Parade |
| Kyoto Animation | Tamako Market | Beyond the Boundary |

## Model

Two-stage transfer learning, pretrained ResNet-50:

1. **Head-only**: backbone frozen, FC layer (2048 → 7) trained 5 epochs, `lr=1e-3`.
2. **Partial unfreeze**: `fc` and `layer4` unfrozen, `lr=1e-4`. Best checkpoint selected by lowest val loss.

## Results

- Test accuracy: **~35%** (random baseline for 7 classes: ~14%).
- Train accuracy reaches 95–100% within a few epochs regardless of configuration (full unfreeze, unfreeze + crop augmentation, `layer4`-only unfreeze) — all three land in the same 34–37% val range.
- Per-class recall (confusion matrix):
  - Trigger: ~68% — best-generalizing class. ヽ(・∀・)ノ
<img width="678" height="637" alt="image" src="https://github.com/user-attachments/assets/84941be5-6f31-4fe5-b5f4-f9d9b3f5b6a3" />

## Explainability (Grad-CAM)

`pytorch-grad-cam`, hooked on `layer4[-1]`, run on both correct and incorrect predictions:

- **Kyoto Animation, Bones, MAPPA, Madhouse**: activation concentrates on faces/character features.
- **Wit Studio**: activation concentrates on stone/brick/architectural background textures, not character rendering. All three training shows (AoT, Vinland Saga, Ranking of Kings) are architecture-heavy — model learned "stone texture → Wit Studio" rather than an actual style. Confirmed by confusion matrix: this didn't transfer to new content (Kabaneri, Vivy).
- **Trigger**: correct predictions on unseen-show images trace linework/silhouette and full-scene composition, not just faces — consistent with its higher held-out recall.
- **ufotable**: background- and face-driven.

### Examples of Grad-CAM's findings:
<img width="585" height="675" alt="Screenshot (98)" src="https://github.com/user-attachments/assets/8bcdacee-330a-4eb7-9e64-67e9a8ca6194" />
<img width="590" height="613" alt="Screenshot (95)" src="https://github.com/user-attachments/assets/18765c16-84a8-4ca7-9a81-53d5a5d2ade7" />


## Limitations

- 320 train images/class is small; contributes to the fast overfitting in stage 6.
