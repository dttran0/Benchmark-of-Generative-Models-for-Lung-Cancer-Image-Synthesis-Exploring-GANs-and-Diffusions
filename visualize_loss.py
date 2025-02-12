import re
import matplotlib.pyplot as plt

def retrieve_loss(text_doc):
    # Read the contents of the file
    with open(text_doc, 'r') as file:
        log_lines = file.readlines()

    # Define a pattern to extract lines with loss
    loss_pattern = r"loss: =([\d.]+)"

    # Extract all matches
    loss_values = []
    for line in log_lines:
        match = re.search(loss_pattern, line)
        if match:
            loss_values.append(match.group(1))
    loss_values = [float(i) for i in loss_values]
    return loss_values

unet_baseline = retrieve_loss('lung-pet-ct loss-noise-baseline-unet.txt')[:800]
ukan_hybrid = retrieve_loss('lung-pet-ct loss-noise-ukan_hybrid.txt')[:800]
print(len(unet_baseline))
print(len(ukan_hybrid))
epochs = list(range(len(unet_baseline)))
#Print the specific loss value you're looking for (if it exists)
plt.figure(figsize=(10, 6))
plt.plot(epochs, unet_baseline, label='UNet-Baseline Loss', color='blue', markersize=1, linestyle='-')
plt.plot(epochs, ukan_hybrid, label='UKan-Hybrid Loss', color='orange', markersize=1, linestyle='-')

# Customizing the plot
plt.title("Lung-Pet-CT Training Loss of UNet-Baseline and UKan-Hybrid", fontsize=16)
plt.xlabel("Epochs", fontsize=14)
plt.ylabel("Loss", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("./Lung-Pet-CT_training_loss_comparison.png", bbox_inches='tight')

# Display the plot
plt.show()
