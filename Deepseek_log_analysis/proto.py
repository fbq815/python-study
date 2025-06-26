import requests
import datetime
from bs4 import BeautifulSoup
from together import Together
from config import TOGETHER_API_KEY

client = Together(api_key=TOGETHER_API_KEY)

# def read_log(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         return f.read()

def find_debug_log_url(base_url):
    print(f"尝试从目录 {base_url} 查找 debug.log...")
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "debug.log" in href:
            if not href.startswith("http"):
                return base_url.rstrip("/") + "/" + href
            else:
                return href
    return None

def fetch_log_from_url(url):
    print(f"获取日志内容：{url}")
    resp = requests.get(url)
    resp.raise_for_status()  # 如果请求失败，会抛异常
    return resp.text

def analyze_log(log_text):
    timestamp = datetime.datetime.now().isoformat()
    prompt = f"""
请分析目录中的debug.log文件，提取并总结：
1. 错误类型：
2. 列出具体错误的case名,case名的具体拼接规则是：需要找到第二个"subtest="后面部分及".s390-virtio"前面部分,请去除括号后输出：
3. 根因分析：
4. 修复建议：

日志内容（唯一标识：{timestamp}）：
{log_text}
"""
    print("开始调用API")
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    print("API调用完成")
    return response.choices[0].message.content

# if __name__ == "__main__":
#     log_data = read_log("logs/example.log")
#     result = analyze_log(log_data)
#     print("=== 分析结果 ===\n")
#     print(result)

if __name__ == "__main__":
    base_url = "http://10.0.136.47/bfu/s390x/functional/RHEL9.7/CTC1-1/test-results"
    debug_log_url = find_debug_log_url(base_url)
    if debug_log_url:
        log_text = fetch_log_from_url(debug_log_url)
        result = analyze_log(log_text)
        print("=== 分析结果 ===\n")
        print(result)
    else:
        print("未找到 debug.log 文件。")