import sys, datetime, requests, json, argparse, time
from foj import FOJ
from gen import table

parser = argparse.ArgumentParser(description='Generate Homework Scores')
parser.add_argument('-g','--group',type=int,default=7,
                    help='Group ID')
parser.add_argument('-t','--token',type=str,default='',
                    help='Cookies')
parser.add_argument('-a','--api',type=str,default='https://api.oj.nctu.me/',
                    help='Formosa OJ API base URL (default: %(default)s)')
parser.add_argument('-p','--problems',type=eval,default=[],
                    help='Problem list')
parser.add_argument('-s','--students',type=str,default='student.txt',
                    help='Student list (default: %(default)s)')
parser.add_argument('-d','--deadline',default='2099-01-01 00:00:00',
                    help='Deadline (default: %(default)s)')
parser.add_argument('-m','--meta',default=None,
                    help='JSON meta file (Optional)')

args = parser.parse_args()

def read_user_list(filename):
    with open(filename, 'r') as fp:
        users=[name for name in fp.read().split() if name[0]!='#']
    return sorted(users)

def calculate_score(pids=[], deadline='2099-10-01 00:00:00'):
    oj = FOJ(args.api,args.group,args.token)
    time_format = '%Y-%m-%d %H:%M:%S'
    deadline = datetime.datetime.strptime(deadline, time_format)
    users = oj.get_users(reverse=True)
    students = read_user_list(args.students)
    score = {stud: {pid:-1 for pid in pids} for stud in students}
    for sub in oj.get_submissions():
        uid = users.get(sub['user_id'], '')
        pid = sub['problem_id']
        subtime = datetime.datetime.strptime(sub['created_at'], time_format)
        if uid in students and pid in pids and subtime<deadline and sub['score']!=None:
            score[uid][pid]=max(score[uid][pid], sub['score'])
    return score

def main():
    if args.meta:
        with open(args.meta, 'r') as fp:
            hws = json.load(fp)
    else:
        hws = [{'id':'', 'pids':args.problems, 'deadline':args.deadline}]
    for hw in hws:
        idx = hw['id']
        pids = sorted(hw['pids'])
        score = calculate_score(pids, hw['deadline'])
        B = {k: [v[p] for p in pids] for k, v in score.items()}
        H = ['ID']+pids
        path = 'HW{0}.html'.format(idx)
        with open(path, 'w') as fp:
            print(table(idx, H, B), file=fp)

if __name__=='__main__':
    main()
