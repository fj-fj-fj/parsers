# Flow

## Find data extraction algorithm using Repl
```bash
(3.11.0) $ make irun merge_checker
```

```python
>>> parser.request()
 'https://api.github.com/search/issues?q=type:pr+is:public+author:{ ? }&per_page=300&authorization_request=...'
        fill placehoder: fj-fj-fj
<Response [200]>
>>>
>>> jdata = _.json()
>>> pr = jdata['items']
>>> assert pr
>>> len(pr)
2
>>> for i in range(2): pr[i]['pull_request']['url']
...
https://api.github.com/repos/ShubhamRathi/detectron2/pulls/1
https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/pulls/3242
>>>
>>> rh = parser.handler._request_handler
>>>
>>> for i in range(2): rh._make_request(pr[i]['pull_request']['url'])
...
<Response [200]>
<Response [200]>
>>> rh._previous_responses
[<Response [200]>, <Response [200]>]
>>>
>>> rh.server_response.url
'https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/pulls/3242'
>>> for r in rh._previous_responses: r.url
...
'https://api.github.com/search/issues?q=type:pr+is:public+author:fj-fj-fj&per_page=300&authorization_request=...'
'https://api.github.com/repos/ShubhamRathi/detectron2/pulls/1'
>>>
>>> pr1 = rh._previous_responses[-1].json()
>>> pr1['merged'], pr1['html_url']
(False, 'https://github.com/ShubhamRathi/detectron2/pull/1')
>>> shortcuts()
>>> nb.pull_request_1 = _
>>>
>>> pr2 = rh.server_response.json()
>>> pr2['merged'], pr2['html_url']
(True, 'https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242')
>>> nb.pull_request_2 = _
>>>
>>> repo_1, repo_2 = pr
>>> *repo_urls, = (_['repository_url'] for _ in (repo_1, repo_2))
>>> repo_urls
['https://api.github.com/repos/ShubhamRathi/detectron2', 'https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io']
>>> nb.pull_request_urls = _
>>>
>>> for repo_url in _: rh._make_request(repo_url)
...
<Response [200]>
<Response [200]>
>>>
>>> project_1 = rh._previous_responses[-1].json()
>>> project_2 = rh.server_response.json()
>>> projects = []
>>>
>>> projects.append({
... 'name': project_1['name'],
... 'html_url': project_1['html_url'],
... 'stars': project_1['stargazers_count'],
... 'pulls': pr[0]})
>>>
>>> projects.append({
... 'name': project_2['name'],
... 'html_url': project_2['html_url'],
... 'stars': project_2['stargazers_count'],
... 'pulls': pr[1]})
>>>
>>> nb.projects = projects
>>>
>>> parser.save()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/mnt/c/dev/fj-fj-fj/parsers/parsers/handlers.py", line 346, in save
    self._ = Parser.save._ = self.handler.save()
                             ^^^^^^^^^^^^^^^^^^^
  File "/mnt/c/dev/fj-fj-fj/parsers/parsers/handlers.py", line 249, in save
    .save(data=self.current_data, step=self._data_handler.step)
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/c/dev/fj-fj-fj/parsers/parsers/storage/files.py", line 119, in save
    return plain_storage_fh.write(data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: write() argument must be str, not list
>>> parser.handler._data_handler.is_json
False
>>> parser.parse()
HandledData(data=<class 'dict'>, fail=False, status_code=0)
>>> parser.handler._data_handler.is_json
True
>>> parser.save()
6254
>>> # FIXME: skip parser.parse() if data is json
>>> # ==========================================
>>>
>>> import pprint
>>> pprint.pprint(projects)
```
```json
[{"html_url": "https://github.com/ShubhamRathi/detectron2",
  "name": "detectron2",
  "pulls": {"active_lock_reason": None,
            "assignee": None,
            "assignees": [],
            "author_association": "NONE",
            "body": "",
            "closed_at": "2021-04-19T19:43:52Z",
            "comments": 0,
            "comments_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/comments",
            "created_at": "2021-04-19T19:38:36Z",
            "draft": False,
            "events_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/events",
            "html_url": "https://github.com/ShubhamRathi/detectron2/pull/1",
            "id": 861776310,
            "labels": [],
            "labels_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/labels{/name}",
            "locked": False,
            "milestone": None,
            "node_id": "MDExOlB1bGxSZXF1ZXN0NjE4NDA0ODk3",
            "number": 1,
            "performed_via_github_app": None,
            "pull_request": {"diff_url": "https://github.com/ShubhamRathi/detectron2/pull/1.diff",
                             "html_url": "https://github.com/ShubhamRathi/detectron2/pull/1",
                             "merged_at": None,
                             "patch_url": "https://github.com/ShubhamRathi/detectron2/pull/1.patch",
                             "url": "https://api.github.com/repos/ShubhamRathi/detectron2/pulls/1"},
            "reactions": {"+1": 0,
                          "-1": 0,
                          "confused": 0,
                          "eyes": 0,
                          "heart": 0,
                          "hooray": 0,
                          "laugh": 0,
                          "rocket": 0,
                          "total_count": 0,
                          "url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/reactions"},
            "repository_url": "https://api.github.com/repos/ShubhamRathi/detectron2",
            "score": 1.0,
            "state": "closed",
            "state_reason": None,
            "timeline_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/timeline",
            "title": "Update INSTALL.md",
            "updated_at": "2021-04-19T19:47:26Z",
            "url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1",
            "user": {"avatar_url": "https://avatars.githubusercontent.com/u/61021761?v=4",
                     "events_url": "https://api.github.com/users/fj-fj-fj/events{/privacy}",
                     "followers_url": "https://api.github.com/users/fj-fj-fj/followers",
                     "following_url": "https://api.github.com/users/fj-fj-fj/following{/other_user}",
                     "gists_url": "https://api.github.com/users/fj-fj-fj/gists{/gist_id}",
                     "gravatar_id": "",
                     "html_url": "https://github.com/fj-fj-fj",
                     "id": 61021761,
                     "login": "fj-fj-fj",
                     "node_id": "MDQ6VXNlcjYxMDIxNzYx",
                     "organizations_url": "https://api.github.com/users/fj-fj-fj/orgs",
                     "received_events_url": "https://api.github.com/users/fj-fj-fj/received_events",
                     "repos_url": "https://api.github.com/users/fj-fj-fj/repos",
                     "site_admin": False,
                     "starred_url": "https://api.github.com/users/fj-fj-fj/starred{/owner}{/repo}",
                     "subscriptions_url": "https://api.github.com/users/fj-fj-fj/subscriptions",
                     "type": "User",
                     "url": "https://api.github.com/users/fj-fj-fj"}},
  "stars": 0},
 {"html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io",
  "name": "rms-support-letter.github.io",
  "pulls": {"active_lock_reason": None,
            "assignee": None,
            "assignees": [],
            "author_association": "CONTRIBUTOR",
            "body": "<!--\r\n"
                    "### Don't edit index.md directly!\r\n"
                    "\r\n"
                    "### To sign, create a file in `_data/signed/` named "
                    "`<username>.yaml` with the following content:\r\n"
                    "\r\n"
                    "```yaml\r\n"
                    "name: <your name here>\r\n"
                    "link: <link to your profile or site>\r\n"
                    "```\r\n"
                    "\r\n"
                    "### Example\r\n"
                    "\r\n"
                    "```yaml\r\n"
                    "name: Richard Matthew Stallman\r\n"
                    "link: https://stallman.org/\r\n"
                    "```\r\n"
                    "\r\n"
                    "Optional stuff you should consider:\r\n"
                    "- Use your real name if possible\r\n"
                    "- Add affiliated organizations or projects if applicable "
                    "(e.g. `John Smith (Free Software Foundation, Popular "
                    "Window Manager Author)`\r\n"
                    "-->\r\n",
            "closed_at": "2021-03-27T07:29:19Z",
            "comments": 0,
            "comments_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/comments",
            "created_at": "2021-03-27T00:38:01Z",
            "draft": False,
            "events_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/events",
            "html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242",
            "id": 842375202,
            "labels": [],
            "labels_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/labels{/name}",
            "locked": True,
            "milestone": None,
            "node_id": "MDExOlB1bGxSZXF1ZXN0NjAxOTY5Mjgy",
            "number": 3242,
            "performed_via_github_app": None,
            "pull_request": {"diff_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242.diff",
                             "html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242",
                             "merged_at": "2021-03-27T07:29:19Z",
                             "patch_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242.patch",
                             "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/pulls/3242"},
            "reactions": {"+1": 0,
                          "-1": 0,
                          "confused": 0,
                          "eyes": 0,
                          "heart": 0,
                          "hooray": 0,
                          "laugh": 0,
                          "rocket": 0,
                          "total_count": 0,
                          "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/reactions"},
            "repository_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io",
            "score": 1.0,
            "state": "closed",
            "state_reason": None,
            "timeline_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/timeline",
            "title": "Create fj-fj-fj.yml",
            "updated_at": "2021-03-27T07:29:19Z",
            "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242",
            "user": {"avatar_url": "https://avatars.githubusercontent.com/u/61021761?v=4",
                     "events_url": "https://api.github.com/users/fj-fj-fj/events{/privacy}",
                     "followers_url": "https://api.github.com/users/fj-fj-fj/followers",
                     "following_url": "https://api.github.com/users/fj-fj-fj/following{/other_user}",
                     "gists_url": "https://api.github.com/users/fj-fj-fj/gists{/gist_id}",
                     "gravatar_id": "",
                     "html_url": "https://github.com/fj-fj-fj",
                     "id": 61021761,
                     "login": "fj-fj-fj",
                     "node_id": "MDQ6VXNlcjYxMDIxNzYx",
                     "organizations_url": "https://api.github.com/users/fj-fj-fj/orgs",
                     "received_events_url": "https://api.github.com/users/fj-fj-fj/received_events",
                     "repos_url": "https://api.github.com/users/fj-fj-fj/repos",
                     "site_admin": False,
                     "starred_url": "https://api.github.com/users/fj-fj-fj/starred{/owner}{/repo}",
                     "subscriptions_url": "https://api.github.com/users/fj-fj-fj/subscriptions",
                     "type": "User",
                     "url": "https://api.github.com/users/fj-fj-fj"}},
  "stars": 2389}]
>>>
```

## Write logic to merge_checker/logic.py and make auto
```bash
(3.11.0) $ make run merge_checker
```

## Final data
```json
{"merged": [{"html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io",
             "name": "rms-support-letter.github.io",
             "pulls": [{"active_lock_reason": None,
                        "assignee": None,
                        "assignees": [],
                        "author_association": "CONTRIBUTOR",
                        "body": "<!--\r\n"
                                "### Don't edit index.md directly!\r\n"
                                "\r\n"
                                "### To sign, create a file in `_data/signed/` "
                                "named `<username>.yaml` with the following "
                                "content:\r\n"
                                "\r\n"
                                "```yaml\r\n"
                                "name: <your name here>\r\n"
                                "link: <link to your profile or site>\r\n"
                                "```\r\n"
                                "\r\n"
                                "### Example\r\n"
                                "\r\n"
                                "```yaml\r\n"
                                "name: Richard Matthew Stallman\r\n"
                                "link: https://stallman.org/\r\n"
                                "```\r\n"
                                "\r\n"
                                "Optional stuff you should consider:\r\n"
                                "- Use your real name if possible\r\n"
                                "- Add affiliated organizations or projects if "
                                "applicable (e.g. `John Smith (Free Software "
                                "Foundation, Popular Window Manager "
                                "Author)`\r\n"
                                "-->\r\n",
                        "closed_at": "2021-03-27T07:29:19Z",
                        "comments": 0,
                        "comments_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/comments",
                        "created_at": "2021-03-27T00:38:01Z",
                        "draft": False,
                        "events_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/events",
                        "html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242",
                        "id": 842375202,
                        "labels": [],
                        "labels_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/labels{/name}",
                        "locked": True,
                        "merged": True,
                        "milestone": None,
                        "node_id": "MDExOlB1bGxSZXF1ZXN0NjAxOTY5Mjgy",
                        "number": 3242,
                        "performed_via_github_app": None,
                        "pull_request": {"diff_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242.diff",
                                         "html_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242",
                                         "merged_at": "2021-03-27T07:29:19Z",
                                         "patch_url": "https://github.com/rms-support-letter/rms-support-letter.github.io/pull/3242.patch",
                                         "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/pulls/3242"},
                        "reactions": {"+1": 0,
                                      "-1": 0,
                                      "confused": 0,
                                      "eyes": 0,
                                      "heart": 0,
                                      "hooray": 0,
                                      "laugh": 0,
                                      "rocket": 0,
                                      "total_count": 0,
                                      "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/reactions"},
                        "repository_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io",
                        "score": 1.0,
                        "state": "closed",
                        "state_reason": None,
                        "timeline_url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242/timeline",
                        "title": "Create fj-fj-fj.yml",
                        "updated_at": "2021-03-27T07:29:19Z",
                        "url": "https://api.github.com/repos/rms-support-letter/rms-support-letter.github.io/issues/3242",
                        "user": {"avatar_url": "https://avatars.githubusercontent.com/u/61021761?v=4",
                                 "events_url": "https://api.github.com/users/fj-fj-fj/events{/privacy}",
                                 "followers_url": "https://api.github.com/users/fj-fj-fj/followers",
                                 "following_url": "https://api.github.com/users/fj-fj-fj/following{/other_user}",
                                 "gists_url": "https://api.github.com/users/fj-fj-fj/gists{/gist_id}",
                                 "gravatar_id": "",
                                 "html_url": "https://github.com/fj-fj-fj",
                                 "id": 61021761,
                                 "login": "fj-fj-fj",
                                 "node_id": "MDQ6VXNlcjYxMDIxNzYx",
                                 "organizations_url": "https://api.github.com/users/fj-fj-fj/orgs",
                                 "received_events_url": "https://api.github.com/users/fj-fj-fj/received_events",
                                 "repos_url": "https://api.github.com/users/fj-fj-fj/repos",
                                 "site_admin": False,
                                 "starred_url": "https://api.github.com/users/fj-fj-fj/starred{/owner}{/repo}",
                                 "subscriptions_url": "https://api.github.com/users/fj-fj-fj/subscriptions",
                                 "type": "User",
                                 "url": "https://api.github.com/users/fj-fj-fj"}}],             "stars": 2389}],
 "unmerged": [{"html_url": "https://github.com/ShubhamRathi/detectron2",
               "name": "detectron2",
               "pulls": [{"active_lock_reason": None,
                          "assignee": None,
                          "assignees": [],
                          "author_association": "NONE",
                          "body": "",
                          "closed_at": "2021-04-19T19:43:52Z",
                          "comments": 0,
                          "comments_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/comments",
                          "created_at": "2021-04-19T19:38:36Z",
                          "draft": False,
                          "events_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/events",
                          "html_url": "https://github.com/ShubhamRathi/detectron2/pull/1",
                          "id": 861776310,
                          "labels": [],
                          "labels_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/labels{/name}",
                          "locked": False,
                          "merged": False,
                          "milestone": None,
                          "node_id": "MDExOlB1bGxSZXF1ZXN0NjE4NDA0ODk3",
                          "number": 1,
                          "performed_via_github_app": None,
                          "pull_request": {"diff_url": "https://github.com/ShubhamRathi/detectron2/pull/1.diff",
                                           "html_url": "https://github.com/ShubhamRathi/detectron2/pull/1",
                                           "merged_at": None,
                                           "patch_url": "https://github.com/ShubhamRathi/detectron2/pull/1.patch",
                                           "url": "https://api.github.com/repos/ShubhamRathi/detectron2/pulls/1"},
                          "reactions": {"+1": 0,
                                        "-1": 0,
                                        "confused": 0,
                                        "eyes": 0,
                                        "heart": 0,
                                        "hooray": 0,
                                        "laugh": 0,
                                        "rocket": 0,
                                        "total_count": 0,
                                        "url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/reactions"},
                          "repository_url": "https://api.github.com/repos/ShubhamRathi/detectron2",
                          "score": 1.0,
                          "state": "closed",
                          "state_reason": None,
                          "timeline_url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1/timeline",
                          "title": "Update INSTALL.md",
                          "updated_at": "2021-04-19T19:47:26Z",
                          "url": "https://api.github.com/repos/ShubhamRathi/detectron2/issues/1",
                          "user": {"avatar_url": "https://avatars.githubusercontent.com/u/61021761?v=4",
                                   "events_url": "https://api.github.com/users/fj-fj-fj/events{/privacy}",
                                   "followers_url": "https://api.github.com/users/fj-fj-fj/followers",
                                   "following_url": "https://api.github.com/users/fj-fj-fj/following{/other_user}",
                                   "gists_url": "https://api.github.com/users/fj-fj-fj/gists{/gist_id}",
                                   "gravatar_id": "",
                                   "html_url": "https://github.com/fj-fj-fj",
                                   "id": 61021761,
                                   "login": "fj-fj-fj",
                                   "node_id": "MDQ6VXNlcjYxMDIxNzYx",
                                   "organizations_url": "https://api.github.com/users/fj-fj-fj/orgs",
                                   "received_events_url": "https://api.github.com/users/fj-fj-fj/received_events",
                                   "repos_url": "https://api.github.com/users/fj-fj-fj/repos",
                                   "site_admin": False,
                                   "starred_url": "https://api.github.com/users/fj-fj-fj/starred{/owner}{/repo}",
                                   "subscriptions_url": "https://api.github.com/users/fj-fj-fj/subscriptions",
                                   "type": "User",
                                   "url": "https://api.github.com/users/fj-fj-fj"}}],
               "stars": 0}]}
```
