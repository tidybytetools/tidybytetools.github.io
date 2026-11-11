/* Filter and search tool cards. No dependencies. */
(function () {
  var search = document.getElementById("tool-search");
  var chips = document.querySelectorAll("[data-filter]");
  var cards = document.querySelectorAll("[data-tool-card]");
  var empty = document.getElementById("filter-empty");
  if (!cards.length) return;

  var activeCat = "all";
  var query = "";

  function norm(s) {
    return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function apply() {
    var shown = 0;
    cards.forEach(function (card) {
      var cat = card.getAttribute("data-category") || "";
      var hay = card.getAttribute("data-search") || "";
      var catOk = activeCat === "all" || cat === activeCat;
      var qOk = !query || hay.indexOf(query) !== -1;
      var on = catOk && qOk;
      card.hidden = !on;
      if (on) shown += 1;
    });
    if (empty) empty.hidden = shown !== 0;
  }

  if (search) {
    search.addEventListener("input", function () {
      query = norm(search.value);
      apply();
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function (ev) {
      ev.preventDefault();
      activeCat = chip.getAttribute("data-filter") || "all";
      chips.forEach(function (c) {
        var on = c === chip;
        c.classList.toggle("is-active", on);
        if (c.tagName === "BUTTON") c.setAttribute("aria-pressed", on ? "true" : "false");
      });
      apply();
    });
  });
})();
