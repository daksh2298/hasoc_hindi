import json


def fetch_data_json():
    file = open('data/dummy.txt')
    datas = file.readlines()
    count = 0
    judgement = ['NAG', 'CAG', 'OAG']
    rows = []
    for data in datas:
        data = json.loads(data)
        data['pre_judgement'] = judgement[count % 3]
        data['num'] = count
        row = [data.get('num'), data.get('text'), data.get('pre_judgement')]
        rows.append(row)
        count += 1
    print(rows)


def resolve_conflict():
    d = ['NOT', 'TIN', 'IND']
    a = ['HOF', 'TIN', 'GRP']
    s = ['HOF', 'TIN', 'IND']
    k = ['NOT', 'UNT', 'GRP']
    m = ['NOT', 'UNT', 'GRP']

    t1 = [d[0], a[0], s[0], k[0], m[0]]
    t2 = [d[1], a[1], s[1], k[1], m[1]]
    t3 = [d[2], a[2], s[2], k[2], m[2]]

    all = [t1, t2, t3]

    print('T1:- {}\nT2:- {}\nT3:- {}'.format(t1, t2, t3))

    for judgement in all:
        set_j = list(set(judgement))
        print(set_j)
        occurence = []
        for s in set_j:
            occurence.append(judgement.count(s))
        print(occurence)
        max_o = max(occurence)
        final = set_j[occurence.index(max_o)]
        print(final)


if __name__ == '__main__':
    resolve_conflict()