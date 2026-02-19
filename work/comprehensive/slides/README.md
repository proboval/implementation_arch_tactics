# Presentation Slides

HTML-to-PPTX slide generation for the study guide presentation.

## Files

- `create_pptx.js` — Node.js script generating 33 HTML slides and converting to PPTX
- `slide-*.html` — Generated HTML slide files (720pt x 405pt, 16:9)
- `thumbnails-*.jpg` — Thumbnail grids for visual validation

## Generating the Presentation

```bash
cd slides
NODE_PATH="<path-to-pptx-skill>/scripts/node_modules" node create_pptx.js
```

Output: `../study_guide.pptx`

## Design

- **Palette**: Deep Navy (#1B2A4A), Teal (#2E86AB), Coral (#E8573A), Light (#F4F6F9)
- **Font**: Arial
- **33 slides** covering all 9 chapters with section dividers, data cards, and key takeaways
