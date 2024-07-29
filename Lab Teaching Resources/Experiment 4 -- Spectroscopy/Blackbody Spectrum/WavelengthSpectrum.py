import numpy as np
import matplotlib.pyplot as plt
import matplotlib

plt.style.use('krytic')


def Bv(wl, T):
    h = 6.626e-34
    c = 3.0e+8
    k = 1.38e-23
    a = 2.0*h*c**2
    b = h*c/(wl*k*T)
    intensity = a / ((wl**5) * (np.exp(b) - 1.0))
    return intensity / 2e11


fig, ax = plt.subplots(1, 1, figsize=(11.7, 8.27))

temps = [5778.0, 7000, 9000]
cols = ['#D81159', '#01172F', '#FAA916']
cols = ['white', 'white', 'white']

wls = np.arange(1e-9, 1.5e-6, 1e-9)  # nm

xs = []
ys = []

max_y = 0

for temp in temps:
    x = wls * 1e9
    y = Bv(wls, temp)

    xs.append(x)
    ys.append(y)

    max_y = max(max(y), max_y)


def wavelength_to_rgb(wavelength, gamma=0.8):
    ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A = 0.3
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)


clim=(0, 1500)
norm = plt.Normalize(*clim)
wl = np.arange(clim[0],clim[1]+1,2)
colorlist = list(zip(norm(wl),[wavelength_to_rgb(w) for w in wl]))
spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

wavelengths = np.linspace(0, 1500, 1500)

y = np.linspace(0, max_y, 100)
X,Y = np.meshgrid(wavelengths, y)

extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))


ax.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')

index_of_label = np.argwhere(xs[0] >= 225)[0][0]

# name = 'Wien\'s Law'
for i in range(len(temps)):
    label = f'{temps[i]:.0f} K'

    # if int(temps[i]) == 5778:
    #     label += " (the Sun)"

    rise = np.abs(ys[i][index_of_label] - ys[i][index_of_label-10])
    run = np.abs(xs[i][index_of_label] - xs[i][index_of_label-10])

    gradient = rise/run
    theta = np.rad2deg(np.arctan(gradient))

    if theta > 70:
        dy = 0.15*ys[i][index_of_label]
        dx = -10
    elif theta > 45:
        dy = 0.15*ys[i][index_of_label]
        dx = -20
    else:
        dy = 0.6*ys[i][index_of_label]
        dx = -20

    ax.text(xs[i][index_of_label]+dx, ys[i][index_of_label]+dy, label, rotation=theta, size=13, color='white')

    line = ax.plot(xs[i], ys[i], label=label, c=cols[i])
    wl_peak = 2898e-3 / temps[i] * 1e6   # nm

    ax.axvline(wl_peak, color=line[0].get_color())
    ax.annotate(rf"$\lambda_\text{{peak}}={wl_peak:.0f}$ nm",
                xy=(wl_peak, (0.5+0.1*i)*max_y),
                xytext=(20, (0.5+0.1*i)*max_y),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
                )

    # name = ''

# ax.legend(frameon=False, loc='upper left')

ax.set_xlabel("Wavelength / nanometers")
ax.grid(False)

for sp in ax.spines.keys():
    if sp not in ['bottom', 'left']:
        ax.spines[sp].set_visible(False)

ax.tick_params(axis='both', which='both', right=False, top=False)
# ax.set_ylim(0.7*max_y)
ax.set_yticklabels([])
ax.set_ylabel("Intensity / arbitrary units")
ax.set_xlim(0, 1500)

fig.suptitle("Blackbody spectrum as predicted by Wien's Law", y=0.95, size=20)

fig.savefig('Wiens_Law_Demonstration.pdf')