# What A Gwan? 🌴

A tiny, dependency-free status-board web app. Post a short update on *what's
going on* and it appears at the top of a live feed. Posts are saved in your
browser (`localStorage`), so they survive a page reload.

No frameworks, no build step, no backend — just open it and go.

## Features

- Post short statuses (up to 140 characters) with a live character counter.
- Newest posts appear first; delete any post with one click.
- Persists across reloads via `localStorage`.
- User text is rendered as plain text (no HTML injection).
- Responsive, mobile-friendly dark UI.

## Run it

Any static file server works. For example:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

or

```bash
npx serve
```

You can also just open `index.html` directly in a browser (most features work;
a server is recommended so ES module loading behaves consistently).

## Test it

The core logic lives in pure functions that are unit-tested without a DOM:

```bash
node js/app.test.js
```

## Project structure

```
index.html        markup: header, post form, feed
css/styles.css    responsive styling
js/app.js         pure logic (exported) + browser DOM wiring
js/app.test.js    unit tests for the pure functions
```
