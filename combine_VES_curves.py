import numpy as np
import matplotlib.pyplot as plt

def plot_combined_ves(stations, threshold=30):
    """
    All stations on one log‑log plot with leachate zone shading.
    stations : list of dicts with 'name' and 'rho_obs'
    """
    default_ab2 = np.array([1.0,1.5,2.0,3.0,4.5,7.0,10.0,15.0,20.0,30.0,45.0,70.0,100.0])

    fig, ax = plt.subplots(figsize=(10, 7))
    for st in stations:
        ab2 = st.get('ab2', default_ab2)
        rho = np.array(st['rho_obs'])
        ax.loglog(ab2, rho, '-o', markersize=4, label=st['name'])

    # Leachate zone
    ax.axhline(threshold, color='purple', linestyle='--', linewidth=1.5, alpha=0.8,
               label=f'Leachate threshold ({threshold} Ωm)')
    ax.fill_between([0.5, 200], 0.1, threshold, color='purple', alpha=0.05)

    ax.set_xlabel('AB/2 (m)')
    ax.set_ylabel('Apparent Resistivity (Ωm)')
    ax.set_title('Combined VES Sounding Curves')
    ax.grid(True, which='both', ls=':')
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# ========================================================
# CHANGE ONLY THESE VALUES
# ========================================================
stations = [
    {'name': 'VES 1',  'rho_obs': [8.95,7.48,7.64,8.20,8.22,9.36,8.76,13.12,12.10,21.10,81.18,86.07,104.35]},
    {'name': 'VES 2',  'rho_obs': [14.95,17.01,17.69,17.42,17.42,14.76,15.72,15.24,25.67,46.06,63.12,76.67,76.56]},
    {'name': 'VES 3',  'rho_obs': [22.94,23.98,20.14,24.26,26.58,24.49,22.84,30.75,35.17,43.49,68.18,65.06,62.05]},
    {'name': 'VES 4',  'rho_obs': [15.23,13.46,16.62,19.86,19.98,18.82,10.48,13.69,13.91,25.27,55.64,118.97,149.20]},
    {'name': 'VES 5',  'rho_obs': [13.75,12.54,12.69,17.87,19.62,15.56,9.36,14.00,13.35,20.19,83.82,70.14,115.73]},
    {'name': 'Control','rho_obs': [861.56,831.17,800.99,772.52,907.28,856.95,766.66,665.02,643.05,512.33,399.68,247.50,273.30]}
]
LEACHATE_THRESHOLD = 30

plot_combined_ves(stations, LEACHATE_THRESHOLD)
