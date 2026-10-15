# Ahmed Turki · personal site

Single `index.html` with inline CSS and a small vanilla JS block (name reveal, scroll reveals, custom cursor). No build step. Live at https://ahturki.github.io once Pages is on.

## Files to add

Paths are case-sensitive on GitHub Pages.

```
assets/photo.jpg               your portrait, about 800 x 1000 px
assets/Ahmed_Turki_Resume.pdf

pitches/SUMCO_Deck.pdf         "Pitch" button
pitches/SUMCO_Model.xlsx       "Model" button
pitches/SUMCO_cover.jpg        card background, about 1200 x 1500 px (optional)
pitches/CPRT_Deck.pdf
pitches/CPRT_Model.xlsx
pitches/CPRT_cover.jpg
pitches/FTAI_Deck.pdf
pitches/FTAI_Model.xlsx
pitches/FTAI_cover.jpg

research/Paper.pdf
research/paper_figure.png      paper card background, wide, about 2100 x 900 px (optional)
research/current_figure.png    current-research card background (optional)
```

Any missing image falls back to a dark card with a large watermark, so nothing looks broken. Good card backgrounds: the title slide of the deck, a photo of the company's product or facility, or the strongest figure from the paper. Pick images with a darker lower third so the white title stays readable.

No model for a pitch? Delete that `<li>` with the Model button.

## Filling in placeholders

Every missing input is wrapped in `<span class="ph">[...]</span>` (amber highlight). Replace the whole span. Before publishing, this should return nothing:

```
grep -n 'class="ph"\|\[LINKEDIN_URL\]\|\[EMAIL\]\|\[ARXIV_OR_DOI_URL\]' index.html
```

The "In progress" research card is optional: delete its `<article>` and change `(02)` to `(01)` in the section header.

## Deploy

Repo **Settings > Pages**: Source = "Deploy from a branch", Branch = `main`, folder `/ (root)`. Each push to `main` redeploys in a minute or two.
