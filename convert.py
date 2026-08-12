import urllib.request
import re

# 1. 替换为你想要抓取的第三方 M3U 链接
M3U_URL = "https://github.com/Healer-sys/Home/blob/61aef903e22e68707bd1fa4ec3793ecdf79ed827/iptv/gx.m3u"

# 2. 转换后保存的 TXT 文件名称
OUTPUT_FILE = "live.txt"

def m3u_to_txt():
    try:
        # 下载远程 M3U 文件
        req = urllib.request.Request(M3U_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')

        lines = content.splitlines()
        channels = {}
        current_group = "未分组"
        current_title = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析 #EXTINF 行，提取分组名称和频道名称
            if line.startswith("#EXTINF:"):
                # 提取 group-title="分类名称"
                group_match = re.search(r'group-title="([^"]+)"', line)
                if group_match:
                    current_group = group_match.group(1)
                else:
                    current_group = "未分组"

                # 提取逗号后面的频道名称
                comma_idx = line.rfind(",")
                if comma_idx != -1:
                    current_title = line[comma_idx + 1:].strip()
                else:
                    current_title = "未知频道"

            # 解析播放地址行
            elif not line.startswith("#"):
                if current_title and line.startswith("http"):
                    if current_group not in channels:
                        channels[current_group] = []
                    channels[current_group].append(f"{current_title},{line}")
                    current_title = ""

        # 按 TVBox 的分组格式写入 live.txt
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for group, items in channels.items():
                f.write(f"{group},#genre#\n")
                for item in items:
                    f.write(f"{item}\n")
                f.write("\n")

        print(f"转换成功！文件已生成：{OUTPUT_FILE}")

    except Exception as e:
        print(f"转换失败，错误信息: {e}")

if __name__ == "__main__":
    m3u_to_txt()
