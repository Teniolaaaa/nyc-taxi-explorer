// javascript for our taxi dashboard
// gael wrote this with help from kevin for the api stuff
// last edited: feb 2026

const API_URL = 'http://localhost:5000';

// need to keep track of charts so we can update them later
let fareChart = null;
let zonesChart = null;

// ==================
// api fetch functions
// ==================

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
                borderColor: '#e94560',
                backgroundColor: 'rgba(233, 69, 96, 0.2)',
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '#e94560'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, labels: { color: '#ccc' } }
            },
            scales: {
                y: { beginAtZero: false, ticks: { color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                x: { ticks: { color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.1)' } }
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
                backgroundColor: 'rgba(233, 69, 96, 0.7)',
                borderColor: '#e94560',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { ticks: { color: '#aaa' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { ticks: { color: '#ccc' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}

// ==================
// filter stuff
// ==================

function setupFilters() {
    // fill in the hour dropdown with 0-23
    const hourSelect = document.getElementById('hour-select');
    for (let h = 0; h < 24; h++) {
        const opt = document.createElement('option');
        opt.value = h;
        opt.textContent = h + ':00 - ' + h + ':59';
        hourSelect.appendChild(opt);
    }
    
    // when user clicks apply button
    document.getElementById('apply-filters').addEventListener('click', async function() {
        const borough = document.getElementById('borough-select').value;
        const hour = document.getElementById('hour-select').value;
        
        const trips = await fetchTrips(borough, hour);
        updateTripsTable(trips);
    });
}

// ==================
// main init function - runs when page loads
// ==================

async function init() {
    console.log('loading dashboard...');
    
    setupFilters();
    
    // get all the data from our api
    const summary = await fetchSummary();
    updateSummary(summary);
    
    const trips = await fetchTrips('', '');
    updateTripsTable(trips);
    
    const fareData = await fetchAvgFareByHour();
    renderFareByHourChart(fareData);
    
    const zonesData = await fetchTopZones();
    renderTopZonesChart(zonesData);
    
    // setup the map
    initMap();
    
    console.log('done!');
}

// ==================
// map stuff - shows nyc with markers for busy zones
// ==================

function initMap() {
    // create map centered on manhattan
    const map = L.map('nyc-map').setView([40.7580, -73.9855], 12);
    
    // add the tile layer (the actual map images)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        maxZoom: 19
    }).addTo(map);
    
    // popular pickup locations in nyc (approximate coords)
    // these are some of the busiest zones based on our data
    const hotspots = [
        { name: "Upper East Side South", lat: 40.7736, lng: -73.9566, trips: 4476 },
        { name: "Upper East Side North", lat: 40.7831, lng: -73.9534, trips: 4185 },
        { name: "Midtown Center", lat: 40.7549, lng: -73.9840, trips: 4030 },
        { name: "Midtown East", lat: 40.7527, lng: -73.9653, trips: 3564 },
        { name: "Times Square", lat: 40.7580, lng: -73.9855, trips: 3419 },
        { name: "Penn Station", lat: 40.7506, lng: -73.9935, trips: 3201 },
        { name: "Lincoln Square", lat: 40.7742, lng: -73.9822, trips: 2987 },
        { name: "Murray Hill", lat: 40.7479, lng: -73.9757, trips: 2845 },
        { name: "Gramercy", lat: 40.7367, lng: -73.9844, trips: 2654 },
        { name: "East Village", lat: 40.7265, lng: -73.9815, trips: 2432 }
    ];
    
    // add circle markers for each hotspot
    // bigger circle = more trips
    hotspots.forEach(spot => {
        const radius = Math.sqrt(spot.trips) * 0.8; // scale the size
        
        L.circleMarker([spot.lat, spot.lng], {
            radius: radius,
            fillColor: '#e94560',
            color: '#fff',
            weight: 2,
            opacity: 0.9,
            fillOpacity: 0.6
        }).addTo(map)
        .bindPopup('<b>' + spot.name + '</b><br>' + spot.trips.toLocaleString() + ' pickups');
    });
    
    // add a legend
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function() {
        const div = L.DomUtil.create('div', 'map-legend');
        div.innerHTML = '<div style="background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; color: white;">' +
            '<b>Pickup Hotspots</b><br>' +
            '<span style="color: #e94560;">●</span> Larger = More trips' +
            '</div>';
        return div;
    };
    legend.addTo(map);
}

// start everything when dom is ready
document.addEventListener('DOMContentLoaded', init);