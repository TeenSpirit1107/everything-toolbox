from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

def truncated_normal_percentile(mean, std, x, low=0, high=100):
    """
    Compute the percentile of a truncated normal distribution.
    """
    # CDF of the original CDF
    cdf_x = norm.cdf(x, mean, std)
    cdf_low = norm.cdf(low, mean, std)
    cdf_high = norm.cdf(high, mean, std)

    # truncated percentile
    percentile = (cdf_x - cdf_low) / (cdf_high - cdf_low) * 100
    return percentile

def plot_truncated_normal(mean, std, x, low=0, high=100):
    """
    Plot the truncated normal distribution as a histogram with 5-point bins
    and mark the user's score position.
    """
    # Generate bins with 5-point intervals
    bins = np.arange(low, high + 5, 5)
    
    # Calculate the probability density for each bin
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_probs = []
    
    for i in range(len(bins) - 1):
        # Calculate the probability mass in each bin
        cdf_low_bin = norm.cdf(bins[i], mean, std)
        cdf_high_bin = norm.cdf(bins[i+1], mean, std)
        prob = cdf_high_bin - cdf_low_bin
        bin_probs.append(prob)
    
    # Normalize by truncation bounds
    cdf_low_trunc = norm.cdf(low, mean, std)
    cdf_high_trunc = norm.cdf(high, mean, std)
    normalization = cdf_high_trunc - cdf_low_trunc
    bin_probs = np.array(bin_probs) / normalization
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(bin_centers, bin_probs, width=4.5, alpha=0.7, 
            color='skyblue', edgecolor='black', label='Distribution')
    
    # Mark the user's position
    plt.axvline(x=x, color='red', linestyle='--', linewidth=2, 
                label=f'Your Score: {x}')
    
    # Add a marker at the top
    max_prob = max(bin_probs)
    plt.plot(x, max_prob * 1.05, 'rv', markersize=12, label='You are here')
    
    # Labels and title
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.title(f'Truncated Normal Distribution\n(Mean={mean}, Std={std}, Range=[{low}, {high}])', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(low - 5, high + 5)
    
    # Add text annotation for percentile
    percentile = truncated_normal_percentile(mean, std, x, low, high)
    plt.text(x, max_prob * 1.15, f'{percentile:.2f}%', 
             ha='center', fontsize=10, color='red', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

print("=== Grade Percentile Calculator ===")
print("==== Author: Yimeng (Rosalind) ====")
print("==== Github Profile: https://github.com/TeenSpirit1107 ====")
print("==== Email: yimengteng@link.cuhk.edu.cn ====")

# check whether it's floating point, if not, ask the user to input again.
while True:
    mean = input("Please enter the mean:\n> ")
    if mean.replace('.', '', 1).isdigit():
        mean = float(mean)
        break
    print("Invalid input. Please enter a valid number.")

while True:
    std = input("Please enter the STANDARD DEVIATION (default 15):\n> ")
    if std.strip() == "":
        std = 15
        break
    if std.replace('.', '', 1).isdigit():
        std = float(std)
        break
    print("Invalid input. Please enter a valid number.")

while True:
    x = input("Please enter your score:\n> ")
    if x.replace('.', '', 1).isdigit():
        x = float(x)
        break
    print("Invalid input. Please enter a valid number.")

while True:
    low = input("Please enter the lower bound: (default 0)\n> ")
    if low.strip() == "":
        low = 0
        break
    if low.replace('.', '', 1).isdigit():
        low = float(low)
        break
    print("Invalid input. Please enter a valid number.")

while True:
    high = input("Please enter the upper bound: (default 100)\n> ")
    if high.strip() == "":
        high = 100
        break
    if high.replace('.', '', 1).isdigit() and float(high) >=x and x >= float(low):
        high = float(high)
        break
    print("Invalid input. Please enter a valid number.")

p = truncated_normal_percentile(mean, std, x, low, high)
plot_truncated_normal(mean, std, x, low, high)
q = 100-p

print(f"Truncated NORMAL distribution within [{low}, {high}]")
print(f"with standard deviation {std} and mean {mean}")
print(f"the score {x} is higher than {p:.2f}% of the students.")
print(f"i.e. you are among the top {q:.2f}%.")