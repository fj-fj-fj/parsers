from typing import Any

import requests


def _main(user_pr):
    pr_items: list = user_pr['items']
    if pr_items is None:
        return []

    pulls_info = fetch_pull_requests_info(pr_items)
    for pr_item, pr_info in zip(pr_items, pulls_info):
        pr_item['merged'] = pr_info['merged']
        pr_item['html_url'] = pr_info['html_url']

    projects = []
    names = set()
    repos = fetch_pull_requests_repos(pr_items)

    for pr_item, repo in zip(pr_items, repos):
        repo_url: str = pr_item['repository_url']
        repo: dict = requests.get(repo_url).json()

        if (name := repo.get('name')) not in names:
            names.add(name)
            projects.append({
                'name': name,
                'html_url': repo.get('html_url'),
                'stars': repo.get('stargazers_count'),
                'pulls': [pr_item]
            })
        elif name in names:
            for project in projects:
                if project['name'] == name:
                    project['pulls'].append(pr_item)

    merged_unmerged: dict = sort_merged_unmerged(projects)
    return merged_unmerged


def fetch_pull_requests_info(pulls):
    return [
        requests.get(pulls[idx]['pull_request']['url']).json()
        for idx in range(len(pulls))
    ]


def fetch_pull_requests_repos(pulls):
    return [
        requests.get(pulls[idx]['repository_url']).json()
        for idx in range(len(pulls))
    ]


def sort_merged_unmerged(projects):
    merged, unmerged = [], []
    for project in projects:
        for pull in project['pulls']:
            merged.append(project) if pull['merged'] else unmerged.append(project)
    return {'merged': merged, 'unmerged': unmerged}


def main(author_pr_json: Any):
    """Handle samples. (API)"""
    return _main(author_pr_json)


if __name__ == '__main__':
    import json
    from pprint import pprint as pp
    with open('./data/merge_checker/repl_1_response.html') as fh:
        user_pr = json.loads(fh.read())
    result = main(user_pr)
