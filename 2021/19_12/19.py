from tqdm import trange
import numpy as np

with open("input.txt") as f:
    a = f.read().splitlines()

scanners = []

for line in a:
    if not line:
        continue
    if line.startswith("--"):
        scanners.append([])
    else:
        scanners[-1].append(line.split(","))
scanners = [np.array(scanner, dtype=int) for scanner in scanners]

all_rotations = []
for i in range(3):
    for b in range(2):
        bclone = np.zeros((3,3), dtype=int)
        bclone[0, i] = (-1)**b
        for j in range(3):
            if i == j:
                continue
            for c in range(2):
                cclone = bclone.copy()
                cclone[1,j] = (-1)**c
                for k in range(3):
                    if k==i or k==j:
                        continue
                    for d in range(2):
                        dclone = cclone.copy()
                        dclone[2, k] = (-1)**d
                        if np.linalg.det(dclone) == -1:
                            continue
                        else:
                            all_rotations.append(dclone)


def get_trans(cloud1, cloud2):
    overlapping = 0
    for r in all_rotations:
        cloud2r = cloud2 @ r
        for point1 in cloud1:
            for point2 in cloud2r:
                cloud2_moved = cloud2r - point2 + point1
                pairwise = np.linalg.norm(cloud1[:, None, :] - cloud2_moved[None, :, :], axis=-1)
                overlapping = max(overlapping, np.sum(pairwise == 0))
                if overlapping >= 12:
                    return r, point1 - point2
    return None

#print(get_overlapping_points(scanners[0], scanners[1]))
to_find = list(range(1, len(scanners)))
to_test = [0]
found_clouds = {0: (np.eye(3), np.zeros(3))}
a = trange(len(to_find))
while to_find:
    ref = to_test.pop(0)
    r, t = found_clouds[ref]
    ref_cloud = scanners[ref] @ r + t
    for c in to_find.copy():
        result = get_trans(ref_cloud, scanners[c])
        if result is not None:
            a.update(1)
            to_find.remove(c)
            to_test.append(c)
            found_clouds[c] = result

total_cloud = np.concatenate([scanners[c] @ r + t for c,(r,t) in found_clouds.items()])
total_cloud = np.unique(total_cloud, axis=0)

print(f"{total_cloud.shape[0]} beacons")

scanner_positions = np.stack([t for c,(r,t) in found_clouds.items()])
pairwise = np.linalg.norm(scanner_positions[:, None, :] - scanner_positions[None, :, :], axis=-1, ord=1)

print(f"Diameter : {np.max(pairwise)}")