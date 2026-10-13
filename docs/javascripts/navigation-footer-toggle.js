const siteRoot = document.documentElement;
const sidebar = document.querySelector(".md-sidebar--primary");

if (sidebar) {
  const toggle = document.createElement("button");
  toggle.className = "home-nav-toggle";
  toggle.type = "button";
  sidebar.prepend(toggle);

  const updateToggle = () => {
    const collapsed = siteRoot.classList.contains("nav-collapsed");
    toggle.textContent = collapsed ? "›" : "‹";
    toggle.setAttribute("aria-expanded", String(!collapsed));
    toggle.setAttribute("aria-label", collapsed ? "Open site navigation" : "Collapse site navigation");
    toggle.title = collapsed ? "Open site navigation" : "Collapse site navigation";
  };

  const setCollapsed = (collapsed) => {
    siteRoot.classList.toggle("nav-collapsed", collapsed);
    try {
      localStorage.setItem("resumeStudioNavigationCollapsed", String(collapsed));
    } catch (_) {}
    updateToggle();
  };

  toggle.addEventListener("click", () => {
    setCollapsed(!siteRoot.classList.contains("nav-collapsed"));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setCollapsed(true);
  });

  const footer = siteRoot.classList.contains("marketing-home")
    ? document.querySelector(".marketing-home-content .footer")
    : document.querySelector(".md-footer");
  if (footer && "IntersectionObserver" in window) {
    const footerObserver = new IntersectionObserver(([entry]) => {
      siteRoot.classList.toggle("footer-visible", entry.isIntersecting);
    });
    footerObserver.observe(footer);
  }

  updateToggle();
}
