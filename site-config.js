// Interfluent site switches. Edit here and every page follows.
window.INTERFLUENT_CONFIG = {
  betaEnabled: true,        // show "Request beta access" (nav, CTA band, /Beta page)
  accessCodeEnabled: false,  // show "Sign in" + access-code gate (/SignIn page, code field on beta form)
  appUrl: '#',              // where a valid access code sends people (kept abstract for now)
  landing: 'index.html'
};


// Shared navigation/footer enhancement: keep Case Studies alongside Blog.
// The DC components render asynchronously, so apply when their links appear.
(function addCaseStudiesLinks() {
  if (typeof document === 'undefined') return;
  const path = '/interfluent.ai/case-studies/';
  function update() {
    const candidates = document.querySelectorAll('a[href]');
    for (const blogLink of candidates) {
      const href = blogLink.getAttribute('href') || '';
      const label = (blogLink.textContent || '').trim();
      if (label !== 'Blog' || !/(?:^|\\/)blog\\/?(?:index\\.html)?(?:[?#].*)?$/.test(href)) continue;
      const nav = blogLink.closest('nav, header, footer, [role="navigation"], [class*="nav"], [class*="footer"]');
      if (!nav) continue;
      const group = blogLink.parentElement;
      if (!group || group.querySelector('a[href*="case-studies"]')) continue;
      if (nav.querySelector('a[href*="case-studies"]')) continue;
      const newLink = blogLink.cloneNode(true);
      newLink.textContent = 'Case Studies';
      newLink.setAttribute('href', path);
      newLink.removeAttribute('aria-current');
      newLink.classList.remove('w--current', 'is-active', 'active');
      blogLink.insertAdjacentElement('afterend', newLink);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', update);
  else update();
  const observer = new MutationObserver(update);
  observer.observe(document.documentElement, { childList: true, subtree: true });
})();
