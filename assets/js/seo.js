(function () {
  var config = window.INTERFLUENT_SEO;
  if (!config || !config.site || !config.pages) return;

  var key = document.documentElement.getAttribute("data-seo-page");
  var page = config.pages[key];
  if (!page) return;

  var site = config.site;
  var baseUrl = (site.baseUrl || "").replace(/\/$/, "");
  var canonical = baseUrl + (page.path || "/");
  var image = page.image || site.defaultImage || "";
  var imageUrl = /^https?:\/\//i.test(image) ? image : baseUrl + (image.charAt(0) === "/" ? image : "/" + image);

  function meta(name, content, property) {
    if (!content) return;
    var selector = property ? 'meta[property="' + name + '"]' : 'meta[name="' + name + '"]';
    var el = document.head.querySelector(selector);
    if (!el) {
      el = document.createElement("meta");
      el.setAttribute(property ? "property" : "name", name);
      document.head.appendChild(el);
    }
    el.setAttribute("content", content);
  }

  function link(rel, href) {
    var el = document.head.querySelector('link[rel="' + rel + '"]');
    if (!el) {
      el = document.createElement("link");
      el.setAttribute("rel", rel);
      document.head.appendChild(el);
    }
    el.setAttribute("href", href);
  }

  document.title = page.title || site.name || "";
  meta("description", page.description || "");
  meta("robots", page.robots || "index,follow");

  link("canonical", canonical);

  meta("og:type", page.type || "website", true);
  meta("og:site_name", site.name || "", true);
  meta("og:locale", site.locale || "en_US", true);
  meta("og:title", page.ogTitle || page.title || "", true);
  meta("og:description", page.ogDescription || page.description || "", true);
  meta("og:url", canonical, true);
  meta("og:image", imageUrl, true);

  meta("twitter:card", site.twitterCard || "summary_large_image");
  meta("twitter:title", page.twitterTitle || page.title || "");
  meta("twitter:description", page.twitterDescription || page.description || "");
  meta("twitter:image", imageUrl);
})();
