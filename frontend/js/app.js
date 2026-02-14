// =============================================================================
// NYC Yellow Taxi Explorer - Frontend JavaScript
// =============================================================================
// Responsibility: Gael Kamunuga Mparaye (Frontend Dashboard)
//
// This file handles:
// 1. Fetching data from backend API
// 2. Rendering charts using Chart.js
// 3. Handling filter interactions
// 4. Updating the UI dynamically
// =============================================================================

// API Base URL - change this if backend runs on different port
const API_BASE_URL = 'http://localhost:5000';

// =============================================================================
// API FUNCTIONS - Fetch data from backend
// =============================================================================

/**
 * Fetch summary statistics from the backend
 * Endpoint: GET /summary
 */
async function fetchSummary() {
    // TODO: Gael - Implement API call
    try {
        const response = await fetch(`${API_BASE_URL}/summary`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching summary:', error);
        return null;
    }
}

/**
 * Fetch trips with optional filters
 * Endpoint: GET /trips?borough=&hour=
 */
async function fetchTrips(borough = '', hour = '') {
    // TODO: Gael - Implement API call with query parameters
    try {
        let url = `${API_BASE_URL}/trips`;
        const params = new URLSearchParams();
        
        if (borough) params.append('borough', borough);
        if (hour) params.append('hour', hour);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching trips:', error);
        return null;
    }
}

/**
 * Fetch average fare by hour
 * Endpoint: GET /average-fare-by-hour
 */
async function fetchAverageFareByHour() {
    // TODO: Gael - Implement API call
    try {
        const response = await fetch(`${API_BASE_URL}/average-fare-by-hour`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching average fare:', error);
        return null;
    }
}

/**
 * Fetch top N busiest zones
 * Endpoint: GET /top-zones?n=10
 */
async function fetchTopZones(n = 10) {
    // TODO: Gael - Implement API call
    try {
        const response = await fetch(`${API_BASE_URL}/top-zones?n=${n}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching top zones:', error);
        return null;
    }
}

// =============================================================================
// CHART FUNCTIONS - Render visualizations
// =============================================================================

/**
 * Render the trips by hour bar chart
 */
function renderTripsbyHourChart(data) {
    // TODO: Gael - Implement chart rendering
    const ctx = document.getElementById('trips-by-hour-chart').getContext('2d');
    
    // Example Chart.js configuration
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.hours,       // Array of hours [0, 1, 2, ..., 23]
            datasets: [{
                label: 'Number of Trips',
                data: data.counts,    // Array of trip counts
                backgroundColor: '#FFD700',
                borderColor: '#e6c200',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Render the top zones horizontal bar chart
 */
function renderTopZonesChart(data) {
    // TODO: Gael - Implement chart rendering
    const ctx = document.getElementById('top-zones-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.zone_names,  // Array of zone names
            datasets: [{
                label: 'Pickup Count',
                data: data.counts,    // Array of pickup counts
                backgroundColor: '#4CAF50',
                borderColor: '#388E3C',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',  // Horizontal bar chart
            responsive: true
        }
    });
}

/**
 * Render the average fare by hour line chart
 */
function renderAvgFareChart(data) {
    // TODO: Gael - Implement chart rendering
    const ctx = document.getElementById('avg-fare-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.hours,
            datasets: [{
                label: 'Average Fare ($)',
                data: data.avg_fares,
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// =============================================================================
// UI UPDATE FUNCTIONS
// =============================================================================

/**
 * Update summary statistics in the UI
 */
function updateSummaryUI(data) {
    // TODO: Gael - Update the stat cards with real data
    document.getElementById('total-trips').textContent = data.total_trips.toLocaleString();
    document.getElementById('avg-fare').textContent = '$' + data.avg_fare.toFixed(2);
    document.getElementById('avg-distance').textContent = data.avg_distance.toFixed(2) + ' miles';
}

/**
 * Populate the trips table with data
 */
function populateTripsTable(trips) {
    // TODO: Gael - Populate the table with trip data
    const tbody = document.getElementById('trips-table-body');
    tbody.innerHTML = '';  // Clear existing rows
    
    trips.forEach(trip => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${trip.pickup_zone}</td>
            <td>${trip.dropoff_zone}</td>
            <td>${trip.distance.toFixed(2)}</td>
            <td>$${trip.fare.toFixed(2)}</td>
            <td>${trip.duration.toFixed(1)}</td>
        `;
        tbody.appendChild(row);
    });
}

// =============================================================================
// EVENT HANDLERS
// =============================================================================

/**
 * Handle filter button click
 */
function setupFilterHandlers() {
    // TODO: Gael - Add event listeners for filters
    const applyBtn = document.getElementById('apply-filters');
    
    applyBtn.addEventListener('click', async () => {
        const borough = document.getElementById('borough-select').value;
        const hour = document.getElementById('hour-select').value;
        
        // Fetch filtered data and update UI
        const trips = await fetchTrips(borough, hour);
        if (trips) {
            populateTripsTable(trips);
        }
    });
}

/**
 * Populate hour dropdown (0-23)
 */
function populateHourDropdown() {
    const select = document.getElementById('hour-select');
    for (let i = 0; i < 24; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i}:00 - ${i}:59`;
        select.appendChild(option);
    }
}

/**
 * Populate borough dropdown
 */
function populateBoroughDropdown() {
    const boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island', 'EWR'];
    const select = document.getElementById('borough-select');
    
    boroughs.forEach(borough => {
        const option = document.createElement('option');
        option.value = borough;
        option.textContent = borough;
        select.appendChild(option);
    });
}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Initialize the dashboard when page loads
 */
async function initDashboard() {
    console.log('Initializing NYC Taxi Explorer Dashboard...');
    
    // Populate dropdowns
    populateHourDropdown();
    populateBoroughDropdown();
    
    // Setup event handlers
    setupFilterHandlers();
    
    // TODO: Gael - Fetch initial data and render charts
    // const summary = await fetchSummary();
    // if (summary) updateSummaryUI(summary);
    
    // const avgFareData = await fetchAverageFareByHour();
    // if (avgFareData) renderAvgFareChart(avgFareData);
    
    // const topZonesData = await fetchTopZones(10);
    // if (topZonesData) renderTopZonesChart(topZonesData);
    
    console.log('Dashboard initialized!');
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);
