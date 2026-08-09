/**
 * STTIMS Export Utilities
 * Shared helpers for exporting table data to Excel (.xlsx) and PDF.
 *
 * Requires these to be loaded BEFORE this file, in the page <head> or
 * before the closing </body>:
 *   <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
 *   <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
 *   <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
 */

function _exportFormatValue(value) {
    if (value === null || value === undefined) return '';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    return value;
}

function _exportSafeToast(message, type) {
    if (typeof showToast === 'function') {
        showToast(message, type);
    } else {
        console.log(`[export] ${type}: ${message}`);
    }
}

/**
 * Export an array of objects to an Excel (.xlsx) file.
 * @param {Array<Object>} data - rows to export
 * @param {Array<{key:string, label:string}>} columns - fields to include, in order
 * @param {string} filename - output filename, without extension
 * @param {string} [sheetName='Data']
 */
function exportArrayToExcel(data, columns, filename, sheetName = 'Data') {
    if (typeof XLSX === 'undefined') {
        _exportSafeToast('Excel export library failed to load. Check your internet connection.', 'error');
        return;
    }
    if (!data || data.length === 0) {
        _exportSafeToast('No data to export', 'warning');
        return;
    }

    const rows = data.map(item => {
        const row = {};
        columns.forEach(col => {
            row[col.label] = _exportFormatValue(item[col.key]);
        });
        return row;
    });

    const worksheet = XLSX.utils.json_to_sheet(rows);

    // Reasonable auto-width per column
    worksheet['!cols'] = columns.map(col => {
        const maxLen = Math.max(
            col.label.length,
            ...rows.map(r => String(r[col.label] ?? '').length)
        );
        return { wch: Math.min(Math.max(maxLen + 2, 10), 40) };
    });

    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

    const dateStr = new Date().toISOString().slice(0, 10);
    XLSX.writeFile(workbook, `${filename}_${dateStr}.xlsx`);

    _exportSafeToast(`Exported ${data.length} record(s) to Excel`, 'success');
}

/**
 * Export an array of objects to a PDF table.
 * @param {Array<Object>} data - rows to export
 * @param {Array<{key:string, label:string}>} columns - fields to include, in order
 * @param {string} filename - output filename, without extension
 * @param {string} [title='Report'] - heading printed at the top of the PDF
 */
function exportArrayToPDF(data, columns, filename, title = 'Report') {
    if (typeof window.jspdf === 'undefined') {
        _exportSafeToast('PDF export library failed to load. Check your internet connection.', 'error');
        return;
    }
    if (!data || data.length === 0) {
        _exportSafeToast('No data to export', 'warning');
        return;
    }

    const { jsPDF } = window.jspdf;
    const isWide = columns.length > 6;
    const doc = new jsPDF({ orientation: isWide ? 'landscape' : 'portrait', unit: 'pt' });

    doc.setFontSize(14);
    doc.setTextColor(20);
    doc.text(title, 40, 40);

    doc.setFontSize(9);
    doc.setTextColor(120);
    doc.text(`Generated: ${new Date().toLocaleString()}  |  ${data.length} record(s)`, 40, 56);

    const head = [columns.map(c => c.label)];
    const body = data.map(item => columns.map(col => {
        const v = _exportFormatValue(item[col.key]);
        return v === null || v === undefined ? '' : String(v);
    }));

    doc.autoTable({
        head,
        body,
        startY: 68,
        styles: { fontSize: 8, cellPadding: 4, overflow: 'linebreak' },
        headStyles: { fillColor: [79, 70, 229], textColor: 255 },
        alternateRowStyles: { fillColor: [245, 245, 250] },
        margin: { left: 40, right: 40 }
    });

    const dateStr = new Date().toISOString().slice(0, 10);
    doc.save(`${filename}_${dateStr}.pdf`);

    _exportSafeToast(`Exported ${data.length} record(s) to PDF`, 'success');
}

console.log('📤 export-utils.js loaded successfully');
