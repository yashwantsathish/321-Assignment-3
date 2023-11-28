from Crypto.Hash import SHA256
import time
import matplotlib.pyplot as plt
import random

count = 0

def hash_input(input_data):
    encoded = input_data.encode()
    data = SHA256.new(encoded)
    return data.hexdigest()

def truncate_digest(digest, truncate_bits):
    # Calculate the number of bytes needed to represent the specified number of bits
    truncate_bytes = (truncate_bits + 7) // 8

    # Create a bitmask with the desired number of bits set to 1
    bitmask = (1 << truncate_bits) - 1

    # Convert the original digest to an integer, apply the bitmask, and convert back to hex
    truncated_digest = hex(int(digest, 16) & bitmask)[2:]

    # Ensure the resulting hex string has the correct length
    truncated_digest = truncated_digest.rjust(truncate_bytes * 2, '0')

    return truncated_digest



def find_collision(truncate_bits):
    global count
    hash_set = set()

    start_time = time.time()
    iterations = 0

    while True:
        input_data = str(random.getrandbits(1024))
        # input_data = str(count)
        hashed_value = truncate_digest(hash_input(input_data), truncate_bits)

        if hashed_value in hash_set:
            # Collision found
            break

        hash_set.add(hashed_value)
        iterations += 1

    end_time = time.time()
    collision_time = end_time - start_time

    return iterations, collision_time

def plot_graphs(digest_sizes, collision_times, num_inputs):
    plt.figure(figsize=(12, 6))

    # Plot 1: Digest Size vs Collision Time
    plt.subplot(1, 2, 1)
    plt.plot(digest_sizes, collision_times, marker='o')
    plt.title('Digest Size vs Collision Time')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Collision Time (seconds)')

    # Plot 2: Digest Size vs Number of Inputs
    plt.subplot(1, 2, 2)
    plt.plot(digest_sizes, num_inputs, marker='o')
    plt.title('Digest Size vs Number of Inputs')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Number of Inputs')

    plt.tight_layout()
    plt.show()

def main():
    min_bits = 8
    max_bits = 50
    step_size = 2

    digest_sizes = list(range(min_bits, max_bits + 1, step_size))
    collision_times = []
    num_inputs = []

    for truncate_bits in digest_sizes:
        iterations, collision_time = find_collision(truncate_bits)
        collision_times.append(collision_time)
        num_inputs.append(iterations)
        print(f"Truncate Bits: {truncate_bits}, Iterations: {iterations}, Collision Time: {collision_time} seconds")

    plot_graphs(digest_sizes, collision_times, num_inputs)

if __name__ == "__main__":
    main()
