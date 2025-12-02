#!/usr/bin/env python3
"""
Fix tracker tabs location - move from inside JavaScript to correct HTML position
"""

# Read the file
with open('index.html', 'r') as f:
    lines = f.readlines()

print(f"📖 Read {len(lines)} lines from index.html")

# The tracker tabs HTML that needs to be moved (extracted from lines 1769-1811)
tracker_tabs_html = '''
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

# Step 1: Remove incorrectly placed tabs (lines 1766-1810, 0-indexed: 1765-1809)
# Line 1767 (index 1766) is: </div><!-- End Quote Tab -->
# Line 1811 (index 1810) is: </div> (before the closing backtick)
print(f"🗑️  Removing lines 1767-1811 (incorrectly placed tabs inside JavaScript)...")

# Remove from index 1766 to 1810 (inclusive)
del lines[1766:1811]

print(f"📊 Now have {len(lines)} lines after removal")

# Step 2: Insert tracker tabs after line 1630 (the real quote tab closing)
# After removal, line numbers shift, but line 1630 stays the same since we removed after it
# Line 1630 (index 1629) should be: </div> (quote tab close)
# We want to insert after index 1629

insert_index = 1630  # Insert after line 1630

print(f"📍 Inserting tracker tabs after line {insert_index} (after quote tab closes)...")

# Insert the tracker tabs HTML
lines.insert(insert_index, tracker_tabs_html)

print(f"📊 Now have {len(lines)} lines after insertion")

# Step 3: Write the fixed file
with open('index.html', 'w') as f:
    f.writelines(lines)

print(f"✅ Fixed! Tracker tabs moved to correct location")
print(f"   - Removed from JavaScript template literal (was lines 1767-1811)")
print(f"   - Inserted after quote tab (line 1630)")
print(f"   - File saved successfully")
