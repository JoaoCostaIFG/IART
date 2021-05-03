import matplotlib.pyplot as plt

#  plt.yscale("log")
plt.ylabel("Time (s)")
plt.xlabel("Input file (row x col - possible router positions)")
data = [(227.18 + 186.32 + 223.10) / 3.0, 504.53, 14489.51]

plt.bar(["Charleston Road (240x180-21942)", "Rue de Londres(559x404-64426)", "Opera(667x540-196899)"], data)
plt.show()
