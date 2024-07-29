import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def mass_number(Z):
    df = pd.read_csv('massnumbers', sep=r"\s+", names=['Z',
                                                       'Symbol',
                                                       'Name',
                                                       'mass'])

    mass = df[df['Z'] == Z]['mass'].to_numpy()[0].astype(float)

    return mass


def get_WLs_for_Z(Z):
    R_infty = 10973731
    me = 0.000548579909  # amu
    M = mass_number(Z)   # amu (ish)

    R = R_infty / (1 + me / M)
    print(1+me/M)

    def WL_for_n1_n2(n1, n2):
        return 1 / (R*Z**2*(1/n1**2-1/n2**2)) / 1e-9

    WLs = []

    for n1 in range(1, 8):
        for n2 in range(1, 8):
            if n1 >= n2: continue
            # if n2 ==

            wl = WL_for_n1_n2(n1, n2)
            print(Z, wl)
            if wl <= 380 or wl >= 780: continue

            WLs.append(wl)

    return WLs


spectra = {
    'Hydrogen': [402.6, 404.6, 404.8, 434, 486, 656],
    'Helium': [402.6, 403.6, 404.8, 415.6, 420.6, 447.1, 471.3, 492.1, 501.5, 587.5, 667.8],
    'Lithium': [460.3, 498.0, 516.7, 546.6, 610.4, 610.4, 670.8, 671.7],
    'Mercury': [404.7, 407.8, 435.8, 546.1, 577.0, 579.0, 643.4]
}

for file in os.listdir('elements'):
    if file not in ['..', '.']:
        dat = np.genfromtxt(f'elements/{file}')
        name = f"{file[0].upper()}{file[1:].lower()}"

        fac = 1

        if file.endswith('.a'):
            fac = 10
            name = name.rsplit('.', 1)[0]

        if name in spectra.keys(): continue

        spectra[name] = dat / fac


def nmToRGB(wavelength):
    Gamma = 0.80
    IntensityMax = 255
    if ((wavelength >= 380) and (wavelength < 440)):
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif ((wavelength >= 440) and (wavelength < 490)):
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif ((wavelength >= 490) and (wavelength < 510)):
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif ((wavelength >= 510) and (wavelength < 580)):
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif ((wavelength >= 580) and (wavelength < 645)):
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    elif ((wavelength >= 645) and (wavelength < 781)):
        red = 1.0
        green = 0.0
        blue = 0.0
    else:
        red = 0.0
        green = 0.0
        blue = 0.0
    # Let the intensity fall off near the vision limits
    if ((wavelength >= 380) and (wavelength < 420)):
        factor = 0.3 + 0.7*(wavelength - 380) / (420 - 380)
    elif ((wavelength >= 420) and (wavelength < 701)):
        factor = 1.0
    elif ((wavelength >= 701) and (wavelength < 781)):
        factor = 0.3 + 0.7*(780 - wavelength) / (780 - 700)
    else:
        factor = 0.0
    if (red != 0):
        red = np.round(IntensityMax * np.power(red * factor, Gamma), 0)
    if (green != 0):
        green = np.round(IntensityMax * np.power(green * factor, Gamma), 0)
    if (blue != 0):
        blue = np.round(IntensityMax * np.power(blue * factor, Gamma), 0)
    return [red/IntensityMax, green/IntensityMax, blue/IntensityMax]


plt.style.use('krytic')

A4 = (11.69, 8.27)

fig, axes = plt.subplots(len(spectra.keys()), 1, sharex=True, figsize=A4)

i = 0

for species, wavelengths in spectra.items():
    for wl in wavelengths:
        if wl < 380 or wl > 780: continue
        rgb = nmToRGB(wl)
        axes[i].axvline(wl, c=rgb, lw=2)
    axes[i].set_ylabel(species)
    axes[i].set_yticks([])

    i += 1

axes[-1].set_xlabel("Wavelength in nanometers")

size = axes[0].yaxis.label.get_fontsize() * 2

bands = {
    'm:ultraviolet': (-np.infty, 400),
    'm:infrared': (750, np.infty)
    }

cutoffs = (350, 800)

dirs = {
    'uv': (r'$\leftarrow$', ''),
    'ir': ('', r'$\rightarrow$')
}

for ax in axes:
    for band_name, span in bands.items():
        if ':' in band_name:
            # IR or UV...
            color = band_name[7:]
            name = band_name[2]+color[0]
            alpha = 0.2
            name = dirs[name][0] + name.upper() + dirs[name][1]
        else:
            color = band_name
            name = band_name
            alpha = 0.3
        print(name)
        span = (max(cutoffs[0], span[0]), min(cutoffs[1], span[1]))

        ax.axvspan(span[0], span[1], color=color, alpha=alpha)
        ax.text(np.mean(span), 0.5, name, ha='center', va='center')
    ax.set_xlim(cutoffs)

fig.suptitle("The Emission Spectra of Selected Elements", y=0.94, size=size)

plt.savefig('wavelength_data_plot.pdf')