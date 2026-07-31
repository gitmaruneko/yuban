async function loadResources(){
  const res = await fetch('data/sample-resources.json');
  const items = await res.json();
  return items;
}

function renderItem(item){
  const statusLabel = item.ai_summary_status === 'verified' ? '已驗證' : 'AI 草稿';
  const statusClass = item.ai_summary_status === 'verified' ? 'verified' : 'draft';
  return `
    <article class="resource-card">
      <div>
        <h3>${item.title}</h3>
        <p>${item.summary}</p>
      </div>
      <div class="resource-meta">
        <span class="tag">${item.category || '未分類'}</span>
        <span class="tag">${item.type || '文章'}</span>
        <span class="tag">${item.source?.name || '來源不明'}</span>
        <span class="tag">${item.age_ranges?.join(', ') || '不限年齡'}</span>
      </div>
      <div class="resource-meta">
        ${item.tags?.map(tag => `<span class="tag">${tag}</span>`).join('')}
      </div>
      <div class="resource-meta">
        <span class="badge type">${item.type || '文章'}</span>
        <span class="badge status ${statusClass}">${statusLabel}</span>
      </div>
      <a class="card-link" href="${item.url || '#'}" target="_blank">查看原始資源</a>
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

function matchesCategory(item, category){
  if(!category) return true;
  return item.category === category;
}

function updateSummary(count, total){
  const summaryEl = document.getElementById('resultsSummary');
  summaryEl.textContent = `共 ${count} 筆資源，從 ${total} 筆示例中篩選。`;
}

(async function(){
  const items = await loadResources();
  const resultsGrid = document.getElementById('resultsGrid');
  const qEl = document.getElementById('q');
  const ageEl = document.getElementById('age-filter');
  const btn = document.getElementById('searchBtn');

  let selectedCategory = '';

  function doSearch(){
    const q = qEl.value.trim();
    const age = ageEl.value;
    const filtered = items.filter(i => matchesQuery(i,q) && matchesAge(i,age) && matchesCategory(i, selectedCategory));
    if(filtered.length === 0){
      resultsGrid.innerHTML = '<p>找不到符合的資源。</p>';
      updateSummary(0, items.length);
      return;
    }
    resultsGrid.innerHTML = filtered.map(renderItem).join('');
    updateSummary(filtered.length, items.length);
  }

  btn.addEventListener('click', doSearch);
  qEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') doSearch(); });
  document.querySelectorAll('.category-pill').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.category-pill').forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      selectedCategory = button.dataset.category;
      doSearch();
    });
  });

  resultsGrid.innerHTML = items.slice(0,6).map(renderItem).join('');
  updateSummary(Math.min(6, items.length), items.length);
})();
