async function loadResources(){
  const res = await fetch('data/sample-resources.json');
  const items = await res.json();
  return items;
}

function renderItem(item){
  return `
    <article class="content" style="padding:12px;margin-bottom:10px">
      <h3>${item.title}</h3>
      <p>${item.summary}</p>
      <p><strong>類型:</strong> ${item.type} • <strong>標籤:</strong> ${item.tags.join(', ')} • <strong>年齡:</strong> ${item.age_ranges.join(', ')}</p>
      <p><a href="${item.url || '#'}" target="_blank">來源連結</a></p>
    </article>
  `;
}

function matchesQuery(item, q){
  if(!q) return true;
  q = q.toLowerCase();
  return (item.title && item.title.toLowerCase().includes(q)) ||
         (item.summary && item.summary.toLowerCase().includes(q)) ||
         (item.tags && item.tags.join(' ').toLowerCase().includes(q));
}

function matchesAge(item, age){
  if(!age) return true;
  return item.age_ranges && item.age_ranges.includes(age);
}

(async function(){
  const items = await loadResources();
  const resultsEl = document.getElementById('results');
  const qEl = document.getElementById('q');
  const ageEl = document.getElementById('age-filter');
  const btn = document.getElementById('searchBtn');

  function doSearch(){
    const q = qEl.value.trim();
    const age = ageEl.value;
    const filtered = items.filter(i => matchesQuery(i,q) && matchesAge(i,age));
    if(filtered.length === 0){
      resultsEl.innerHTML = '<p>找不到符合的資源。</p>';
      return;
    }
    resultsEl.innerHTML = filtered.map(renderItem).join('');
  }

  btn.addEventListener('click', doSearch);
  qEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') doSearch(); });

  // initial render
  resultsEl.innerHTML = items.slice(0,6).map(renderItem).join('');
})();
