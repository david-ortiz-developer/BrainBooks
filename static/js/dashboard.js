/* Dashboard demo JS
   - Injects demo data into DOM
   - Handles modal video playback
   - Animates bars and counters
*/

document.addEventListener("DOMContentLoaded", ()=> {
  
  // --- Fill header/profile ---
  document.getElementById("user-name").textContent = `Hola, ${user.name}`;
  document.getElementById("user-score").textContent = `Puntaje: ${user.score}`;
  document.getElementById("profile-name").textContent = user.name;
  document.getElementById("score-big").textContent = user.score;
  document.getElementById("progress-fill").style.width = `${user.progress}%`;
  document.getElementById("progress-meta").textContent = `${user.tasksDone}/${user.tasksTotal} tareas`;

  // --- KPIs ---
  document.getElementById("kpi-1").textContent = kpis.delivery;
  document.getElementById("kpi-2").textContent = kpis.models;
  document.getElementById("kpi-3").textContent = kpis.feedback;
  document.getElementById("kpi-4").textContent = kpis.incidents;
  document.getElementById("kpi-5").textContent = kpis.earnings;
  document.getElementById("kpi-6").textContent = kpis.clusters;

  // --- Feed ---
  const feedRoot = document.getElementById("feed");
  feed.forEach(item => {
    const node = document.createElement("div");
    node.className = "feed-item";
    node.innerHTML = `
      <div class="feed-avatar">${item.author.charAt(0)}</div>
      <div class="feed-body">
        <div class="feed-meta"><strong>${item.author}</strong> · <span>${item.time}</span></div>
        <div class="feed-text">${item.text}</div>
        <div class="feed-actions">
          <button class="btn small" data-author="${item.author}" onclick="javascript:openOpinionPrompt('${item.author}')">Comentar</button>
          <button class="btn small" onclick="javascript:rateItem(this)">⭐ ${item.rating}</button>
        </div>
      </div>
    `;
    feedRoot.appendChild(node);
  });

  // --- Videos ---
  const videoList = document.getElementById("video-list");
  videos.forEach(v=>{
    const el = document.createElement("div");
    el.className = "video-item";
    el.setAttribute("data-id", v.id);
    el.innerHTML = `
      <div class="video-thumb">▶</div>
      <div style="flex:1">
        <div style="font-weight:700">${v.title}</div>
        <div style="font-size:0.85rem;color:rgba(255,255,255,0.6)">${v.length}</div>
      </div>
      <div>
        <button class="btn" onclick="javascript:playVideo('${v.id}','${v.title}')">Ver</button>
      </div>
    `;
    videoList.appendChild(el);
  });

  // --- Timeline ---
  const timelineRoot = document.getElementById("timeline");
  timeline.forEach(t=>{
    const node = document.createElement("div");
    node.className = "timeline-item";
    node.innerHTML = `
      <div style="width:8px;height:8px;border-radius:50%;background:var(--accent);margin-top:6px"></div>
      <div style="flex:1">
        <div style="font-weight:700">${t.title}</div>
        <div class="timeline-bar" aria-hidden="true"><div class="timeline-fill" style="width:${t.progress}%"></div></div>
      </div>
      <div class="timeline-meta">${t.eta}</div>
    `;
    timelineRoot.appendChild(node);
  });
  document.getElementById("timeline-summary").textContent = `${timeline.length} items`;

  // --- Calendar ---
  const calRoot = document.getElementById("calendar");
  calendar.forEach(d=>{
    const dnode = document.createElement("div");
    dnode.className = "day" + (d.note ? "" : "");
    if (d.day === "Mie") dnode.classList.add("today");
    dnode.innerHTML = `<div style="font-weight:700">${d.day} <span style="opacity:.8">${d.date}</span></div><div style="font-size:0.85rem;color:var(--muted)">${d.note}</div>`;
    calRoot.appendChild(dnode);
  });

  // --- Notifications badge demo ---
  document.getElementById("notif-count").textContent = feed.length;

  // --- Clock (simple) ---
  const clockEl = document.getElementById("clock");
  function tick() {
    const now = new Date();
    const time = now.toLocaleTimeString();
    clockEl.textContent = time;
  }
  tick();
  setInterval(tick, 1000);

  // --- Modal video support ---
  const modal = document.getElementById("video-modal");
  const modalClose = document.getElementById("modal-close");
  const videoContainer = document.getElementById("video-container");
  const videoCaption = document.getElementById("video-caption");
  window.playVideo = (id, title) => {
    // For demo we show a placeholder; replace with embed if you have URLs
    videoContainer.innerHTML = `<div style="background:#000;height:420px;display:flex;align-items:center;justify-content:center;color:#fff">Demo video: ${title}</div>`;
    videoCaption.textContent = title;
    modal.setAttribute("aria-hidden","false");
  };
  modalClose.addEventListener("click", ()=> modal.setAttribute("aria-hidden","true"));
  modal.addEventListener("click", (e)=> { if (e.target === modal) modal.setAttribute("aria-hidden","true") });

  // --- Small interaction helpers ---
  window.openOpinionPrompt = (author) => {
    const opinion = prompt(`Escribe tu comentario para ${author}:`);
    if(opinion) alert("Gracias. Comentario enviado (demo).");
  };
  window.rateItem = (btn) => {
    btn.textContent = "⭐ Gracias";
    btn.disabled = true;
  };

  // Entrance animations (counters)
  animateCount(document.getElementById("score-big"), 0, user.score, 900);
  animateCount(document.getElementById("kpi-2"), 0, kpis.models, 900);
  animateCount(document.getElementById("kpi-3"), 0, kpis.feedback, 900);

  // helper to animate numbers
  function animateCount(el, start, end, duration){
    const startTs = performance.now();
    function step(now){
      const t = Math.min(1, (now - startTs)/duration);
      const val = Math.floor(start + (end - start) * easeOutCubic(t));
      el.textContent = val;
      if(t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function easeOutCubic(t){ return 1 - Math.pow(1 - t, 3); }

});