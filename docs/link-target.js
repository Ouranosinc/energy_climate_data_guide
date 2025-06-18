<script>
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("a[href^='http']").forEach(link => {
    if (!link.href.includes(window.location.hostname)) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  });
});
</script>
