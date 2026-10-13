(async () => {
  const status = document.getElementById("release-status");
  const grid = document.getElementById("download-grid");
  if (!status || !grid) return;

  const releasesUrl = "https://api.github.com/repos/FaniBhushan/ResumeStudio/releases/latest";

  function platformFor(name) {
    const normalized = name.toLowerCase();
    if (normalized.includes("windows")) return "windows";
    if (normalized.includes("macos-arm64")) return "macos-arm64";
    if (normalized.includes("macos-x64")) return "macos-x64";
    if (normalized.includes("linux")) return "linux";
    return "other";
  }

  try {
    const response = await fetch(releasesUrl, {
      headers: { Accept: "application/vnd.github+json" },
    });
    if (!response.ok) throw new Error("No release found");

    const release = await response.json();
    const assets = release.assets.filter((asset) => /\.(exe|dmg|appimage)$/i.test(asset.name));
    if (!assets.length) throw new Error("No installer assets found");

    const order = ["windows", "macos-arm64", "macos-x64", "linux"];
    assets.sort((left, right) => order.indexOf(platformFor(left.name)) - order.indexOf(platformFor(right.name)));
    status.textContent = `Latest release: ${release.tag_name}`;

    for (const asset of assets) {
      const link = document.createElement("a");
      link.className = "download-card";
      link.href = asset.browser_download_url;
      link.setAttribute("download", asset.name);

      const platform = document.createElement("span");
      platform.className = "download-platform";
      const name = asset.name.toLowerCase();
      platform.textContent = name.includes("windows")
        ? "Windows"
        : name.includes("macos-arm64")
          ? "macOS · Apple silicon"
          : name.includes("macos-x64")
            ? "macOS · Intel"
            : name.includes("linux")
              ? "Linux"
              : "Installer";

      const filename = document.createElement("span");
      filename.className = "download-filename";
      filename.textContent = asset.name;

      const size = document.createElement("span");
      size.className = "download-size";
      size.textContent = `${(asset.size / (1024 * 1024)).toFixed(1)} MB · Download ↗`;

      link.append(platform, filename, size);
      grid.append(link);
    }
  } catch {
    status.textContent = "No installer release is available yet.";
    const link = document.createElement("a");
    link.className = "md-button";
    link.href = "https://github.com/FaniBhushan/ResumeStudio/releases";
    link.textContent = "Check GitHub Releases";
    grid.append(link);
  }
})();
