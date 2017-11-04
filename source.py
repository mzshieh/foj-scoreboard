import sys, datetime, requests, json, argparse, time, os
from foj import FOJ
from gen import table

parser = argparse.ArgumentParser(description='Get Homework Source')
parser.add_argument('-g','--group',type=int,default=7,
                    help='Group ID')
parser.add_argument('-t','--token',type=str,default='',
                    help='Cookies')
parser.add_argument('-a','--api',type=str,default='https://api.oj.nctu.me/',
                    help='Formosa OJ API base URL (default: %(default)s)')
parser.add_argument('-p','--problems',type=eval,default=[],
                    help='Problem list (use python format)')
parser.add_argument('-s','--students',type=str,default='student.txt',
                    help='Student list (default: %(default)s)')
parser.add_argument('-d','--deadline',default='2099-01-01 00:00:00',
                    help='Deadline (default: %(default)s)')
parser.add_argument('-m','--meta',default=None,
                    help='JSON meta file (Optional)')

args = parser.parse_args()
if args.meta!=None:
    with open(args.meta) as FILE:
        meta = json.load(FILE)
else:
    meta = {}

if meta.get('api'):
    args.api = meta.get('api')
if meta.get('token'):
    args.token = meta.get('token')
if meta.get('students'):
    args.students = meta.get('students')
if meta.get('homeworks'):
    homeworks = meta.get('homeworks')
else:
    homeworks = [{'id':'', 
                  'gid':args.group,
                  'pids': args.problems,
                  'deadline': args.deadline}]

def get_students(filename):
    with open(filename, 'r') as fp:
        users=[name for name in fp.read().split() if name[0]!='#']
    return sorted(users)

def get_source(gid,pids=[], deadline='2099-10-01 00:00:00'):
    oj = FOJ(args.api,gid,args.token)
    time_format = '%Y-%m-%d %H:%M:%S'
    deadline = datetime.datetime.strptime(deadline, time_format)
    users = oj.get_users(reverse=True)
    students = get_students(args.students)
    for sub in oj.get_submissions():
        sid = sub['id']
        uid = users.get(sub['user_id'], '')
        pid = sub['problem_id']
        subtime = datetime.datetime.strptime(sub['created_at'], time_format)
        if uid in students and pid in pids and subtime<deadline and sub['score']!=None:
            print('Processing {}\'s submission {}'.format(uid,sid))
            filename = oj.get_filename(sid)
            directory = '{}/{}'.format(pid,uid)
            os.makedirs(directory,exist_ok=True)
            source_code = oj.get_source(sid)
            with open('{}/{}-{}'.format(directory,sid,filename),'w') as FILE:
                print(source_code,end='',file=FILE)

def main():
    for hw in homeworks:
        idx = hw['id']
        pids = sorted(hw['pids'])
        get_source(hw['gid'], pids, hw['deadline'])

if __name__=='__main__':
    main()
