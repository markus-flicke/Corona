import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

plt.rcParams['figure.figsize'] = (20, 8)
plt.rcParams['figure.dpi'] = 72
plt.rcParams['font.size'] = 20

PROJECTION_COL, DEATH_COL, INFECTION_COL = sns.color_palette(n_colors=3)


def main():
    """
    Dynamic graph representation of the current Wikipedia data on the Chinese Corona Virus outbreak in 2020.
    :return:
    """

    df = _get()
    df = _clean(df)
    _plot(df)


def _get():
    df = pd.read_html('https://en.wikipedia.org/wiki/Timeline_of_the_2019%E2%80%9320_Wuhan_coronavirus_outbreak')[1]
    df = df[[('DateCST', 'DateCST'), ('Cases', 'Confirmed'), ('Deaths', 'Deaths'), ('Recovered', 'Recovered')]]
    df.columns = ['date', 'infections', 'deaths', 'recovered']
    df.date = pd.to_datetime(df.date)
    return df.copy()


def _clean(df):
    df = df.dropna(thresh=3)
    df.infections = df.infections.where(df.infections.notnull(), df.infections.shift(1))
    df.deaths = df.deaths.where(df.deaths.notnull(), df.deaths.shift(1))
    for i in range(3):
        df.recovered = df.recovered.where(df.recovered.notnull(), df.recovered.shift(1))
    df.recovered = df.recovered.where(df.recovered.notnull(), 0)
    return df.copy()


def _plot(df):
    fig, ax = plt.subplots(1, 1)
    ax2 = ax.twinx()
    ax2.plot(df.date, 100 * df.deaths / (df.infections + df.recovered), '--', alpha=0.5, marker='.', label='kill rate')
    ax.plot(df.date, df.infections, marker='.', color=INFECTION_COL, label='infections')
    ax.plot(df.date, df.deaths, marker='.', color=DEATH_COL, label='deaths')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())

    fig.suptitle('Corona Virus Wuhan')
    fig.legend(loc=2)
    ax.grid()
    plt.savefig('corona.png')
    plt.show()



if __name__ == '__main__':
    main()
