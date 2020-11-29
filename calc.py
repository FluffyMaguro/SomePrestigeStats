import json
import datetime
from pprint import pprint 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

fig_size = (10.1,6)

# Data generated from my replays and my parser. Excluded non-blizzard maps, common partners.
with open('player_levels.json','r') as f:
    data = json.load(f)

for idx, i in enumerate(data):
    data[idx][3] = int(i[3].replace(':',''))

data = sorted(data, key=lambda x:x[3])
data = [i for i in data if i[1] != 'Potato' and i[0][:3] != '98-']


# [handle, name, level, date]
# min date: 20171228210954 (after ascension was released)

def generate_ally_levels():
    """ Percent of sub/mastery/ascension over time """
    current_month = (2017,12)
    new_data = list()

    xval = list()
    yval_sub = list()
    yval_asc = list()
    yval_mas = list()

    for rep in data:
        year = rep[3]//10**10
        month = (rep[3]//10**8) % 100

        if current_month == (year, month):
            new_data.append(rep)

        elif len(new_data) == 0:
            # No data for that month
            print(current_month, '---')
        else:
            # Analyse previous month   
            levels = [i[2] for i in new_data]
            slevels = [i for i in levels if i == 0]
            mlevels = [i for i in levels if 0 < i <= 90] #mastery
            alevels = [i for i in levels if 90 < i] #ascension

            print(current_month, 100*len(slevels)/len(levels), len(levels))

            xval.append(current_month)
            yval_sub.append(100*len(slevels)/len(levels))
            yval_asc.append(100*len(alevels)/len(levels))
            yval_mas.append(100*len(mlevels)/len(levels))

            # Update month
            current_month = (year, month)
            new_data = list()


    xlabels = [f"{i[0]} - {i[1]:02}" for i in xval]
    x = [datetime.datetime.strptime(str(i[0])+str(i[1]), '%Y%m') for i in xval]

    labels = ["Submastery ", "Mastery", "Ascension"]

    fig, ax = plt.subplots()
    fig.set_size_inches(fig_size)
    ax.stackplot(x, yval_sub, yval_mas, yval_asc, labels=labels)

    prestige_path = datetime.datetime.strptime('2020:8', '%Y:%m')
    plt.plot([prestige_path,prestige_path],[0,100],'k-',lw=0.5)
    plt.text(prestige_path, 93, 'Prestige patch ',  horizontalalignment='right')

    plt.xticks(x, rotation='vertical', labels=xlabels)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    ax.legend(loc='upper center')
    plt.subplots_adjust(bottom=0.20)
    plt.title('Ally levels in StarCraft II Co-op')
    plt.ylabel('Percent of games')
    plt.show()


def generate_histogram():
    levels = [i[2] for i in data]
    mlevels = [i for i in levels if 0 < i <= 90] #mastery
    alevels = [i for i in levels if 90 < i] #ascension
    malevels = mlevels+alevels

    ### HISTOGRAM
    plt.hist(levels, bins=100, range=(1,1000))
    plt.gcf().set_size_inches(fig_size)
    plt.title('Ally mastery+ level distribution')
    plt.xlabel('Mastery/ascension levels')
    plt.ylabel('Games')
    plt.plot([90,90],[0,350],'k-',lw=0.5)
    plt.text(90, 330, ' Full mastery')
    plt.show()

generate_ally_levels()
generate_histogram()


### PIE CHART (no useful information here)
# values = [len(alevels), len(mlevels), len(levels) - len(alevels) - len(mlevels)]
# labels = ['Ascension','Mastery','1-15 levels']

# fig, ax = plt.subplots()
# fig.set_size_inches(fig_size)
# ax.pie(values, labels=labels, pctdistance=0.7, explode=[0,0,0], autopct='%1.1f%%', startangle=90)
# ax.set_title('Ally levels')
# plt.show()