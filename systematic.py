# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:10:25 2018

@author: jxz12
"""
import numpy as np

# parse the data
def unpack(name):
    stress = []
    with open(name) as lines:
        for line in lines:
            vals = line.rstrip().split(' ')
            if len(vals) > 1:
                stress.append((int(vals[0]),float(vals[1]),float(vals[2])/1000))
    return stress

# save determines whether to overwrite minmins for ordering (as well as convergence vs 15 iterations)
# save=True
save=False

# tracks the min, max, avg at every iteration
def get_stress(stress):
    iterations = max(stress, key=lambda x:x[0])[0] + 1
    runs = len(stress) / iterations
    avg = [0] * iterations
    minn = [float('inf')] * iterations
    maxx = [0] * iterations
    for point in stress:
        avg[point[0]] += point[1]
        minn[point[0]] = min(minn[point[0]], point[1])
        maxx[point[0]] = max(maxx[point[0]], point[1])
    for i in range(iterations):
        avg[i] /= runs
    return avg, minn, maxx

def get_stress_end(stress):
    avg = 0
    minn = float('inf')
    maxx = 0
    runs = 0
    iterations = 0
    
    prev_point = [-1,0,0]
    for point in stress:
        if point[0] < prev_point[0]:
            final_stress = prev_point[1]
            minn = min(minn, final_stress)
            maxx = max(maxx, final_stress)
            avg += final_stress
            runs += 1
        prev_point = point
        iterations += 1
        
    minn = min(minn, prev_point[1])
    maxx = max(maxx, prev_point[1])
    avg += prev_point[1]
    runs += 1
    return avg/runs, minn, maxx, iterations/runs

#%%
import glob

# gets the min, avg, max stress at a certain iteration in each graph
# also gets the minimum of all minimums
def get_range(extension, iteration):
    result = {}
    for file in glob.glob("data/"+extension):
        stress = unpack(file)
        name = file[5:-len(extension)+1]
        
        if save is False:
            avgg, minn, maxx = get_stress(stress)
            result[name] = {"minmin": minn[-1],
                            "min": minn[iteration],
                            "avg": avgg[iteration],
                            "max": maxx[iteration]}
        else:
            avgg, minn, maxx, iters = get_stress_end(stress)
            result[name] = {"minmin": minn,
                            "min": minn,
                            "avg": avgg,
                            "max": maxx,
                            "iters": iters}
    return result


# get values at the 15th iteration
if save:
    range1 = get_range("*_maj_converged.txt", -1)
    range2 = get_range("*_wcr_converged30.txt", -1)
else:
    range1 = get_range("*_maj.txt", 14)
    range2 = get_range("*_wcr.txt", 14)


#print(min(range1.values(), key=lambda x: x['iters']))
#print(max(range1.values(), key=lambda x: x['iters']))
#print(min(range2.values(), key=lambda x: x['iters']))
#print(max(range2.values(), key=lambda x: x['iters']))
#
#total1 = 0
#total2 = 0
#for name in range1.keys():
#    total1 += range1[name]['iters']
#    total2 += range2[name]['iters']
#print('{} {}'.format(total1/len(range1), total2/len(range1)))

    

# normalise all the data to the minimum of all minimums
n = len(range1)
if save is True:
    minmins = {}
    
diffs = {}
i=0
for name in range1.keys():
    if save is True:
        minmin = min(range1[name]["minmin"], range2[name]["minmin"])
        minmins[name] = minmin
    else:
        minmin = minmins[name]
        
    norm = lambda x: x/minmin
    range1[name]['min'] = norm(range1[name]['min'])
    range1[name]['avg'] = norm(range1[name]['avg'])
    range1[name]['max'] = norm(range1[name]['max'])
    range2[name]['min'] = norm(range2[name]['min'])
    range2[name]['avg'] = norm(range2[name]['avg'])
    range2[name]['max'] = norm(range2[name]['max'])
    diffs[name] = range1[name]['avg'] - range2[name]['avg']


#%%

if save is True:
    # first sort by average difference
    names = sorted(range1.keys(), key=lambda x: diffs[x])
    #names = sorted(final.keys(), key=lambda x: minmins[x])
    
    # get the group names using the groups.csv file
    def get_groups():
        groups = {}
        with open('groups.csv') as lines:
            for line in lines:
                vals = line.rstrip().split(',')
                if len(vals) > 1:
                    groups[vals[1]] = vals[0]
        return groups
    
    # now sort by group name
    groups = get_groups()
    names = sorted(names, key=lambda x: groups[x])


# plot error bars
import matplotlib.pyplot as plt
plt.clf()
plt.figure(figsize=(20,3))
plt.margins(.008, .05)
plt.semilogy()

def plot_errorbars(stress, names, offset, col, label, fmt):
    avgs = []
    mins = []
    maxs = []
    yerr0 = []
    yerr1 = []
    for name in names:
        avg = stress[name]['avg']
        avgs.append(avg)
        mins.append(stress[name]['min'])
        maxs.append(stress[name]['max'])
        yerr0.append(stress[name]['avg'] - stress[name]['min'])
        yerr1.append(stress[name]['max'] - stress[name]['avg'])
        
    plt.errorbar(np.arange(offset, len(names)+offset, 1), avgs, yerr=[yerr0, yerr1],
                 fmt=fmt, alpha=.7, elinewidth=2.5, color=col, label=label)
    print(sum(avgs)/len(avgs))
#    print(sum(mins)/len(mins))
#    print(sum(maxs)/len(maxs))


cmap = plt.get_cmap('tab10')
plot_errorbars(range1, names, 0, cmap(.1), 'majorization', '_')
plot_errorbars(range2, names, 0, cmap(0), 'SGD', '.')
#plot_errorbars(range1, names, 0, cmap(.6), '$\omega<2$', '_')
#plot_errorbars(range2, names, 0, cmap(0), '$\omega\leq 1$', '.')
#plt.grid(True, linewidth=.1)

# add ticks
group_names = []
gname = ""
swap = False
group_ticks = []
for i in range(n):
    if gname != groups[names[i]]:
        swap = not swap
        gname = groups[names[i]]
    if swap == True:
        group_ticks.append(0)
    else:
        group_ticks.append(1)
    group_names.append('{}    {}'.format(names[i],groups[names[i]]))
#    group_names.append('{}'.format(groups[names[i]]))

plt.rcParams['font.size'] = 13
plt.xticks(range(n), group_names, rotation=90, fontsize=4)
plt.legend()
plt.ylabel('stress')
#plt.ylim(ymin=.97, ymax=2)
plt.ylim(ymin=.95, ymax=10)


plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom='off')

if save:
    plt.title(r'$\rightarrow \infty$', fontweight='bold')
    plt.savefig('systematic_inf.svg')
else:
    plt.title(r'15 iterations', fontweight='bold')
    plt.savefig('systematic_15.svg')

