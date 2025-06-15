// API endpoint for project data
const API_ENDPOINT = '/data.json';
const GITHUB_USERNAME = 'mdminhazulhaque';

// DOM elements
const projectsGrid = document.getElementById('projectsGrid');
const loadingSpinner = document.getElementById('loadingSpinner');

// Fetch and display projects
async function fetchProjects() {
    try {
        console.log('Fetching projects from:', API_ENDPOINT);
        
        const response = await fetch(API_ENDPOINT);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const projects = await response.json();
        console.log('Projects fetched:', projects);
        
        displayProjects(projects);
        
    } catch (error) {
        console.error('Error fetching projects:', error);
        displayError();
    }
}

// Display projects in the grid
function displayProjects(projects) {
    // Remove loading spinner
    if (loadingSpinner) {
        loadingSpinner.remove();
    }
    
    // Clear the grid
    projectsGrid.innerHTML = '';
    
    if (!projects || projects.length === 0) {
        displayEmpty();
        return;
    }
    
    // Create project cards
    projects.forEach(project => {
        const projectCard = createProjectCard(project);
        projectsGrid.appendChild(projectCard);
    });
}

// Create a project card element
function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'bg-gradient-to-br from-card-bg to-slate-700 rounded-2xl overflow-hidden shadow-xl border border-border-dark';
    
    // Generate GitHub URL
    const githubUrl = `https://github.com/${GITHUB_USERNAME}/${project.name}`;
    
    // Create image element or placeholder
    const imageElement = project.image 
        ? `<img src="${project.image}" alt="${project.name}" class="absolute inset-0 w-full h-full object-cover" onerror="this.parentElement.innerHTML='<div class=\\"absolute inset-0 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center\\"><i class=\\"fas fa-code text-4xl text-white\\"></i></div>`
        : '<div class="absolute inset-0 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center"><i class="fas fa-code text-4xl text-white"></i></div>';
    
    card.innerHTML = `
        <div class="relative w-full pb-[52.36%] overflow-hidden">
            ${imageElement}
        </div>
        <div class="p-4">
            <h3 class="text-lg font-semibold font-mono mb-2 text-slate-100">${escapeHtml(project.name)}</h3>
            <p class="text-sm text-slate-400 mb-4 leading-relaxed">${escapeHtml(project.description || 'No description available.')}</p>
            <div class="flex flex-wrap gap-2">
                <a href="${githubUrl}" target="_blank" rel="noopener noreferrer" 
                   class="flex items-center gap-2 px-3 py-1.5 bg-gray-800 text-white rounded-md text-xs font-medium">
                    <i class="fab fa-github"></i>
                    <span>GitHub</span>
                </a>
                ${project.url ? `
                    <a href="${project.url}" target="_blank" rel="noopener noreferrer" 
                       class="flex items-center gap-2 px-3 py-1.5 bg-blue-600 text-white rounded-md text-xs font-medium">
                        <i class="fas fa-external-link-alt"></i>
                        <span>Open</span>
                    </a>
                ` : ''}
            </div>
        </div>
    `;
    
    return card;
}

// Display error message
function displayError() {
    if (loadingSpinner) {
        loadingSpinner.remove();
    }
    
    projectsGrid.innerHTML = `
        <div class="col-span-full text-center py-16 text-slate-400">
            <i class="fas fa-exclamation-triangle text-5xl mb-6 text-red-500"></i>
            <h3 class="text-2xl font-semibold mb-4 text-slate-300">Failed to Load Projects</h3>
            <p class="mb-8 text-lg">Unable to fetch project data. Please try again later.</p>
            <button onclick="location.reload()" class="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium">
                Retry
            </button>
        </div>
    `;
}

// Display empty state
function displayEmpty() {
    if (loadingSpinner) {
        loadingSpinner.remove();
    }
    
    projectsGrid.innerHTML = `
        <div class="col-span-full text-center py-16 text-slate-400">
            <i class="fas fa-folder-open text-5xl mb-6"></i>
            <h3 class="text-2xl font-semibold mb-4 text-slate-300">No Projects Found</h3>
            <p class="text-lg">Check back later for new projects!</p>
        </div>
    `;
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Smooth scrolling for anchor links
function smoothScroll() {
    // Smooth scrolling removed for instant navigation
}

// Add loading animation to project cards
function addCardAnimations() {
    // Animation removed - projects will display immediately without scroll effects
}

// Add scroll-based animations
function addScrollAnimations() {
    // All scroll animations removed for cleaner experience
}

// Initialize the application
function init() {
    console.log('Initializing portfolio website...');
    
    // Fetch and display projects
    fetchProjects();
    
    console.log('Portfolio website initialized!');
}

// Start the application when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
