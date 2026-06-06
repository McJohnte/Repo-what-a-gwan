// "What A Gwan?" — a tiny status-board app.
// Logic is split into pure functions (exported + unit-tested) and DOM wiring
// (only runs in a browser). No dependencies, no build step.

const STORAGE_KEY = "what-a-gwan.posts";

// --- Storage abstraction ---------------------------------------------------
// Uses localStorage in the browser, falls back to an in-memory store in Node
// (so the pure functions are testable without a DOM).
const memoryStore = {};
function getStorage() {
  try {
    if (typeof localStorage !== "undefined") return localStorage;
  } catch (_) {
    /* accessing localStorage can throw in some sandboxed contexts */
  }
  return {
    getItem: (k) => (k in memoryStore ? memoryStore[k] : null),
    setItem: (k, v) => {
      memoryStore[k] = String(v);
    },
  };
}

// --- Pure-ish logic --------------------------------------------------------
export function loadPosts() {
  const raw = getStorage().getItem(STORAGE_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (_) {
    return []; // corrupt data — start fresh rather than crash
  }
}

export function savePosts(posts) {
  getStorage().setItem(STORAGE_KEY, JSON.stringify(posts));
  return posts;
}

export function addPost(posts, text, now = Date.now()) {
  const trimmed = String(text == null ? "" : text).trim();
  if (!trimmed) return posts; // ignore empty/whitespace-only input
  const post = {
    id: `${now}-${Math.random().toString(36).slice(2, 8)}`,
    text: trimmed,
    createdAt: now,
  };
  return [post, ...posts];
}

export function deletePost(posts, id) {
  return posts.filter((p) => p.id !== id);
}

export function formatTimeAgo(createdAt, now = Date.now()) {
  const seconds = Math.max(0, Math.floor((now - createdAt) / 1000));
  if (seconds < 45) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

// --- DOM wiring (browser only) ---------------------------------------------
function initDom() {
  const form = document.getElementById("post-form");
  const input = document.getElementById("post-input");
  const feed = document.getElementById("feed");
  const emptyState = document.getElementById("empty-state");
  const charCount = document.getElementById("char-count");

  let posts = loadPosts();

  function render() {
    feed.replaceChildren();
    emptyState.hidden = posts.length > 0;

    for (const post of posts) {
      const li = document.createElement("li");
      li.className = "post";

      const body = document.createElement("div");
      body.className = "post__body";

      const text = document.createElement("p");
      text.className = "post__text";
      text.textContent = post.text; // textContent => no HTML injection

      const time = document.createElement("span");
      time.className = "post__time";
      time.textContent = formatTimeAgo(post.createdAt);

      body.append(text, time);

      const del = document.createElement("button");
      del.className = "post__delete";
      del.type = "button";
      del.setAttribute("aria-label", "Delete post");
      del.textContent = "✕";
      del.addEventListener("click", () => {
        posts = deletePost(posts, post.id);
        savePosts(posts);
        render();
      });

      li.append(body, del);
      feed.append(li);
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const next = addPost(posts, input.value);
    if (next === posts) return; // nothing added (empty input)
    posts = savePosts(next);
    input.value = "";
    updateCount();
    render();
    input.focus();
  });

  function updateCount() {
    charCount.textContent = String(input.maxLength - input.value.length);
  }
  input.addEventListener("input", updateCount);

  updateCount();
  render();
}

if (typeof document !== "undefined") {
  initDom();
}
