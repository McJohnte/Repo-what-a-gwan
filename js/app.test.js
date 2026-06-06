// Minimal dependency-free test runner for the pure functions in app.js.
// Run with:  node js/app.test.js
import assert from "node:assert/strict";
import {
  addPost,
  deletePost,
  formatTimeAgo,
  loadPosts,
  savePosts,
} from "./app.js";

let passed = 0;
function test(name, fn) {
  fn();
  passed++;
  console.log(`  ✓ ${name}`);
}

console.log("Running app.test.js\n");

test("addPost prepends a new post and keeps existing ones", () => {
  const start = [{ id: "a", text: "old", createdAt: 1 }];
  const next = addPost(start, "hello", 1000);
  assert.equal(next.length, 2);
  assert.equal(next[0].text, "hello");
  assert.equal(next[1].id, "a");
  assert.equal(start.length, 1, "original array must not be mutated");
});

test("addPost trims whitespace", () => {
  const next = addPost([], "  spaced  ", 1000);
  assert.equal(next[0].text, "spaced");
});

test("addPost ignores empty / whitespace-only input", () => {
  const start = [];
  assert.equal(addPost(start, "   "), start);
  assert.equal(addPost(start, ""), start);
  assert.equal(addPost(start, null), start);
});

test("addPost stamps id and createdAt", () => {
  const [post] = addPost([], "hi", 12345);
  assert.equal(post.createdAt, 12345);
  assert.ok(typeof post.id === "string" && post.id.length > 0);
});

test("deletePost removes only the matching id", () => {
  const posts = [
    { id: "a", text: "1", createdAt: 1 },
    { id: "b", text: "2", createdAt: 2 },
  ];
  const next = deletePost(posts, "a");
  assert.deepEqual(next.map((p) => p.id), ["b"]);
  assert.equal(posts.length, 2, "original array must not be mutated");
});

test("formatTimeAgo covers the ranges", () => {
  const now = 1_000_000_000_000;
  assert.equal(formatTimeAgo(now, now), "just now");
  assert.equal(formatTimeAgo(now - 10_000, now), "just now");
  assert.equal(formatTimeAgo(now - 5 * 60_000, now), "5m ago");
  assert.equal(formatTimeAgo(now - 3 * 3_600_000, now), "3h ago");
  assert.equal(formatTimeAgo(now - 2 * 86_400_000, now), "2d ago");
});

test("save/load round-trips through storage", () => {
  const posts = addPost([], "persist me", 42);
  savePosts(posts);
  const loaded = loadPosts();
  assert.deepEqual(loaded, posts);
});

console.log(`\nAll ${passed} tests passed.`);
