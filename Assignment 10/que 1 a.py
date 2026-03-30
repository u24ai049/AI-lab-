import random
import csv

# 🔹 Function to read CSV file
def read_csv(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    data.append([float(x) for x in row])
    except Exception as e:
        print("Error opening file:", e)
    return data


# 🔹 Euclidean distance (squared)
def distance_sq(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(len(a)))


def main():
    # 🔹 Read data
    X = read_csv("cities.csv")

    n = len(X)
    dim = len(X[0])
    k = 3

    # 🔹 Initialize random centers
    random.seed(42)
    chosen = set()
    centers = []

    while len(centers) < k:
        idx = random.randint(0, n - 1)
        if idx not in chosen:
            centers.append(X[idx][:])  # copy
            chosen.add(idx)

    lr = 0.01
    iterations = 100
    labels = [0] * n

    # 🔹 Gradient Descent K-Means
    for _ in range(iterations):

        # Step 1: Assign clusters
        for i in range(n):
            min_dist = float('inf')
            best_cluster = 0

            for j in range(k):
                d = distance_sq(X[i], centers[j])
                if d < min_dist:
                    min_dist = d
                    best_cluster = j

            labels[i] = best_cluster

        # Step 2: Update centers using gradient
        for j in range(k):
            gradient = [0.0] * dim
            count = 0

            for i in range(n):
                if labels[i] == j:
                    count += 1
                    for d in range(dim):
                        gradient[d] += (centers[j][d] - X[i][d])

            if count > 0:
                for d in range(dim):
                    gradient[d] *= 2
                    centers[j][d] -= lr * gradient[d]

    # 🔹 Compute SSD
    ssd = 0
    for i in range(n):
        min_dist = float('inf')
        for j in range(k):
            d = distance_sq(X[i], centers[j])
            min_dist = min(min_dist, d)
        ssd += min_dist

    # 🔹 Output
    print("Final Centers:")
    for c in centers:
        print(*c)

    print("SSD:", ssd)


if __name__ == "__main__":
    main()