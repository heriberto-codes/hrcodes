(() => {
  const menu = document.querySelector(".mobile-nav");
  if (!menu) return;

  const summary = menu.querySelector("summary");
  const links = menu.querySelectorAll("nav a");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let closeTimer;

  const updateLabel = (isOpen) => {
    summary.setAttribute("aria-expanded", String(isOpen));
    summary.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
  };

  const openMenu = () => {
    window.clearTimeout(closeTimer);
    menu.classList.remove("is-closing");
    menu.open = true;
    updateLabel(true);

    requestAnimationFrame(() => {
      requestAnimationFrame(() => menu.classList.add("is-open"));
    });
  };

  const closeMenu = ({ returnFocus = false } = {}) => {
    if (!menu.open) return;

    window.clearTimeout(closeTimer);
    menu.classList.remove("is-open");
    menu.classList.add("is-closing");
    updateLabel(false);

    const delay = reducedMotion.matches ? 0 : 270;
    closeTimer = window.setTimeout(() => {
      menu.open = false;
      menu.classList.remove("is-closing");
      if (returnFocus) summary.focus();
    }, delay);
  };

  menu.classList.add("is-ready");
  updateLabel(menu.open);
  if (menu.open) menu.classList.add("is-open");

  summary.addEventListener("click", (event) => {
    event.preventDefault();
    if (menu.open && !menu.classList.contains("is-closing")) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  links.forEach((link) => link.addEventListener("click", () => closeMenu()));

  document.addEventListener("pointerdown", (event) => {
    if (menu.open && !menu.contains(event.target)) closeMenu();
  });

  menu.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu({ returnFocus: true });
  });
})();
