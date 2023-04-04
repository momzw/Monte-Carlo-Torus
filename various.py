import numpy as np
import rebound
import os
import shutil
from tqdm import tqdm
import pandas as pd
import copy
from serpens_analyzer import SerpensAnalyzer, PhaseCurve
import matplotlib.pyplot as plt
import matplotlib
import scipy.optimize as sp

matplotlib.use('TkAgg')
matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
matplotlib.rc('text', usetex=True)
matplotlib.rc('text.latex', preamble=r'\usepackage{amssymb}')
#plt.style.use('seaborn-v0_8')


def orbit_sol():

    G = 6.6743e-11

    # Set a range of semi-major axes to check (and pericenters for when e!=0):
    a = 1.01 * 69911e3 * np.linspace(1.2, 1.8, 200000)
    w = np.linspace(0, 2*np.pi, 10000)

    # Orbital periods
    T = 2 * np.pi * np.sqrt(a**3/(G*0.365*1.898e27))

    # Fixed phases after t0
    phases = np.array([0.65, 0.4])

    # Set dates to check:
    dates = np.array([["2015-12-07 04:31", 2457363.69313672],
                      ["2016-01-01 05:22", 2457388.72868279],
                      ["2019-11-11 13:32", 2458799.06791922],
                      ["2022-09-25 09:00", 2459847.79251231],
                      ["2022-10-20 07:30", 2459872.81516997],
                      ["2022-11-03 05:00", 2459886.71188757],
                      ["2022-11-14 08:00", 2459897.83748205],
                      ["2022-11-17 03:00", 2459900.62927906],
                      ["2022-11-28 06:00", 2459911.75471299],
                      ["2022-12-12 04:00", 2459925.67171136],
                      ["2022-12-23 07:04", 2459936.79957287],
                      ["2022-12-26 02:00", 2459939.58845666],
                      ["2016-01-15 03:10", 2457402.63672867],
                      ["2023-01-03 10:08", 2459947.92726799],
                      ["2023-01-06 04:53", 2459950.70847165],
                      ["2023-01-08 23:39", 2459953.49035973],
                      ["2023-01-11 18:25", 2459956.27223777],
                      ["2023-01-14 13:11", 2459959.05410612],
                      ["2023-01-17 07:56", 2459961.83527034],
                      ["2023-01-20 02:42", 2459964.61711949],
                      ["2023-01-22 21:28", 2459967.39895940],
                      ["2023-01-25 16:13", 2459970.18009599],
                      ["2023-01-28 10:59", 2459972.96191840],
                      ["2023-01-31 05:44", 2459975.74303804],
                      ["2023-02-03 00:30", 2459978.52484407],
                      ["2023-02-05 19:16", 2459981.30664256],
                      ["2023-02-08 14:02", 2459984.08843367],
                      ["2023-02-11 08:48", 2459986.87021793],
                      ["2023-02-14 03:33", 2459989.65130116],
                      ["2023-02-16 22:19", 2459992.43307256],
                      ["2023-02-19 17:05", 2459995.21483827],
                      ["2023-02-22 11:50", 2459997.99590420],
                      ["2023-02-25 06:36", 2460000.77765964],
                      ["2023-02-28 01:22", 2460003.55941073],
                      ["2023-10-11 09:04", 2460228.87978633],
                      ["2023-10-25 06:52", 2460242.78908222],
                      ["2023-11-08 04:41", 2460256.69894613],
                      ["2023-11-19 07:43", 2460267.82587894],
                      ["2023-11-22 02:29", 2460270.60793891],
                      ["2023-12-03 05:32", 2460281.73539485],
                      ["2023-12-14 08:35", 2460292.86269663],
                      ["2023-12-17 03:20", 2460295.64397583],
                      ["2023-12-28 06:23", 2460306.77107229],
                      ["2023-12-31 01:09", 2460309.5529942],
                      ["2024-01-11 04:12", 2460320.67988477],
                      ["2024-01-22 07:15", 2460331.80661763],
                      ["2024-01-25 02:00", 2460334.58775701],
                      ["2024-02-05 05:03", 2460345.71431384],
                      ["2024-02-19 02:52", 2460359.62251892],
                      ["2024-03-04 00:40", 2460373.52989522],
                      ["2024-03-15 03:43", 2460384.65615342],
                      ["2024-03-29 01:31", 2460398.56343303],
                      ])

    # BJD and time after first BJD (t0)
    t = dates[:,1].astype(float)
    dt = np.asarray([(dates[:,1].astype(float)[i] - dates[:,1].astype(float)[0]) * 86400 for i in range(np.size(t))])
    sol_a = []
    sol_T = []
    sol_w = []
    coll_phases = []

    e = 0
    for i in tqdm(range(np.size(a)), "Checking a and w"):
        # Calculate phase angles for the fixed phases with phi(t0)=0.67
        m1 = ((2*np.pi/T[i] * dt[1] + 0.67 * 2 * np.pi) % (2*np.pi)) / (2*np.pi)    # Angle modulo 2pi mapped to [0,1]
        m2 = ((2*np.pi/T[i] * dt[2] + 0.67 * 2 * np.pi) % (2*np.pi)) / (2*np.pi)

        if not e == 0:
            nu1 = rebound.M_to_f(e, m1) / (2*np.pi)
            nu2 = rebound.M_to_f(e, m2) / (2*np.pi)

            for j in range(np.size(w)):
                nu1 = nu1 + w[j]
                nu2 = nu2 + w[j]

                if np.abs((nu1 - phases[0])) < 0.005:
                    if np.abs((nu2 - phases[1])) < 0.005:
                        sol_a.append(a[i] / (1.01 * 69911e3))
                        sol_T.append(T[i])
                        sol_w.append(w[j])
                        all_phases = [0.67]
                        all_phases.append(nu1)
                        all_phases.append(nu2)
                        for ti in dt[3:]:
                            all_phases.append(((2 * np.pi / T[i] * ti + 0.67 * 2 * np.pi) % (2 * np.pi)) / (2 * np.pi))
                        coll_phases.append(all_phases)
        else:
            if np.abs((m1 - phases[0])) < 0.005:
                if np.abs((m2 - phases[1])) < 0.005:
                    sol_a.append(a[i] / (1.01 * 69911e3))
                    sol_T.append(T[i])
                    sol_w.append(0.)

                    # Calculate/append all phases for the semi-major axis solution found.
                    all_phases = [0.67]
                    all_phases.append(m1)
                    all_phases.append(m2)
                    for ti in dt[3:]:
                        all_phases.append(((2 * np.pi / T[i] * ti + 0.67 * 2 * np.pi) % (2 * np.pi)) / (2 * np.pi))
                    coll_phases.append(all_phases)  # Collect phases for file output

    # Saving data...
    pericenters = np.asarray([f"w = {np.round(sol_w[j],3)}" for j in range(np.size(sol_w))])
    header = ["date", "BJD", "delta_t [s]"]
    for j in range(np.size(sol_a)):
        header.append(f"phase for a = {np.round(sol_a[j],3)}")

    phase_outputs = np.vstack((header[3:], pericenters, np.round(np.asarray(coll_phases).T,5)))
    all_output = np.hstack((np.vstack((header[:3], np.array(["-", "-", "-"]), np.vstack((dates[:,0], t, dt)).T)), phase_outputs))
    np.savetxt("temporary.txt", all_output, fmt="%-20s", delimiter=" ", newline='\n')

    df = pd.DataFrame(all_output)
    df.to_excel('temporary.xlsx', index=False, header=False)


def pngToGif(path, fps, name=None):
    """
    TOOL TO COMBINE PNG TO GIF
    """
    import imageio
    #imageio.plugins.ffmpeg.download()

    files = []
    for file in os.listdir(path):
        if file.startswith('SERPENS_'):
            cutoff = file[::-1].find('_')
            files.append(file[:-cutoff])

    if name is None:
        name = path[path.find('--')+2:path.find('/p')]
    writer = imageio.get_writer(f'sim_{name}.mp4', fps=fps, macro_block_size=None)

    for im in sorted(files, key=len):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and f'{im}' in file:
                im2 = os.path.join(path, file)
                writer.append_data(imageio.v2.imread(im2))
    writer.close()
# pngToGif('output/22022023--14-25_moonsource/plots', 5, name="test")


def calculate_vb(temperatures, v_M):

    def func(x, v_M, T):
        v_m = np.sqrt(3 * 1.380649e-23 * T / (23 * 1.660539066e-27))
        v_m *= 1e-3
        xi = 1/(v_M/np.sqrt(v_m**2 + x**2) - 1)
        xi_term = np.sqrt(14/9 + 1/3 * xi - 1)
        return v_m - x/xi_term

    if isinstance(temperatures, (list, np.ndarray)) and isinstance(v_M, (list, np.ndarray)):
        assert len(temperatures) == len(v_M)
        roots = []
        for i in range(len(temperatures)):
            root = sp.fsolve(func, 2, args=(v_M[i], temperatures[i]))
            roots.append(root)
        return roots
    elif isinstance(temperatures, (int, float)) and isinstance(v_M, (int, float)):
        root = sp.fsolve(func, 2, args=(v_M, temperatures))
        return root
    else:
        print("Invalid types for temperatures and/or maximal velocities")
        return
#calculate_vb(temperatures=[7754, 1400, 1120, 1740, 963, 1200, 1450, 1322], v_M=[46.62, 15.24, 11.86, 16.02, 12.43, 23.8, 17.82, 13.35])


def calculate_dsync():
    import objects
    w_init = 1.77e-4
    alpha = 0.26
    Q_diss = 1e6
    gc = 6.6743e-11
    tau_sync = 100e6 * 3.154e7
    d_sync_au = []
    for i in range(2, 11):
        celest = objects.celestial_objects(moon=True, set=i)
        star_mass = celest["star"]["m"]
        planet_mass = celest["planet"]["m"]
        planet_radius = celest["planet"]["r"]
        d = (9/4 * 1/(alpha*Q_diss) * gc*planet_mass/planet_radius**3 * 1/w_init * star_mass**2/planet_mass**2 * planet_radius**6 * tau_sync)**(1/6)
        d_sync_au.append(d * 6.68459e-12)
    return d_sync_au


def calculate_massloss_sat(los_obs, tau, cel_set):
    import objects
    amu = 1.660539066e-27
    celest = objects.celestial_objects(moon=True, set=cel_set)
    star_radius = celest["star"]["r"]
    mass_loss = los_obs*10000 * np.pi * star_radius**2 * 23 * amu / tau
    return np.log10(mass_loss)


def calculate_alfven(eta=.3):
    import objects
    gc = 6.6743e-11
    ages = np.array([5, 4.3, 3.5, 3.6, 5, 3, 2, 9.4, 6.3])
    spt = np.array(['G', 'K', 'G', 'G', 'G', 'F', 'K', 'G', 'K'])
    lxuv = np.zeros(9)
    for i, type in enumerate(spt):
        if type == 'G':
            lxuv[i] = 0.19 * 10**29.35 * ages[i]**(-1.69)
        elif type == 'K':
            lxuv[i] = 0.234 * 10**28.87 * ages[i]**(-1.72)
        elif type == 'F':
            lxuv[i] = 0.155 * 10**29.83 * ages[i]**(-1.72)

    dmdt_therm = []
    r_alf = []
    for j in range(2, 11):
        celest = objects.celestial_objects(moon=True, set=j)
        star_mass = celest["star"]["m"]
        planet_mass = celest["planet"]["m"]
        planet_radius = celest["planet"]["r"]
        semimajor = celest["planet"]["a"]
        xi = semimajor * (1/(3*planet_radius**3) * planet_mass/star_mass)**(1/3)
        k = 1 - 3/2 * xi - 1/(2 * xi**3)
        mass_loss = eta/(4 * gc * k) * planet_radius**3/(semimajor**2 * planet_mass) * lxuv[j-2]*1e-7 * 1e3
        dmdt_therm.append(mass_loss)
        r_alf.append((1e6/-mass_loss)**(1/5) * 19.8 * 69911e3 / planet_radius)

    return np.asarray(dmdt_therm), np.asarray(r_alf)


def velocity_distributions():
    from scipy.stats import maxwell

    temp_eq = 1400  # W49
    temp_tidal = 1902   # W49
    m = 23 * 1.660539066e-27    # Na
    k_B = 1.38066e-23

    # MAXWELL:
    maxwell_scale_eq = np.sqrt((k_B * temp_eq) / m)
    maxwell_scale_tidal = np.sqrt((k_B * temp_tidal) / m)
    x = np.linspace(0, 8000, 300)

    # SPUTTERING:

    def phi(x, scale):
        v_M = 15.24*1000
        v_b = calculate_vb(temp_eq, v_M/1000) * 1000
        a = scale

        def phi_unnorm(x):
            f_v = 1 / v_b * (x / v_b) ** 3 \
                  * (v_b ** 2 / (v_b ** 2 + x ** 2)) ** a \
                  * (1 - np.sqrt((x ** 2 + v_b ** 2) / (v_M ** 2)))
            return f_v

        def phi_int(x):
            integral_bracket = (1 + x ** 2) ** (5 / 2) * v_b / v_M / (2 * a - 5) - (1 + x ** 2) ** (
                    3 / 2) * v_b / v_M / (2 * a - 3) - x ** 4 / (2 * (a - 2)) - a * x ** 2 / (
                                       2 * (a - 2) * (a - 1)) - 1 / (2 * (a - 2) * (a - 1))

            f_v_integrated = integral_bracket * (1 + x ** 2) ** (-a)
            return f_v_integrated

        upper_bound = np.sqrt((v_M / v_b) ** 2 - 1)
        normalization = 1 / (phi_int(upper_bound) - phi_int(0))
        f_pdf = normalization * phi_unnorm(x)
        return f_pdf

    fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=150)
    #fig.suptitle("Velocity Distributions", fontsize='x-large')
    ax.plot(x, maxwell.pdf(x, scale=maxwell_scale_eq), label=r'Maxwell $T_{\mathrm{eq}}$', color='blue')
    ax.plot(x, maxwell.pdf(x, scale=maxwell_scale_tidal), label=r'Maxwell $T_{\mathrm{tidal}}$', color='cornflowerblue')
    ax.plot(x, phi(x, scale=3), label=r'Sputtering $T_{\mathrm{eq}}$, $\alpha=3$', color='orange')
    ax.plot(x, phi(x, scale=7/3), label=r'Sputtering $T_{\mathrm{eq}}$, $\alpha=7/3$', color='red')

    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel(r"Probability density [10$^{-4}$]", fontsize=22)
    ax.set_xlabel("Velocity in m/s", fontsize=22)
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.legend(prop={'size': 22}, framealpha=1)
    plt.grid()
    plt.tight_layout()
    plt.savefig("veldist.png")
    plt.show()

    #import plotly.express as px
    #df = pd.DataFrame({
    #    'x': x,
    #    'Maxwell T_eq': maxwell.pdf(x, scale=maxwell_scale_eq),
    #    'Maxwell T_tidal': maxwell.pdf(x, scale=maxwell_scale_tidal),
    #    'Sputtering alpha 3': phi(x, scale=3),
    #    'Sputtering alpha 7/3': phi(x, scale=7/3)
    #})
    #
    #fig = px.line(df, x='x', y=df.columns[1:])
    #fig.write_image("fig1.png")
    #fig.show()


#sa = SerpensAnalyzer(save_output=False, r_cutoff=4)

#sa.top_down(timestep=31, d=2, colormesh=False, scatter=False, triplot=True, show=True, smoothing=.5, trialpha=1, lim=4,
#            celest_colors=['orange', 'bisque', 'white', 'yellow', 'green', 'green'],
#            colormap=plt.cm.get_cmap("afmhot"), show_moon=False)

#sa.los(timestep=201, show=True, show_planet=True, show_moon=False, lim=4,
#       celest_colors=['yellow', 'sandybrown', 'yellow', 'yellow', 'green', 'green'], scatter=True, colormesh=False,
#       colormap=plt.cm.afmhot)

#sa.plot3d(121, log_cutoff=-5)
#sa.transit_curve('simulation-HD189-ExoIo-Na-physical-HV')

pc = PhaseCurve()
pc.plot_curve_external('XO-2N', part_dens=True, column_dens=True)
#sa.phase_curve(load_path=[#'simulation-W17-ExoEarth-Na-physical-HV',
#                          #'simulation-W17-ExoIo-Na-physical-HV',
#                          #'simulation-W17-ExoEnce-Na-physical-HV',
#                          'simulation-W69-ExoEarth-Na-3h-HV',
#                          'simulation-W69-ExoIo-Na-3h-HV',
#                          'simulation-W69-ExoEnce-Na-3h-HV',
#                          ],
#               fig=True, part_dens=True, column_dens=False, title=r'WASP-69 b - 3h', savefig=False)


