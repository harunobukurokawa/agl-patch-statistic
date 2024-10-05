#!/usr/bin/python3

import sys
import os
import subprocess
import pandas

def get_commit_count(repo_dir, year):
	func_result = []

	if os.path.isdir(repo_dir + "/.git"):
		cur_dir = os.getcwd()
		os.chdir(repo_dir)

		from_date = year + "-01-01"
		to_date = year + "-12-31"

		cmd = "git shortlog -se --since=" + from_date + " --until=" + to_date
		git_command = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
		stdout_result = git_command.stdout.decode("utf8")
		stdout_result = stdout_result.strip('\n')
		results = stdout_result.split('\n')
		for result in results:
			str_result = str(result)
			str_result = str_result.strip(' ')
			split_result = str_result.split('\t')

			if len(split_result) > 1:
				cmd = "git log  --author=\"" + split_result[1] + "\" --numstat --pretty=\"%H\" --no-merges  | awk \'NF==3 {plus+=$1; minus+=$2} END {printf(\"%d\\n\", plus+minus)}\'"
				git_command = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
				stdout_result = git_command.stdout.decode("utf8")
				auther_list = []
				auther_list.append(split_result[1])
				auther_list.append(split_result[0])
				auther_list.append(stdout_result.strip())
				func_result.append(auther_list)

		os.chdir(cur_dir)

	return func_result

def counting_commiter(commiters_raw, year):
	df = pandas.DataFrame(commiters_raw , columns=['Auther', 'commits', 'line'])
	df['commits'] = df['commits'].astype(int)
	df['line'] = df['line'].astype(int)
	commits = df.groupby('Auther')['commits'].sum()
	lines = df.groupby('Auther')['line'].sum()
	commits = commits.sort_values(ascending=False)
	lines = lines.sort_values(ascending=False)

	cur_dir = os.getcwd()
	commits.to_csv(cur_dir + "/commits-" + year + ".csv", header=False)
	lines.to_csv(cur_dir + "/lines-" + year + ".csv", header=False)

	return commiters_raw

def main():
	args = sys.argv
	
	if 1 >= len(args):
		print('no args.')
		exit()

	year = sys.argv[1]

	commiters = []
	commiters_raw = []

	cur_dir = os.getcwd()
	repo_cat_dirs = os.listdir(cur_dir)
	for repo_cat_dir in repo_cat_dirs:
		if not repo_cat_dir.startswith('.') and os.path.isdir(repo_cat_dir):
			repos = os.listdir(repo_cat_dir)
			for repo in repos:
				if not repo.startswith('.'):
					target_dir = cur_dir + "/" + repo_cat_dir + "/" + repo
					commt_lists = get_commit_count(target_dir, year)
					for commt_list in commt_lists:
					#if len(commt_lists) > 0:
						commiters_raw.append(commt_list)

	counting_commiter(commiters_raw, year)

if __name__ == "__main__":
	main()
