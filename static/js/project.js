'use strict';
const tabs = [...document.querySelectorAll('[role="tab"]')];
const panels = [...document.querySelectorAll('.camera-panel')];
const rate = document.querySelector('#playback-rate');
const status = document.querySelector('#play-status');
let playbackGeneration = 0;
const activeVideos = () => [...document.querySelector('.camera-panel:not([hidden])').querySelectorAll('video')];
const pauseComparison = () => { playbackGeneration++; panels.forEach(p => p.querySelectorAll('video').forEach(v => v.pause())); };
function selectTab(index) {
  pauseComparison();
  tabs.forEach((tab, i) => { tab.setAttribute('aria-selected', String(i === index)); tab.tabIndex = i === index ? 0 : -1; panels[i].hidden = i !== index; });
  status.textContent = '';
  document.querySelector('#play-all').disabled = false;
  activeVideos().forEach(v => { v.playbackRate = Number(rate.value); });
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(index));
  tab.addEventListener('keydown', e => {
    let next = index;
    if (e.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (e.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    else if (e.key === 'Home') next = 0;
    else if (e.key === 'End') next = tabs.length - 1;
    else return;
    e.preventDefault(); selectTab(next); tabs[next].focus();
  });
});
document.querySelector('#play-all').addEventListener('click', async () => {
  const generation = ++playbackGeneration;
  const button = document.querySelector('#play-all');
  button.disabled = true; status.textContent = 'Loading the selected rollouts…';
  const videos = activeVideos();
  const results = await Promise.allSettled(videos.map(v => { v.playbackRate = Number(rate.value); return v.play(); }));
  if (generation !== playbackGeneration) return;
  button.disabled = false;
  status.textContent = results.some(r => r.status === 'rejected') ? 'Some videos could not start. Use their individual play controls or open the video directly.' : 'Playing the selected rollouts. Each clip retains its own timeline.';
});
document.querySelector('#pause-all').addEventListener('click', () => { pauseComparison(); document.querySelector('#play-all').disabled = false; status.textContent = 'Paused.'; });
document.querySelector('#restart-all').addEventListener('click', () => { pauseComparison(); activeVideos().forEach(v => { if (v.readyState > 0) v.currentTime = 0; }); document.querySelector('#play-all').disabled = false; status.textContent = 'Reset to the beginning. Select Play all three to start.'; });
rate.addEventListener('change', () => activeVideos().forEach(v => { v.playbackRate = Number(rate.value); }));
document.querySelectorAll('.trial-select').forEach(select => select.addEventListener('change', () => {
  select.closest('.example-group').querySelectorAll('.example-trial').forEach((panel, index) => { panel.querySelectorAll('video').forEach(v => v.pause()); panel.hidden = index !== Number(select.value); });
}));
document.querySelector('.examples').addEventListener('toggle', e => { if (!e.target.open) e.target.querySelectorAll('video').forEach(v => v.pause()); });
document.addEventListener('visibilitychange', () => { if (document.hidden) { pauseComparison(); document.querySelectorAll('video').forEach(v => v.pause()); document.querySelector('#play-all').disabled = false; } });
document.querySelectorAll('video').forEach(video => {
  video.addEventListener('error', () => { if (video.closest('.camera-panel') && !video.closest('.camera-panel').hidden) status.textContent = 'A video could not load. Try its Open video link or reload the page.'; });
});
selectTab(0);

document.querySelector(".simulation-demos").addEventListener("toggle", e => { if (!e.target.open) e.target.querySelectorAll("video").forEach(v => v.pause()); });
