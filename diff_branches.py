import requests
import json
import ast
import csv
import argparse


def get_api(repo, branch, date, token, count):
    api = 'https://api.github.com/repos/{}/commits?sha={}&since={}&access_token={}&per_page=100&page={}'.format(repo, branch, date, token, count)
    return api


def save_output(commits):
    with open('output.csv', 'w') as output:
         writer = csv.writer(output)
         for value, key in commits.items():
              writer.writerow([key, value])


def get_data(commits_data, branch, token, date):
      repo_response = {}
      page_number = 0
      repo_number = 0
      repos = []
      with open("repos_list") as file:
          for line in file:
              line = line.strip()
              repos.append(line)
      while repo_number != len(repos):
          api = get_api(repos[repo_number], branch, date, token, page_number)
          print (api)
          page_number += 1
          print("repository: {} page: {}".format(repos[repo_number], page_number))
          r = requests.get(api)
          if(r.ok):
              repo_response = json.loads(r.text or r.content)
          if not repo_response:
              print("end of list.")
              repo_number += 1
              page_number = 0
          for y in repo_response:
              if y['commit']['message'] in commits_data:
                   commits_data[y['commit']['message']] += 1
              else:
                   commits_data[y['commit']['message']] = 1
          return commits_data


def main():
    commits_data = {}
    github_token = open("token", "r")
    github_token = github_token.read()
    parser = argparse.ArgumentParser()
    parser.add_argument("branch_master")
    parser.add_argument("branch_diff")
    parser.add_argument("date")
    args = parser.parse_args()
    branch_master = args.branch_master
    branch_diff = args.branch_diff
    date = args.date
    get_data(commits_data, branch_diff, github_token, date)
    get_data(commits_data, branch_master, github_token, date)
    save_output(commits_data)
if __name__ == '__main__':
    main()
