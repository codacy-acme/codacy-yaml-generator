#!/usr/bin/env python3
import argparse
import requests
import json

from os.path import exists


baseYamlFile = '''---
engines:
  '''


def checkIfRepoHasYamlFile(baseurl, provider, organization, repo, token):
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/organizations/%s/%s/repositories/%s/files?search=.codacy.y' % (
        baseurl, provider, organization, repo)
    r = requests.get(url, headers=headers)
    try:
        files = json.loads(r.text)
        for file in files['data']:
            if file['path'] == '.codacy.yaml' or file['path'] == '.codacy.yml':
                return True
        return False
    except:
        return None


def listRepositories(baseurl, provider, organization, token):
    result = []
    cursor = ''
    hasNextPage = True
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    while hasNextPage:
        url = '%s/api/v3/organizations/%s/%s/repositories?limit=10000%s' % (
            baseurl, provider, organization, cursor)
        r = requests.get(url, headers=headers)
        repos = json.loads(r.text)
        for repo in repos['data']:
            result.append({
                'provider': repo['provider'],
                'owner': repo['owner'],
                'name': repo['name'],
                'languages': repo['languages'],
                'remoteIdentifier': repo['remoteIdentifier'],
                'hasYamlFile': False
            })
        hasNextPage = 'cursor' in repos['pagination']
        if hasNextPage:
            cursor = '&cursor=%s' % repos['pagination']['cursor']
    return result


def addFileToRepoGLE(projectId, branch, fileContent, providerUrl, providerToken):
    headers = {
        'Content-Type': 'application/json',
        'PRIVATE-TOKEN': providerToken
    }

    payload = {
        'branch': branch,
        'commit_message': 'Add Codacy Configuration File',
        'actions': [
            {
                'action': 'create',
                'file_path': '.codacy.yaml',
                'content': fileContent
            }
        ]
    }
    url = '%s/api/v4/projects/%s/repository/commits' % (
        providerUrl, projectId)
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    print(f'\t{r.text}')


def main():
    parser = argparse.ArgumentParser(description='Codacy YAML file generator')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    parser.add_argument('--providerurl', dest='providerurl',
                        help='git provider server address')
    parser.add_argument('--providertoken', dest='providertoken', default=None,
                        help='the api-provider token to be used on the REST API', required=True)
    parser.add_argument('--branch', dest='branch', default='main',
                        help='Branch name where config file shall be written', required=True)
    args = parser.parse_args()
    print('Codacy YAML file generator')
    repos = listRepositories(args.baseurl, args.provider,
                             args.organization, args.token)
    for repo in repos:
        repo['hasYamlFile'] = checkIfRepoHasYamlFile(
            args.baseurl, args.provider, args.organization, repo['name'], args.token)
    for repo in repos:
        print(repo['name'])
        hasSpecificConfiguration = False
        if repo['hasYamlFile'] == False:
            yamlFile = baseYamlFile
            for language in repo['languages']:
                if exists(f'./data/{language}.yaml'):
                    hasSpecificConfiguration = True
                    with open(f'./data/{language}.yaml', 'r') as file:
                        data = file.read().replace('\n', '\n  ')
                        yamlFile += data
            if hasSpecificConfiguration:
                print('\tUploading Codacy Configuration File')
                addFileToRepoGLE(repo['remoteIdentifier'], 'master', yamlFile, args.providerurl, args.providertoken)
            else:
                print('\tNo known exclude paths found, Codacy Configuration File will not be added')
        else:
            print('\tAlready has a Codacy Configuration File')


main()
