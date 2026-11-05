
const root = document.documentElement;
const savedTheme = localStorage.getItem('stats-theme');
if (savedTheme) root.setAttribute('data-theme', savedTheme);

document.getElementById('theme-toggle').addEventListener('click', () => {
  const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('stats-theme', next);
});

document.getElementById('sidebar-toggle').addEventListener('click', () => {
  document.body.classList.toggle('nav-open');
});
document.querySelectorAll('.toc-link').forEach(a => a.addEventListener('click', () => {
  document.body.classList.remove('nav-open');
}));

const setGroupExpanded = (btn, expanded) => {
  btn.setAttribute('aria-expanded', String(expanded));
  btn.closest('.toc-module').querySelector('.submenu').hidden = !expanded;
};
document.querySelectorAll('.module-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    setGroupExpanded(btn, btn.getAttribute('aria-expanded') !== 'true');
  });
});

document.getElementById('collapse-all').addEventListener('click', () => {
  document.querySelectorAll('.module-toggle').forEach(btn => setGroupExpanded(btn, false));
});
document.getElementById('expand-all').addEventListener('click', () => {
  document.querySelectorAll('.module-toggle').forEach(btn => setGroupExpanded(btn, true));
});

document.getElementById('search-box').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('.toc > li').forEach(li => {
    if (li.classList.contains('toc-module')) {
      const subLinks = li.querySelectorAll('.submenu .toc-link');
      let anyMatch = false;
      subLinks.forEach(a => {
        const match = !q || a.textContent.toLowerCase().includes(q);
        a.parentElement.classList.toggle('search-hidden', !match);
        if (match) anyMatch = true;
      });
      const moduleLink = li.querySelector('.toc-module-link');
      const moduleMatch = !q || moduleLink.textContent.toLowerCase().includes(q);
      li.classList.toggle('search-hidden', !(anyMatch || moduleMatch));
      if (q && (anyMatch || moduleMatch)) setGroupExpanded(li.querySelector('.module-toggle'), true);
    } else {
      const a = li.querySelector('.toc-link');
      const match = !q || a.textContent.toLowerCase().includes(q);
      li.classList.toggle('search-hidden', !match);
    }
  });
});

document.querySelector('.toc-link[aria-current="page"]')?.scrollIntoView({ block: 'nearest' });

const backBtn = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
  backBtn.style.display = window.scrollY > 600 ? 'block' : 'none';
});
backBtn.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

(function () {
  const wrap = document.querySelector('.wf-wrap');
  if (!wrap) return;
  const grid = wrap.querySelector('.wf');
  const svg = wrap.querySelector('.wf-lines');
  const edges = JSON.parse(wrap.dataset.edges);
  const MIN_WIDTH = 760, RADIUS = 9, BUS = 20, NS = 'http://www.w3.org/2000/svg';

  const rounded = (pts) => {
    let d = `M${pts[0].x},${pts[0].y}`;
    for (let i = 1; i < pts.length - 1; i++) {
      const prev = pts[i - 1], cur = pts[i], next = pts[i + 1];
      const r1 = Math.min(RADIUS, Math.hypot(cur.x - prev.x, cur.y - prev.y) / 2);
      const r2 = Math.min(RADIUS, Math.hypot(next.x - cur.x, next.y - cur.y) / 2);
      const a = { x: cur.x + Math.sign(prev.x - cur.x) * r1, y: cur.y + Math.sign(prev.y - cur.y) * r1 };
      const b = { x: cur.x + Math.sign(next.x - cur.x) * r2, y: cur.y + Math.sign(next.y - cur.y) * r2 };
      d += ` L${a.x},${a.y} Q${cur.x},${cur.y} ${b.x},${b.y}`;
    }
    const last = pts[pts.length - 1];
    return d + ` L${last.x},${last.y}`;
  };

  const draw = () => {
    svg.querySelectorAll('path').forEach(p => p.remove());
    grid.querySelectorAll('.wf-label').forEach(el => el.remove());
    if (wrap.clientWidth < MIN_WIDTH) return;

    const origin = grid.getBoundingClientRect();
    const box = (id) => {
      const r = grid.querySelector(`[data-node="${id}"]`).getBoundingClientRect();
      return { l: r.left - origin.left, r: r.right - origin.left, t: r.top - origin.top, b: r.bottom - origin.top,
               cx: (r.left + r.right) / 2 - origin.left, cy: (r.top + r.bottom) / 2 - origin.top };
    };
    const items = edges.map(([from, to, label, dashed]) => {
      const s = box(from), t = box(to);
      const [sideS, sideT] = t.t >= s.b - 1 ? ['b', 't'] : t.l >= s.r - 1 ? ['r', 'l'] : ['l', 'r'];
      return { from, to, label, dashed, s, t, sideS, sideT };
    });

    // Several arrows on one side of a box are spread out, ordered by where they come from / go to.
    const slots = new Map();
    items.forEach(it => {
      [['s', it.from, it.sideS, it.t], ['t', it.to, it.sideT, it.s]].forEach(([end, id, side, other]) => {
        const key = id + '|' + side;
        if (!slots.has(key)) slots.set(key, []);
        slots.get(key).push({ it, end, side, other });
      });
    });
    const anchor = (b, side, f) => side === 'b' ? { x: b.l + (b.r - b.l) * f, y: b.b }
      : side === 't' ? { x: b.l + (b.r - b.l) * f, y: b.t }
      : side === 'r' ? { x: b.r, y: b.t + (b.b - b.t) * f } : { x: b.l, y: b.t + (b.b - b.t) * f };
    slots.forEach(list => {
      const vertical = list[0].side === 'b' || list[0].side === 't';
      list.sort((p, q) => vertical ? p.other.cx - q.other.cx : p.other.cy - q.other.cy);
      list.forEach((entry, i) => {
        const own = entry.end === 's' ? entry.it.s : entry.it.t;
        entry.it[entry.end + 'p'] = anchor(own, entry.side, (i + 1) / (list.length + 1));
      });
    });

    items.forEach(it => {
      const a = it.sp, b = it.tp;
      let pts;
      if (it.sideS === 'b') {
        const midY = Math.max(a.y + 10, b.y - BUS);
        pts = Math.abs(a.x - b.x) < 1 ? [a, b] : [a, { x: a.x, y: midY }, { x: b.x, y: midY }, b];
      } else {
        const midX = (a.x + b.x) / 2;
        pts = Math.abs(a.y - b.y) < 1 ? [a, b] : [a, { x: midX, y: a.y }, { x: midX, y: b.y }, b];
      }
      const path = document.createElementNS(NS, 'path');
      path.setAttribute('d', rounded(pts));
      path.setAttribute('marker-end', 'url(#wf-arrow)');
      if (it.dashed) path.setAttribute('class', 'wf-dashed');
      svg.appendChild(path);

      if (it.label) {
        const el = document.createElement('span');
        el.className = 'wf-label';
        el.textContent = it.label;
        const first = pts[1];
        el.style.left = (it.sideS === 'b' ? a.x : (a.x + first.x) / 2) + 'px';
        el.style.top = (it.sideS === 'b' ? a.y + Math.min(12, (first.y - a.y) / 2 + 2) : a.y) + 'px';
        grid.appendChild(el);
      }
    });
  };

  new ResizeObserver(draw).observe(wrap);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
  draw();
})();
