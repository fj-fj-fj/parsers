# Merge-Checker

## Introduction
 See which projects the GitHub user made pull-requests to that were merged.

- On the main page, enter the username on the GitHub and click `Send`
- As a result, a page with a list of projects to which the user made a pull-request to that was merged. For each project you can see:
  - the name of the project
  - link to the project on GitHub
  - number of stars on GitHub
  - links to merged pull-requests from the user
  - links to non-merciless pull-requests from the user
  - each pull-request displays the number of comments in this pull-request
 
The parser is used by Githab API.

#
Since for unauthenticated requests, rate limiting allows up to [60 requests per hour](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting "Rate limiting") , it is advisable to add an authorization token to `constants.AUTORIZATION_PARAM`.
