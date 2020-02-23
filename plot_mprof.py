import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["lines.marker"] = "+"
plt.rcParams["lines.linewidth"] = 1

chains_2 = ["./mprofile_20200223154930.dat", "./mprofile_20200223155050.dat"]
chains_4 = ["./mprofile_20200223160846.dat", "./mprofile_20200223161249.dat"]
chains_6 = ["./mprofile_20200223161912.dat", "./mprofile_20200223162345.dat"]
chains_10 = ["./mprofile_20200223164606.dat", "./mprofile_20200223175438.dat"]
chains_15 = ["./mprofile_20200223175930.dat", "./mprofile_20200223181756.dat"]

def read_mem_file(fname):
    df = pd.read_csv(fname, sep="\s+", usecols=[1, 2], header=None, names=["mem", "time"], skiprows=1, index_col=False)
    df["time"] = df.time - df.time[0]
    return df

max_mem_no_list = []
max_mem_pre_list = []
mem_diff_list = []

for nchains, fnames in zip(
        (2, 4, 6, 10, 15),
        (chains_2, chains_4, chains_6, chains_10, chains_15)
):
    df_no = read_mem_file(fnames[0])
    df_preallocate = read_mem_file(fnames[1])
    mem_max_no = df_no.mem.max().item()
    max_mem_no_list.append(mem_max_no)
    mem_max_pre = df_preallocate.mem.max().item()
    max_mem_pre_list.append(mem_max_pre)
    mem_diff = mem_max_no - mem_max_pre
    mem_diff_list.append(mem_diff)
    x = .2 * df_preallocate.time.max()
    fig, ax = plt.subplots()
    ax.plot(df_no.time, df_no.mem, label="No preallocation", color="C1")
    ax.plot(df_preallocate.time, df_preallocate.mem, label="Preallocation", color="C0")
    ax.axhline(mem_max_no, color="C1", ls="--")
    ax.axhline(mem_max_pre, color="C0", ls="--")
    ax.plot((x, x), (mem_max_pre, mem_max_no), color="k", marker="_")
    ax.text(x, (mem_max_pre + mem_max_no) / 2, " Memory difference = {:.1f} MiB".format(mem_diff), va="center", ha="left")
    ax.set_title(r"$N_{{chains}}={}$".format(nchains))
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Memory used (MiB)")
    ax.legend()
    fig.savefig("mem_usage_{}chains.png".format(nchains))

labels = ['2', '4', '6', '10', '15']
x = np.arange(len(labels))
width = 0.35

fig1, ax1 = plt.subplots(1, 2, figsize=(16, 9))
data_pre = ax1[0].bar(x - width/2, max_mem_pre_list, width, label="Preallocation")
data_no = ax1[0].bar(x + width/2, max_mem_no_list, width, label="No Preallocation")

ax1[0].set_xlabel('Chains')
ax1[0].set_ylabel('Max Memory Usage (MiB)')
ax1[0].set_title("Maximum memory usage vs Chains")
ax1[0].legend()

data_diff = ax1[1].bar(x, mem_diff_list, width, label="Max Memory Difference")
ax1[1].set_xlabel('Chains')
ax1[1].set_ylabel('Max Memory Usage Difference (MiB)')
ax1[1].set_title("Maximum memory usage difference vs Chains")
ax1[1].legend(loc=2)

fig1.savefig("summary.png")
