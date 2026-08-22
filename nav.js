(function () {
  const page = (window.location.pathname.split('/').pop() || 'index.html');
  const current = page === '' ? 'index.html' : page;

  document.querySelectorAll('.nav-dropdown-link[data-page]').forEach(function (link) {
    if (link.getAttribute('data-page') === current) {
      link.classList.add('active');
      const group = link.closest('.nav-group');
      if (group) {
        group.classList.add('is-current');
        const toggle = group.querySelector('.nav-group-toggle');
        if (toggle) toggle.classList.add('active');
      }
    }
  });

  document.querySelectorAll('.nav-group-toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      const group = btn.closest('.nav-group');
      const wasOpen = group.classList.contains('is-open');
      document.querySelectorAll('.nav-group.is-open').forEach(function (g) {
        g.classList.remove('is-open');
      });
      if (!wasOpen) group.classList.add('is-open');
    });
  });

  document.addEventListener('click', function () {
    document.querySelectorAll('.nav-group.is-open').forEach(function (g) {
      g.classList.remove('is-open');
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.nav-group.is-open').forEach(function (g) {
        g.classList.remove('is-open');
      });
    }
  });
})();
