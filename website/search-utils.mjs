export const RESULTS_PAGE_SIZE = 24;

const RESOURCE_CATEGORY_BY_TYPE = {
  "文章": "學習教材",
  "影片": "學習教材",
  "工具／用品": "機構",
  "連結入口": "機構",
  "混合型內容": "學習教材",
};

function inferAgeGroups(ageRanges = []) {
  const groups = [];
  if (ageRanges.some((age) => ["孕期", "0-1歲", "1-3歲", "3-6歲"].includes(age))) {
    groups.push("學齡前");
  }
  if (ageRanges.includes("全齡")) groups.push("全齡");
  return groups;
}

export function normalizeResource(resource) {
  const ageRanges = Array.isArray(resource.age_ranges) ? resource.age_ranges : [];
  const valuesOr = (value, fallback) => (Array.isArray(value) && value.length ? value : fallback);
  return {
    ...resource,
    age_groups: valuesOr(resource.age_groups, inferAgeGroups(ageRanges)),
    regions: valuesOr(resource.regions, ["全國"]),
    resource_categories: valuesOr(
      resource.resource_categories,
      [RESOURCE_CATEGORY_BY_TYPE[resource.type] || "學習教材"],
    ),
    audiences: valuesOr(resource.audiences, ["家長"]),
    origin_region: resource.origin_region || "台灣",
    languages: valuesOr(resource.languages, ["繁體中文"]),
  };
}

export function getSearchableText(resource) {
  return [
    resource.title,
    resource.summary,
    resource.topic,
    resource.topic_group,
    ...(resource.age_groups || []),
    ...(resource.regions || []),
    ...(resource.resource_categories || []),
    ...(resource.audiences || []),
    resource.origin_region,
    ...(resource.languages || []),
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
      resource.age_groups?.includes(state.age) ||
      resource.age_ranges.includes(state.age) ||
      (state.age !== "全齡" && resource.age_ranges.includes("全齡"));
    const matchesTopic = !state.topic || resource.topic === state.topic;
    const matchesSource = !state.source || resource.source.type === state.source;
    const matchesType = !state.type || resource.type === state.type;
    const matchesRegion = !state.region || resource.regions?.includes(state.region);
    const matchesCategory =
      !state.category || resource.resource_categories?.includes(state.category);
    const matchesAudience = !state.audience || resource.audiences?.includes(state.audience);
    const matchesOrigin = !state.origin || resource.origin_region === state.origin;
    const matchesLanguage = !state.language || resource.languages?.includes(state.language);
    return (
      matchesAge &&
      matchesTopic &&
      matchesSource &&
      matchesType &&
      matchesRegion &&
      matchesCategory &&
      matchesAudience &&
      matchesOrigin &&
      matchesLanguage
    );
  });
}

export function getVisibleResources(resources, visibleCount = RESULTS_PAGE_SIZE) {
  return resources.slice(0, visibleCount);
}