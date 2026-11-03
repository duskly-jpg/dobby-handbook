// render.js — fetch markdown + marked 渲染，无构建依赖
const content = document.getElementById("content");
const navLinks = document.querySelectorAll("nav a[data-page]");

function setActive(link) {
  navLinks.forEach(a => a.classList.remove("active"));
  link.classList.add("active");
}

async function load(page) {
  content.innerHTML = '<p class="loading">加载中…</p>';
  try {
    const r = await fetch(page);
    if (!r.ok) throw new Error(r.status);
    const md = await r.text();
    content.innerHTML = '<div class="markdown-body">' + marked.parse(md) + "</div>";
    content.scrollTop = 0;
    window.scrollTo(0, 0);
    // 相对链接的 md 互相跳转
    content.querySelectorAll("a[href$='.md']").forEach(a => {
      a.addEventListener("click", e => {
        e.preventDefault();
        load(new URL(a.getAttribute("href"), "pages/").pathname.replace(/^\//, ""));
      });
    });
  } catch (e) {
    content.innerHTML = '<p class="loading">加载失败: ' + e.message + "</p>";
  }
}

navLinks.forEach(a => a.addEventListener("click", () => { setActive(a); load(a.dataset.page); }));
setActive(navLinks[0]);
load(navLinks[0].dataset.page);
