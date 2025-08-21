# from flask import Flask, request, jsonify, render_template
# import os
# import importlib.util

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

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

#         # Import the calculation module
#         spec = importlib.util.spec_from_file_location(calc_type, calc_file)
#         calc_module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(calc_module)

#         # Call the calculate function
#         result = calc_module.calculate(grid_data, selected_columns, headers, additional_data)
        
#         return jsonify({
#             'success': True,
#             'result': result
#         })

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import os
import importlib.util
from bs4 import BeautifulSoup
import io
import pandas as pd
from openpyxl import Workbook
import re


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
    


# @app.route('/api/export', methods=['POST'])
# def export_all():
#     history = request.json.get('history')
#     if not history:
#         return jsonify({'error': 'No results to export'}), 400

#     output = io.BytesIO()
#     # Create Excel writer
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         for entry in history:
#             sheet = entry.get('type', 'Sheet')[:31]
#             html = entry.get('output_html', '')
#             # Strip HTML tags
#             text = re.sub(r'<[^>]+>', '', html)
#             lines = [line.strip() for line in text.splitlines() if line.strip()]
#             df = pd.DataFrame({'Result': lines})
#             df.to_excel(writer, sheet_name=sheet, index=False)
#         # No writer.save() here
#     output.seek(0)

#     return send_file(
#         output,
#         as_attachment=True,
#         download_name='analysis_results.xlsx',
#         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )



@app.route('/api/export', methods=['POST'])
def export_all():
    history = request.json.get('history', [])
    # 1) If no results in history, return 400
    if not history:
        return jsonify({'error': 'No results to export'}), 400

    # Prepare in-memory Excel workbook
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sheet_count = 0
        for entry in history:
            sheet_name = str(entry.get('type', 'Sheet'))[:31] or f"Sheet{sheet_count+1}"
            html = entry.get('output_html', '')
            # 2) Strip HTML tags safely
            text = re.sub(r'<[^>]+>', '', html)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if not lines:
                # Skip empty result
                continue
            df = pd.DataFrame({'Result': lines})
            # 3) Write sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            sheet_count += 1

        # 4) If no sheets written, error
        if sheet_count == 0:
            return jsonify({'error': 'No non-empty results to export'}), 400
        # Context manager auto-saves; no writer.save()

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='analysis_results.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )



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
