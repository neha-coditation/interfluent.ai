// Interfluent site switches. Edit here and every page follows.
window.INTERFLUENT_CONFIG = {
  betaEnabled: true,        // show "Request beta access" (nav, CTA band, /Beta page)
  accessCodeEnabled: false,  // show "Sign in" + access-code gate (/SignIn page, code field on beta form)
  appUrl: '#',              // where a valid access code sends people (kept abstract for now)
  landing: 'index.html'
};


// Add the Case Studies destination to each rendered desktop/mobile nav and footer.
(function addCaseStudiesLinks() {
  const destination = '/interfluent.ai/case-studies/';
  const isBlog = (link) => {
    const raw = link.getAttribute('href') || '';
    try {
      const url = new URL(raw, document.baseURI);
      return /\\/blog\\/?(?:index\\.html)?$/.test(url.pathname) && /blog/i.test(link.textContent || '');
    } catch (_) { return false; }
  };
  let queued = false;
  function update() {
    queued = false;
    document.querySelectorAll('a[href]').forEach(link => {
      if (!isBlog(link)) return;
      const area = link.closest('nav, header, footer, [role="navigation"], [class*="nav"], [class*="footer"]');
      if (!area) return;
      if (area.querySelector('a[href*="case-studies"]')) return;
      const next = link.cloneNode(true);
      next.textContent = 'Case Studies';
      next.href = destination;
      next.removeAttribute('aria-current');
      next.classList.remove('active', 'is-active', 'w--current');
      link.insertAdjacentElement('afterend', next);
    });
  }
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(update);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', schedule);
  else schedule();
  new MutationObserver(schedule).observe(document.documentElement, {childList:true, subtree:true});
})();
