import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix


def plot_for_p3(probs, labels=None, model_name=""):
    plt.close("all")
    fig = plt.figure(figsize=(16, 9), dpi=160)

    plt.subplot(1,2,1)

    Y = np.ones_like(probs) / 2
    X = np.arange(probs.shape[0])
    plt.scatter(X, probs)
    plt.scatter(X, labels, c="C2")
    plt.xlabel("Sample #")
    plt.ylabel("Outlier Probability")
    plt.title(f"{model_name}: {probs.shape[0]} samples")
    plt.plot(X, Y, color='gray', linestyle='dashed', alpha=0.8,linewidth=6)

    plt.subplot(1, 2, 2)

    Y = np.ones_like(probs) / 2
    X = np.arange(probs.shape[0])
    plt.scatter(X, probs)
    plt.scatter(X, labels, c="C2")
    plt.xlabel("Sample #")
    plt.ylabel("Outlier Probability")
    plt.xlim((0, probs.shape[0]/200))
    plt.title(f"{model_name}: {int(probs.shape[0]/200)} samples (for better label comparison)")
    plt.plot(X, Y, color='gray', linestyle='dashed', alpha=0.8, linewidth=6)



    plt.savefig(f"../p3plots/{model_name}_scatter.png", bbox_inches='tight')

    fig = plt.figure(figsize=(6, 4), dpi=160)
    A = confusion_matrix(labels, np.round(probs))
    sns.heatmap(A, annot=True, cmap='Oranges', fmt='g')
    plt.xlabel("Actual")
    plt.ylabel("Prediction")
    plt.title(f"{model_name}: {int(probs.shape[0] / 200)} samples (for better label comparison)")
    plt.savefig(f"../p3plots/{model_name}_heatmap.png", bbox_inches='tight')