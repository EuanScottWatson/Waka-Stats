import json
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from collections import Counter

LANGUAGES = ['Python', 'Swift', 'Cocoa', 'Kotlin', 'Haskell', 'Java', 'Other', 'Markdown']


class Day:
    def __init__(self, date: str, coding: float, building: float, languages: dict[str, float]) -> None:
        self.date = date
        self.coding = 0 if coding is None else coding
        self.building = 0 if building is None else building
        self.languages = languages

    def __str__(self) -> str:
        return f"{self.date}:\n\tCoding: {self.coding}\n\tBuilding: {self.building}"


def extract_coding(data):
    days = []
    for day in data:
        cats = day['categories']
        coding, building = None, None
        for cat in cats:
            if cat['name'] == "Coding":
                coding = float(cat['decimal'])
            if cat['name'] == "Building":
                building = float(cat['decimal'])

        langs = day['languages']
        supported = {l: 0 for l in LANGUAGES}
        for lang in langs:
            if lang['name'] in supported:
                supported[lang['name']] += float(lang['decimal'])
            else:
                supported['Other'] += float(lang['decimal'])

        days.append(Day(day['date'], coding, building, supported))
    
    total = round(sum(map(lambda x: x.coding + x.building, days)), 2)
    total_langs = Counter({l: 0 for l in LANGUAGES})

    for d in days:
        total_langs += Counter(d.languages)

    total_langs = dict(sorted(total_langs.items(), key=lambda i: i[1], reverse=True))

    print(f"This data ranges from {days[0].date} to {days[-1].date}")
    print(f"You spent {total} hours coding.")
    print("Of which you spent:")
    for l, t in total_langs.items():
        print(f"\t{round(t, 2)} hours coding in {l}")


    return days


class InteractiveLegend(object):
    def __init__(self, legend) -> None:
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()


def interactive(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()
    
    return InteractiveLegend(ax.get_legend())


def plot(days):
    fig, ax = plt.subplots()

    dates = [dt.datetime.strptime(d.date ,'%Y-%m-%d').date() for d in days]

    timings = {l: [] for l in LANGUAGES}
    timings['Coding'] = list(map(lambda x: x.coding, days))
    timings['Building'] = list(map(lambda x: x.building, days))

    for d in days:
        for l, t in d.languages.items():
            timings[l].append(t)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))

    timings = dict(sorted(timings.items(), key=lambda i: i[1], reverse=True))

    for l, ts in timings.items():
        plt.plot(dates, ts, label=l)

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1, borderaxespad=0)
    fig.subplots_adjust(right=0.85)

    plt.gcf().autofmt_xdate()

    plt.xlim(dates[0], dates[-1])
    plt.ylim(bottom=0)

    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.title("Hours Spent Coding in Different Languages")

    leg = interactive()

    plt.show()


def main():
    with open('data.json') as js:
        data = json.load(js)
        
        days = extract_coding(data['days'])
        plot(days)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for l in sys.argv[1:]:
            if l not in LANGUAGES:
                LANGUAGES.append(l)
    
    main()
