import sys
import os
import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter, filtfilt
import matplotlib.pyplot as plt


def validate_waveform(NPROCS):
	print(np)
	# target output dir
	target_output_dir="OUTPUT_FILES_NP%s"%NPROCS


	def butter_lowpass(cutoff, fs, order=5):
	    nyq = 0.5 * fs
	    normal_cutoff = cutoff / nyq
	    b, a = butter(order, normal_cutoff, btype='low', analog=False)
	    return b, a

	def butter_lowpass_filter(data, cutoff, fs, order=5):
	    b, a = butter_lowpass(cutoff, fs, order=order)
	    #y = lfilter(b, a, data)
	    y = filtfilt(b, a, data)
	    return y


	#---Input parameters---#
	# read waveform
	itheta = 0
	amp = 5e5 # plot amplitude exaggeration
	lw=1.5 # plot line width
	cutoff = 50.0
	t0 = 6.0

	# Applying lowpass filter to eliminate high-frequency numerical oscilation
	order = 6
	dt = 7.0e-3
	fs = 1/dt# sample rate, Hz
	cutoff = 10.0  # desired cutoff frequency of the filter, Hz
	#-----------------------#

	# location of stations where seismograms are validated
	R_validate = 20e3 # radius of validating locations
	theta_span = 30 #deg
	theta = np.arange(-90,270,theta_span) * np.pi / 180.
	val_cx = R_validate*np.cos(theta)
	val_cz = R_validate*np.sin(theta)

	number_of_station=len(theta)

	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8), dpi=80, sharey=True)


	for i in range(number_of_station):

		plottheta = (theta[itheta] * 180 / np.pi)
		itheta = itheta + 1

		with open("./Benchmark_result/AA.S%04d.BXX.sema"%i, 'r') as fi:
			temp_df = pd.read_csv(fi,  header=None, engine='python', delim_whitespace=True, comment='#')

		temp	= temp_df.values
		tx 		= temp[:,0]
		ax_P 		= temp[:,1]

		with open("./Benchmark_result/AA.S%04d.BXZ.sema"%i, 'r') as fi:
			temp_df = pd.read_csv(fi,  header=None, engine='python', delim_whitespace=True, comment='#')

		temp	= temp_df.values
		tz 		= temp[:,0]
		az_P 		= temp[:,1]

		with open("../%s/AA.S%04d.BXX.sema"%(target_output_dir, i), 'r') as fi:
			temp_df = pd.read_csv(fi,  header=None, engine='python', delim_whitespace=True, comment='#')

		temp	= temp_df.values
		ax_C 		= temp[:,1]

		with open("../%s/AA.S%04d.BXZ.sema"%(target_output_dir, i), 'r') as fi:
			temp_df = pd.read_csv(fi,  header=None, engine='python', delim_whitespace=True, comment='#')

		temp	= temp_df.values
		az_C 		= temp[:,1]


		# apply lowpass filter to remove numerical oscilation
		ax_P = butter_lowpass_filter(ax_P, cutoff, fs, order)
		ax_C = butter_lowpass_filter(ax_C, cutoff, fs, order)
		az_P = butter_lowpass_filter(az_P, cutoff, fs, order)
		az_C = butter_lowpass_filter(az_C, cutoff, fs, order)


		ax1.plot(tx+t0, plottheta+amp*ax_P, 'k-', lw=lw)
		ax1.plot(tx+t0, plottheta+amp*ax_C, 'r:', lw=lw)

		ax2.plot(tx+t0, plottheta+amp*az_P, 'k-', lw=lw)
		ax2.plot(tx+t0, plottheta+amp*az_C, 'r:', lw=lw)


	#ax1.set_xlim(0.0, right)
	ax1.set_xlabel('Time (s)')
	ax1.set_ylabel('Azimuth ($^{\circ}$)')
	ax2.set_xlabel('Time (s)')
	ax2.set_ylabel('Azimuth ($^{\circ}$)')
	ax2.legend(['Benchmark true model', 'Validation case with NP %s'%NPROCS], loc=1)

	ax1.set_title('x-acceleration (m/s/s)')
	ax2.set_title('z-acceleration (m/s/s)')

	fig.suptitle('Validation of Benchmark: Low-Pass with %4.2f (Hz)'%(cutoff), fontsize=12)

	plt.savefig("validation_NP%s.png"%NPROCS, dpi=300)
	plt.show()


if __name__ == "__main__":

	args=sys.argv
	if len(args)!=2:
		print('\033[36m'+"Please input number of processors when running this script. \ne.g. python validate_waveform.py 4"+'\033[0m')
		exit()

	NPROCS=args[1]
	validate_waveform(NPROCS)
