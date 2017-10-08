import sys
import datetime
import requests
import json

class FOJ:
    def __init__(self,api_base,group_id,token):
        self.api = api_base
        self.gid = group_id
        self.cookies = {'token':token}

    def get_users(self,reverse=False):
        url=self.api+'groups/{}/users/'.format(self.gid)
        res = requests.get(url,cookies=self.cookies).text
        if reverse:
            return {user['id']:user['name'] for user in json.loads(res)['msg']}
        return {user['name']:user['id'] for user in json.loads(res)['msg']}

    def get_submissions(self,uid=0, pid=0, count=1048576):
        url = self.api+'submissions/?group_id={}&&page=1'.format(self.gid)
        if uid>0: url += '&user_id={}'.format(uid)
        if pid>0: url += '&problem_id={}'.format(pid)
        url += '&count={}'.format(count)
        res = requests.get(url,cookies=self.cookies).text
        return json.loads(res)['msg']['submissions']
