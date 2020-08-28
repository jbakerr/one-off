from salesforce_reporting import Connection, ReportParser
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
from textwrap import fill
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter


def generate_hist_year(df, subset):

    colors = ["tab:red", "tab:blue", "tab:green", "tab:pink", "tab:olive"]

    sites = df["Site"].unique()

    fig, axes = plt.subplots(
        1, 4, figsize=(13, 3.75), dpi=100, sharex=True, sharey=True
    )

    for i, (ax, year) in enumerate(
        zip(axes.flatten(), sorted(df["High School Class"].unique()))
    ):

        x = df.loc[(df["High School Class"] == year), "GPA (Term)"]
        mu = x.mean()
        sigma = x.std()
        median = x.median()
        ax.hist(
            x,
            alpha=0.5,
            bins=20,
            density=False,
            stacked=True,
            label=str(year),
            color=colors[i],
        )
        ax.set_title(
            "Class of "
            + str(year)
            + "\n $\mu={mu:.2f}$, $\sigma={sigma:.2f}$, \u1E8B={median:.2f}".format(
                mu=mu, sigma=sigma, median=median
            ),
            fontsize=16,
        )

    plt.suptitle(
        "Histogram of {subset}'s Incoming Cohort GPAs".format(subset=subset),
        y=1.15,
        size=16,
    )
    plt.tight_layout()

    for ax in axes.flat:
        ax.set_xlabel("GPA", fontsize=14)
        ax.set_ylabel("Count of Students", fontsize=14)

    for ax in axes.flat:
        ax.label_outer()


def generate_bar_grade_bucket(df, subset, style=None):
    colors = ["tab:red", "tab:blue", "tab:green", "tab:pink", "tab:olive"]

    sites = df["Site"].unique()
    num_years = len(df["High School Class"].unique())
    if num_years == 1:
        num_years += 1

    fig, axes = plt.subplots(
        1, num_years, figsize=(16, 4.75), dpi=100, sharex=True, sharey=True
    )

    for i, (ax, year) in enumerate(
        zip(axes.flatten(), sorted(df["High School Class"].unique()))
    ):

        x = df.loc[(df["High School Class"] == year), "GPA Bucket (Term)"].value_counts(
            normalize=True
        )
        x = x.reindex(
            index=["Below 2.5", "2.5 to 2.74", "2.75 to 2.99", "3.0 to 3.49", "3.5+"]
        )

        ax.bar(x.index, x, alpha=0.5, label=str(year), color=colors[i])
        ax.set_title("Class of " + str(year), fontsize=16)
        ax.set_xlabel("GPA", fontsize=16)
        ax.set_ylabel("% of Students", fontsize=16)

        ax.xaxis.set_tick_params(rotation=45, labelsize=16)

        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

        ax.label_outer()

        for x, y in zip(x.index, x):
            ax.text(x, y - 0.04, "{:.0%}".format(y), ha="center", fontsize=16)

    plt.suptitle(
        "Breakdown of {subset}'s Incoming Cohort GPAs".format(subset=subset),
        y=1.15,
        size=20,
        ha="center",
        fontweight=style,
    )
    if num_years == 2:
        fig.delaxes(axes[1])
        fig.set_size_inches(8, 3.5)

        plt.suptitle(
            "Breakdown of {subset}'s Incoming Cohort GPAs".format(subset=subset),
            y=1.15,
            size=12,
            ha="center",
            fontweight="bold",
        )
        # fig.suptitle(size=12)

    plt.tight_layout()


def generate_all_charts(df, region, type):
    subset = region
    _df = df[df["Region"] == region]
    if type == "year":
        generate_hist_year(_df, subset=region)
    elif type == "bucket":
        generate_bar_grade_bucket(_df, subset=region, style="bold")
    else:
        generate_hist_combined(_df, subset=region)
    sites = _df.Site.unique()
    if len(sites) > 1:
        for site in sites:
            site_df = _df[_df.Site == site]
            if type == "year":
                generate_hist_year(site_df, subset=site)
            elif type == "bucket":
                generate_bar_grade_bucket(site_df, subset=site)
            else:
                generate_hist_combined(site_df, subset=site)


def generate_hist_combined(df, subset):
    fig, axes = plt.subplots(
        1, 1, figsize=(4.25, 3.75), dpi=100, sharex=True, sharey=True
    )
    x = df["GPA (Term)"]
    mu = x.mean()
    sigma = x.std()
    median = x.median()
    ax = plt.hist(x, alpha=0.5, bins=20, density=False, stacked=False, color="tab:blue")
    plt.title(
        str(subset)
        + "\n $\mu={mu:.2f}$, $\sigma={sigma:.2f}$, \u1E8B={median:.2f}".format(
            mu=mu, sigma=sigma, median=median
        ),
        fontsize=16,
    )

    plt.xlabel("GPA", fontsize=14)
    plt.ylabel("Count of Students", fontsize=14)
