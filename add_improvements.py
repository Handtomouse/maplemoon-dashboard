#!/usr/bin/env python3
"""
Add 4 dashboard improvements:
1. Cost breakdown tooltips
2. Asset library tab
3. Mobile optimization
4. Approval workflow system
"""

# Read the HTML file
with open('index.html', 'r') as f:
    html = f.read()

print("📖 Read index.html")

# ============================================================================
# IMPROVEMENT 1: COST BREAKDOWN TOOLTIPS
# ============================================================================

tooltip_css = '''
        /* Cost Breakdown Tooltips */
        .price-tooltip {
            position: relative;
            cursor: help;
        }

        .price-tooltip::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #66584D;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            line-height: 1.4;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
        }

        .price-tooltip::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: #66584D;
            opacity: 0;
            transition: opacity 0.3s ease;
            margin-bottom: 2px;
        }

        .price-tooltip:hover::after,
        .price-tooltip:hover::before {
            opacity: 1;
        }

        .rate-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 6px;
        }

        .rate-badge.full {
            background: rgba(52, 152, 219, 0.15);
            color: #3498DB;
        }

        .rate-badge.discount {
            background: rgba(46, 204, 113, 0.15);
            color: #27AE60;
        }

        .rate-badge.mates {
            background: rgba(243, 156, 18, 0.15);
            color: #F39C12;
        }
'''

# Find </style> before </head> and insert tooltip CSS
style_end = html.find('</style>', 0, html.find('</head>'))
html = html[:style_end] + tooltip_css + html[style_end:]

print("✅ Added tooltip CSS")

# ============================================================================
# IMPROVEMENT 2: MOBILE OPTIMIZATION CSS
# ============================================================================

mobile_css = '''
        /* Mobile Optimization */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
                max-width: 100%;
            }

            h1 {
                font-size: 1.5rem !important;
            }

            h2 {
                font-size: 1.25rem !important;
            }

            /* Tab Navigation - Convert to Dropdown on Mobile */
            .tab-navigation {
                flex-direction: column;
                gap: 5px;
                border-bottom: none;
            }

            .tab-button {
                width: 100%;
                text-align: left;
                border-bottom: 1px solid rgba(212, 165, 116, 0.2);
                border-radius: 8px;
                padding: 14px 16px;
            }

            .tab-button.active {
                background: rgba(212, 165, 116, 0.2);
            }

            /* Kanban Board - Single Column on Mobile */
            .kanban-board {
                grid-template-columns: 1fr;
                gap: 15px;
            }

            .kanban-column {
                width: 100%;
            }

            /* Stats - Stack Vertically */
            .tracker-stats {
                grid-template-columns: 1fr;
                gap: 12px;
            }

            .stat-card {
                padding: 15px;
            }

            .stat-value {
                font-size: 1.75rem;
            }

            /* Spec Table - Horizontal Scroll */
            .spec-table-container {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }

            .spec-table {
                min-width: 600px;
                font-size: 0.85rem;
            }

            .spec-table th,
            .spec-table td {
                padding: 10px 8px;
            }

            /* Timeline */
            .timeline-countdown {
                font-size: 2rem;
            }

            /* Pricing Table */
            .pricing-table {
                font-size: 0.85rem;
            }

            .pricing-row {
                grid-template-columns: 1fr;
                gap: 8px;
                padding: 12px;
            }

            /* Buttons - Larger Touch Targets */
            button, .button, .tab-button {
                min-height: 44px;
                padding: 12px 16px;
            }

            /* Tooltips - Better Mobile Positioning */
            .price-tooltip::after {
                white-space: normal;
                max-width: 250px;
                left: 0;
                transform: none;
            }

            .price-tooltip::before {
                left: 20px;
                transform: none;
            }
        }

        @media (max-width: 480px) {
            .container {
                padding: 10px;
            }

            h1 {
                font-size: 1.25rem !important;
            }

            .stat-value {
                font-size: 1.5rem;
            }

            .timeline-countdown {
                font-size: 1.75rem;
            }
        }
'''

# Insert mobile CSS after tooltip CSS
html = html[:style_end] + mobile_css + html[style_end:]

print("✅ Added mobile-responsive CSS")

# ============================================================================
# IMPROVEMENT 3: APPROVAL WORKFLOW CSS
# ============================================================================

approval_css = '''
        /* Approval Workflow System */
        .approval-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 8px;
        }

        .approval-status.pending {
            background: rgba(243, 156, 18, 0.15);
            color: #F39C12;
        }

        .approval-status.approved {
            background: rgba(46, 204, 113, 0.15);
            color: #27AE60;
        }

        .approval-status.changes-requested {
            background: rgba(231, 76, 60, 0.15);
            color: #E74C3C;
        }

        .approval-buttons {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }

        .approve-btn,
        .changes-btn {
            flex: 1;
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .approve-btn {
            background: #27AE60;
            color: white;
        }

        .approve-btn:hover {
            background: #229954;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
        }

        .changes-btn {
            background: rgba(231, 76, 60, 0.1);
            color: #E74C3C;
            border: 1px solid rgba(231, 76, 60, 0.3);
        }

        .changes-btn:hover {
            background: rgba(231, 76, 60, 0.2);
            transform: translateY(-1px);
        }

        /* Approval Modal */
        .approval-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 10000;
            align-items: center;
            justify-content: center;
        }

        .approval-modal.active {
            display: flex;
        }

        .approval-modal-content {
            background: white;
            padding: 30px;
            border-radius: 16px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        .approval-modal h3 {
            margin: 0 0 20px 0;
            color: #66584D;
        }

        .approval-modal textarea {
            width: 100%;
            min-height: 120px;
            padding: 12px;
            border: 2px solid rgba(212, 165, 116, 0.3);
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.95rem;
            resize: vertical;
        }

        .approval-modal textarea:focus {
            outline: none;
            border-color: #D4A574;
        }

        .approval-modal-buttons {
            display: flex;
            gap: 12px;
            margin-top: 20px;
        }

        .approval-modal-buttons button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .submit-feedback-btn {
            background: #E74C3C;
            color: white;
        }

        .submit-feedback-btn:hover {
            background: #C0392B;
        }

        .cancel-feedback-btn {
            background: rgba(0, 0, 0, 0.05);
            color: #666;
        }

        .cancel-feedback-btn:hover {
            background: rgba(0, 0, 0, 0.1);
        }
'''

html = html[:style_end] + approval_css + html[style_end:]

print("✅ Added approval workflow CSS")

# ============================================================================
# IMPROVEMENT 4: ASSET LIBRARY TAB
# ============================================================================

# Find the timeline tab button and add asset library button after it
timeline_button = html.find('<button class="tab-button" onclick="switchTab(\'timeline\', event)">Timeline</button>')
asset_button = '\n        <button class="tab-button" onclick="switchTab(\'assets\', event)">Assets & Specs</button>'

html = html[:timeline_button + len('<button class="tab-button" onclick="switchTab(\'timeline\', event)">Timeline</button>')] + asset_button + html[timeline_button + len('<button class="tab-button" onclick="switchTab(\'timeline\', event)">Timeline</button>'):]

print("✅ Added Assets & Specs tab button")

# Find the timeline tab content and add asset library tab after it
timeline_tab_end = html.find('</div>\n    </div>\n\n    \n    <script>', html.find('<div id="timeline-tab" class="tab-content">'))

asset_library_tab = '''

    <!-- Assets & Specs Tab -->
    <div id="assets-tab" class="tab-content">
        <h2 style="color: var(--mm-brown); margin-bottom: 20px;">Assets & Specifications Library</h2>

        <div style="background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #3498DB;">
            <strong style="color: #3498DB;">📦 Central Asset Repository</strong>
            <p style="margin: 8px 0 0 0; color: #666;">All required specs, barcodes, and dimensions in one place. Items marked in red need your attention.</p>
        </div>

        <div class="spec-table-container">
            <table class="spec-table" id="asset-table">
                <!-- Asset table will be loaded via JavaScript -->
            </table>
        </div>
    </div>
'''

html = html[:timeline_tab_end] + asset_library_tab + html[timeline_tab_end:]

print("✅ Added Assets & Specs tab content")

# Write updated HTML
with open('index.html', 'w') as f:
    f.write(html)

print("✅ Updated index.html with all improvements")
print("\n📋 Summary:")
print("   1. ✅ Cost breakdown tooltips (CSS added)")
print("   2. ✅ Asset library tab (HTML + button added)")
print("   3. ✅ Mobile optimization (Responsive CSS added)")
print("   4. ✅ Approval workflow UI (CSS added)")
print("\n⚠️  Still need to:")
print("   - Update JavaScript to render tooltips on prices")
print("   - Update JavaScript to render asset library table")
print("   - Update JavaScript to handle approval workflow")
print("   - Update project_status.json with approval/asset data")
