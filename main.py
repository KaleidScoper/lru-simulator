import random
from collections import deque

def generate_page_sequence(length, max_page):
    """随机生成页面访问序列"""
    return [random.randint(1, max_page) for _ in range(length)]

def lru_page_replacement(pages, frame_count):
    """LRU 页面置换算法"""
    frames = deque(maxlen=frame_count)  # 用作内存页框
    page_faults = 0
    replacement_history = []
    stack_states = []

    for page in pages:
        if page not in frames:
            # 页面未命中，需要置换
            page_faults += 1
            if len(frames) >= frame_count:
                # 替换最久未使用的页面
                replaced = frames.popleft()
            else:
                replaced = None
            frames.append(page)
        else:
            # 页面命中，移动到最近使用位置
            frames.remove(page)
            frames.append(page)
            replaced = None

        # 记录当前置换信息和栈状态
        replacement_history.append((page, replaced))
        stack_states.append(list(frames))

    return page_faults, replacement_history, stack_states

def display_results(pages, frame_count, replacement_history, stack_states):
    """显示置换过程和栈变化"""
    print("\n页面访问序列:", pages)
    print("内存页框大小:", frame_count)
    print("\n置换图 (格式: 访问页面 -> 被替换页面):")
    for i, (page, replaced) in enumerate(replacement_history):
        print(f"访问页面 {page} -> {'无替换' if replaced is None else f'替换页面 {replaced}'}")

    print("\n栈的变化 (每行表示一个状态):")
    for i, state in enumerate(stack_states):
        print(f"访问页面 {pages[i]} 后栈状态: {state}")

def main():
    print("=== LRU 页面置换算法模拟器 ===")
    try:
        length = int(input("请输入页面访问序列的长度: "))
        max_page = int(input("请输入页面编号的最大值: "))
        frame_count = int(input("请输入内存页框的数量: "))

        pages = generate_page_sequence(length, max_page)
        page_faults, replacement_history, stack_states = lru_page_replacement(pages, frame_count)

        display_results(pages, frame_count, replacement_history, stack_states)

        print(f"\n总页面错误数: {page_faults}")
    except ValueError:
        print("输入无效，请输入正整数。")

if __name__ == "__main__":
    main()
