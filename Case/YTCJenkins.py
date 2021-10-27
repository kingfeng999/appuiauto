# -*- coding:utf-8 -*-
import jenkins
import re, os, time
import yaml, time,io
import json, requests
from selenium import webdriver


def GetYaml():
    yamlPath = os.path.join(os.getcwd(), ".\JenkinsBranch.yaml")
    f = io.open(yamlPath, 'r', encoding='utf-8')
    d = yaml.load(f.read())
    return d


def linkJenkins():
    yamlData = GetYaml()
    jenkins_server_url = yamlData['Jenkins']['url']
    userName = yamlData['Jenkins']['username']
    password = yamlData['Jenkins']['password']

    server = jenkins.Jenkins(jenkins_server_url, username=userName, password=password)
    return server


def GetBranch():
    server = linkJenkins()
    jobsLen = len(server.get_jobs())
    branchList = []
    masterList = []
    for i in range(jobsLen):
        # print(server.get_jobs()[i]['name'])
        matchObj = re.findall(re.compile(r'<name>\*/(.*?)</name>'), server.get_job_config(server.get_jobs()[i]['name']))
        if matchObj is None:
            print("ServerName:" + server.get_jobs()[i]['name'] + u"  分支名称：" + "None")
            continue
        elif matchObj[0] != "master":
            branchList.append(u"服务名：" + server.get_jobs()[i]['name'] + "    " + u"分支名：" + matchObj[0])
            continue
        else:
            masterList.append(u"服务名：" + server.get_jobs()[i]['name'] + "    " + u"分支名：" + matchObj[0])
    return branchList, masterList


def CheckBranch():
    branchList = GetBranch()[0]
    masterList = GetBranch()[1]
    for i in range(len(branchList)):
        print(branchList[i])
    print("\n")
    for i in range(len(masterList)):
        print(masterList[i])


def SetBranch():
    yamlData = GetYaml()
    jenkins_server_url = yamlData['Jenkins']['url']
    userName = yamlData['Jenkins']['username']
    password = yamlData['Jenkins']['password']

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(jenkins_server_url)
    driver.find_element_by_id("j_username").send_keys(userName)
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_id("yui-gen1-button").click()

    server = linkJenkins()
    jobsLen = len(server.get_jobs())
    mustBuildJob = GetYaml()['Server']
    for i in range(jobsLen):
        jobName = server.get_jobs()[i]['name']
        for key in mustBuildJob:
            if jobName == key:
                driver.get(jenkins_server_url + "job/" + key + "/configure")
                branchKey = driver.find_element_by_xpath(
                    '//*[@id="main-panel"]/div/div/div/form/table/tbody/tr[52]/td[3]/div/div[1]/table/tbody/tr[1]/td[3]/input')
                if str(mustBuildJob[key]) not in branchKey.text:
                    branchKey.clear()
                    branchKey.send_keys("*/" + str(mustBuildJob[key]))
                    time.sleep(2)
                    driver.find_element_by_name("Submit").click()
                    server.build_job(jobName)


def SetMaster():
    yamlData = GetYaml()
    jenkins_server_url = yamlData['Jenkins']['url']
    userName = yamlData['Jenkins']['username']
    password = yamlData['Jenkins']['password']

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(jenkins_server_url)
    driver.find_element_by_id("j_username").send_keys(userName)
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_id("yui-gen1-button").click()

    server = linkJenkins()
    jobsLen = len(server.get_jobs())
    for i in range(jobsLen):
        driver.get(jenkins_server_url + "job/" + server.get_jobs()[i]['name'] + "/configure")
        branchKey = driver.find_element_by_xpath(
            '//*[@id="main-panel"]/div/div/div/form/table/tbody/tr[52]/td[3]/div/div[1]/table/tbody/tr[1]/td[3]/input')
        branch = branchKey.get_attribute('value').split('/')[1]
        if branch == 'master':
            continue
        # print(branch)
        branchKey.clear()
        branchKey.send_keys("*/master")
        time.sleep(1)
        driver.find_element_by_name("Submit").click()
        server.build_job(server.get_jobs()[i]['name'])


def GetBranchGit():
    server = linkJenkins()
    jobsLen = len(server.get_jobs())
    branchList = []
    for i in range(jobsLen):
        matchObj = re.findall(re.compile(r'<name>\*/(.*?)</name>'), server.get_job_config(server.get_jobs()[i]['name']))
        codeURL = re.findall(re.compile(r'<url>(.*?)</url>'), server.get_job_config(server.get_jobs()[i]['name']))
        branchList.append(codeURL[0] + ":" + matchObj[0])
        # print(codeURL[0])
        # print(server.get_jobs()[i]['name'],codeURL[0]+":"+matchObj[0])
    jsonData = {
        "key": "your_secret_key",
        "target": branchList
    }
    return jsonData


def Cobra():
    headers = {"Content-Type": "application/json"}
    r = requests.post("http://172.16.10.237:8888/api/add", data=json.dumps(GetBranchGit()), headers=headers)
    print(json.loads(r.text))
    responceData = json.loads(r.text)
    sid = responceData["result"]["sid"]
    return sid


def GetCobraStatus(sid):
    headers = {"Content-Type": "application/json"}
    jsonData = {
        "key": "your_secret_key",
        "sid": sid
    }
    r = requests.post("http://172.16.10.237:8888/api/status", data=json.dumps(jsonData), headers=headers)
    return r.text


if __name__ == "__main__":
    # CheckBranch()
    SetBranch()
    # SetMaster()
    # print(json.dumps(GetBranchGit()))
    # sid = Cobra()
    # print(sid)
    # while True:
    #     status = GetCobraStatus(sid)
    #     # print(status)
    #     cobraStatus = json.loads(status)["result"]["status"]
    #     if cobraStatus == "running":
    #         print(status)
    #         time.sleep(10)
    #     elif cobraStatus != "running":
    #         print(json.loads(status)["result"]["report"])
    #         break