import csv
import random


def suvalineaeg(a, b):
    aeg = round(random.uniform(a, b), 3)
    return aeg


def taisringi_aeg():
    total = 0
    lap_times = []
    sector_times = []
    errors = []

    for lap in range(1, 11):
        s1 = suvalineaeg(alg, lopp)
        s2 = suvalineaeg(alg, lopp)
        s3 = suvalineaeg(alg, lopp)

        number = random.randint(1, 10)
        if number == 2:
            s1 = suvalineaeg(30, 90)
            s2 = suvalineaeg(30, 90)
            s3 = suvalineaeg(30, 90)
            errors.append("True")
        else:
            errors.append("False")

        lap_time = s1 + s2 + s3
        total += lap_time
        lap_times.append(lap_time)
        sector_times.append([s1, s2, s3])

    return total, lap_times, sector_times, errors


def sec2time(sec, n_msec=3):
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)


racers = ["Mario", "Romet", "Viru", "Mattias", "Kaur"]
alg, lopp = 23, 26

with open("race_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Ring", "Nimi", "Aeg", "Sektor1", "Sektor2", "Sektor3", "Viga"])

    for racer in racers:
        total_time, lap_times, sector_times, errors = taisringi_aeg()
        for i, (lap_time, sector, error) in enumerate(zip(lap_times, sector_times, errors), start=1):
            s1, s2, s3 = sector
            formatted_time = "{:.3f}".format(lap_time)
            writer.writerow([i, racer, formatted_time, s1, s2, s3, error])

print("Andmed on salvestatud CSV-faili 'race_results.csv'.")

Filename = 'race_results.csv'
results = []
fastest_lap = ['Unknown', 9999]
three_sektors = [['Unknown', 9999], ['Unknown', 9999], ['Unknown', 9999]]
lap_times = {}
lap_errors = {}

with open(Filename, mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Skip header row
    for data in reader:
        lap_number = int(data[0])
        name = data[1]
        lap_time = float(data[2])
        sector1 = float(data[3])
        sector2 = float(data[4])
        sector3 = float(data[5])
        error = True if data[6].lower() == 'true' else False
        if lap_time < fastest_lap[1]:
            fastest_lap[0] = name
            fastest_lap[1] = lap_time
        if sector1 < three_sektors[0][1]:
            three_sektors[0][0] = name
            three_sektors[0][1] = sector1
        if sector2 < three_sektors[1][1]:
            three_sektors[1][0] = name
            three_sektors[1][1] = sector2
        if sector3 < three_sektors[2][1]:
            three_sektors[2][0] = name
            three_sektors[2][1] = sector3

        if name not in lap_times:
            lap_times[name] = 0
        lap_times[name] += lap_time

        if error:
            if name not in lap_errors:
                lap_errors[name] = []
            lap_errors[name].append(lap_number)

        results.append([name, lap_time, error])

lap_times = sorted(lap_times.items(), key=lambda x: x[1])

rank = 1
for idx, (name, total_time) in enumerate(lap_times):
    time_difference = sec2time(total_time - fastest_lap[1])
    error_laps = lap_errors.get(name, '[]')
    time_difference_from_first = sec2time(total_time - lap_times[0][1])
    fastest_lap_str = 'FASTEST' if name == fastest_lap[0] else ''
    print(f"{rank} {name.ljust(10)} {sec2time(total_time)} {error_laps} {fastest_lap_str}")
    rank += 1

print('Sektori parimad')
total = sum(driver[1] for driver in three_sektors)
for idx, driver in enumerate(three_sektors):
    print(f"Sektor {idx + 1} {driver[0].ljust(10)} {sec2time(driver[1])}")
print('Unelmate Ring', sec2time(total))

