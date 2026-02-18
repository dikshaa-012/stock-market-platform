const API_BASE = 'http://localhost:8000/api';

// Navigation
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Remove active class from all buttons and sections
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

        // Add active class to clicked button and corresponding section
        e.target.classList.add('active');
        const sectionId = e.target.dataset.section;
        document.getElementById(sectionId).classList.add('active');

        // Load data for section
        if (sectionId === 'dashboard') loadDashboard();
        else if (sectionId === 'companies') loadCompanies();
    });
});

// Load dashboard
async function loadDashboard() {
    try {
        const [gainers, losers] = await Promise.all([
            fetch(`${API_BASE}/top-gainers`).then(r => r.json()),
            fetch(`${API_BASE}/top-losers`).then(r => r.json())
        ]);

        const gainersList = document.getElementById('gainers-list');
        const losersList = document.getElementById('losers-list');

        gainersList.innerHTML = gainers.gainers.map(stock =>
            `<div class="stock-item">
                <span class="stock-ticker">${stock.ticker}</span>
                <span>${stock.name}</span>
                <span class="return-positive">+${stock.return_percent}%</span>
            </div>`
        ).join('');

        losersList.innerHTML = losers.losers.map(stock =>
            `<div class="stock-item">
                <span class="stock-ticker">${stock.ticker}</span>
                <span>${stock.name}</span>
                <span class="return-negative">${stock.return_percent}%</span>
            </div>`
        ).join('');
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load companies
async function loadCompanies() {
    try {
        const companies = await fetch(`${API_BASE}/companies`).then(r => r.json());
        const grid = document.getElementById('companies-grid');

        grid.innerHTML = companies.map(company =>
            `<div class="company-card">
                <div class="company-ticker">${company.ticker}</div>
                <div class="company-name">${company.name}</div>
                <div class="company-sector">${company.sector}</div>
            </div>`
        ).join('');

        // Add click handlers to load detailed data
        document.querySelectorAll('.company-card').forEach(card => {
            card.addEventListener('click', () => {
                const ticker = card.querySelector('.company-ticker').textContent;
                loadStockDetail(ticker);
            });
        });
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

// Load stock detail
async function loadStockDetail(ticker) {
    try {
        const data = await fetch(`${API_BASE}/stock/${ticker}?days=30`).then(r => r.json());
        const stats = await fetch(`${API_BASE}/summary/${ticker}`).then(r => r.json());

        // Switch to analysis section
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        document.querySelector('[data-section="analysis"]').classList.add('active');
        document.getElementById('analysis').classList.add('active');

        // Populate forms
        document.getElementById('analysisTicker').value = ticker;

        // Display charts
        displayPriceChart(data);
        displayReturnsChart(data);
        displayVolatilityStats(stats);
    } catch (error) {
        console.error('Error loading stock detail:', error);
    }
}

// Display price chart
function displayPriceChart(data) {
    const dates = data.map(d => d.date);
    const prices = data.map(d => d.close_price);
    const ma7 = data.map(d => d.moving_avg_7);

    const trace1 = {
        x: dates,
        y: prices,
        name: 'Close Price',
        type: 'scatter',
        mode: 'lines',
        line: { color: '#0066cc', width: 2 }
    };

    const trace2 = {
        x: dates,
        y: ma7,
        name: '7-Day MA',
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ff6666', width: 2, dash: 'dash' }
    };

    const layout = {
        title: 'Price Trend',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price' },
        hovermode: 'x unified'
    };

    Plotly.newPlot('priceChart', [trace1, trace2], layout, { responsive: true });
}

// Display returns chart
function displayReturnsChart(data) {
    const dates = data.map(d => d.date);
    const returns = data.map(d => d.daily_return || 0);

    const colors = returns.map(r => r >= 0 ? '#00cc00' : '#ff3333');

    const trace = {
        x: dates,
        y: returns,
        name: 'Daily Returns %',
        type: 'bar',
        marker: { color: colors }
    };

    const layout = {
        title: 'Daily Returns',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Return %' },
        hovermode: 'x unified'
    };

    Plotly.newPlot('returnsChart', [trace], layout, { responsive: true });
}

// Display volatility stats
function displayVolatilityStats(stats) {
    const container = document.getElementById('volatilityStats');

    container.innerHTML = `
        <div class="stat-box">
            <label>Current Price</label>
            <value>₹${stats.current_price}</value>
        </div>
        <div class="stat-box">
            <label>52-Week High</label>
            <value>₹${stats.high_52week}</value>
        </div>
        <div class="stat-box">
            <label>52-Week Low</label>
            <value>₹${stats.low_52week}</value>
        </div>
        <div class="stat-box">
            <label>7-Day MA</label>
            <value>₹${stats.moving_avg_7}</value>
        </div>
        <div class="stat-box">
            <label>Daily Return</label>
            <value class="${stats.daily_return >= 0 ? 'return-positive' : 'return-negative'}">
                ${stats.daily_return > 0 ? '+' : ''}${stats.daily_return}%
            </value>
        </div>
        <div class="stat-box">
            <label>Volatility</label>
            <value>${stats.volatility}%</value>
        </div>
    `;
}

// Compare stocks
document.getElementById('compareBtn').addEventListener('click', async () => {
    const ticker1 = document.getElementById('ticker1').value.toUpperCase();
    const ticker2 = document.getElementById('ticker2').value.toUpperCase();
    const days = document.getElementById('compareDays').value;

    if (!ticker1 || !ticker2) {
        alert('Please enter both ticker symbols');
        return;
    }

    try {
        const comparison = await fetch(
            `${API_BASE}/compare?ticker1=${ticker1}&ticker2=${ticker2}&days=${days}`
        ).then(r => r.json());

        const resultsDiv = document.getElementById('comparison-results');
        resultsDiv.innerHTML = `
            <div class="comparison-card">
                <h3>${ticker1}</h3>
                <div class="comparison-stat">
                    <label>Current Price:</label>
                    <value>₹${comparison.stock1.current_price}</value>
                </div>
                <div class="comparison-stat">
                    <label>Return:</label>
                    <value class="${comparison.stock1.return_percent >= 0 ? 'return-positive' : 'return-negative'}">
                        ${comparison.stock1.return_percent > 0 ? '+' : ''}${comparison.stock1.return_percent}%
                    </value>
                </div>
                <div class="comparison-stat">
                    <label>Volatility:</label>
                    <value>${(comparison.stock1.volatility * 100).toFixed(2)}%</value>
                </div>
            </div>
            <div class="comparison-card">
                <h3>${ticker2}</h3>
                <div class="comparison-stat">
                    <label>Current Price:</label>
                    <value>₹${comparison.stock2.current_price}</value>
                </div>
                <div class="comparison-stat">
                    <label>Return:</label>
                    <value class="${comparison.stock2.return_percent >= 0 ? 'return-positive' : 'return-negative'}">
                        ${comparison.stock2.return_percent > 0 ? '+' : ''}${comparison.stock2.return_percent}%
                    </value>
                </div>
                <div class="comparison-stat">
                    <label>Volatility:</label>
                    <value>${(comparison.stock2.volatility * 100).toFixed(2)}%</value>
                </div>
            </div>
            <div class="comparison-card">
                <h3>Correlation Analysis</h3>
                <div class="comparison-stat">
                    <label>Correlation:</label>
                    <value>${comparison.correlation.toFixed(4)}</value>
                </div>
                <div class="comparison-stat">
                    <label>Volatility Ratio:</label>
                    <value>${comparison.volatility_ratio.toFixed(4)}</value>
                </div>
                <div class="comparison-stat">
                    <label>Return Difference:</label>
                    <value class="${comparison.return_difference >= 0 ? 'return-positive' : 'return-negative'}">
                        ${comparison.return_difference > 0 ? '+' : ''}${comparison.return_difference}%
                    </value>
                </div>
            </div>
        `;
    } catch (error) {
        alert('Error comparing stocks: ' + error.message);
    }
});

// Analyze stock
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const ticker = document.getElementById('analysisTicker').value.toUpperCase();
    const days = document.getElementById('analysisDays').value;

    if (!ticker) {
        alert('Please enter a ticker symbol');
        return;
    }

    try {
        const [data, stats] = await Promise.all([
            fetch(`${API_BASE}/stock/${ticker}?days=${days}`).then(r => r.json()),
            fetch(`${API_BASE}/summary/${ticker}`).then(r => r.json())
        ]);

        displayPriceChart(data);
        displayReturnsChart(data);
        displayVolatilityStats(stats);
    } catch (error) {
        alert('Error analyzing stock: ' + error.message);
    }
});

// Search companies
document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.company-card').forEach(card => {
        const ticker = card.querySelector('.company-ticker').textContent.toLowerCase();
        const name = card.querySelector('.company-name').textContent.toLowerCase();

        if (ticker.includes(searchTerm) || name.includes(searchTerm)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
});

// Load dashboard on page load
window.addEventListener('load', loadDashboard);
