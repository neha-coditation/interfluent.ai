// Interfluent site switches. Edit here and every page follows.
window.INTERFLUENT_CONFIG = {
  betaEnabled: true,        // show "Request beta access" (nav, CTA band, /Beta page)
  accessCodeEnabled: false,  // show "Sign in" + access-code gate (/SignIn page, code field on beta form)
  appUrl: '#',              // where a valid access code sends people (kept abstract for now)
  landing: 'index.html'
};


// Add Case Studies to each independently rendered navigation/footer menu.
(function () {
  const destination = '/interfluent.ai/case-studies/';
  function isBlog(link) {
    try {
      const pathname = new URL(link.getAttribute('href'), document.baseURI).pathname;
      return /\/blog\/?(?:index\.html)?$/.test(pathname) && /blog/i.test(link.textContent || '');
    } catch (_) { return false; }
  }
  function update() {
    document.querySelectorAll('a[href]').forEach(link => {
      if (!isBlog(link)) return;
      if (!link.closest('nav, header, footer, [role="navigation"], [class*="nav"], [class*="footer"], dc-import')) return;
      const parent = link.parentElement;
      if (!parent || Array.from(parent.children).some(el => el.matches('a[href*="case-studies"]'))) return;
      const item = link.cloneNode(true);
      item.textContent = 'Case Studies';
      item.setAttribute('href', destination);
      item.removeAttribute('aria-current');
      item.classList.remove('active', 'is-active', 'w--current');
      link.insertAdjacentElement('afterend', item);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', update);
  else update();
  const observer = new MutationObserver(update);
  observer.observe(document.documentElement, {childList: true, subtree: true});
})();
