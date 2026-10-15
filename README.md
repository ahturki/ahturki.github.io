# Ahmed Turki · personal site

Single `index.html` with inline CSS and a small vanilla JS block (name reveal, scroll reveals, custom cursor). No build step. Live at https://ahturki.github.io once Pages is on.

## Files

Everything lives in `assets/`. Paths are case-sensitive on GitHub Pages.

| File | Used for |
|---|---|
| `photo.jpg` | Portrait (cropped and compressed from `photo.png`, which the page does not load) |
| `copart_logo.png` (cropped from `copart.png`), `FTAI.png`, `SUMCO.png` | Logos on the pitch cards |
| `CPRT_Memo.pdf`, `FTAI_Memo.pdf` | "Memo" buttons |
| `The_Cradles_of_Planets_Review_Paper.pdf` | "Paper" button |
| `hltau.jpg` | Paper card image (Fig. 1 of the paper, ALMA (ESO/NAOJ/NRAO)) |
| `Ahmed_Turki_Resume.pdf` | Resume buttons. **Not uploaded yet.** |

**SUMCO memo:** upload it as `assets/SUMCO_Memo.pdf`, then uncomment the button block marked in the SUMCO card in `index.html`.

**Current research card:** deliberately broad (the question only). Do not add method, data sources or results there until the paper is out.

## Deploy

Repo **Settings > Pages**: Source = "Deploy from a branch", Branch = `main`, folder `/ (root)`. Each push to `main` redeploys in a minute or two.
