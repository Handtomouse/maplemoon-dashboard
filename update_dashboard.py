#!/usr/bin/env python3
"""
Update dashboard to add project tracker tabs
"""
import re

# Read current index.html
with open('index.html', 'r') as f:
    html = f.read()

# Find the closing </head> tag to add tracker CSS
head_close = html.find('</head>')

tracker_css = '''
    <style>
        /* Tab Navigation */
        .tab-navigation {
            display: flex;
            gap: 10px;
            margin: 30px 0 20px 0;
            border-bottom: 2px solid #D4A574;
            padding-bottom: 0;
        }

        .tab-button {
            padding: 12px 24px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            color: #66584D;
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            bottom: -2px;
        }

        .tab-button:hover {
            color: #D4A574;
            background: rgba(212, 165, 116, 0.05);
        }

        .tab-button.active {
            color: #D4A574;
            border-bottom-color: #D4A574;
            background: rgba(212, 165, 116, 0.08);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Project Tracker Styles */
        .tracker-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(212, 165, 116, 0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .stat-label {
            font-size: 0.85rem;
            color: #66584D;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #D4A574;
        }

        .stat-value.blocked { color: #E74C3C; }
        .stat-value.progress { color: #3498DB; }
        .stat-value.ready { color: #F39C12; }

        /* Kanban Board */
        .kanban-board {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .kanban-column {
            background: rgba(212, 165, 116, 0.05);
            padding: 20px;
            border-radius: 12px;
            border: 2px solid rgba(212, 165, 116, 0.2);
        }

        .kanban-column h3 {
            margin: 0 0 20px 0;
            font-size: 1.1rem;
            color: #66584D;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .kanban-card {
            background: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            border: 1px solid rgba(212, 165, 116, 0.2);
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            transition: all 0.2s ease;
        }

        .kanban-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }

        .kanban-card.blocked {
            border-left: 4px solid #E74C3C;
        }

        .kanban-card.critical {
            background: rgba(231, 76, 60, 0.05);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }

        .card-title {
            font-weight: 700;
            color: #66584D;
            font-size: 0.95rem;
        }

        .card-price {
            color: #D4A574;
            font-weight: 700;
            font-size: 0.9rem;
        }

        .card-meta {
            font-size: 0.8rem;
            color: #999;
            margin: 8px 0;
        }

        .progress-bar {
            background: rgba(212, 165, 116, 0.2);
            height: 6px;
            border-radius: 3px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            background: #D4A574;
            height: 100%;
            transition: width 0.3s ease;
        }

        .blocker-alert {
            background: rgba(231, 76, 60, 0.1);
            color: #E74C3C;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin: 10px 0;
            font-weight: 600;
        }

        .card-notes {
            font-size: 0.85rem;
            color: #666;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(212, 165, 116, 0.2);
        }

        /* Spec Tracker Table */
        .spec-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        .spec-table th {
            background: #66584D;
            color: white;
            padding: 14px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .spec-table td {
            padding: 12px 14px;
            border-bottom: 1px solid rgba(212, 165, 116, 0.2);
            font-size: 0.9rem;
        }

        .spec-table tr:hover {
            background: rgba(212, 165, 116, 0.05);
        }

        .spec-table tr.blocked {
            background: rgba(231, 76, 60, 0.05);
        }

        .spec-status {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .spec-status.complete {
            background: rgba(46, 204, 113, 0.15);
            color: #27AE60;
        }

        .spec-status.blocked {
            background: rgba(231, 76, 60, 0.15);
            color: #E74C3C;
        }

        .spec-status.ready {
            background: rgba(243, 156, 18, 0.15);
            color: #F39C12;
        }

        .spec-status.in-progress {
            background: rgba(52, 152, 219, 0.15);
            color: #3498DB;
        }

        /* Timeline */
        .timeline-container {
            margin: 30px 0;
        }

        .timeline-header {
            background: linear-gradient(135deg, #66584D 0%, #D4A574 100%);
            color: white;
            padding: 20px;
            border-radius: 12px 12px 0 0;
            text-align: center;
        }

        .timeline-countdown {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 10px 0;
        }

        .timeline-items {
            background: white;
            padding: 20px;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        .timeline-week {
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #D4A574;
            background: rgba(212, 165, 116, 0.05);
            border-radius: 4px;
        }

        .timeline-week.blocked {
            border-left-color: #E74C3C;
            background: rgba(231, 76, 60, 0.05);
        }

        .timeline-week h4 {
            margin: 0 0 10px 0;
            color: #66584D;
            font-size: 1.1rem;
        }

        .timeline-items-list {
            list-style: none;
            padding: 0;
            margin: 10px 0 0 0;
        }

        .timeline-items-list li {
            padding: 6px 0;
            color: #666;
            font-size: 0.9rem;
        }

        .timeline-items-list li::before {
            content: "•";
            color: #D4A574;
            font-weight: bold;
            margin-right: 8px;
        }
    </style>
'''

html = html[:head_close] + tracker_css + html[head_close:]

# Find the main container after the header to add tabs
# Look for the section after the header that contains the main content
main_start = html.find('<div class="container">')

if main_start == -1:
    print("ERROR: Could not find main container")
    exit(1)

# Find where to insert tab navigation (after container opening)
insert_point = html.find('>', main_start) + 1

tab_nav = '''
    <!-- Tab Navigation -->
    <div class="tab-navigation">
        <button class="tab-button active" onclick="switchTab('quote')">Quote & Invoice</button>
        <button class="tab-button" onclick="switchTab('tracker')">Project Tracker</button>
        <button class="tab-button" onclick="switchTab('specs')">Spec Tracker</button>
        <button class="tab-button" onclick="switchTab('timeline')">Timeline</button>
    </div>

    <!-- Quote Tab (existing content) -->
    <div id="quote-tab" class="tab-content active">
'''

html = html[:insert_point] + tab_nav + html[insert_point:]

# Find the end of the main container to close the quote tab and add new tabs
container_end = html.rfind('</div>', 0, html.rfind('</body>'))

new_tabs = '''
    </div><!-- End Quote Tab -->

    <!-- Project Tracker Tab -->
    <div id="tracker-tab" class="tab-content">
        <h2 style="color: var(--mm-brown); margin-bottom: 20px;">Project Tracker</h2>

        <div class="tracker-stats" id="tracker-stats">
            <!-- Stats will be loaded via JavaScript -->
        </div>

        <div class="kanban-board" id="kanban-board">
            <!-- Kanban cards will be loaded via JavaScript -->
        </div>
    </div>

    <!-- Spec Tracker Tab -->
    <div id="specs-tab" class="tab-content">
        <h2 style="color: var(--mm-brown); margin-bottom: 20px;">Specification Tracker</h2>

        <div style="background: rgba(231, 76, 60, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #E74C3C;">
            <strong style="color: #E74C3C;">⚠️ CRITICAL BLOCKERS</strong>
            <p style="margin: 8px 0 0 0; color: #666;">The following items are blocking project progress and need immediate attention:</p>
        </div>

        <table class="spec-table" id="spec-table">
            <!-- Table will be loaded via JavaScript -->
        </table>
    </div>

    <!-- Timeline Tab -->
    <div id="timeline-tab" class="tab-content">
        <h2 style="color: var(--mm-brown); margin-bottom: 20px;">Project Timeline</h2>

        <div class="timeline-container">
            <div class="timeline-header">
                <div style="font-size: 1.1rem; opacity: 0.9;">Days Until Christmas Deadline</div>
                <div class="timeline-countdown" id="countdown">--</div>
                <div style="font-size: 0.95rem; opacity: 0.8;">Target: December 22, 2025</div>
            </div>

            <div class="timeline-items" id="timeline-items">
                <!-- Timeline will be loaded via JavaScript -->
            </div>
        </div>
    </div>
'''

html = html[:container_end] + new_tabs + html[container_end:]

# Add JavaScript before </body>
body_close = html.rfind('</body>')

tracker_js = '''
    <script>
        // Tab switching
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });

            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');

            // Activate button
            event.target.classList.add('active');

            // Load data if needed
            if (tabName !== 'quote' && !window.projectDataLoaded) {
                loadProjectData();
            }
        }

        // Load project data from JSON
        async function loadProjectData() {
            try {
                const response = await fetch('data/project_status.json');
                const data = await response.json();

                renderStats(data);
                renderKanban(data);
                renderSpecTable(data);
                renderTimeline(data);
                updateCountdown(data.project.targetDate);

                window.projectDataLoaded = true;
            } catch (error) {
                console.error('Error loading project data:', error);
            }
        }

        function renderStats(data) {
            const stats = document.getElementById('tracker-stats');
            stats.innerHTML = `
                <div class="stat-card">
                    <div class="stat-label">Total Project Value</div>
                    <div class="stat-value">$${data.project.totalValue.toLocaleString()}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">In Progress</div>
                    <div class="stat-value progress">$${data.project.inProgressValue.toLocaleString()}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Blocked</div>
                    <div class="stat-value blocked">$${data.project.blockedValue.toLocaleString()}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Ready to Start</div>
                    <div class="stat-value ready">$${data.project.readyValue.toLocaleString()}</div>
                </div>
            `;
        }

        function renderKanban(data) {
            const board = document.getElementById('kanban-board');

            const statuses = {
                'in_progress': { title: '🟢 In Progress', items: [] },
                'blocked': { title: '🔴 Blocked', items: [] },
                'ready': { title: '🟡 Ready to Start', items: [] },
                'completed': { title: '✅ Completed', items: [] }
            };

            // Group products by status
            data.products.forEach(product => {
                if (statuses[product.status]) {
                    statuses[product.status].items.push(product);
                }
            });

            // Render columns
            board.innerHTML = Object.entries(statuses).map(([status, column]) => `
                <div class="kanban-column">
                    <h3>${column.title} <span style="opacity: 0.6; font-size: 0.9rem;">(${column.items.length})</span></h3>
                    ${column.items.map(item => `
                        <div class="kanban-card ${item.blocker ? 'blocked' : ''} ${item.critical ? 'critical' : ''}">
                            <div class="card-header">
                                <div class="card-title">${item.name}</div>
                                <div class="card-price">$${item.price.toLocaleString()}</div>
                            </div>
                            <div class="card-meta">
                                ${item.week} ${item.weekDates ? `(${item.weekDates})` : ''}
                            </div>
                            ${item.progress !== undefined ? `
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${item.progress}%"></div>
                                </div>
                                <div style="font-size: 0.8rem; color: #999;">${item.progress}% complete</div>
                            ` : ''}
                            ${item.blocker ? `
                                <div class="blocker-alert">⚠️ ${item.blocker}</div>
                            ` : ''}
                            ${item.notes ? `
                                <div class="card-notes">${item.notes}</div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            `).join('');
        }

        function renderSpecTable(data) {
            const table = document.getElementById('spec-table');

            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Week</th>
                        <th>Status</th>
                        <th>Specs Complete</th>
                        <th>Blocker</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.products.map(product => `
                        <tr class="${product.blocker ? 'blocked' : ''}">
                            <td><strong>${product.fullName || product.name}</strong></td>
                            <td>${product.week}</td>
                            <td>
                                <span class="spec-status ${product.status.replace('_', '-')}">${product.status.replace('_', ' ').toUpperCase()}</span>
                            </td>
                            <td>${product.specsComplete ? '✅ Yes' : '❌ No'}</td>
                            <td style="color: ${product.blocker ? '#E74C3C' : '#999'}; font-weight: ${product.blocker ? '600' : 'normal'};">
                                ${product.blocker || '—'}
                            </td>
                            <td style="font-weight: 600;">$${product.price.toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
        }

        function renderTimeline(data) {
            const timeline = document.getElementById('timeline-items');

            const weeks = {
                'Week 1': [],
                'Week 2': [],
                'Week 3': [],
                'Week 4': [],
                'Ongoing': []
            };

            data.products.forEach(product => {
                const week = product.week || 'Other';
                if (!weeks[week]) weeks[week] = [];
                weeks[week].push(product);
            });

            timeline.innerHTML = Object.entries(weeks)
                .filter(([week, items]) => items.length > 0)
                .map(([week, items]) => {
                    const hasBlocker = items.some(item => item.blocker);
                    const weekDates = items[0]?.weekDates || '';

                    return `
                        <div class="timeline-week ${hasBlocker ? 'blocked' : ''}">
                            <h4>${week} ${weekDates ? `— ${weekDates}` : ''}</h4>
                            <ul class="timeline-items-list">
                                ${items.map(item => `
                                    <li>
                                        <strong>${item.name}</strong> ($${item.price.toLocaleString()})
                                        ${item.blocker ? `<br><span style="color: #E74C3C;">⚠️ ${item.blocker}</span>` : ''}
                                        ${item.progress !== undefined && item.progress > 0 ? `<br><span style="color: #3498DB;">${item.progress}% complete</span>` : ''}
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    `;
                }).join('');
        }

        function updateCountdown(targetDate) {
            const target = new Date(targetDate);
            const now = new Date();
            const diff = target - now;
            const days = Math.ceil(diff / (1000 * 60 * 60 * 24));

            document.getElementById('countdown').textContent = days;
        }

        // Load data when switching to tracker tabs
        window.projectDataLoaded = false;
    </script>
'''

html = html[:body_close] + tracker_js + html[body_close:]

# Write updated HTML
with open('index.html', 'w') as f:
    f.write(html)

print("✅ Dashboard updated with project tracker tabs!")
print("   - Added tab navigation")
print("   - Added Project Tracker (Kanban board)")
print("   - Added Spec Tracker (table view)")
print("   - Added Timeline view")
print("   - Added JavaScript for data loading")
