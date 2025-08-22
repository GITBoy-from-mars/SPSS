# import numpy as np
# import pandas as pd

# def calculate(data, selected_columns, headers, additional_data={}):
#     """
#     Calculate mean for selected columns
#     """
#     try:
#         # Convert data to DataFrame
#         df = pd.DataFrame(data, columns=headers)
        
#         results = {}
        
#         for col_idx in selected_columns:
#             col_name = headers[col_idx]
#             col_data = df.iloc[:, col_idx]
            
#             # Convert to numeric, ignoring non-numeric values
#             numeric_data = pd.to_numeric(col_data, errors='coerce').dropna()
            
#             if len(numeric_data) > 0:
#                 mean_value = np.mean(numeric_data)
#                 results[col_name] = {
#                     'mean': round(mean_value, 4),
#                     'count': len(numeric_data),
#                     'valid_data_points': len(numeric_data)
#                 }
#             else:
#                 results[col_name] = {
#                     'error': 'No valid numeric data found'
#                 }
        
#         # Format results for display
#         result_html = ""
#         for col, stats in results.items():
#             if 'error' in stats:
#                 result_html += f"<p><strong>{col}:</strong> {stats['error']}</p>"
#             else:
#                 result_html += f"""
#                 <p><strong>{col}:</strong><br>
#                 Mean: {stats['mean']}<br>
#                 Valid Cases: {stats['count']}</p>
#                 """
        
#         return result_html
        
#     except Exception as e:
#         return f"Error calculating mean: {str(e)}"













import pandas as pd
import numpy as np

def calculate(data, selected_columns, headers, additional_data={}):
    """
    Calculate mean for selected columns
    """
    try:
        if not data or len(data) == 0:
            return "No data provided for calculation"
            
        if not selected_columns or len(selected_columns) == 0:
            return "No columns selected for calculation"
            
        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=headers[:len(data[0])] if data else headers)
        
        results = {}
        
        for col_idx in selected_columns:
            if col_idx >= len(headers):
                continue
                
            col_name = headers[col_idx]
            col_data = df.iloc[:, col_idx] if col_idx < df.shape[1] else pd.Series([])
            
            # Convert to numeric, ignoring non-numeric values
            numeric_data = pd.to_numeric(col_data, errors='coerce').dropna()
            
            if len(numeric_data) > 0:
                mean_value = np.mean(numeric_data)
                results[col_name] = {
                    'mean': round(mean_value, 4),
                    'count': len(numeric_data),
                    'total_cases': len(col_data),
                    'missing_cases': len(col_data) - len(numeric_data)
                }
            else:
                results[col_name] = {
                    'error': 'No valid numeric data found in this column'
                }
        
        # Format results for display
        if not results:
            return "No valid columns found for calculation"
            
        result_html = "<div style='font-family: Arial, sans-serif;'>"
        
        for col, stats in results.items():
            if 'error' in stats:
                result_html += f"""
                <div style='margin-bottom: 15px; padding: 10px; background: #ffebee; border-left: 4px solid #f44336;'>
                    <strong>{col}:</strong> {stats['error']}
                </div>
                """
            else:
                result_html += f"""
                <div style='margin-bottom: 15px; padding: 10px; background: #e8f5e8; border-left: 4px solid #4caf50;'>
                    <strong>Columns {col}</strong><br>
                    <strong>Mean:</strong> {stats['mean']}<br>
                    <strong>Number of Observations:</strong> {stats['count']}<br>
                    
                </div>
                """
        
        result_html += "</div>"
        return result_html
        
    except Exception as e:
        return f"<div style='color: red; font-family: Arial;'>Error calculating mean: {str(e)}</div>"
    


# <strong>Total Samples:</strong> {stats['total_cases']}<br>
# {f"<br><strong>Missing Samples:</strong> {stats['missing_cases']}" if stats['missing_cases'] > 0 else ""}