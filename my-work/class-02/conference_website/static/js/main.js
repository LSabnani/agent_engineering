// Global Application State
let conferenceData = {
    metadata: {},
    talks: []
};

let activeCategory = 'All';
let searchQuery = '';
let bookmarkedTalkIds = [];

// DOM Elements
const timelineContainer = document.getElementById('timeline-container');
const speakersGridContainer = document.getElementById('speakers-grid-container');
const searchInput = document.getElementById('search-input');
const clearSearchBtn = document.getElementById('clear-search-btn');
const categoryChips = document.querySelectorAll('.category-chips .chip');
const filtersStatus = document.getElementById('filters-status');
const filtersStatusText = document.getElementById('filters-status-text');
const resetFiltersBtn = document.getElementById('reset-filters-btn');
const bookmarkToggleBtn = document.getElementById('bookmark-toggle-btn');
const bookmarkCountEl = document.getElementById('bookmark-count');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadBookmarks();
    fetchConferenceData();
    setupEventListeners();
});

// Load Bookmarks from LocalStorage
function loadBookmarks() {
    const saved = localStorage.getItem('gcp_bookmarks');
    if (saved) {
        try {
            bookmarkedTalkIds = JSON.parse(saved);
        } catch (e) {
            bookmarkedTalkIds = [];
        }
    }
    updateBookmarkUI();
}

// Save Bookmarks to LocalStorage
function saveBookmarks() {
    localStorage.setItem('gcp_bookmarks', JSON.stringify(bookmarkedTalkIds));
    updateBookmarkUI();
}

// Update Header Bookmark Count and active filters if on bookmark category
function updateBookmarkUI() {
    bookmarkCountEl.textContent = bookmarkedTalkIds.length;
    if (activeCategory === 'Bookmarks') {
        renderTimeline();
    }
}

// Fetch Schedule & Speaker Data from Flask API
async function fetchConferenceData() {
    try {
        const response = await fetch('/api/schedule');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        conferenceData.metadata = data.conference;
        conferenceData.talks = data.schedule;
        
        updateHeaderAndHero();
        renderTimeline();
        renderSpeakers();
        startCountdown(data.conference.date + ' 09:00:00 GMT-0700');
    } catch (error) {
        console.error('Failed to load conference data:', error);
        timelineContainer.innerHTML = `
            <div class="no-results">
                <h3>Error Loading Schedule</h3>
                <p>Please make sure the Flask backend is running and refresh the page.</p>
            </div>
        `;
    }
}

// Update static text content in Hero and Header
function updateHeaderAndHero() {
    const meta = conferenceData.metadata;
    document.getElementById('conf-title').textContent = meta.title || 'GCP Next-Gen Summit 2026';
    document.getElementById('conf-date').textContent = meta.date || 'October 15, 2026';
    document.getElementById('conf-location').textContent = meta.location || 'San Francisco, CA';
    document.getElementById('conf-tz').textContent = `Timezone: ${meta.timezone || 'PDT'}`;
}

// Start Hero Section Countdown Timer
function startCountdown(targetDateStr) {
    const targetDate = new Date(targetDateStr).getTime();
    
    function updateTimer() {
        const now = new Date().getTime();
        const difference = targetDate - now;
        
        if (difference < 0) {
            // Event is active or past
            document.getElementById('days').textContent = '00';
            document.getElementById('hours').textContent = '00';
            document.getElementById('minutes').textContent = '00';
            document.getElementById('seconds').textContent = '00';
            document.querySelector('.countdown-card h3').textContent = 'Summit In Progress!';
            return;
        }
        
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);
        
        document.getElementById('days').textContent = String(days).padStart(2, '0');
        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
    }
    
    updateTimer();
    setInterval(updateTimer, 1000);
}

// Filter and Render the Timeline/Schedule
function renderTimeline() {
    timelineContainer.innerHTML = '';
    
    // Filter logic
    const filteredTalks = conferenceData.talks.filter(talk => {
        // Category Filter
        if (activeCategory === 'Bookmarks') {
            if (!bookmarkedTalkIds.includes(talk.id)) return false;
        } else if (activeCategory !== 'All') {
            if (talk.category !== activeCategory && talk.type !== 'break') return false;
        }
        
        // Search Filter
        if (searchQuery.trim() !== '') {
            const query = searchQuery.toLowerCase();
            const matchesTitle = talk.title.toLowerCase().includes(query);
            const matchesDesc = talk.description.toLowerCase().includes(query);
            const matchesSpeaker = talk.speakers.some(spk => 
                (spk.first_name + ' ' + spk.last_name).toLowerCase().includes(query)
            );
            
            if (!matchesTitle && !matchesDesc && !matchesSpeaker) return false;
        }
        
        return true;
    });
    
    // Show/Hide filter active status indicator
    if (activeCategory !== 'All' || searchQuery.trim() !== '') {
        filtersStatus.style.display = 'flex';
        filtersStatusText.textContent = `Showing ${filteredTalks.length} of ${conferenceData.talks.length} schedule items`;
    } else {
        filtersStatus.style.display = 'none';
    }
    
    if (filteredTalks.length === 0) {
        timelineContainer.innerHTML = `
            <div class="no-results">
                <h3>No Talks Found</h3>
                <p>Try resetting the search query or changing filters to view more items.</p>
            </div>
        `;
        return;
    }
    
    filteredTalks.forEach(talk => {
        const isSaved = bookmarkedTalkIds.includes(talk.id);
        const cardClass = talk.type === 'break' ? 'schedule-card break-card' : 'schedule-card';
        const categoryClass = talk.type === 'break' ? 'category-break' : 
                              (talk.category === 'Infrastructure & Architecture' ? 'category-infra' : 'category-data');
        
        const speakersHtml = talk.speakers.map(spk => `
            <div class="speaker-compact">
                <div class="speaker-avatar flex-center">
                    ${spk.first_name[0]}${spk.last_name[0]}
                </div>
                <div>
                    <span class="speaker-name">${spk.first_name} ${spk.last_name}</span>
                    <a href="${spk.linkedin_url}" class="speaker-linkedin" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn profile">
                        <svg class="icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                            <rect x="2" y="9" width="4" height="12"></rect>
                            <circle cx="4" cy="4" r="2"></circle>
                        </svg>
                    </a>
                </div>
            </div>
        `).join('');
        
        const bookmarkBtnHtml = talk.type !== 'break' ? `
            <button class="bookmark-btn ${isSaved ? 'saved' : ''}" data-id="${talk.id}" aria-label="Save talk to schedule">
                <svg class="icon" viewBox="0 0 24 24" fill="${isSaved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                </svg>
            </button>
        ` : '';
        
        const itemHtml = `
            <div class="timeline-item">
                <div class="timeline-node"></div>
                <div class="${cardClass}">
                    <div class="card-time">
                        <span class="time-range">
                            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            ${talk.start_time} - ${talk.end_time}
                        </span>
                        <span class="duration-tag">${talk.type === 'break' ? '60 mins' : '45 mins'}</span>
                    </div>
                    <div class="card-details">
                        <div class="card-meta">
                            <span class="card-id">${talk.id}</span>
                            <span class="card-category ${categoryClass}">${talk.category}</span>
                        </div>
                        <h3 class="card-title">${talk.title}</h3>
                        <p class="card-desc">${talk.description}</p>
                        ${talk.speakers.length > 0 ? `<div class="card-speakers">${speakersHtml}</div>` : ''}
                    </div>
                    ${bookmarkBtnHtml}
                </div>
            </div>
        `;
        
        timelineContainer.insertAdjacentHTML('beforeend', itemHtml);
    });
    
    // Add bookmark click handlers
    document.querySelectorAll('.bookmark-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = btn.getAttribute('data-id');
            toggleBookmark(id);
        });
    });
}

// Toggle Bookmarking Talk
function toggleBookmark(talkId) {
    const index = bookmarkedTalkIds.indexOf(talkId);
    if (index === -1) {
        bookmarkedTalkIds.push(talkId);
    } else {
        bookmarkedTalkIds.splice(index, 1);
    }
    saveBookmarks();
    renderTimeline();
}

// Render the Unique Speakers Gallery Section
function renderSpeakers() {
    speakersGridContainer.innerHTML = '';
    
    // Deduplicate speakers list from talks
    const speakersMap = new Map();
    conferenceData.talks.forEach(talk => {
        talk.speakers.forEach(spk => {
            const key = `${spk.first_name} ${spk.last_name}`;
            if (!speakersMap.has(key)) {
                speakersMap.set(key, spk);
            }
        });
    });
    
    if (speakersMap.size === 0) {
        speakersGridContainer.innerHTML = '<p>No speakers profile available.</p>';
        return;
    }
    
    speakersMap.forEach((spk) => {
        const initials = `${spk.first_name[0]}${spk.last_name[0]}`;
        const title = spk.linkedin_url.includes('k8s') ? 'GKE Architect' : 
                      spk.linkedin_url.includes('vertex') ? 'AI Research Lead' : 
                      spk.linkedin_url.includes('serverless') ? 'Developer Advocate' : 
                      spk.linkedin_url.includes('spanner') ? 'Database Lead' : 
                      spk.linkedin_url.includes('dataflow') ? 'Data Architect' : 'Cloud Engineer';
                      
        const speakerHtml = `
            <div class="speaker-card">
                <div class="speaker-card-avatar">
                    <div class="speaker-card-avatar-inner flex-center">
                        ${initials}
                    </div>
                </div>
                <h3>${spk.first_name} ${spk.last_name}</h3>
                <p class="speaker-title">${title}</p>
                <a href="${spk.linkedin_url}" class="speaker-social-btn" target="_blank" rel="noopener noreferrer">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                        <rect x="2" y="9" width="4" height="12"></rect>
                        <circle cx="4" cy="4" r="2"></circle>
                    </svg>
                    LinkedIn
                </a>
            </div>
        `;
        
        speakersGridContainer.insertAdjacentHTML('beforeend', speakerHtml);
    });
}

// Setup Keyboard & Mouse Event Listeners
function setupEventListeners() {
    // Search input functionality
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        if (searchQuery.length > 0) {
            clearSearchBtn.style.display = 'block';
        } else {
            clearSearchBtn.style.display = 'none';
        }
        renderTimeline();
    });
    
    // Clear search button
    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        clearSearchBtn.style.display = 'none';
        renderTimeline();
    });
    
    // Category chips filter toggle
    categoryChips.forEach(chip => {
        chip.addEventListener('click', () => {
            categoryChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeCategory = chip.getAttribute('data-category');
            renderTimeline();
        });
    });
    
    // Reset filters link
    resetFiltersBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        clearSearchBtn.style.display = 'none';
        
        categoryChips.forEach(c => c.classList.remove('active'));
        categoryChips[0].classList.add('active'); // 'All' chip
        activeCategory = 'All';
        
        renderTimeline();
    });
    
    // Header Bookmarks shortcut toggle
    bookmarkToggleBtn.addEventListener('click', () => {
        // Toggle the Bookmarks Chip
        const bookmarksChip = document.getElementById('filter-bookmarks-btn');
        categoryChips.forEach(c => c.classList.remove('active'));
        
        if (activeCategory === 'Bookmarks') {
            categoryChips[0].classList.add('active'); // Set to 'All'
            activeCategory = 'All';
        } else {
            bookmarksChip.classList.add('active');
            activeCategory = 'Bookmarks';
        }
        renderTimeline();
    });
}
