import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from together import Together
from config import TOGETHER_API_KEY
import datetime

client = Together(api_key=TOGETHER_API_KEY)

def find_subdirectories(base_url):
    print(f"访问目录: {base_url}")
    resp = requests.get(base_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    subdirs = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith("/") and href != "../":
            full_url = urljoin(base_url + "/", href)
            subdirs.append(full_url)
    return subdirs

def fetch_log_from_url(url):
    print(f"获取日志内容：{url}")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def analyze_log(log_text):
    timestamp = datetime.datetime.now().isoformat()
    prompt = f"""
请先明确case名称的寻找规则：
case名称的具体拼接规则是：需要找到debug.log文件中的第二个"subtest="后面部分及".s390-virtio"前面部分,请去除括号后输出
请帮我判断以下测试日志是否包含错误，并进行如下分析：
1. 是否存在错误（请明确回答“是”或“否”）：
2. 如果存在错误，请列出case名称；
3. 如果无错误，请只输出一行带有case号和case名称及PASS的内容。
4. 不要输出太多无效内容，无论正确还是错误将结论合并为一句话
5. 最后把所有存在错误的case名以逗号为间隔排列,例如: 错误case名称1,错误case名称2

日志内容（唯一标识：{timestamp}）：
{log_text}
"""
    print("开始调用API分析日志...")
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    print("API调用完成")
    return response.choices[0].message.content

if __name__ == "__main__":
    base_url = "http://10.0.136.47/bfu/s390x/functional/RHEL9.7/CTC1-1/test-results"
    subdirs = find_subdirectories(base_url)
    print(f"找到 {len(subdirs)} 个一级子目录。")

    for subdir_url in subdirs:
        debug_log_url = urljoin(subdir_url, "debug.log")
        try:
            log_text = fetch_log_from_url(debug_log_url)
        except requests.HTTPError:
            print(f"{debug_log_url} 不存在或无法访问，跳过。")
            continue

        analysis_result = analyze_log(log_text)
        # 判断LLM回答中是否包含“是”来判断是否有错误（可根据实际回答微调）
        if "是" in analysis_result or "错误" in analysis_result or "fail" in analysis_result.lower():
            print(f"\n=== 日志 {debug_log_url} 分析结果（含错误） ===\n{analysis_result}\n")
        else:
            print(f"日志 {debug_log_url} 判定无错误，未显示分析内容。")
