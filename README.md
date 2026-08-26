# Ground Effect — WebAR POC (Eletre X launch)

A no-app, browser-based AR activation for the **Type 79 / ground-effect** car display.
Guest scans a code → phone browser opens → live camera feed with **yellow ground-effect
airflow streaming under a ghosted car**, reacting to how they tilt and sweep the phone.

Works on **iPhone (Safari) and Android (Chrome)** — no download, no app store, no licence.

## What's in here
- `index.html` — the whole experience, one self-contained file.
- `make_qr.py` — generates the scan code + branded table card. **Edit the `URL` at the top first.**
- `qr_raw.png` — the bare scan code (Lotus-Yellow on black).
- `scan_card.png` — A5 table card with the code, ready to print for a plinth.

## Test it on your phone in ~2 minutes
The one hard rule: **the camera only works over HTTPS.** You can't open the file
directly (`file://`) or over plain localhost from another device. Two easy options:

**Option A — Netlify Drop (fastest, free, no account needed)**
1. Go to https://app.netlify.com/drop
2. Drag this whole folder onto the page.
3. It gives you a live `https://…netlify.app` link.
4. Open that link on your phone → tap **Begin** → **Allow** camera + motion.

**Option B — GitHub Pages**
1. New repo → upload `index.html` → Settings → Pages → deploy from `main`.
2. Use the `https://…github.io/…` link on your phone.

Then put your live link into `make_qr.py` (the `URL =` line), run `python3 make_qr.py`,
and `scan_card.png` regenerates pointing at it.

## What it proves vs. what a production build adds
This POC is a **camera passthrough + composited airflow layer** driven by the phone's
gyroscope. It reads as AR and is bulletproof across devices — deliberately chosen over
true SLAM AR (WebXR), which **does not run on iOS Safari** and would leave iPhone guests
with a black screen at the event.

A production version would add:
- A proper 3D Eletre X / Type 79 model (glTF) instead of the ghost silhouette.
- Surface detection so the car "sits" on the real floor (8th Wall — paid licence — if you
  want world-locked AR that still works on iOS).
- Real CFD-style airflow art directed with the 3D team.
- A short capture/share-back so the guest leaves with a clip (ties to "what goes home").

## Branding notes (kept to the launch rules)
- Black + Lotus Yellow `#FFF200`, Overpass, the straight-line-that-bends as design DNA.
- Guest-facing wording is **Lotus / Eletre X** only — no "Rule Bender", no ENIGMA/AGMC.
- Copy is plain: "Scan to see the floor work", "Point your phone under the car".
