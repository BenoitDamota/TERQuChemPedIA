import matplotlib.pyplot as plt
import matplotlib as mpl
from math import floor
import h5_keys
import numpy as np
from matplotlib import gridspec
from h5_keys import *
import h5py


mpl.rcParams['agg.path.chunksize'] = 10000


def plot_distrib_rmses_val(rmses, model_name, figures_loc):
    """ Display errors distribution """

    fig = plt.figure()

    plt.axis("off")

    # Linear Y scale
    ax1 = fig.add_subplot(121)
    ax1.set_title(model_name + " model\n Errors distribution")
    ax1.set_xlabel("Absolute error (pm)")
    ax1.set_ylabel("Test set occurrences (linear scale)")
    ax1.hist(rmses, floor(max(rmses)-min(rmses)))

    # Logarithmic Y scale
    ax2 = fig.add_subplot(122)
    ax2.set_yscale("log")
    ax2.set_title(model_name + " model\n Errors distribution")
    ax2.set_xlabel("Absolute error (pm)")
    ax2.set_ylabel("Test set occurrences (logarithmic scale)")

    ax2.hist(rmses, floor(max(rmses) - min(rmses)))

    plt.gcf().subplots_adjust(wspace=0.3)

    plt.savefig(figures_loc + model_name + "_distrib_rmse_val.png", dpi=250)
    plt.show()


def plot_rmse_distrib_dist(rmses, targets, model_name, figures_loc, bonds_lengths_loc):

    gs = gridspec.GridSpec(2, 1, height_ratios=[13, 1])

    ax = plt.subplot(gs[0])

    ax.set_title(model_name + " model " + "\nError distribution depending on target distances")
    ax.set_xlabel("Target distance (pm)")
    ax.set_ylabel("Absolute error (pm)")
    ax.plot(targets, rmses, ",", label="Absolute error (pm)", alpha=0.8)
    ax.set_xlim(xmin=min(targets), xmax=max(targets))

    ax2 = plt.subplot(gs[1])

    bonds_lengths_h5 = h5py.File(bonds_lengths_loc, "r")
    bonds_lengths = np.array(bonds_lengths_h5[distances_key])
    hist_bonds = np.histogram(bonds_lengths, np.arange(min(targets)/10000, max(targets)/10000, 0.0001))[0]
    ax2.axis('off')

    cmap = mpl.cm.Blues
    norm = mpl.colors.Normalize()

    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, values=hist_bonds,
                                    norm=norm,
                                    orientation='horizontal')

    cb1.set_label('Bond lengths representation')

    plt.tight_layout()

    plt.savefig(figures_loc + model_name + "_distrib_rmse_dist.png", dpi=250)

    plt.show()


def fun_id(x):
    return x


def plot_targets_pred(targets, preds, anum_1, anum_2, model_name, figures_loc, bonds_lengths_loc):
    gs = gridspec.GridSpec(2, 1, height_ratios=[13, 1])

    # Predictions depending on target distances plot
    ax = plt.subplot(gs[0])
    ax.set_title(model_name + " model\n Predictions depending on target distances")
    ax.set_xlabel("Target distance (pm)")
    ax.set_ylabel("Predicted distance (pm)")
    ax.plot(targets, preds, ",")
    ax.set_xlim(xmin=min(targets), xmax=max(targets))

    # Perfect model plot
    x = np.linspace(min(targets), max(targets))
    ax.plot(x, fun_id(x), color='darkgreen', label="Theoretical perfect model")
    ax.legend(loc='lower center', shadow=False)

    # Distances representation plot
    ax2 = plt.subplot(gs[1])
    bonds_lengths_h5 = h5py.File(bonds_lengths_loc, "r")
    bonds_lengths = np.array(bonds_lengths_h5[distances_key])
    hist_bonds = np.histogram(bonds_lengths, np.arange(min(targets) / 10000, max(targets) / 10000, 0.0001))[0]
    ax2.axis('off')

    cmap = mpl.cm.Blues
    norm = mpl.colors.Normalize()

    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, values=hist_bonds,
                                    norm=norm,
                                    orientation='horizontal')

    cb1.set_label('Bond lengths representation')

    plt.tight_layout()

    plt.savefig(figures_loc + model_name + "_preds_targets.png", dpi=250)

    plt.show()


def print_stats_errors(errors):
    print("Dataset size : "+str(len(errors)))
    print("Mean error : " + str(np.mean(errors)))
    print("Median error : " + str(np.median(errors)))
    print("Standard deviation : " + str(np.std(errors)))
    print("Min error : " + str(min(errors)))
    print("Max error : " + str(max(errors)))


def plot_model_results(errors, predictions, targets, model_name, anum_1, anum_2, bonds_lengths_loc, plots_dir,
                       plot_error_distrib, plot_targets_error_distrib, plot_targets_predictions):

    print("Plotting "+model_name)

    print_stats_errors(errors)

    if plot_error_distrib:
        plot_distrib_rmses_val(errors, model_name, plots_dir)

    if plot_targets_error_distrib:
        plot_rmse_distrib_dist(errors, targets, model_name, plots_dir, bonds_lengths_loc)

    if plot_targets_predictions:
        plot_targets_pred(targets, predictions, anum_1, anum_2, model_name, plots_dir, bonds_lengths_loc)


def biggest_errors_CIDs(errors, test_prepared_input_loc, n):
    """
    Prints the CIDs the molecules causing the n biggest errors
    :param errors:
    :param predictions:
    :param targets:
    :return:
    """

    cids = np.array(h5py.File(test_prepared_input_loc, 'r')[h5_keys.pubchem_id_key])