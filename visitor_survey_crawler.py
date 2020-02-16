import requests

""" example for suspicious_url_lsit.txt
www.google.co.jp
www.yahoo.co.jp
www.bing.co.jp
"""
url_list = r"here_your_suspicious_url_list.txt"
output = r"here_your_output_dir\%s.txt"

susp_keyword = [
    r'<META http-equiv="refresh"',
    r'window.location = '
]

req_header = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ja"
}

with open(url_list, "r") as f:
    url_list = [s.replace("\n", "") for s in f.readlines()]

for url in url_list:
    resp = requests.get("https://%s" % url, headers = req_header)

    # malicious scorering
    score = 0
    for keyword in susp_keyword:
        if resp.text.find(keyword) != -1:
            score += 1
    score = score / len(susp_keyword)
    if score >= 0.5:
        url = "[susp]" + url
    elif score >= 0.8:
        url = "[mal]" + url

    # output result
    with open(output % url, "a", encoding="utf-8") as f:
        f.write("=================================\n")
        for res_header in resp.headers.items():
            f.write("%s:%s\n" % res_header)
        f.write("=================================\n")
        f.write("%s" % resp.text)

