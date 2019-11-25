import csv

with open('/home/andreyk/Work/exchange/doctors.csv') as f:
    reader = csv.DictReader(f,
                            ('idx', 'snils', 'fio', 'mo_code', 'mo_name', 'name', 'code'),
                            delimiter=',', quotechar='"')
    posts = {}
    for row in reader:
        snils = row['snils'].strip()
        fio = tuple(row['fio'].strip().split())
        code = row['code'].replace(' \n', '')
        name = row['name'].strip()
        if code or name:
            posts[(snils, fio)] = (code, name)

for (snils, fio), (code, name) in posts.items():
    print(f"('{snils}', '{fio[0]}', '{fio[1]}', '{fio[2]}', '{code}', '{name}'),")
