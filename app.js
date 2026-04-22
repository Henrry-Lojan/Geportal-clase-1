// --- VARIABLES GLOBALES ---
let map, tileLayer, cityOutlineLayer, neighborhoodLayer, mergedLayer, gridLayer;
let allNeighborhoods = [];
let selectedParishName = "";

document.addEventListener('DOMContentLoaded', async () => {
    initMap();
    await loadLocalData();
    setupFilters();
    initMeta();
});

function initMap() {
    map = L.map('map', {
        zoomControl: false, 
        fadeAnimation: false, 
        zoomAnimation: false,
        attributionControl: false
    }).setView([-4.007, -79.202], 14);
    
    tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    cityOutlineLayer = L.geoJSON(null, {
        style: { color: "#bdc3c7", weight: 0.5, fillOpacity: 0.05, interactive: false }
    }).addTo(map);

    neighborhoodLayer = L.geoJSON(null, {
        style: { color: "#2980b9", weight: 2, fillOpacity: 0.1 },
        onEachFeature: (feature, layer) => {
            layer.bindTooltip(`<b>Barrio:</b> ${feature.properties.barrio}`, { sticky: true });
        }
    }).addTo(map);

    mergedLayer = L.layerGroup().addTo(map);
    gridLayer = L.layerGroup().addTo(map);
}

function drawGrid() {
    gridLayer.clearLayers();
    const bounds = map.getBounds();
    const step = 0.005;
    const style = { color: '#000', weight: 0.5, opacity: 0.2, dashArray: '5, 5' };
    for (let lat = Math.floor(bounds.getSouth() / step) * step; lat <= bounds.getNorth(); lat += step) {
        L.polyline([[lat, bounds.getWest()], [lat, bounds.getEast()]], style).addTo(gridLayer);
    }
    for (let lng = Math.floor(bounds.getWest() / step) * step; lng <= bounds.getEast(); lng += step) {
        L.polyline([[bounds.getSouth(), lng], [bounds.getNorth(), lng]], style).addTo(gridLayer);
    }
}

function initMeta() {
    document.getElementById('print-date').innerText = new Date().toLocaleDateString();
}

window.updatePrintMeta = () => {
    document.getElementById('print-st-name').innerText = document.getElementById('student-name').value || "_________________";
};

async function loadLocalData() {
    try {
        const res = await fetch('./limites_barriales.json');
        const data = await res.json();
        allNeighborhoods = data.features;
        cityOutlineLayer.addData(data);
        map.fitBounds(cityOutlineLayer.getBounds());
    } catch (e) { console.error(e); }
}

function setupFilters() {
    const parishSelect = document.getElementById('province-select');
    const parishes = [...new Set(allNeighborhoods.map(f => f.properties.parroquia))].sort();
    parishSelect.innerHTML = '<option value="">-- Ver Toda la Ciudad --</option>';
    parishes.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p; opt.textContent = p;
        parishSelect.appendChild(opt);
    });

    parishSelect.onchange = (e) => {
        selectedParishName = e.target.value;
        const titleText = selectedParishName ? `MAPA DE LA PARROQUIA URBANA: ${selectedParishName.toUpperCase()}` : "MAPA DE LAS PARROQUIAS URBANAS DE LOJA";
        document.getElementById('map-title').innerText = titleText;
        filterMap(selectedParishName);
    };
}

function filterMap(parishName) {
    neighborhoodLayer.clearLayers();
    mergedLayer.clearLayers();
    if (parishName) {
        const filtered = allNeighborhoods.filter(f => f.properties.parroquia === parishName);
        neighborhoodLayer.addData({ type: "FeatureCollection", features: filtered });
        map.fitBounds(neighborhoodLayer.getBounds(), { padding: [50, 50] });
    } else {
        map.fitBounds(cityOutlineLayer.getBounds());
    }
}

document.getElementById('btn-clip').onclick = () => {
    if (!selectedParishName) return alert("Selecciona una parroquia.");
    mergedLayer.clearLayers();
    const parishFeatures = allNeighborhoods.filter(f => f.properties.parroquia === selectedParishName);
    try {
        let unionResult = parishFeatures[0];
        for (let i = 1; i < parishFeatures.length; i++) {
            unionResult = turf.union(unionResult, parishFeatures[i]);
        }
        const lLayer = L.geoJSON(unionResult, {
            style: { color: "#e67e22", weight: 5, fillOpacity: 0.4, dashArray: '10, 10' }
        }).addTo(mergedLayer);
        map.fitBounds(lLayer.getBounds(), { padding: [100, 100] });
        drawGrid();
    } catch (e) { alert("Error."); }
};

// --- IMPRESIÓN MAESTRA (DIMENSIONES A4 FÍSICAS) ---
document.getElementById('btn-print').onclick = function() {
    const sidebar = document.getElementById('sidebar');
    const mapCont = document.getElementById('map-container');
    const mapDiv = document.getElementById('map');
    
    // 1. Forzar tamaño A4 Landscape en píxeles
    sidebar.style.display = 'none';
    mapCont.style.width = '297mm';
    mapCont.style.height = '210mm';
    mapCont.style.marginLeft = '0';
    mapCont.style.position = 'absolute';
    mapCont.style.left = '0px';
    mapCont.style.top = '0px';
    mapCont.style.zIndex = '99999';

    // Mantenemos el tileLayer (mapa de fondo) para que salga en el PDF
    // map.removeLayer(tileLayer); <-- ESTA LÍNEA SE ELIMINA

    setTimeout(() => {
        map.invalidateSize();
        
        let targetArea = null;
        if (mergedLayer.getLayers().length > 0) {
            targetArea = L.featureGroup(mergedLayer.getLayers());
        } else if (neighborhoodLayer.getLayers().length > 0) {
            targetArea = neighborhoodLayer;
        }

        if (targetArea) {
            const bounds = targetArea.getBounds();
            const center = bounds.getCenter();
            const zoom = map.getBoundsZoom(bounds) - 1;

            // FIJAMOS EL CENTRO POR COORDENADAS (No hay fallo posible)
            map.setView(center, zoom, { animate: false });
            
            setTimeout(() => {
                drawGrid();
                setTimeout(() => {
                    window.print();
                    window.location.reload(); 
                }, 1200);
            }, 600);
        }
    }, 500);
};
