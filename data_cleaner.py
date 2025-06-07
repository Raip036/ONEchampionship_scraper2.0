import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("one_fighters_all.csv")

# --- Plotting ---
plt.figure(figsize=(10, 12))  # Wider and MUCH taller (key adjustment)

# Create the countplot
ax = sns.countplot(
    y="Country_1",
    data=df,
    order=df["Country_1"].value_counts().index,
    palette="viridis",
)

# Add count labels on bars
for p in ax.patches:
    width = p.get_width()
    ax.text(
        width + 0.5,  # Position label just outside the bar
        p.get_y() + p.get_height() / 2,  # Center vertically
        f"{int(width)}",  # Display count
        ha="left",
        va="center",
        fontsize=10,
    )

# Adjust layout and fonts
plt.title("Top Countries in ONE Championship", fontsize=16, pad=20)
plt.xlabel("Number of Fighters", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=12)  # Larger font for country names

# Increase spacing between y-axis labels (critical fix!)
ax.yaxis.set_tick_params(pad=20)  # Adds vertical padding between labels

# Ensure tight layout to prevent clipping
plt.tight_layout()

# Save high-resolution image
plt.savefig("fighters_by_country.png", dpi=300, bbox_inches="tight")

plt.show()