import requests


def gql(query, vars, token):
    data = {"query": query, "variables": vars}
    request = requests.post(
        "https://api.github.com/graphql", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    if request.status_code == 200:
        data = request.json()
        if len(data.get("errors", [])) > 0:
            raise Exception(f"Query errored:\n{data}")
        return data
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, query
            )
        )


def users(github_token: str, org: str):
    query = """
    query($cursor: String, $org: String!) {
      organization(login: $org) {
        membersWithRole(first: 100, after: $cursor) {
          nodes {
            id
            name
            login
            company
            location
            websiteUrl
            status {
              emoji
              message
            }
          }
          pageInfo {
            endCursor
            startCursor
            hasNextPage
          }
        }
      }
    }
    """

    cursor = None
    users = {}

    print("getting github users...")
    while True:
        result = gql(query, vars={"org": org, "cursor": cursor}, token=github_token)

        for user in result["data"]["organization"]["membersWithRole"]["nodes"]:
            # TODO: Should create a class for user
            u = user
            u["github_id"] = user["id"]
            u["id"] = None
            u["website_url"] = user["websiteUrl"]
            if user["status"]:
                u["status_message"] = user["status"]["message"]
                u["status_emoji"] = user["status"]["emoji"]
            else:
                u["status_message"] = None
                u["status_emoji"] = None

            users[u["github_id"]] = u

        pageInfo = result["data"]["organization"]["membersWithRole"]["pageInfo"]
        print(len(users))
        if not pageInfo["hasNextPage"]:
            break
        cursor = pageInfo["endCursor"]

    return users
