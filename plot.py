import matplotlib.pyplot as plt
import json
from glob import glob
import numpy as np

SIZES = [550, 500, 450, 400, 350, 300, 250, 200, 150, 100]
QUALITIES = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

mat = np.zeros((len(SIZES), len(QUALITIES)))

files = list(glob("data/*.json"))
for file in files:
    with open(file) as f:
        data = json.load(f)

        size_idx = SIZES.index(data["size"])
        quality_idx = QUALITIES.index(data["quality"])

        mat[size_idx, quality_idx] += data["output_size"]

# mean
mat /= len(glob("examples/*"))
mat /= 1000

fig, ax = plt.subplots()
im = ax.imshow(mat, cmap=plt.magma())

plt.xlabel("thumbnail quality")
ax.set_xticks(np.arange(len(QUALITIES)), labels=QUALITIES)

plt.ylabel("thumbnail size")
ax.set_yticks(np.arange(len(SIZES)), labels=[f"{s}px" for s in SIZES])

for i in range(len(SIZES)):
    for j in range(len(QUALITIES)):

        color = "black" if mat[i, j] > 40 else "white"

        text = ax.text(j, i, f"{mat[i, j]:.1f}", ha="center", va="center", color=color)

ax.set_title("Thumbnail size (kB)")
fig.tight_layout()
plt.savefig("thumbnail_size.png", dpi=200)
plt.show()
print("done")
print(mat)