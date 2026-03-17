document.addEventListener("DOMContentLoaded", () => {
  const navGroups = document.querySelectorAll(
    ".bd-links .bd-sidenav > li.toctree-l1.has-children > details",
  );

  navGroups.forEach((group) => {
    group.open = true;
    group.setAttribute("open", "open");
  });
});
