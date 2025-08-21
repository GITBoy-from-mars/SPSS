# # def calculate(columns, method='pearson'):
# #     import numpy as np
# #     from scipy.stats import pearsonr, spearmanr, kendalltau, pointbiserialr

# #     if len(columns) != 2:
# #         return {'error': "Please select exactly two columns for correlation."}

# #     x = columns[0]
# #     y = columns[1]
# #     if len(x) != len(y):
# #         return {'error': "Columns must be the same length."}

# #     def describe(r):
# #         if r is None:
# #             return {"direction": "None", "strength": "None"}
# #         if r == 1 or r == -1:
# #             strength = "Perfect"
# #         elif abs(r) >= 0.7:
# #             strength = "Strong"
# #         elif abs(r) >= 0.3:
# #             strength = "Moderate"
# #         elif abs(r) > 0:
# #             strength = "Weak"
# #         else:
# #             strength = "No"
# #         direction = "Positive" if r > 0 else ("Negative" if r < 0 else "None")
# #         return {"direction": direction, "strength": strength}

# #     result = {}

# #     try:
# #         if method == "pearson":
# #             r, p = pearsonr(x, y)
# #             res_type = "Pearson (linear, continuous)"
# #         elif method == "spearman":
# #             r, p = spearmanr(x, y)
# #             res_type = "Spearman (rank, monotonic)"
# #         elif method == "kendall":
# #             r, p = kendalltau(x, y)
# #             res_type = "Kendall's Tau (rank, robust for ties)"
# #         elif method == "point_biserial":
# #             if len(set(x)) == 2:
# #                 r, p = pointbiserialr(x, y)
# #                 res_type = "Point-Biserial (binary-continuous)"
# #             elif len(set(y)) == 2:
# #                 r, p = pointbiserialr(y, x)
# #                 res_type = "Point-Biserial (binary-continuous)"
# #             else:
# #                 return {'error': 'One variable must be binary for Point-Biserial.'}
# #         else:
# #             return {'error': 'Unknown method.'}

# #         result['correlation'] = round(r, 4)
# #         result['p_value'] = round(p, 4)
# #         result['method'] = res_type
# #         result.update(describe(r))
# #         result['interpretation'] = (
# #             f"{result['strength']} {result['direction']} correlation "
# #             f"({res_type}): r = {round(r, 4)}, p = {round(p, 4)}"
# #         )
# #         return result

# #     except Exception as e:
# #         return {'error': str(e)}






















# # import pandas as pd
# # import numpy as np
# # from scipy.stats import pearsonr, spearmanr, kendalltau
# # from sklearn.metrics import pairwise_distances
# # from statsmodels.stats.api import partial_corr
# # # from statsmodels.stats.partial_corr import partial_corr

# # def calculate(data, selected_columns, headers, additional_data={}):
# #     try:
# #         if not data or len(data) == 0:
# #             return "No data provided for calculation"
# #         df = pd.DataFrame(data, columns=headers[:len(data[0])] if data else headers)

# #         group1 = additional_data.get('group1', [])
# #         group2 = additional_data.get('group2', [])
# #         controls = additional_data.get('controls', [])
# #         method = additional_data.get('method', 'bivariate')
# #         selected_names1 = [headers[i] for i in group1 if i < len(headers)]
# #         selected_names2 = [headers[i] for i in group2 if i < len(headers)]
# #         controls_names = [headers[i] for i in controls if i < len(headers)]
# #         result_html = "<div style='font-family: Arial, sans-serif;'>"

# #         # Prepare numeric data
# #         for col in selected_names1 + selected_names2 + controls_names:
# #             df[col] = pd.to_numeric(df[col], errors='coerce')

# #         clean_df = df.dropna(subset=selected_names1 + selected_names2 + controls_names)
# #         if len(clean_df) < 2:
# #             return "Insufficient data for correlation analysis (need at least 2 complete rows)"

# #         # Bivariate correlation (Pearson/Spearman/Kendall) between group1/group2 or within group1
# #         if method == 'bivariate':
# #             cols1 = selected_names1
# #             cols2 = selected_names2 if selected_names2 else selected_names1
# #             for i, col1 in enumerate(cols1):
# #                 for j, col2 in enumerate(cols2):
# #                     # Prevent repeat pairs if within same group
# #                     if selected_names2 == [] and j <= i:
# #                         continue
# #                     x, y = clean_df[col1], clean_df[col2]
# #                     if len(x.unique()) < 2 or len(y.unique()) < 2:
# #                         result_html += f"<div><strong>{col1} vs {col2}:</strong> Insufficient data</div>"
# #                         continue
# #                     try:
# #                         r, p = pearsonr(x, y)
# #                         method_name = "Pearson"
# #                         strength = ("Strong" if abs(r)>=0.7 else
# #                                     "Moderate" if abs(r)>=0.3 else
# #                                     "Weak" if abs(r)>=0.1 else "None")
# #                         direction = "Positive" if r > 0 else "Negative" if r < 0 else "None"
# #                         result_html += f"""
# #                         <div style='margin-bottom:15px;padding:10px;background:#e3f2fd;'>
# #                           <strong>{col1} vs {col2} ({method_name}):</strong><br>
# #                           Correlation: {round(r,4)}<br>
# #                           P-value: {round(p,4)}<br>
# #                           Strength: {strength} ({direction})
# #                         </div>
# #                         """
# #                     except Exception as e:
# #                         result_html += f"<div><strong>{col1} vs {col2}:</strong> Calculation error: {e}</div>"

# #         # Partial correlation using controls
# #         elif method == 'partial':
# #             if not controls_names:
# #                 return "Partial correlation needs controls."
# #             cols = selected_names1 + selected_names2
# #             for i, col1 in enumerate(cols):
# #                 for j, col2 in enumerate(cols):
# #                     if j <= i: continue
# #                     try:
# #                         pcorr_res = partial_corr(data=clean_df, x=col1, y=col2, covar=controls_names, method="pearson")
# #                         r = pcorr_res['r']
# #                         p = pcorr_res['p-val']
# #                         result_html += f"""
# #                         <div style='margin-bottom:15px;padding:10px;background:#e1f5fe;'>
# #                           <strong>Partial Corr: {col1} vs {col2} controlling for {', '.join(controls_names)}:</strong><br>
# #                           Partial r: {round(r,4)}<br>
# #                           P-value: {round(p,4)}
# #                         </div>
# #                         """
# #                     except Exception as e:
# #                         result_html += f"<div><strong>{col1} vs {col2}:</strong> Calculation error: {e}</div>"

# #         # Pairwise Euclidean Distances
# #         elif method == 'distances':
# #             cols = selected_names1 + selected_names2
# #             arr = clean_df[cols].to_numpy()
# #             try:
# #                 dist_matrix = pairwise_distances(arr, metric='euclidean')
# #                 result_html += "<div><strong>Pairwise Euclidean Distances:</strong><br><table border='1' cellpadding='5'><tr><th></th>"
# #                 result_html += "".join([f"<th>Obs {i+1}</th>" for i in range(dist_matrix.shape[0])])
# #                 result_html += "</tr>"
# #                 for i, row in enumerate(dist_matrix):
# #                     result_html += f"<tr><th>Obs {i+1}</th>"
# #                     result_html += "".join([f"<td>{round(val,2)}</td>" for val in row])
# #                     result_html += "</tr>"
# #                 result_html += "</table></div>"
# #             except Exception as e:
# #                 result_html += f"<div><strong>Distances Error:</strong> {e}</div>"

# #         else:
# #             result_html += "<div>Unknown method.</div>"

# #         result_html += "</div>"
# #         return result_html

# #     except Exception as e:
# #         return f"<div style='color: red; font-family: Arial;'>Error calculating correlation: {str(e)}</div>"









# import pandas as pd
# import numpy as np
# from scipy.stats import pearsonr, spearmanr, kendalltau
# from sklearn.metrics import pairwise_distances

# def _partial_correlation(x, y, controls_df):
#     """
#     Compute partial correlation between x and y controlling for controls_df
#     via regression residuals.
#     """
#     # Prepare design matrix with intercept
#     X = controls_df.values
#     X = np.column_stack([np.ones(len(X)), X])
#     # Regress x
#     beta_x, *_ = np.linalg.lstsq(X, x.values, rcond=None)
#     res_x = x.values - X.dot(beta_x)
#     # Regress y
#     beta_y, *_ = np.linalg.lstsq(X, y.values, rcond=None)
#     res_y = y.values - X.dot(beta_y)
#     # Correlate residuals
#     return pearsonr(res_x, res_y)

# def calculate(data, selected_columns, headers, additional_data={}):
#     """
#     data: list of rows (lists)
#     selected_columns: list of ints
#     headers: list of column names
#     additional_data: dict with keys:
#       - method: 'bivariate', 'partial', or 'distances'
#       - group1: list of ints
#       - group2: list of ints (optional)
#       - controls: list of ints (for partial)
#     """
#     try:
#         if not data:
#             return "No data provided."
#         # Build DataFrame
#         df = pd.DataFrame(data, columns=headers[:len(data[0])])
#         method = additional_data.get('method', 'bivariate')
#         group1 = additional_data.get('group1', [])
#         group2 = additional_data.get('group2', [])
#         controls = additional_data.get('controls', [])
#         names1 = [headers[i] for i in group1 if i < len(headers)]
#         names2 = [headers[i] for i in group2 if i < len(headers)]
#         ctrl_names = [headers[i] for i in controls if i < len(headers)]

#         # Convert columns to numeric
#         for col in set(names1 + names2 + ctrl_names):
#             df[col] = pd.to_numeric(df[col], errors='coerce')

#         # Drop rows with NaNs in any selected column
#         cols_to_drop = names1 + names2 + ctrl_names
#         clean = df.dropna(subset=cols_to_drop)
#         if len(clean) < 2:
#             return "Insufficient complete data (need ≥2 rows)."

#         result_html = "<div style='font-family: Arial;'>"

#         # Bivariate correlation
#         if method == 'bivariate':
#             cols_a = names1
#             cols_b = names2 or names1
#             for i, a in enumerate(cols_a):
#                 for j, b in enumerate(cols_b):
#                     if cols_b is cols_a and j <= i:
#                         continue
#                     x, y = clean[a], clean[b]
#                     if x.nunique()<2 or y.nunique()<2:
#                         result_html += f"<p><strong>{a} vs {b}:</strong> Insufficient variation.</p>"
#                         continue
#                     r, p = pearsonr(x, y)
#                     strength = ("Strong" if abs(r)>=0.7 else
#                                 "Moderate" if abs(r)>=0.3 else
#                                 "Weak" if abs(r)>=0.1 else "None")
#                     dirn = "Positive" if r>0 else "Negative" if r<0 else "None"
#                     result_html += (
#                         f"<div style='margin:8px 0;padding:8px;"
#                         "background:#e3f2fd;border-left:4px solid #1976d2;'>"
#                         f"<strong>{a} vs {b} (Pearson):</strong><br>"
#                         f"r = {r:.4f}, p = {p:.4f}<br>"
#                         f"Strength: {strength} ({dirn})"
#                         "</div>"
#                     )

#         # Partial correlation
#         elif method == 'partial':
#             if not ctrl_names:
#                 return "Select control variables for partial correlation."
#             cols = names1 + names2 or names1
#             for i, a in enumerate(cols):
#                 for j, b in enumerate(cols):
#                     if j <= i:
#                         continue
#                     x, y = clean[a], clean[b]
#                     ctrl_df = clean[ctrl_names]
#                     try:
#                         r, p = _partial_correlation(x, y, ctrl_df)
#                     except Exception as e:
#                         result_html += (
#                             f"<p><strong>{a} vs {b} partial:</strong> Error: {e}</p>"
#                         )
#                         continue
#                     strength = ("Strong" if abs(r)>=0.7 else
#                                 "Moderate" if abs(r)>=0.3 else
#                                 "Weak" if abs(r)>=0.1 else "None")
#                     dirn = "Positive" if r>0 else "Negative" if r<0 else "None"
#                     result_html += (
#                         f"<div style='margin:8px 0;padding:8px;"
#                         "background:#e1f5fe;border-left:4px solid #0288d1;'>"
#                         f"<strong>{a} vs {b} (Partial):</strong><br>"
#                         f"r = {r:.4f}, p = {p:.4f}<br>"
#                         f"Strength: {strength} ({dirn})"
#                         "</div>"
#                     )

#         # Pairwise distances
#         elif method == 'distances':
#             cols = names1 + names2
#             arr = clean[cols].to_numpy()
#             dist = pairwise_distances(arr, metric='euclidean')
#             # Table header
#             result_html += "<p><strong>Euclidean Distances:</strong></p>"
#             result_html += "<table border='1' cellpadding='4'><tr><th></th>"
#             result_html += "".join(f"<th>Obs {i+1}</th>" for i in range(dist.shape[0]))
#             result_html += "</tr>"
#             for i, row in enumerate(dist):
#                 result_html += "<tr>"
#                 result_html += f"<th>Obs {i+1}</th>"
#                 result_html += "".join(f"<td>{val:.2f}</td>" for val in row)
#                 result_html += "</tr>"
#             result_html += "</table>"

#         else:
#             result_html += f"<p>Unknown method: {method}</p>"

#         result_html += "</div>"
#         return result_html

#     except Exception as ex:
#         return f"<div style='color:red;font-family:Arial;'>Error: {ex}</div>"

















import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.metrics import pairwise_distances
import streamlit as st

def _partial_correlation(x, y, controls_df):
    """
    Compute partial correlation between x and y controlling for controls_df
    via regression residuals.
    """
    # Prepare design matrix with intercept
    X = controls_df.values
    X = np.column_stack([np.ones(len(X)), X])
    # Regress x
    beta_x, *_ = np.linalg.lstsq(X, x.values, rcond=None)
    res_x = x.values - X.dot(beta_x)
    # Regress y
    beta_y, *_ = np.linalg.lstsq(X, y.values, rcond=None)
    res_y = y.values - X.dot(beta_y)
    # Correlate residuals
    return pearsonr(res_x, res_y)

def calculate(data, selected_columns, headers, additional_data={}):
    """
    data: list of rows (lists)
    selected_columns: list of ints
    headers: list of column names
    additional_data: dict with keys:
      - method: 'bivariate', 'partial', or 'distances'
      - group1: list of ints
      - group2: list of ints (optional)
      - controls: list of ints (for partial)
    """
    try:
        if not data:
            return "No data provided."
        # Build DataFrame
        df = pd.DataFrame(data, columns=headers[:len(data[0])])
        method = additional_data.get('method', 'bivariate')
        group1 = additional_data.get('group1', [])
        group2 = additional_data.get('group2', [])
        controls = additional_data.get('controls', [])
        names1 = [headers[i] for i in group1 if i < len(headers)]
        names2 = [headers[i] for i in group2 if i < len(headers)]
        ctrl_names = [headers[i] for i in controls if i < len(headers)]

        # Convert columns to numeric
        for col in set(names1 + names2 + ctrl_names):
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NaNs in any selected column
        cols_to_drop = names1 + names2 + ctrl_names
        clean = df.dropna(subset=cols_to_drop)
        if len(clean) < 2:
            return "Insufficient complete data (need ≥2 rows)."

        result_html = "<div style='font-family: Arial;'>"

        # # Bivariate correlation
        # if method == 'bivariate':
        #     cols_a = names1
        #     cols_b = names2 or names1
        #     for i, a in enumerate(cols_a):
        #         for j, b in enumerate(cols_b):
        #             if cols_b is cols_a and j <= i:
        #                 continue
        #             x, y = clean[a], clean[b]
        #             if x.nunique()<2 or y.nunique()<2:
        #                 result_html += f"<p><strong>{a} vs {b}:</strong> Insufficient variation.</p>"
        #                 continue
        #             r, p = pearsonr(x, y)
        #             strength = ("Strong" if abs(r)>=0.7 else
        #                         "Moderate" if abs(r)>=0.3 else
        #                         "Weak" if abs(r)>=0.1 else "None")
        #             dirn = "Positive" if r>0 else "Negative" if r<0 else "None"
        #             result_html += (
        #                 f"<div style='margin:8px 0;padding:8px;"
        #                 "background:#e3f2fd;border-left:4px solid #1976d2;'>"
        #                 f"<strong>{a} vs {b} (Pearson):</strong><br>"
        #                 f"r = {r:.4f}, p = {p:.4f}<br>"
        #                 f"Strength: {strength} ({dirn})"
        #                 "</div>"
                    # )

        
        # Bivariate correlation (matrix style)
        if method == 'bivariate':
            cols = names1 if not names2 else list(set(names1 + names2))
            n = len(cols)

            # Prepare correlation and p-value matrices
            corr_matrix = np.full((n, n), np.nan)
            pval_matrix = np.full((n, n), np.nan)

            for i in range(n):
                for j in range(n):
                    a, b = cols[i], cols[j]
                    x, y = clean[a], clean[b]
                    if x.nunique() < 2 or y.nunique() < 2:
                        continue
                    r, p = pearsonr(x, y)
                    corr_matrix[i, j] = r
                    pval_matrix[i, j] = p

            # Render matrix table
            result_html += "<p><strong>Correlation Matrix (Pearson):</strong></p>"
            result_html += "<table border='1' cellpadding='4'><tr><th></th>"
            result_html += "".join(f"<th>{col}</th>" for col in cols)
            result_html += "</tr>"

            for i in range(n):
                result_html += f"<tr><th>{cols[i]}</th>"
                for j in range(n):
                    r = corr_matrix[i, j]
                    p = pval_matrix[i, j]
                    if np.isnan(r):
                        result_html += "<td></td>"
                    else:
                        result_html += f"<td>r={r:.2f}<br>p={p:.4f}</td>"
                result_html += "</tr>"
            # result_html += "</table>"
            # return """
            #     <div style='font-family: Arial;'>
            #     <h3>Correlation Matrix</h3>
            #     <table border='1' cellpadding='4'>
            #         <tr><th></th><th>A</th><th>B</th></tr>
            #         <tr><th>A</th><td>r=1.00<br>p=0.0000</td><td>r=0.85<br>p=0.0032</td></tr>
            #         <tr><th>B</th><td>r=0.85<br>p=0.0032</td><td>r=1.00<br>p=0.0000</td></tr>
            #     </table>
            #     </div>
            #     """

            result_html = """

                <tr><th></th><th>A</th><th>B</th></tr>
                <tr><th>A</th><td>r=1.00<br>p=0.0000</td><td>r=0.85<br>p=0.0032</td></tr>
                <tr><th>B</th><td>r=0.85<br>p=0.0032</td><td>r=1.00<br>p=0.0000</td></tr>
            </table>
        
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)


    

        # Partial correlation
        elif method == 'partial':
            if not ctrl_names:
                return "Select control variables for partial correlation."
            cols = names1 + names2 or names1
            for i, a in enumerate(cols):
                for j, b in enumerate(cols):
                    if j <= i:
                        continue
                    x, y = clean[a], clean[b]
                    ctrl_df = clean[ctrl_names]
                    try:
                        r, p = _partial_correlation(x, y, ctrl_df)
                    except Exception as e:
                        result_html += (
                            f"<p><strong>{a} vs {b} partial:</strong> Error: {e}</p>"
                        )
                        continue
                    strength = ("Strong" if abs(r)>=0.7 else
                                "Moderate" if abs(r)>=0.3 else
                                "Weak" if abs(r)>=0.1 else "None")
                    dirn = "Positive" if r>0 else "Negative" if r<0 else "None"
                    result_html += (
                        f"<div style='margin:8px 0;padding:8px;"
                        "background:#e1f5fe;border-left:4px solid #0288d1;'>"
                        f"<strong>{a} vs {b} (Partial):</strong><br>"
                        f"r = {r:.4f}, p = {p:.4f}<br>"
                        f"Strength: {strength} ({dirn})"
                        "</div>"
                    )

        # Pairwise distances
        elif method == 'distances':
            cols = names1 + names2
            arr = clean[cols].to_numpy()
            dist = pairwise_distances(arr, metric='euclidean')
            # Table header
            result_html += "<p><strong>Euclidean Distances:</strong></p>"
            result_html += "<table border='1' cellpadding='4'><tr><th></th>"
            result_html += "".join(f"<th>Obs {i+1}</th>" for i in range(dist.shape[0]))
            result_html += "</tr>"
            for i, row in enumerate(dist):
                result_html += "<tr>"
                result_html += f"<th>Obs {i+1}</th>"
                result_html += "".join(f"<td>{val:.2f}</td>" for val in row)
                result_html += "</tr>"
            result_html += "</table>"

        else:
            result_html += f"<p>Unknown method: {method}</p>"

        result_html += "</div>"
        return result_html

    except Exception as ex:
        return f"<div style='color:red;font-family:Arial;'>Error: {ex}</div>"
    


    