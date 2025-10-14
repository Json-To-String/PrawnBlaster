import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

fontsize = 12
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['xtick.major.size'] = 7
mpl.rcParams['ytick.major.size'] = 7
mpl.rcParams['xtick.minor.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 1.5
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["ytick.labelsize"] = fontsize
mpl.rcParams["xtick.labelsize"] = fontsize
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['figure.autolayout'] = True

run_number_list = (np.arange(22,26))
#note: this is for the initial runs we did with the original firmware prior to Jason's PR. I used the same analysis
#for all files, but just note the frequency range is limited to 100-200 MHz here, although we did test to 220 MHz when
#we updated the firmware. I just edited the code in a separate, duplicate file to account for those higher frequencies.
#note2: I added comments above some functions to explain what I am doing; hope that's helpful!

#save the data in arrays
def get_data(run_name):
    datafile = r"C:\Users\josie\Prawnblaster_project\Data\trace_" + run_name + ".csv"
    data = pd.read_csv(datafile)
    xvalues = data['x-axis'].tolist()
    yvalues = data['D0-D7'].tolist()
    x_length, y_length = len(xvalues), len(yvalues)
    x = np.array(xvalues[2:x_length]).astype(float)
    y = np.array(yvalues[2:y_length]).astype(float)
    return x,y

#determine the frequency
def square_wave_frequency(x,y):
    rising_edges = np.where((y[:-1] < 1) & (y[1:] >= 1))[0]
    if len(rising_edges) < 2:
        raise ValueError("Not enough rising edges detected to estimate frequency")
    else:
        times = x[rising_edges]
        periods = np.diff(times)
        avg_period = np.mean(periods)
        freq_std = np.std(1/periods) / np.sqrt(len(periods))
        freq = 1.0 / avg_period
    return freq, freq_std, periods

#create residuals based on expected frequency values and errors
residual_list = []
error_list = []
for run_number in run_number_list:
    run_name = str(run_number)
    x, y = get_data(run_name)
    if 3 <= run_number <=7:
        expected = 1.667e6
    elif 8 <= run_number <= 12:
        expected = 2.5e6
    else:
        expected = 3.33e6
    freq_meas, freq_meas_unc, p = square_wave_frequency(x,y)
    # plt.hist(p,bins=50)
    # plt.show()
    residuals = freq_meas - expected
    residual_list.append(residuals)
    error_list.append(freq_meas_unc)
    # x_values = np.linspace(1, 100, 100)
print(error_list)

Freq_array = np.array([100,100,100,100,100,150,150,150,150,150,200,200,200,200,200])

residual_list = np.array(residual_list)
error_list = np.array(error_list)

#Markers for each frequency
numbers = np.array([100, 150, 200])
unique = np.unique(numbers)
markers = ['.', 'x', '*']

run_number_list = run_number_list-3
for i, num in enumerate(unique):
    indices = np.where(Freq_array == num)
    plt.scatter(run_number_list[indices], residual_list[indices], marker=markers[i], label=f'Frequency {num}', s=100,alpha=0.6)

# plt.scatter(run_number_list,residual_list, s=12)
plt.errorbar(run_number_list, residual_list,yerr= error_list,linestyle='none',capsize=5,color="black")
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Run Number", fontsize=fontsize)
plt.ylabel("Residuals (Hz)", fontsize=fontsize)
# plt.ylim(-400,3500)
plt.legend()
plt.savefig("Residuals.png", dpi=150)
plt.show()

print(residual_list)