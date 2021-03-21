import csv, sys, os

class test:
    def __init__(self, test_name, config):
        self.test_name = test_name
        self.config = config
        self.vals = {}

    def add_val(self, key, val):
        self.vals[key] = val

want_vals = ['final_tick', 'system.switch_cpus.iew.branchMispredicts',
 'system.switch_cpus.iew.exec_branches', 'system.switch_cpus.iew.predictedNotTakenIncorrect',
 'system.switch_cpus.iew.predictedNotTakenIncorrect', 'system.switch_cpus.iew.predictedTakenIncorrect',
 'system.switch_cpus.branchPred.lookups', 'system.switch_cpus.branchPred.condPredicted',
 'system.switch_cpus.branchPred.condIncorrect', 'system.switch_cpus.commit.branchMispredicts']
tests = []

for d in os.walk('.'):
    if 'stats.txt' not in d[2]:
        continue

    dir_name = d[0]
    dir_parts = dir_name[2:].split('-')
    if len(dir_parts) < 3:
        dir_parts.append("")
    stat_file = dir_name + '/stats.txt'
    t = test(dir_parts[0], "%s_%s" % (dir_parts[1], dir_parts[2]))
    print (dir_name)

    with open(stat_file, 'r') as file:
        for line in file:
            s = line.split()
            if len(s) <= 0:
                continue
            if s[0] in want_vals:
                t.add_val(s[0], s[1])

    tests.append(t)

tests.sort(key=lambda x: x.config + x.test_name, reverse=False)
with open('stats.csv', mode='w') as csv_file:
    fieldnames = ['predictor', 'benchmark'] + want_vals
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for t in tests:
        row = {
            'predictor':t.test_name, 
            'benchmark': t.config
        }
        row.update(t.vals)
        writer.writerow(row)