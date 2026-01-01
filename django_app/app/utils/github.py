import requests
import base64
from urllib.parse import urlparse
import uuid
from app.utils.ai_agent import analyze_code_with_llm
import logging
logger = logging.getLogger(__name__)

def get_owner_and_repo(url):
    passed_url = urlparse(url)
    path_parts = passed_url.path.strip("/").split("/")
    if len(path_parts) >= 2:
        owner, repo = path_parts[0], path_parts[1]
        return owner, repo
    return None, None

#print(get_owner_and_repo("https://github.com/YogeshBodke21/Python"))

#token = config("GITHUB_TOKEN")


def fetch_pr_files(repositry_url, pr_number, github_token):
    print("--->fetch_pr_files")
    owner, repo = get_owner_and_repo(repositry_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization" : f"token {github_token}"}
    response = requests.get(url, headers=headers)
    print("---", owner, repo )
    response.raise_for_status()
    contents = {}
    print("---response in json", response.json())
    for file in response.json():
        raw_url = file["raw_url"]
        filename = file["filename"]

        raw_resp = requests.get(raw_url, headers=headers)
        raw_resp.raise_for_status()
        print("raw_resp", raw_resp)
        contents[filename] = raw_resp.text
    print("contents---", contents)
    return contents
    #return response.json()


#print(fetch_pr_files("https://github.com/YogeshBodke21/Python", 1, token))

def fetch_pr_file_content(repositry_url, file_path, github_token):
    print("--->Inside fetch_pr_file_content")
    owner, repo = get_owner_and_repo(repositry_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization" : f"token {github_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content =  response.json()
    return base64.b64decode(content['content'].decode())

#print(fetch_pr_file_content("https://github.com/YogeshBodke21/Python", "new_file", token))


def analyze_llm_response(repo_url, pr_number, github_token):
    print("----Inside analyze_llm_response")
    Task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)
        combine_result = []
        print("----Inside pr_files", pr_files)
        for file_name, content in pr_files.items():
            print("Processing file:", file_name)
            # no need to fetch content again, it's already in `content`
            # print("----Inside file", file)
            # file_name = file['filename']
            #whole_content = fetch_pr_file_content(repo_url, file_name, github_token)
            llm_result = analyze_code_with_llm(content, file_name)
            # print(content, file_name)
            #llm_result = analyze_code_with_llm(whole_content, file_name)
            combine_result.append({"file_name":file_name, "Results":llm_result})

        return {"Task_id" : Task_id, "results": combine_result}
    except Exception as e:
        print(e)
        return {"Task_id" : Task_id, "results":[]}
        
#print(analyze_llm_response("https://github.com/YogeshBodke21/Python", "1", config("GITHUB_TOKEN")))
