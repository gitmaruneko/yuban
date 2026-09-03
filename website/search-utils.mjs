export const RESULTS_PAGE_SIZE = 24;

export function getSearchableText(resource) {
  return [
    resource.title,
    resource.summary,
    resource.topic,
    resource.topic_group,
    resource.source.name,
    resource.source.type,
    resource.type,
    resource.type_label,
    ...resource.tags,
  ]
    .join(" ")
    .normalize("NFKC")
    .toLocaleLowerCase("zh-Hant");
}

export function searchResources(resources, query, SearchEngine = null) {
  const trimmedQuery = query.trim();
  if (!trimmedQuery) return resources;

  if (SearchEngine) {
    const searchEngine = new SearchEngine(resources, {
      includeScore: true,
      ignoreLocation: true,
      threshold: 0.36,
      minMatchCharLength: 2,
      keys: [
        { name: "title", weight: 0.32 },
        { name: "summary", weight: 0.24 },
        { name: "tags", weight: 0.16 },
        { name: "topic", weight: 0.12 },
        { name: "topic_group", weight: 0.06 },
        { name: "source.name", weight: 0.06 },
        { name: "type_label", weight: 0.04 },
      ],
    });
    return searchEngine.search(trimmedQuery).map((result) => result.item);
  }

  const normalizedQuery = trimmedQuery.normalize("NFKC").toLocaleLowerCase("zh-Hant");
  return resources.filter((resource) => getSearchableText(resource).includes(normalizedQuery));
}

export function filterResources(resources, state) {
  return resources.filter((resource) => {
    const matchesAge =
      !state.age ||
      resource.age_ranges.includes(state.age) ||
      (state.age !== "全齡" && resource.age_ranges.includes("全齡"));
    const matchesTopic = !state.topic || resource.topic === state.topic;
    const matchesSource = !state.source || resource.source.type === state.source;
    const matchesType = !state.type || resource.type === state.type;
    return matchesAge && matchesTopic && matchesSource && matchesType;
  });
}

export function getVisibleResources(resources, visibleCount = RESULTS_PAGE_SIZE) {
  return resources.slice(0, visibleCount);
}