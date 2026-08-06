// News Highlights Frontend JavaScript Logic

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const themeToggleBtn = document.getElementById("theme-toggle");
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const clearSearchBtn = document.getElementById("clear-search-btn");
    const filterBanner = document.getElementById("filter-banner");
    const bannerText = document.getElementById("banner-text");
    const newsGrid = document.getElementById("news-grid");
    const loader = document.getElementById("news-loader");
    const errorState = document.getElementById("news-error");
    const errorMessage = document.getElementById("error-message");
    const retryBtn = document.getElementById("retry-btn");
    const emptyState = document.getElementById("news-empty");
    const tabButtons = document.querySelectorAll(".tab-item");

    // Application State
    let currentTopic = "top";
    let currentSearchQuery = "";

    // 1. Theme Management (Light / Dark)
    const initTheme = () => {
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "light") {
            document.body.classList.remove("dark-theme");
            document.body.classList.add("light-theme");
        } else {
            document.body.classList.add("dark-theme");
            document.body.classList.remove("light-theme");
        }
    };

    themeToggleBtn.addEventListener("click", () => {
        if (document.body.classList.contains("dark-theme")) {
            document.body.classList.remove("dark-theme");
            document.body.classList.add("light-theme");
            localStorage.setItem("theme", "light");
        } else {
            document.body.classList.remove("light-theme");
            document.body.classList.add("dark-theme");
            localStorage.setItem("theme", "dark");
        }
    });

    // 2. Fetch News API Helper
    const fetchNews = async () => {
        // Show loading state, hide other views
        showView("loading");

        let url = `/api/news?topic=${currentTopic}`;
        if (currentSearchQuery) {
            url = `/api/news?q=${encodeURIComponent(currentSearchQuery)}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (response.ok && data.status === "success") {
                renderNews(data.articles);
            } else {
                throw new Error(data.message || "Failed to load articles.");
            }
        } catch (error) {
            console.error("Fetch Error:", error);
            errorMessage.textContent = error.message || "An unexpected error occurred. Please check your connection.";
            showView("error");
        }
    };

    // 3. Render News Cards
    const renderNews = (articles) => {
        if (!articles || articles.length === 0) {
            showView("empty");
            return;
        }

        newsGrid.innerHTML = ""; // Clear existing grid

        articles.forEach((article) => {
            const relativeTime = formatRelativeTime(article.published);
            
            const card = document.createElement("article");
            card.className = "news-card";
            card.innerHTML = `
                <div class="card-body">
                    <span class="card-source-badge">${escapeHTML(article.source)}</span>
                    <h3 class="card-title">${escapeHTML(article.title)}</h3>
                </div>
                <div class="card-meta">
                    <span class="card-date" title="${escapeHTML(article.published)}">
                        <i class="fa-regular fa-clock"></i> ${relativeTime}
                    </span>
                    <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="card-action-link">
                        Read Story <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            `;
            newsGrid.appendChild(card);
        });

        showView("grid");
    };

    // Helper: Escape HTML strings to prevent XSS
    const escapeHTML = (str) => {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    };

    // Helper: Format Date String to Relative Time
    const formatRelativeTime = (dateStr) => {
        if (!dateStr) return "Recently";
        try {
            const past = new Date(dateStr);
            const now = new Date();
            const diffMs = now - past;
            
            if (isNaN(diffMs)) return dateStr; // Fallback to raw string if parsing fails
            
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMins / 600);
            
            if (diffMins < 1) return "Just now";
            if (diffMins < 60) return `${diffMins}m ago`;
            if (diffHours < 24) return `${diffHours}h ago`;
            
            // Format fallback: "August 5, 2026"
            return past.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
        } catch (e) {
            return dateStr;
        }
    };

    // 4. Navigation Tab Switchers
    tabButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            // Remove active classes
            tabButtons.forEach(btn => {
                btn.classList.remove("active");
                btn.setAttribute("aria-selected", "false");
            });

            // Set clicked button as active
            const clickedBtn = e.currentTarget;
            clickedBtn.classList.add("active");
            clickedBtn.setAttribute("aria-selected", "true");

            // Reset search query
            currentSearchQuery = "";
            searchInput.value = "";
            filterBanner.style.display = "none";

            // Fetch news for the chosen topic
            currentTopic = clickedBtn.dataset.topic;
            fetchNews();
        });
    });

    // 5. Search Logic
    const executeSearch = () => {
        const value = searchInput.value.trim();
        if (!value) return;

        currentSearchQuery = value;
        bannerText.textContent = `Showing results for "${value}"`;
        filterBanner.style.display = "flex";

        // Deactivate all topic tabs, as we're in search mode
        tabButtons.forEach(btn => {
            btn.classList.remove("active");
            btn.setAttribute("aria-selected", "false");
        });

        fetchNews();
    };

    searchButton.addEventListener("click", executeSearch);
    searchInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            executeSearch();
        }
    });

    // 6. Clear Search Logic
    clearSearchBtn.addEventListener("click", () => {
        currentSearchQuery = "";
        searchInput.value = "";
        filterBanner.style.display = "none";

        // Select the "Top Stories" tab back
        const topStoriesTab = document.getElementById("tab-top");
        tabButtons.forEach(btn => {
            btn.classList.remove("active");
            btn.setAttribute("aria-selected", "false");
        });
        topStoriesTab.classList.add("active");
        topStoriesTab.setAttribute("aria-selected", "true");

        currentTopic = "top";
        fetchNews();
    });

    // 7. View Manager Helper
    const showView = (viewName) => {
        // Hide all views
        loader.style.display = "none";
        errorState.style.display = "none";
        newsGrid.style.display = "none";
        emptyState.style.display = "none";

        // Show requested view
        if (viewName === "loading") {
            loader.style.display = "flex";
        } else if (viewName === "error") {
            errorState.style.display = "flex";
        } else if (viewName === "grid") {
            newsGrid.style.display = "grid";
        } else if (viewName === "empty") {
            emptyState.style.display = "flex";
        }
    };

    // 8. Retry Logic
    retryBtn.addEventListener("click", fetchNews);

    // Initializations
    initTheme();
    fetchNews();
});
