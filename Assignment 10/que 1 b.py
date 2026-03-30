import random

# 🔹 Squared distance
def dist_sq(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(len(a)))


def main():
    # 🔹 Sample data
    X = [
        [1, 2], [2, 1], [3, 2],
        [8, 9], [9, 8], [10, 9],
        [50, 50], [52, 51], [49, 48]
    ]

    n = len(X)
    dim = len(X[0])
    k = 3

    # 🔹 Initialize centers
    random.seed(42)
    chosen = set()
    centers = []

    while len(centers) < k:
        idx = random.randint(0, n - 1)
        if idx not in chosen:
            centers.append(X[idx][:])  # copy
            chosen.add(idx)

    labels = [0] * n

    for _ in range(50):

        # 🔸 Step 1: Assign clusters
        for i in range(n):
            best = float('inf')
            cluster = 0
            for j in range(k):
                d = dist_sq(X[i], centers[j])
                if d < best:
                    best = d
                    cluster = j
            labels[i] = cluster

        # 🔸 Step 2: Newton update
        for j in range(k):

            gradient = [0.0] * dim
            count = 0

            # 🔹 Compute gradient
            for i in range(n):
                if labels[i] == j:
                    count += 1
                    for d in range(dim):
                        gradient[d] += -2 * (X[i][d] - centers[j][d])

            if count == 0:
                continue

            # 🔹 Hessian scalar
            hessian_scalar = 2.0 * count

            # 🔹 Newton update
            for d in range(dim):
                centers[j][d] = centers[j][d] - (1.0 / hessian_scalar) * gradient[d]

    # 🔹 Output
    print("Centers:")
    for c in centers:
        print(*c)


if __name__ == "__main__":
    main()