// GCT Conference - Frontend Logic

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const filterBtns = document.querySelectorAll(".filter-btn");
  const timelineItems = document.querySelectorAll(".timeline-item");
  const noResultsCard = document.getElementById("no-results");

  let activeCategory = "all";
  let searchQuery = "";

  /**
   * Run the filtering algorithm combining both search query and active category.
   */
  function filterSchedule() {
    let visibleCount = 0;

    timelineItems.forEach((item) => {
      // 1. Category Filter Check
      const categoriesStr = item.getAttribute("data-categories") || "";
      const categories = categoriesStr.split(",").map(c => c.trim().toLowerCase());
      const isBreak = item.classList.contains("break-item");

      // Break items are always visible under 'all', but hidden under specific categories
      const categoryMatch =
        activeCategory === "all" ||
        (!isBreak && categories.includes(activeCategory.toLowerCase()));

      // 2. Search Text Check
      const title = (item.querySelector(".talk-title")?.textContent || "").toLowerCase();
      const desc = (item.querySelector(".talk-desc")?.textContent || "").toLowerCase();
      
      const speakerNames = Array.from(item.querySelectorAll(".speaker-name"))
        .map((s) => s.textContent.toLowerCase())
        .join(" ");

      const tags = Array.from(item.querySelectorAll(".cat-tag"))
        .map((t) => t.textContent.toLowerCase())
        .join(" ");

      const searchContent = `${title} ${desc} ${speakerNames} ${tags}`;
      const searchMatch = searchQuery === "" || searchContent.includes(searchQuery);

      // Combine conditions
      if (categoryMatch && searchMatch) {
        item.classList.remove("hidden");
        // Trigger subtle animation on reappear
        item.style.animation = "none";
        // Force reflow
        void item.offsetWidth;
        item.style.animation = "fadeIn 0.4s ease forwards";
        visibleCount++;
      } else {
        item.classList.add("hidden");
      }
    });

    // 3. Toggle No Results Card
    if (visibleCount === 0) {
      noResultsCard.classList.remove("hidden");
    } else {
      noResultsCard.classList.add("hidden");
    }
  }

  // Listen to input in the search bar
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    filterSchedule();
  });

  // Listen to clicks on category pills
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Switch active class
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      activeCategory = btn.getAttribute("data-category");
      filterSchedule();
    });
  });
});
