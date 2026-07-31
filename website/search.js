async function loadResources(){
  const res = await fetch('data/sample-resources.json');
  const items = await res.json();
  return items;
}

function renderItem(item){
  const statusLabel = item.ai_summary_status === 'verified' ? '已驗證' : 'AI 草稿';
  const statusClass = item.ai_summary_status === 'verified' ? 'verified' : 'draft';
  const tags = item.tags?.map(tag => `<span class="meta-text">${tag}</span>`).join('') || '';
  const category = item.category ? `<span class="meta-text">${item.category}</span>` : '';
  const type = item.type ? `<span class="meta-text">${item.type}</span>` : '';
  const age = item.age_ranges ? `<span class="meta-text">${item.age_ranges.join('、')}</span>` : '';

  return `
    <li class="resource-item">
      <div class="resource-row">
        <div>
          <a class="resource-link" href="${item.url || '#'}" target="_blank" rel="noopener noreferrer">
            ${item.title}
            <span class="resource-tooltip">
              <span class="badge status ${statusClass}">${statusLabel}</span>
              <span class="tooltip-text">${item.summary || '無摘要'}</span>
            </span>
          </a>
        </div>
        <div class="resource-meta">
          ${tags}
          ${category}
          ${type}
          ${age}
        </div>
      </div>
    </li>
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
