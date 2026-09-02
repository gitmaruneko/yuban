const RESOURCE_DATA_URL = "data/sample-resources.json";

function setText(selector, value) {
  document.querySelector(selector).textContent = value;
}

function getStatus(resource) {
  const verified = resource.ai_summary_status === "verified";
  return {
    label: verified ? "人工核實" : "AI 整理・待人工核實",
    className: verified ? "verified" : "draft",
  };
}

function renderRelatedResources(resources, currentResource) {
  const container = document.querySelector("#relatedResources");
  const related = resources
    .filter(
      (resource) =>
        resource.id !== currentResource.id &&
        resource.topic_group === currentResource.topic_group,
    )
    .slice(0, 3);

  if (!related.length) {
    document.querySelector(".related-section").hidden = true;
    return;
  }

  related.forEach((resource) => {
    const link = document.createElement("a");
    link.className = "related-link";
    link.href = `resource.html?id=${encodeURIComponent(resource.id)}`;

    const topic = document.createElement("span");
    topic.textContent = resource.topic;
    const title = document.createElement("strong");
    title.textContent = resource.title;
    link.append(topic, title);
    container.append(link);
  });
}

(async function initializeResourceDetail() {
  const loading = document.querySelector("#detailLoading");
  const error = document.querySelector("#detailError");
  const content = document.querySelector("#detailContent");
  const resourceId = new URLSearchParams(window.location.search).get("id");

  try {
    const response = await fetch(RESOURCE_DATA_URL);
    if (!response.ok) throw new Error(`Resource request failed: ${response.status}`);
    const resources = await response.json();
    const resource = resources.find((item) => item.id === resourceId);
    if (!resource) throw new Error("Resource not found");

    const status = getStatus(resource);
    const statusElement = document.querySelector("#detailStatus");
    statusElement.textContent = status.label;
    statusElement.classList.add(status.className);

    setText("#breadcrumbTitle", resource.title);
    setText("#detailTopicGroup", resource.topic_group);
    setText("#detailTitle", resource.title);
    setText("#detailSummary", resource.summary);
    setText("#detailAge", resource.age_label);
    setText("#detailTopic", resource.topic);
    setText("#detailType", resource.type_label);
    setText("#detailSourceType", resource.source.type);
    setText("#detailCredibility", resource.credibility_note);
    setText("#detailNotice", resource.notice);
    setText("#detailSourceName", resource.source.name);
    setText(
      "#reviewedAt",
      resource.reviewed_at ? `資料核實日期：${resource.reviewed_at}` : "尚待人工核實",
    );

    const tagList = document.querySelector("#detailTags");
    resource.tags.forEach((tag) => {
      const item = document.createElement("li");
      item.textContent = tag;
      tagList.append(item);
    });

    const sourceLink = document.querySelector("#originalSourceLink");
    sourceLink.href = resource.url;
    sourceLink.setAttribute("aria-label", `前往「${resource.source.name}」原始網站（另開新視窗）`);

    const reportLink = document.querySelector("#reportResource");
    const reportParams = new URLSearchParams({
      mode: "report",
      title: resource.title,
      url: resource.url,
    });
    reportLink.href = `submit.html?${reportParams.toString()}`;

    document.title = `${resource.title}｜育伴 YuBan`;
    renderRelatedResources(resources, resource);
    loading.hidden = true;
    content.hidden = false;
  } catch (caughtError) {
    console.error(caughtError);
    loading.hidden = true;
    error.hidden = false;
  }
})();
