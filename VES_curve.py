import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.lines import Line2D

def plot_ves_curve(ab2, apparent_resistivity, station_label='VES',
                   threshold=30, layer_rhos=None, layer_thicks=None):
    """
    Plot a smooth VES sounding curve from observed field data.
    Smooth VES sounding curve with observed data and leachate threshold.
    Plot a smooth VES sounding curve and indicate interpreted layer
    boundaries with their true resistivities AND thicknesses.

    Parameters
    ----------
    ab2 : array_like
        AB/2 electrode half‑spacings (m).
    apparent_resistivity : array_like
        Apparent resistivity values (Ωm).
    station_label : str
        Title of the plot.
    threshold : float
        Resistivity (Ωm) below which the leachate zone is shaded.
    layer_rhos : list, optional
        True resistivities (Ωm) of the layers from inversion.
    layer_thicks : list, optional
        Thicknesses (m) of the layers; the last thickness (half‑space) is ignored.
    """
    log_ab2 = np.log10(ab2)
    log_rho = np.log10(apparent_resistivity)

    # Dense grid for the smooth model curve
    ab2_fine = np.logspace(np.log10(min(ab2)*0.9),
                           np.log10(max(ab2)*1.05), 400)
    cs = CubicSpline(log_ab2, log_rho)
    rho_fine = 10 ** cs(np.log10(ab2_fine))

    fig, ax = plt.subplots(figsize=(8, 6))

    # Observed data and smooth model
    ax.loglog(ab2_fine, rho_fine, 'r-', linewidth=2, label='Smooth model')
    ax.loglog(ab2, apparent_resistivity, 'ko', markersize=6, label='Observed data')

    # Leachate zone shading and threshold line
    ax.axhline(threshold, color='purple', linestyle='--', linewidth=1.5, alpha=0.8,
               label=f'Leachate zone (< {threshold} Ωm)')
    ax.fill_between([min(ab2_fine), max(ab2_fine)], 0.1, threshold,
                    color='purple', alpha=0.05)

    # ---------------------------------------------------------------
    # Layer annotation (resistivity + thickness)
    # ---------------------------------------------------------------
    if layer_rhos is not None and layer_thicks is not None:
        prev_depth = 0.0 # Start of the current layer

        # Label the first layer (from 0 to layer_thicks[0])
        if len(layer_thicks) > 0:
            rho_first_layer = layer_rhos[0]
            thick_first_layer = layer_thicks[0]

            # Position the text for the first layer.
            # Using log-midpoint between min(ab2_fine) and thick_first_layer
            x_start_plot_range = min(ab2_fine) if min(ab2_fine) > 0 else 0.1
            x_label_pos_first = np.exp((np.log(x_start_plot_range) + np.log(thick_first_layer)) / 2)

            label_text_first = f'ρ = {rho_first_layer:.1f} Ωm\nh = {thick_first_layer:.2f} m'
            ax.text(x_label_pos_first, threshold * 0.5,
                    label_text_first, fontsize=8, color='gray',
                    ha='center', va='top')

            # Draw the first interface line
            ax.axvline(x=thick_first_layer, color='gray', linestyle='--', 
                       linewidth=1.0, alpha=0.7)

            prev_depth = thick_first_layer

        # Iterate over remaining finite layers (from second layer onwards)
        for i in range(1, len(layer_thicks)):
            rho = layer_rhos[i]
            thick = layer_thicks[i]
            current_depth = prev_depth + thick

            # Vertical dashed line at current_depth (interface)
            ax.axvline(x=current_depth, color='gray', linestyle='--', 
                       linewidth=1.0, alpha=0.7)

            # Label for the current layer, placed within its depth range (logarithmic midpoint)
            x_label_pos = np.exp((np.log(prev_depth) + np.log(current_depth)) / 2)
            label_text = f'ρ = {rho:.1f} Ωm\nh = {thick:.2f} m'
            ax.text(x_label_pos, threshold * 0.5,
                    label_text, fontsize=8, color='gray',
                    ha='center', va='top')

            prev_depth = current_depth

        # Handle the last layer (half-space) if it exists
        if len(layer_rhos) > len(layer_thicks):
            half_space_rho = layer_rhos[len(layer_thicks)]
            # Place the label for the half-space after the last interface
            # Using log midpoint between the last interface and max(ab2_fine)
            x_label_pos_half_space = np.exp((np.log(prev_depth) + np.log(max(ab2_fine))) / 2)

            label_text_half_space = f'ρ = {half_space_rho:.1f} Ωm\nh = ∞'
            ax.text(x_label_pos_half_space, threshold * 0.5,
                    label_text_half_space, fontsize=8, color='gray',
                    ha='center', va='top')

    ax.set_xlabel('AB/2 (m)')
    ax.set_ylabel('Apparent Resistivity (Ωm)')
    ax.set_title(f'{station_label} Sounding Curve')
    ax.grid(True, which='both', ls=':')

    # Consolidated legend handling
    handles, labels = ax.get_legend_handles_labels()
    if layer_rhos is not None and layer_thicks is not None:
        layer_line = Line2D([0], [0], color='gray', linestyle='--', linewidth=1.0,
                            label='Layer boundaries (inversion)')
        handles.append(layer_line)
        labels.append('Layer boundaries (inversion)')
    ax.legend(handles=handles, labels=labels, loc='best')

    plt.tight_layout()
    plt.show()

# ========================================================
# CHANGE ONLY THESE VALUES
# ========================================================

# =====================================================================
# CHANGE ONLY THE VALUES BELOW FOR A DIFFERENT STATION
# =====================================================================
AB2 = np.array([1.0, 1.5, 2.0, 3.0, 4.5, 7.0, 10.0, 15.0, 20.0, 30.0, 45.0, 70.0, 100.0])
RHO = np.array([8.95, 7.48, 7.64, 8.20, 8.22, 9.36, 8.76, 13.12, 12.10, 21.10, 81.18, 86.07, 104.35])
STATION = 'VES 1'
LEACHATE_THRESHOLD = 30   # Ωm – values below this indicate possible contamination

# ---- Interpreted layers (from RES1DINV) ----
LAYER_RESISTIVITIES = [8, 5, 20, 80]    # true resistivity (Ωm) for each layer
LAYER_THICKNESSES   = [1.5, 4.0, 10.0] # thickness (m) – omit the half‑space
# =====================================================================


plot_ves_curve(AB2, RHO, STATION, LEACHATE_THRESHOLD,
               layer_rhos=LAYER_RESISTIVITIES, layer_thicks=LAYER_THICKNESSES)
