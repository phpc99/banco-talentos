document.addEventListener("DOMContentLoaded", () => {
  const tabs = Array.from(document.querySelectorAll(".carreira-tab"));
  const cards = Array.from(document.querySelectorAll(".carreira-card"));

  if (!tabs.length || !cards.length) return;

  function ativar(target) {
    // tabs
    tabs.forEach((t) => {
      const on = t.dataset.target === target;
      t.classList.toggle("is-active", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
    });

    // cards
    cards.forEach((c) => {
      const on = c.dataset.role === target;
      c.classList.toggle("is-active", on);
      c.hidden = !on;
    });
  }

  // estado inicial
  ativar("cont1");

  tabs.forEach((t) => {
    t.addEventListener("click", () => {
      ativar(t.dataset.target);
    });
  });
});
