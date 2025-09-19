# Frontend

Static site served from S3 that helps players find the correct subscription URL.

- `index.html` — main picker UI used in production.
- `legacy-index.html` — minimal legacy landing page retained for reference.
- `script.js` — fetches season/division/team data from S3 and builds the calendar URL.
- `styles.css` — layout and theming.

Open `frontend/index.html` in a browser or sync the directory to your static hosting bucket when deploying.
