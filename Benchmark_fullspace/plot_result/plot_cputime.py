import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

nprocs=[1, 2, 4, 8, 16, 32, 64, 128] # vector of trial number of processors
cputime=[3800, 1920, 1, 1, 1, 1, 1, 1] # cpu time [s] 

fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)

ax.plot(nprocs, cputime, 'kx-', lw=1.5)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('Number of processors')
ax.set_ylabel('CPU time [s]')
ax.set_title('Scalability of SPECFEM2D parallelization')
ax.set_ylim(1e0, 5e3)

ax.set_xticks(nprocs, minor=False)
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
ax.tick_params(axis='x', which='minor', bottom=False)
plt.grid(which='major',color='gray',linestyle='--')
plt.grid(which='minor', axis="y", color='gray',linestyle='--')

plt.savefig("benchmark_cputime.png", dpi=300)
plt.show()
