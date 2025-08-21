# from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
# import os
# import importlib.util
# from bs4 import BeautifulSoup
# import io
# import pandas as pd
# from openpyxl import Workbook
# import re


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/calculations/<filename>.html')
# def serve_calculation_html(filename):
#     """Serve calculation HTML files from calculations folder"""
#     try:
#         return send_from_directory('calculations', f"{filename}.html")
#     except FileNotFoundError:
#         return f"Calculation file '{filename}' not found", 404

# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     """Serve static files"""
#     try:
#         return send_from_directory('static', filename)
#     except FileNotFoundError:
#         return f"Static file '{filename}' not found", 404

# @app.route('/api/calculate', methods=['POST'])
# def calculate():
#     try:
#         data = request.json
#         calc_type = data.get('calculation_type')
#         grid_data = data.get('data', [])
#         selected_columns = data.get('columns', [])
#         headers = data.get('headers', [])
#         additional_data = data.get('additional_data', {})

#         # Dynamic import of calculation module
#         calc_file = f"calculations/{calc_type}.py"
        
#         if not os.path.exists(calc_file):
#             return jsonify({
#                 'success': False,
#                 'error': f'Calculation type {calc_type} not found'
#             })

#         # Import the calculation module dynamically
#         spec = importlib.util.spec_from_file_location(calc_type, calc_file)
#         calc_module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(calc_module)

#         # Call the calculate function
#         if hasattr(calc_module, 'calculate'):
#             result = calc_module.calculate(grid_data, selected_columns, headers, additional_data)
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': f'No calculate function found in {calc_type}.py'
#             })
        
#         return jsonify({
#             'success': True,
#             'result': result
#         })

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })
    


# # @app.route('/api/export', methods=['POST'])
# # def export_all():
# #     history = request.json.get('history')
# #     if not history:
# #         return jsonify({'error': 'No results to export'}), 400

# #     output = io.BytesIO()
# #     # Create Excel writer
# #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #         for entry in history:
# #             sheet = entry.get('type', 'Sheet')[:31]
# #             html = entry.get('output_html', '')
# #             # Strip HTML tags
# #             text = re.sub(r'<[^>]+>', '', html)
# #             lines = [line.strip() for line in text.splitlines() if line.strip()]
# #             df = pd.DataFrame({'Result': lines})
# #             df.to_excel(writer, sheet_name=sheet, index=False)
# #         # No writer.save() here
# #     output.seek(0)

# #     return send_file(
# #         output,
# #         as_attachment=True,
# #         download_name='analysis_results.xlsx',
# #         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# #     )



# @app.route('/api/export', methods=['POST'])
# def export_all():
#     history = request.json.get('history', [])
#     # 1) If no results in history, return 400
#     if not history:
#         return jsonify({'error': 'No results to export'}), 400

#     # Prepare in-memory Excel workbook
#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         sheet_count = 0
#         for entry in history:
#             sheet_name = str(entry.get('type', 'Sheet'))[:31] or f"Sheet{sheet_count+1}"
#             html = entry.get('output_html', '')
#             # 2) Strip HTML tags safely
#             text = re.sub(r'<[^>]+>', '', html)
#             lines = [line.strip() for line in text.splitlines() if line.strip()]
#             if not lines:
#                 # Skip empty result
#                 continue
#             df = pd.DataFrame({'Result': lines})
#             # 3) Write sheet
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#             sheet_count += 1

#         # 4) If no sheets written, error
#         if sheet_count == 0:
#             return jsonify({'error': 'No non-empty results to export'}), 400
#         # Context manager auto-saves; no writer.save()

#     output.seek(0)
#     return send_file(
#         output,
#         as_attachment=True,
#         download_name='analysis_results.xlsx',
#         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )



# @app.route('/calculations/correlate.html')
# def correlate_popup():
#     # First popup: settings UI
#     return send_from_directory('calculations', 'correlate.html')

# @app.route('/calculations/corr_result.html')
# def corr_result_popup():
#     # Second popup: matrix display UI
#     return send_from_directory('calculations', 'corr_result.html')



# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)






























# from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
# import os
# import importlib.util
# from bs4 import BeautifulSoup
# import io
# import pandas as pd
# from openpyxl import Workbook
# import re


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/calculations/<filename>.html')
# def serve_calculation_html(filename):
#     """Serve calculation HTML files from calculations folder"""
#     try:
#         return send_from_directory('calculations', f"{filename}.html")
#     except FileNotFoundError:
#         return f"Calculation file '{filename}' not found", 404

# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     """Serve static files"""
#     try:
#         return send_from_directory('static', filename)
#     except FileNotFoundError:
#         return f"Static file '{filename}' not found", 404

# @app.route('/api/calculate', methods=['POST'])
# def calculate():
#     try:
#         data = request.json
#         calc_type = data.get('calculation_type')
#         grid_data = data.get('data', [])
#         selected_columns = data.get('columns', [])
#         headers = data.get('headers', [])
#         additional_data = data.get('additional_data', {})

#         # Dynamic import of calculation module
#         calc_file = f"calculations/{calc_type}.py"
        
#         if not os.path.exists(calc_file):
#             return jsonify({
#                 'success': False,
#                 'error': f'Calculation type {calc_type} not found'
#             })

#         # Import the calculation module dynamically
#         spec = importlib.util.spec_from_file_location(calc_type, calc_file)
#         calc_module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(calc_module)

#         # Call the calculate function
#         if hasattr(calc_module, 'calculate'):
#             result = calc_module.calculate(grid_data, selected_columns, headers, additional_data)
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': f'No calculate function found in {calc_type}.py'
#             })
        
#         return jsonify({
#             'success': True,
#             'result': result
#         })

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })
    


# @app.route('/api/export', methods=['POST'])
# def export_all():
#     """
#     Improved export endpoint:
#     - Expects JSON { history: [ { type: "Label", output_html: "<table>...</table>" }, ... ] }
#     - For each history entry parses any <table> elements and writes them to Excel sheets.
#     - If no tables found for an entry, falls back to a text-based single-column sheet.
#     """
#     history = request.json.get('history', [])
#     if not history:
#         return jsonify({'error': 'No results to export'}), 400

#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         sheet_idx = 0
#         for entry in history:
#             # sheet base name (trim to Excel sheet limit)
#             base_name = str(entry.get('type', 'Sheet'))[:31] or f"Sheet{sheet_idx+1}"
#             html = entry.get('output_html', '') or ''

#             # Parse HTML for tables
#             soup = BeautifulSoup(html, 'html.parser')
#             tables = soup.find_all('table')

#             if tables:
#                 for t_i, table in enumerate(tables):
#                     # Extract rows
#                     rows = []
#                     for tr in table.find_all('tr'):
#                         # Prefer th if present in this row, otherwise td
#                         ths = tr.find_all('th')
#                         if ths:
#                             cells = [th.get_text(strip=True) for th in ths]
#                         else:
#                             tds = tr.find_all('td')
#                             cells = [td.get_text(strip=True) for td in tds]
#                         # Only append if there's any cell text (skip empty rows)
#                         if any(cell != '' for cell in cells):
#                             rows.append(cells)

#                     if not rows:
#                         continue

#                     # Normalize row lengths
#                     maxc = max(len(r) for r in rows)
#                     norm_rows = [r + [''] * (maxc - len(r)) for r in rows]

#                     # Decide DataFrame: if first row looks like header (has th in thead or the first tr had th),
#                     # use it as header; otherwise write all rows as-is.
#                     use_header = False
#                     # check for thead or first tr containing <th>
#                     if table.find('thead') is not None:
#                         use_header = True
#                     else:
#                         first_tr = table.find('tr')
#                         if first_tr and first_tr.find_all('th'):
#                             use_header = True

#                     if use_header and len(norm_rows) > 1:
#                         df = pd.DataFrame(norm_rows[1:], columns=norm_rows[0])
#                     else:
#                         # no header detected: create column names like Col1...ColN
#                         col_names = [f"Col{i+1}" for i in range(maxc)]
#                         df = pd.DataFrame(norm_rows, columns=col_names)

#                     # Write to a sheet; if multiple tables per entry, append suffix
#                     sheet_title = base_name if (t_i == 0) else f"{base_name}_{t_i+1}"
#                     sheet_title = sheet_title[:31]  # Excel sheet name limit
#                     try:
#                         df.to_excel(writer, sheet_name=sheet_title, index=False)
#                         sheet_idx += 1
#                     except Exception as e:
#                         # fallback: write as plain text sheet if DataFrame writing fails
#                         fallback_lines = [" | ".join(row) for row in norm_rows]
#                         fallback_df = pd.DataFrame({'Result': fallback_lines})
#                         fallback_title = (sheet_title + "_txt")[:31]
#                         fallback_df.to_excel(writer, sheet_name=fallback_title, index=False)
#                         sheet_idx += 1

#             else:
#                 # Fallback: no tables found -> export text content
#                 text = soup.get_text(separator='\n')
#                 lines = [ln for ln in (l.strip() for l in text.splitlines()) if ln]
#                 if not lines:
#                     continue
#                 df = pd.DataFrame({'Result': lines})
#                 try:
#                     df.to_excel(writer, sheet_name=base_name, index=False)
#                     sheet_idx += 1
#                 except Exception:
#                     # last-ditch fallback: small generic sheet
#                     small_df = pd.DataFrame({'Result': ["Export error writing sheet"]})
#                     small_df.to_excel(writer, sheet_name=(base_name)[:31], index=False)
#                     sheet_idx += 1

#         if sheet_idx == 0:
#             return jsonify({'error': 'No parsable results to export'}), 400

#     output.seek(0)
#     return send_file(
#         output,
#         as_attachment=True,
#         download_name='analysis_results.xlsx',
#         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )



# @app.route('/calculations/correlate.html')
# def correlate_popup():
#     # First popup: settings UI
#     return send_from_directory('calculations', 'correlate.html')

# @app.route('/calculations/corr_result.html')
# def corr_result_popup():
#     # Second popup: matrix display UI
#     return send_from_directory('calculations', 'corr_result.html')



# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)














# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import os
import importlib.util
from bs4 import BeautifulSoup
import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import re
import html as html_mod

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculations/<filename>.html')
def serve_calculation_html(filename):
    """Serve calculation HTML files from calculations folder"""
    try:
        return send_from_directory('calculations', f"{filename}.html")
    except FileNotFoundError:
        return f"Calculation file '{filename}' not found", 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('static', filename)
    except FileNotFoundError:
        return f"Static file '{filename}' not found", 404

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        calc_type = data.get('calculation_type')
        grid_data = data.get('data', [])
        selected_columns = data.get('columns', [])
        headers = data.get('headers', [])
        additional_data = data.get('additional_data', {})

        # Dynamic import of calculation module
        calc_file = f"calculations/{calc_type}.py"
        
        if not os.path.exists(calc_file):
            return jsonify({
                'success': False,
                'error': f'Calculation type {calc_type} not found'
            })

        # Import the calculation module dynamically
        spec = importlib.util.spec_from_file_location(calc_type, calc_file)
        calc_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(calc_module)

        # Call the calculate function
        if hasattr(calc_module, 'calculate'):
            result = calc_module.calculate(grid_data, selected_columns, headers, additional_data)
        else:
            return jsonify({
                'success': False,
                'error': f'No calculate function found in {calc_type}.py'
            })
        
        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


# ---------- helper formatting functions for Excel export ----------
def _excel_autofit_ws(ws):
    """Auto-size columns based on cell contents (best-effort)."""
    for col in ws.columns:
        max_len = 0
        try:
            col_letter = get_column_letter(col[0].column)
        except Exception:
            continue
        for cell in col:
            if cell.value is None:
                continue
            val = str(cell.value)
            if len(val) > max_len:
                max_len = len(val)
        adjusted_width = (max_len + 2)
        ws.column_dimensions[col_letter].width = adjusted_width if adjusted_width < 60 else 60


def _apply_table_style(ws, start_row, start_col, end_row, end_col):
    """Apply borders, alignment and wrap_text to a rectangular area."""
    thin = Side(border_style="thin", color="000000")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=True)


def _parse_mean_text_to_table(text):
    """
    Heuristic: parse text like shown by your mean function:
      Columns A
      Mean:
      2.1333
      Number of Observations:
      30
    Returns list of dict rows: [ { 'Variable': 'A', 'Mean': 2.1333, 'N': 30, 'Missing': ... }, ... ]
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    rows = []
    i = 0
    while i < len(lines):
        line = lines[i]
        var_match = None
        # patterns like "Columns A" or "Columns X" or "Column A" or "A:" or "1: ColumnName"
        m = re.match(r'Columns?\s+(.+)', line, flags=re.I)
        if m:
            var = m.group(1).strip()
            mean_val = None
            n_val = None
            missing = None
            # look ahead a few lines
            j = i+1
            while j < min(i+8, len(lines)):
                l = lines[j]
                if l.lower().startswith('mean'):
                    # next non-empty line is the numeric value (or same line)
                    possible = lines[j+1] if j+1 < len(lines) else ''
                    if re.match(r'^-?\d+(\.\d+)?$', possible):
                        mean_val = float(possible)
                        j += 1
                if 'number of observations' in l.lower() or 'valid cases' in l.lower() or 'valid' in l.lower():
                    possible = lines[j+1] if j+1 < len(lines) else ''
                    if re.match(r'^\d+$', possible):
                        n_val = int(possible)
                        j += 1
                if 'missing' in l.lower():
                    possible = lines[j+1] if j+1 < len(lines) else ''
                    if re.match(r'^\d+$', possible):
                        missing = int(possible)
                        j += 1
                j += 1
            rows.append({'Variable': var, 'Mean': mean_val, 'N': n_val, 'Missing': missing})
            # advance i to j
            i = j
            continue

        # alternative format: lines like "1:Name" or "A: Name"
        m2 = re.match(r'^(\d+|[A-Za-z]{1,4})\s*:\s*(.+)$', line)
        if m2:
            var = m2.group(2).strip()
            # same look-ahead
            mean_val = None
            n_val = None
            j = i+1
            while j < min(i+8, len(lines)):
                l = lines[j]
                if l.lower().startswith('mean'):
                    possible = lines[j+1] if j+1 < len(lines) else ''
                    if re.match(r'^-?\d+(\.\d+)?$', possible):
                        mean_val = float(possible)
                        j += 1
                if 'number of observations' in l.lower() or 'valid cases' in l.lower():
                    possible = lines[j+1] if j+1 < len(lines) else ''
                    if re.match(r'^\d+$', possible):
                        n_val = int(possible)
                        j += 1
                j += 1
            rows.append({'Variable': var, 'Mean': mean_val, 'N': n_val, 'Missing': None})
            i = j
            continue

        i += 1

    return rows


def _parse_generic_block_text_to_kv_blocks(text):
    """
    Parse text into labelled blocks. Useful for correlation text output that
    wasn't returned as a <table>.
    Returns list of (label, [lines...])
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    blocks = []
    cur_label = None
    cur_lines = []
    for ln in lines:
        if not ln.strip():
            # blank line -> end current block
            if cur_label or cur_lines:
                blocks.append((cur_label if cur_label else '', [l for l in cur_lines if l.strip()]))
            cur_label = None
            cur_lines = []
            continue
        # if a line looks like a variable header (short), treat as label
        if re.match(r'^[A-Za-z0-9 _-]{1,30}$', ln) and len(ln.strip()) <= 20 and len(ln.split()) <= 4:
            # If we have a current block, close it
            if cur_label or cur_lines:
                blocks.append((cur_label if cur_label else '', [l for l in cur_lines if l.strip()]))
            cur_label = ln.strip()
            cur_lines = []
        else:
            cur_lines.append(ln)
    if cur_label or cur_lines:
        blocks.append((cur_label if cur_label else '', [l for l in cur_lines if l.strip()]))
    return blocks




@app.route('/api/export', methods=['POST'])
def api_export():
    """
    Export 'history' array (frontend provided) to a single-sheet Excel workbook
    titled "Analysis Results". Each history item is appended with 5 blank rows
    between analyses. The function attempts to parse HTML tables and common
    text outputs (mean/correlation) into nicely formatted spreadsheet blocks.
    """
    try:
        payload = request.get_json(force=True) or {}
        history = payload.get('history', []) if payload else []

        # Keep only items that have non-empty output_html
        history = [h for h in history if h and h.get('output_html') and str(h.get('output_html')).strip()]
        if not history:
            return jsonify({"error": "No results to export"}), 400

        wb = Workbook()
        ws = wb.active
        ws.title = "Analysis Results"

        # Styles
        title_font = Font(bold=True, size=12)
        header_fill = PatternFill(start_color='DDDDDD', end_color='DDDDDD', fill_type='solid')
        header_font = Font(bold=True)
        left_header_fill = PatternFill(start_color='EEEEEE', end_color='EEEEEE', fill_type='solid')
        left_header_font = Font(bold=True)
        left_align = Alignment(horizontal='left', vertical='top', wrap_text=True)
        center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

        current_row = 1

        for idx, item in enumerate(history):
            entry_type = str(item.get('type', 'analysis')).strip() or f"analysis_{idx+1}"
            title = f"{entry_type.capitalize()} (analysis {idx+1})"
            html = item.get('output_html', '') or ''
            soup = BeautifulSoup(str(html), 'html.parser')

            # Try to find tables first
            tables = soup.find_all('table')
            if tables:
                # Use only first table per history item to keep structure consistent.
                # If multiple tables exist, append them sequentially.
                for t_i, table in enumerate(tables):
                    # title for this table (only write the entry title for the first table)
                    ws.cell(row=current_row, column=1, value=(title if t_i == 0 else f"{entry_type} (table {t_i+1})")).font = title_font
                    ws.cell(row=current_row, column=1).alignment = left_align
                    # if table has many columns, we won't merge — keep simple
                    current_row += 1

                    # collect rows and normalize columns
                    rows = []
                    has_th = False
                    for tr in table.find_all('tr'):
                        # if row has th use them as header cells
                        ths = tr.find_all('th')
                        if ths:
                            has_th = True
                            row_cells = [th.get_text(separator='\n').strip() for th in ths]
                        else:
                            tds = tr.find_all('td')
                            row_cells = [td.get_text(separator='\n').strip() for td in tds]
                        # convert multi-line cell text into single-line with ' ; ' separator
                        row_cells = [' ; '.join([ln.strip() for ln in rc.splitlines() if ln.strip()]) for rc in row_cells]
                        if any(rc != '' for rc in row_cells):
                            rows.append(row_cells)

                    if not rows:
                        ws.cell(row=current_row, column=1, value="(empty table)")
                        current_row += 1
                        continue

                    max_cols = max(len(r) for r in rows)
                    # normalize row lengths
                    norm_rows = [r + [''] * (max_cols - len(r)) for r in rows]

                    # decide header row: prefer explicit th/thead else use first row
                    header_row = None
                    data_rows = norm_rows
                    if has_th:
                        header_row = norm_rows[0]
                        data_rows = norm_rows[1:]
                    else:
                        # to keep spreadsheet readable, treat first row as header if it seems appropriate
                        header_row = norm_rows[0]
                        data_rows = norm_rows[1:]

                    start_data_row = current_row
                    # write header
                    for c_idx, h in enumerate(header_row, start=1):
                        cell = ws.cell(row=current_row, column=c_idx, value=h)
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = center_align
                    current_row += 1

                    # write data rows
                    for r in data_rows:
                        for c_idx in range(1, max_cols + 1):
                            val = r[c_idx - 1] if c_idx - 1 < len(r) else ''
                            cell = ws.cell(row=current_row, column=c_idx, value=(val if val != '' else None))
                            # left-most column get left-header styling for easy reading
                            if c_idx == 1:
                                cell.fill = left_header_fill
                                cell.font = left_header_font
                                cell.alignment = left_align
                            else:
                                cell.alignment = left_align
                        current_row += 1

                    # apply table border & autosize for the block
                    end_row = current_row - 1
                    end_col = max_cols
                    _apply_table_style(ws, start_data_row, 1, end_row, end_col)
                    _excel_autofit_ws(ws)

                    # small gap between multiple tables from same entry
                    current_row += 1

            else:
                # No table: try to parse common outputs
                text = soup.get_text(separator="\n").strip()
                text_lower = text.lower()

                written_any = False

                # 1) Mean-like output
                if 'mean' in text_lower and 'columns' in text_lower:
                    parsed = _parse_mean_text_to_table(text)
                    if parsed:
                        ws.cell(row=current_row, column=1, value=f"{title} - Mean").font = title_font
                        ws.cell(row=current_row, column=1).alignment = left_align
                        current_row += 1

                        headers = ['Variable', 'Mean', 'N', 'Missing']
                        for cidx, h in enumerate(headers, start=1):
                            cell = ws.cell(row=current_row, column=cidx, value=h)
                            cell.font = header_font
                            cell.fill = header_fill
                            cell.alignment = center_align
                        current_row += 1

                        for row in parsed:
                            ws.cell(row=current_row, column=1, value=row.get('Variable'))
                            ws.cell(row=current_row, column=2, value=(round(row['Mean'], 4) if row.get('Mean') is not None else None))
                            ws.cell(row=current_row, column=3, value=row.get('N'))
                            ws.cell(row=current_row, column=4, value=row.get('Missing'))
                            current_row += 1

                        _apply_table_style(ws, current_row - len(parsed) - 1, 1, current_row - 1, 4)
                        _excel_autofit_ws(ws)
                        written_any = True

                # 2) Generic correlation-like or block output -> create 2-col block
                if not written_any:
                    blocks = _parse_generic_block_text_to_kv_blocks(text)
                    if blocks:
                        ws.cell(row=current_row, column=1, value=title).font = title_font
                        ws.cell(row=current_row, column=1).alignment = left_align
                        current_row += 1

                        start_block_row = current_row
                        for label, lines in blocks:
                            if label:
                                cell = ws.cell(row=current_row, column=1, value=label)
                                cell.font = header_font
                                cell.fill = header_fill
                                cell.alignment = left_align
                                current_row += 1
                            for ln in lines:
                                # try to split into kv by ":" otherwise entire text in first column
                                if ':' in ln:
                                    left, right = ln.split(':', 1)
                                    ws.cell(row=current_row, column=1, value=left.strip())
                                    ws.cell(row=current_row, column=2, value=right.strip())
                                else:
                                    ws.cell(row=current_row, column=1, value=ln)
                                current_row += 1
                            current_row += 1

                        _apply_table_style(ws, start_block_row, 1, current_row - 1, 2)
                        _excel_autofit_ws(ws)
                        written_any = True

                # 3) Last fallback: write entire text into a single cell
                if not written_any:
                    ws.cell(row=current_row, column=1, value=title).font = title_font
                    current_row += 1
                    cell = ws.cell(row=current_row, column=1, value=text if text else "(no readable output)")
                    cell.alignment = left_align
                    current_row += 1
                    _excel_autofit_ws(ws)

            # leave 5 blank rows between analyses
            current_row += 5

        # Save workbook to bytes and return
        out = io.BytesIO()
        wb.save(out)
        out.seek(0)

        return send_file(
            out,
            as_attachment=True,
            download_name='analysis_results.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as ex:
        return jsonify({"error": f"Export failed: {str(ex)}"}), 500











# 33


# @app.route('/api/export', methods=['POST'])
# def api_export():
#     """
#     Universal exporter: accepts JSON { history: [ { type, output_html, grid_data, headers }, ... ] }
#     Produces a single workbook "Analysis Results" with each history entry appended (5 blank rows between).
#     Robust: catches per-item errors and continues; writes error notes into workbook rather than failing.
#     """
#     try:
#         payload = request.get_json(force=True) or {}
#         history = payload.get('history', []) if payload else []

#         # keep only items with any non-empty content (html/text/grid)
#         cleaned = []
#         for h in history:
#             if not h:
#                 continue
#             out_html = (h.get('output_html') or "").strip()
#             has_grid = bool(h.get('grid_data'))
#             if out_html or has_grid:
#                 cleaned.append(h)
#         history = cleaned

#         if not history:
#             return jsonify({"error": "No results to export"}), 400

#         import hashlib
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Analysis Results"

#         # Styles
#         title_font = Font(bold=True, size=12)
#         header_fill      = PatternFill(start_color='FFE6E6E6', end_color='FFE6E6E6', fill_type='solid')
#         left_header_fill = PatternFill(start_color='FFEFEFEF', end_color='FFEFEFEF', fill_type='solid')
#         row_fill_odd     = PatternFill(start_color='FFFFFFFF', end_color='FFFFFFFF', fill_type='solid')
#         row_fill_even    = PatternFill(start_color='FFFBFBFB', end_color='FFFBFBFB', fill_type='solid')
#         # header_fill = PatternFill(start_color='E6E6E6', end_color='E6E6E06', fill_type='solid')
#         # left_header_fill = PatternFill(start_color='EFEFEF', end_color='EFEFEF', fill_type='solid')
#         header_font = Font(bold=True)
#         left_header_font = Font(bold=True)
#         left_align = Alignment(horizontal='left', vertical='top', wrap_text=True)
#         center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
#         # row_fill_odd = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
#         # row_fill_even = PatternFill(start_color='FBFBFB', end_color='FBFBFB', fill_type='solid')

#         current_row = 1
#         seen_hashes = set()

#         def html_to_rows_generic(table):
#             """Return normalized rows for a BeautifulSoup table element."""
#             rows = []
#             for tr in table.find_all('tr'):
#                 # prefer th for header row
#                 ths = tr.find_all('th')
#                 if ths:
#                     cells = [th.get_text(separator='\n').strip() for th in ths]
#                 else:
#                     tds = tr.find_all('td')
#                     cells = [td.get_text(separator='\n').strip() for td in tds]
#                 # join multi-line cell contents with ' ; ' to keep it Excel-friendly
#                 cells = [' ; '.join([ln.strip() for ln in c.splitlines() if ln.strip()]) for c in cells]
#                 if any(c != '' for c in cells):
#                     rows.append(cells)
#             return rows

#         for idx, item in enumerate(history):
#             try:
#                 item_type = str(item.get('type', f"analysis_{idx+1}"))
#                 title = f"{item_type.capitalize()} (analysis {idx+1})"

#                 out_html = (item.get('output_html') or "").strip()
#                 grid = item.get('grid_data')
#                 headers = item.get('headers') or []

#                 # Skip duplicates by hash of output_html + grid data
#                 key_material = out_html if out_html else repr(grid)
#                 key_hash = hashlib.sha1(key_material.encode('utf-8')).hexdigest()
#                 if key_hash in seen_hashes:
#                     # skip duplicate content
#                     continue
#                 seen_hashes.add(key_hash)

#                 wrote = False

#                 # 1) If grid snapshot provided -> write it as a small table
#                 if grid and isinstance(grid, list) and any(len(r) for r in grid):
#                     ws.cell(row=current_row, column=1, value=title).font = title_font
#                     ws.cell(row=current_row, column=1).alignment = left_align
#                     current_row += 1
#                     # optionally write headers if provided
#                     if headers:
#                         for cidx, h in enumerate(headers, start=1):
#                             cell = ws.cell(row=current_row, column=cidx, value=h)
#                             cell.font = header_font
#                             cell.fill = header_fill
#                             cell.alignment = center_align
#                         current_row += 1
#                     # write rows
#                     for r in grid:
#                         for cidx, val in enumerate(r, start=1):
#                             ws.cell(row=current_row, column=cidx, value=(val if val != '' else None))
#                         current_row += 1
#                     _apply_table_style(ws, current_row - len(grid) - (1 if headers else 0), 1, current_row - 1, max(1, len(grid[0]) if grid else 1))
#                     _excel_autofit_ws(ws)
#                     wrote = True

#                 # 2) If HTML present -> parse and export tables or fallback to parsed text blocks
#                 if out_html:
#                     soup = BeautifulSoup(out_html, 'html.parser')
#                     tables = soup.find_all('table')

#                     if tables:
#                         # write each table sequentially under the same title
#                         ws.cell(row=current_row, column=1, value=title).font = title_font
#                         ws.cell(row=current_row, column=1).alignment = left_align
#                         current_row += 1

#                         for t_i, table in enumerate(tables):
#                             rows = html_to_rows_generic(table)
#                             if not rows:
#                                 continue
#                             maxc = max(len(r) for r in rows)
#                             norm_rows = [r + [''] * (maxc - len(r)) for r in rows]

#                             # decide header row: if first row has non-empty cells treat as header
#                             header = norm_rows[0]
#                             data_rows = norm_rows[1:] if len(norm_rows) > 1 else []

#                             # attempt to detect labeled matrix (first column is row labels and first header cell blank)
#                             labeled_matrix = False
#                             if header and header[0] == '':
#                                 # if rows have first cell non-empty, it's a labeled matrix (like correlation)
#                                 if any(dr and dr[0].strip() != '' for dr in data_rows):
#                                     labeled_matrix = True

#                             # write header(s)
#                             if labeled_matrix:
#                                 # write top-left empty then column headers from header[1:]
#                                 ws.cell(row=current_row, column=1, value='')
#                                 for cidx, h in enumerate(header[1:], start=2):
#                                     cell = ws.cell(row=current_row, column=cidx, value=h)
#                                     cell.font = header_font
#                                     cell.fill = header_fill
#                                     cell.alignment = center_align
#                             else:
#                                 for cidx, h in enumerate(header, start=1):
#                                     cell = ws.cell(row=current_row, column=cidx, value=h)
#                                     cell.font = header_font
#                                     cell.fill = header_fill
#                                     cell.alignment = center_align

#                             current_row += 1

#                             # write data rows
#                             for r_i, dr in enumerate(data_rows):
#                                 fill = row_fill_even if (r_i % 2 == 1) else row_fill_odd
#                                 if labeled_matrix:
#                                     # first column is row label
#                                     ws.cell(row=current_row, column=1, value=dr[0]).font = left_header_font
#                                     ws.cell(row=current_row, column=1).fill = left_header_fill
#                                     ws.cell(row=current_row, column=1).alignment = left_align
#                                     for cidx, val in enumerate(dr[1:], start=2):
#                                         cell = ws.cell(row=current_row, column=cidx, value=(val if val != '' else None))
#                                         cell.alignment = left_align
#                                         cell.fill = fill
#                                 else:
#                                     for cidx, val in enumerate(dr, start=1):
#                                         cell = ws.cell(row=current_row, column=cidx, value=(val if val != '' else None))
#                                         if cidx == 1:
#                                             cell.fill = left_header_fill
#                                             cell.font = left_header_font
#                                         else:
#                                             cell.fill = fill
#                                         cell.alignment = left_align
#                                 current_row += 1

#                             _apply_table_style(ws, current_row - len(data_rows) - 1, 1, current_row - 1, maxc)
#                             _excel_autofit_ws(ws)
#                             current_row += 1
#                         wrote = True

#                     else:
#                         # No table: try to parse as mean/median/mode blocks, else generic kv blocks
#                         text = soup.get_text(separator="\n").strip()
#                         low = text.lower()
#                         if 'mean' in low and 'columns' in low:
#                             parsed = _parse_mean_text_to_table(text)
#                             if parsed:
#                                 ws.cell(row=current_row, column=1, value=f"{title} - Mean").font = title_font
#                                 ws.cell(row=current_row, column=1).alignment = left_align
#                                 current_row += 1
#                                 hdrs = ['Variable', 'Mean', 'N', 'Missing']
#                                 for cidx, h in enumerate(hdrs, start=1):
#                                     cell = ws.cell(row=current_row, column=cidx, value=h)
#                                     cell.font = header_font
#                                     cell.fill = header_fill
#                                     cell.alignment = center_align
#                                 current_row += 1
#                                 for pr in parsed:
#                                     ws.cell(row=current_row, column=1, value=pr.get('Variable'))
#                                     ws.cell(row=current_row, column=2, value=(round(pr['Mean'],4) if pr.get('Mean') is not None else None))
#                                     ws.cell(row=current_row, column=3, value=pr.get('N'))
#                                     ws.cell(row=current_row, column=4, value=pr.get('Missing'))
#                                     current_row += 1
#                                 _apply_table_style(ws, current_row - len(parsed) - 1, 1, current_row - 1, 4)
#                                 _excel_autofit_ws(ws)
#                                 wrote = True

#                         if not wrote:
#                             # generic kv-block parsing
#                             blocks = _parse_generic_block_text_to_kv_blocks(text)
#                             if blocks:
#                                 ws.cell(row=current_row, column=1, value=title).font = title_font
#                                 ws.cell(row=current_row, column=1).alignment = left_align
#                                 current_row += 1
#                                 start_row_block = current_row
#                                 for label, lines in blocks:
#                                     if label:
#                                         cell = ws.cell(row=current_row, column=1, value=label)
#                                         cell.font = header_font
#                                         cell.fill = header_fill
#                                         cell.alignment = left_align
#                                         current_row += 1
#                                     for ln in lines:
#                                         if ':' in ln:
#                                             left, right = ln.split(':', 1)
#                                             ws.cell(row=current_row, column=1, value=left.strip())
#                                             ws.cell(row=current_row, column=2, value=right.strip())
#                                         else:
#                                             ws.cell(row=current_row, column=1, value=ln)
#                                         current_row += 1
#                                     current_row += 1
#                                 _apply_table_style(ws, start_row_block, 1, current_row - 1, 2)
#                                 _excel_autofit_ws(ws)
#                                 wrote = True

#                         if not wrote:
#                             # fallback: write whole text into a single cell
#                             ws.cell(row=current_row, column=1, value=title).font = title_font
#                             current_row += 1
#                             ws.cell(row=current_row, column=1, value=text)
#                             ws.cell(row=current_row, column=1).alignment = left_align
#                             current_row += 1
#                             _excel_autofit_ws(ws)
#                             wrote = True

#                 # If nothing wrote (shouldn't happen) write a small note
#                 if not wrote:
#                     ws.cell(row=current_row, column=1, value=f"{title} - (no parsable output)")
#                     current_row += 1

#             except Exception as e_item:
#                 # per-item error: write an error note and continue
#                 ws.cell(row=current_row, column=1, value=f"{item_type} (analysis {idx+1}) - Export error")
#                 ws.cell(row=current_row, column=2, value=str(e_item))
#                 current_row += 1

#             # gap of 5 rows between entries
#             current_row += 5

#         # final autosize
#         _excel_autofit_ws(ws)

#         out = io.BytesIO()
#         wb.save(out)
#         out.seek(0)
#         return send_file(
#             out,
#             as_attachment=True,
#             download_name='analysis_results.xlsx',
#             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )

#     except Exception as ex:
#         app.logger.exception("Export failed")
#         return jsonify({"error": f"Export failed: {str(ex)}"}), 500





@app.route('/calculations/correlate.html')
def correlate_popup():
    # First popup: settings UI
    return send_from_directory('calculations', 'correlate.html')

@app.route('/calculations/corr_result.html')
def corr_result_popup():
    # Second popup: matrix display UI
    return send_from_directory('calculations', 'corr_result.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
