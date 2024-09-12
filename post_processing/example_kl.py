import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, entropy

# Revised function to include a third plot which is halfway between different shapes and different means
def generate_kl_divergence_figure(target_kl_divergence=1.0):
    # Generate two distributions with similar means but different variances
    mean1, mean2 = 0, 0  # Same means
    std1 = 0.5  # Skinny distribution
    std2 = 1.0  # Initial guess for fat distribution

    # Adjust std2 to match target KL divergence for similar mean condition
    x = np.linspace(-10, 10, 1000)
    p1 = norm.pdf(x, mean1, std1)
    p2 = norm.pdf(x, mean2, std2)

    current_kl_divergence = entropy(p1, p2)
    epsilon = 0.001  # Tolerance for KL divergence

    # Adjusting std2 using a finer approach for precision
    while abs(current_kl_divergence - target_kl_divergence) > epsilon:
        std2 += (target_kl_divergence - current_kl_divergence) * 0.01  # Proportional adjustment
        p2 = norm.pdf(x, mean2, std2)
        current_kl_divergence = entropy(p1, p2)

    # Plot the first graph
    plt.figure(figsize=(8, 15))

    plt.subplot(3, 1, 1)
    plt.plot(x, p1, label=f"Dist 1 (mean={mean1}, std={std1})")
    plt.plot(x, p2, label=f"Dist 2 (mean={mean2}, std={std2:.2f})")
    plt.title(f"KL Divergence (similar mean): {current_kl_divergence:.2f}")
    plt.legend()

    # Generate two distributions with similar shapes but different means
    std3, std4 = 1.0, 1.0  # Same standard deviations
    mean3, mean4 = 0, 0.1  # Start with different means

    # Adjust mean4 to match target KL divergence for similar shape condition
    p3 = norm.pdf(x, mean3, std3)
    p4 = norm.pdf(x, mean4, std4)

    current_kl_divergence = entropy(p3, p4)

    # Adjust mean4 to match the target KL divergence
    while abs(current_kl_divergence - target_kl_divergence) > epsilon:
        mean4 += (target_kl_divergence - current_kl_divergence) * 0.01  # Proportional adjustment
        p4 = norm.pdf(x, mean4, std4)
        current_kl_divergence = entropy(p3, p4)

    # Plot the second graph
    plt.subplot(3, 1, 2)
    plt.plot(x, p3, label=f"Dist 3 (mean={mean3}, std={std3})")
    plt.plot(x, p4, label=f"Dist 4 (mean={mean4:.2f}, std={std4})")
    plt.title(f"KL Divergence (similar shape): {current_kl_divergence:.2f}")
    plt.legend()

    # Generate third distribution halfway between different variances and different means
    mean5 = (mean2 + mean4) / 2
    std5 = (std2 + std4) / 2

    p5 = norm.pdf(x, mean1, std1)
    p6 = norm.pdf(x, mean5, std5)

    current_kl_divergence = entropy(p5, p6)

    # Adjust p6 to achieve the target divergence halfway between the two types
    while abs(current_kl_divergence - target_kl_divergence) > epsilon:
        mean5 += (target_kl_divergence - current_kl_divergence) * 0.005
        std5 += (target_kl_divergence - current_kl_divergence) * 0.005
        p6 = norm.pdf(x, mean5, std5)
        current_kl_divergence = entropy(p5, p6)

    # Plot the third graph
    plt.subplot(3, 1, 3)
    plt.plot(x, p5, label=f"Dist 5 (mean={mean1}, std={std1})")
    plt.plot(x, p6, label=f"Dist 6 (mean={mean5:.2f}, std={std5:.2f})")
    plt.title(f"KL Divergence (halfway between): {current_kl_divergence:.2f}")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Run the function to generate the figure with three plots
generate_kl_divergence_figure(target_kl_divergence=0.25)

