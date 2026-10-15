# Ahmed Turki · Equity Research site

One-page portfolio for the Citadel Associate Program application. Single `index.html` with inline CSS and a small vanilla JS block (hero text reveal, scroll reveals, custom cursor, live clock). No build step.

## Folder structure

```
/index.html
/assets/favicon.svg
/assets/Ahmed_Turki_Resume.pdf      <- add
/pitches/SUMCO_Memo.pdf             <- add
/pitches/SUMCO_Deck.pdf             <- add
/pitches/SUMCO_Model.xlsx           <- add
/pitches/CPRT_Memo.pdf              <- add
/pitches/CPRT_Deck.pdf              <- add
/pitches/CPRT_Model.xlsx            <- add
/pitches/FTAI_Memo.pdf              <- add
/pitches/FTAI_Deck.pdf              <- add
/pitches/FTAI_Model.xlsx            <- add
```

GitHub Pages paths are case-sensitive. `CPRT_memo.pdf` will 404 if the link says `CPRT_Memo.pdf`.

## Filling in placeholders

Every missing input is wrapped in `<span class="ph">[...]</span>`, which renders as an amber highlight. Replace the whole span (tags included) with your text. Before publishing, this should return nothing:

```
grep -n 'class="ph"\|\[LINKEDIN_URL\]\|\[EMAIL\]' index.html
```

Other edits:

- **Direction tag**: change `<span class="dir">...</span>` to `<span class="dir long">LONG</span>` or `<span class="dir short">SHORT</span>`.
- **Implied return color**: add `class="pos"` or `class="neg"` to the Implied `<dd>`.
- **FTAI short report row**: delete the `Short report` `<dt>`/`<dd>` pair if the pitch is SHORT.
- **Pitch order**: cut and paste whole `<details class="row">` blocks and renumber the `01`, `02`, `03` labels.
- **Linking straight to a pitch**: `https://ahturki.github.io/#cprt` (or `#sumco`, `#ftai`) scrolls to that pitch and opens it.

## Deploy to GitHub Pages

1. On GitHub, create a new **public** repo named exactly `ahturki.github.io`.
2. Copy `index.html`, `assets/`, and `pitches/` (with all nine files and the resume) into it:
   ```
   git clone https://github.com/ahturki/ahturki.github.io.git
   cd ahturki.github.io
   # copy files in
   git add -A && git commit -m "Initial site" && git push
   ```
3. Repo **Settings > Pages**: Source = "Deploy from a branch", Branch = `main`, folder `/ (root)`. Save.
4. Wait 1 to 2 minutes, then open `https://ahturki.github.io`.
5. Click every link once (resume, nine pitch files, LinkedIn, GitHub, email) in a private window.
6. Run Lighthouse (Chrome DevTools > Lighthouse > Mobile) against the live URL.
7. Paste the link into a Slack or LinkedIn draft to check the preview card.
