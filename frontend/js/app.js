/*
    NYC Taxi Explorer - Frontend JavaScript
    Author: Teniola Adam Olaleye
    
    Handles API calls, charts, and UI updates
*/

const API_URL = 'http://localhost:5000';

// Chart instances (so we can destroy and recreate them)
let fareChart = null;
let zonesChart = null;

// ============================================
// API Functions
// ============================================

async function fetchSummary() {
    try {
        const res = await fetch(API_URL + '/summary');
        if (!res.ok) throw new Error('Failed to fetch');
        return await res.json();
    } catch (err) {
        console.error('Error getting summary:', err);
        return null;
    }
}

async function fetchTrips(borough, hour) {
    try {
        let url = API_URL + '/trips';
        let params = [];
        
        if (borough) params.push('borough=' + borough);
        if (hour !== '') params.push('hour=' + hour);
        
        if (params.length > 0) {
            url += '?' + params.join('&');
        }
        
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to fetch');
        return await res.json();
    } catch (err) {
        console.error('Error getting trips:', err);
        return null;
    }
}

async function fetchAvgFareByHour() {
    try {
        const res = await fetch(API_URL + '/average-fare-by-hour');
        if (!res.ok) throw new Error('Failed to fetch');
        return await res.json();
    } catch (err) {
        console.error('Error getting fare data:', err);
        return null;
    }
}

async function fetchTopZones() {
    try {
        const res = await fetch(API_URL + '/top-zones?n=10');
        if (!res.ok) throw new Error('Failed to fetch');
        return await res.json();
    } catch (err) {
        console.error('Error getting top zones:', err);
        return null;
    }
}

// ============================================
// UI Update Functions
// ============================================

function updateSummary(data) {
    if (!data) {
        document.getElementById('total-trips').textContent = 'Error';
        document.getElementById('avg-fare').textContent = 'Error';
        document.getElementById('avg-distance').textContent = 'Error';
        return;
    }
    
    document.getElementById('total-trips').textContent = data.total_trips.toLocaleString();
    document.getElementById('avg-fare').textContent = '$' + data.average_fare;
    document.getElementById('avg-distance').textContent = data.average_distance + ' mi';
}

function updateTripsTable(trips) {
    const tbody = document.getElementById('trips-body');
    
    if (!trips || trips.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No trips found</td></tr>';
        return;
    }
    
    let html = '';
    for (let i = 0; i < trips.length; i++) {
        const trip = trips[i];
        html += '<tr>';
        html += '<td>' + (trip.pickup_zone_id || '-') + '</td>';
        html += '<td>' + (trip.dropoff_zone_id || '-') + '</td>';
        html += '<td>' + (trip.trip_distance ? trip.trip_distance.toFixed(2) : '-') + '</td>';
        html += '<td>$' + (trip.fare_amount ? trip.fare_amount.toFixed(2) : '-') + '</td>';
        html += '<td>' + (trip.trip_duration_minutes ? trip.trip_duration_minutes.toFixed(1) : '-') + '</td>';
        html += '<td>' + (trip.pickup_hour !== undefined ? trip.pickup_hour : '-') + '</td>';
        html += '</tr>';
    }
    
    tbody.innerHTML = html;
}

// ============================================
// Chart Functions
// ============================================

function renderFareByHourChart(data) {
    const ctx = document.getElementById('fare-by-hour-chart').getContext('2d');
    
    // Destroy old chart if exists
    if (fareChart) {
        fareChart.destroy();
    }
    
    if (!data || data.length === 0) {
        return;
    }
    
    // Extract hours and fares from data
    const hours = [];
    const fares = [];
    
    for (let i = 0; i < data.length; i++) {
        hours.push(data[i].hour + ':00');
        fares.push(data[i].average_fare);
    }
    
    fareChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: [{
                label: 'Average Fare ($)',
                data: fares,
                borderColor: '#FFD700',
                backgroundColor: 'rgba(255, 215, 0, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function renderTopZonesChart(data) {
    const ctx = document.getElementById('top-zones-chart').getContext('2d');
    
    // Destroy old chart if exists
    if (zonesChart) {
        zonesChart.destroy();
    }
    
    if (!data || data.length === 0) {
        return;
    }
    
    // Extract zone ids and counts
    const zones = [];
    const counts = [];
    
    for (let i = 0; i < data.length; i++) {
        zones.push('Zone ' + data[i].pickup_zone_id);
        counts.push(data[i].trip_count);
    }
    
    zonesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: zones,
            datasets: [{
                label: 'Number of Pickups',
                data: counts,
                backgroundColor: '#4CAF50',
                borderColor: '#388E3C',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',  // horizontal bar
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// ============================================
// Event Handlers
// ============================================

function setupFilters() {
    // Populate hour dropdown (0-23)
    const hourSelect = document.getElementById('hour-select');
    for (let h = 0; h < 24; h++) {
        const opt = document.createElement('option');
        opt.value = h;
        opt.textContent = h + ':00 - ' + h + ':59';
        hourSelect.appendChild(opt);
    }
    
    // Apply filters button
    document.getElementById('apply-filters').addEventListener('click', async function() {
        const borough = document.getElementById('borough-select').value;
        const hour = document.getElementById('hour-select').value;
        
        // Fetch filtered trips
        const trips = await fetchTrips(borough, hour);
        updateTripsTable(trips);
    });
}

// ============================================
// Initialize Dashboard
// ============================================

async function init() {
    console.log('Starting NYC Taxi Explorer...');
    
    // Setup filter dropdowns
    setupFilters();
    
    // Load summary stats
    const summary = await fetchSummary();
    updateSummary(summary);
    
    // Load initial trips
    const trips = await fetchTrips('', '');
    updateTripsTable(trips);
    
    // Load and render charts
    const fareData = await fetchAvgFareByHour();
    renderFareByHourChart(fareData);
    
    const zonesData = await fetchTopZones();
    renderTopZonesChart(zonesData);
    
    console.log('Dashboard loaded!');
}

// Run when page loads
document.addEventListener('DOMContentLoaded', init);
