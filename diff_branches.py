import requests
import json
import ast
import unicodecsv as csv
import argparse

# def get_data():
#     api = 'https://api.github.com/repos/{}/commits?sha={}&access_token={}&per_page=100&page={}'.format(repos[z], branch, github_token, str(x))
# return api

def main():
    contr = {}
    github_token = open("token", "r")
    github_token = github_token.read()
    parser = argparse.ArgumentParser()
    parser.add_argument("branch_master")
    parser.add_argument("branch_diff")
    args = parser.parse_args()
    branch_master = args.branch_master
    branch_diff = args.branch_diff

    repo_response = {}
    print (branch_diff)
    print (branch_master)
    x = 0
    z = 0
    repos = []
    with open("repos_list") as file:
        for line in file: 
            line = line.strip()
            repos.append(line)
    while z != len(repos):
         api()
         api = 'https://api.github.com/repos/{}/commits?sha=R5.0&access_token={}&per_page=100&page={}'.format(repos[z], github_token, str(x))
         x += 1
         print(api)
         print "repository: {} page: {}".format(repos[z], x)
         r = requests.get(api)
         if(r.ok):
              repo_response = json.loads(r.text or r.content)
         if not repo_response:
              print "end of list."
              z += 1
              x = 0
         for y in repo_response:
              # print repo_response[y]
              if y['commit']['message'] in contr:
                   contr[y['commit']['message']] += 1
              else:
                   contr[y['commit']['message']] = 1
         with open('output.csv', 'wb') as output:
              writer = csv.writer(output, encoding='utf-8')
              for key, value in contr.iteritems():
                   writer.writerow([key, value])

if __name__ == '__main__':
    main()