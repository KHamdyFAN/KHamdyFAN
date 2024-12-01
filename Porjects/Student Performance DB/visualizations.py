import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image, ImageTk


def plot_performance(data, x_axis, y_axis):
    """
    Function to plot the performance data.
    """
    if x_axis not in data.columns or y_axis not in data.columns:
        raise ValueError(f"Data must contain '{x_axis}' and '{y_axis}' columns")

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.barplot(x=x_axis, y=y_axis, data=data, palette="viridis")
    plt.title(f'{y_axis.capitalize()} by {x_axis.capitalize()}')
    plt.xlabel(x_axis.capitalize())
    plt.ylabel(y_axis.capitalize())
    plt.tight_layout()

    # Save the plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', facecolor='lightgray')
    buf.seek(0)
    img = Image.open(buf)

    return ImageTk.PhotoImage(img)
