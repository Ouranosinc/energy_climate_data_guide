window.addEventListener("load", function () {

  function openCalloutForHash() {
    if (!window.location.hash) return;

    const target = document.querySelector(window.location.hash);
    if (!target) return;

    // Find collapsible parent
    const collapseEl = target.closest(".collapse");
    if (!collapseEl) return;

    // Use Bootstrap's API
    if (window.bootstrap && bootstrap.Collapse) {
      const instance = bootstrap.Collapse.getOrCreateInstance(collapseEl, {
        toggle: false
      });
      instance.show();
    }

    // Scroll AFTER animation starts
    setTimeout(() => {
      target.scrollIntoView({ block: "start" });
    }, 300);
  }

  openCalloutForHash();
  window.addEventListener("hashchange", openCalloutForHash);

});
