# Codacy YAML File Generator

A tool that checks if a repo has a Codacy Configuration file and, if not, generates and uploads a one.

⚠️ Currently only working for GitLab Enteprise ⚠️

## Pre-conditions

The `requirements.txt` lists all Python libraries that should be installed before running the script:

```bash
pip install -r requirements.txt
```

You should create a yaml file, inside data folder, with the paths you want to exclude in each tool.  
e.g..   

```
.  
+-- _config.yml  
+-- data  
|   +-- Java.yaml  
|   +-- Markdown.yaml  
```

Inside each file, the content should look like:
./data/Java.yaml
```yaml
spotbugs:
  exclude_paths:
    - "**/tests"
```

./data/Markdown.yaml
```yaml
markdownlint:
  exclude_paths:
    - "**/temp/*.md"
```

## Usage

python3 main.py [-h] --token TOKEN --provider PROVIDER --organization ORGANIZATION [--baseurl BASEURL] [--providerurl PROVIDERURL] --providertoken PROVIDERTOKEN
               --branch BRANCH


optional arguments:  
  -h, --help            show this help message and exit  
  --token TOKEN         the api-token to be used on the REST API  
  --provider PROVIDER   git provider  
  --organization ORGANIZATION                     organization id  
  --baseurl BASEURL     codacy server address (ignore if cloud)  
  --providerurl PROVIDERURL git provider server address  
  --providertoken PROVIDERTOKEN the api-provider token to be used on the REST API  
  --branch BRANCH       Branch name wh ere config file shall be written  
