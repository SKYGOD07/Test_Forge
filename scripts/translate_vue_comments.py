import os
import re

def translate_chinese_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dictionary of known comment translations
    comment_map = {
        '卡片描述（模拟需求完整展示）': 'Card description',
        '卡片底部': 'Card footer',
        '底部装饰线 (hover时展开)': 'Bottom decoration line (expands on hover)',
        '加载状态': 'Loading state',
        '历史回放详情弹窗': 'History replay detail modal',
        '弹窗头部': 'Modal header',
        '弹窗内容': 'Modal content',
        '模拟需求': 'Simulation requirements',
        '推演回放分割线': 'Simulation replay divider',
        '导航按钮': 'Navigation buttons',
        '不可回放提示': 'Replay unavailable notice',
        '状态': 'State',
        '卡片布局配置 - 调整为更宽的比例': 'Card layout configuration',
        '动态计算容器高度样式': 'Dynamically calculate container height style',
        '折叠态：固定高度': 'Collapsed: fixed height',
        '展开态：高度由内容撑开，不设上限': 'Expanded: height driven by content',
        '展开时增加底部内边距，确保内容不被遮挡': 'Add bottom padding when expanded',
        '切换展开/折叠状态（防抖+动画锁）': 'Toggle expanded/collapsed state with debounce and lock',
        '如果正在执行动画，暂存目标状态，等动画结束后执行': 'If animating, defer target state until transition finishes',
        '如果已经处于目标状态，无需重复触发': 'Skip if already in target state',
        '清除之前的防抖定时器': 'Clear debounce timer',
        '设置防抖': 'Set debounce',
        '真正的切换逻辑': 'Toggle state logic',
        '加锁，防止动画期间状态被重入': 'Lock transition to prevent re-entrancy',
        '平滑切换高度': 'Smoothly transition height',
        '动画结束后解锁，并检查是否有暂存的待执行状态': 'Unlock and check pending state on transition end',
        '打开历史回放弹窗': 'Open history replay modal',
        '关闭弹窗': 'Close modal',
        '格式化日期时间': 'Format datetime',
        '截断文本': 'Truncate text',
        '检查步骤可用性（严格只看当前字段）': 'Check step availability',
        '图谱构建可用': 'Graph construction available',
        '环境搭建可用': 'Environment setup available',
        '分析报告可用': 'Analysis report available',
        '步骤1：图谱构建（只要有 graph_id 就可用）': 'Step 1: Graph construction (available if graph_id exists)',
        '步骤2：环境搭建（只有状态为 completed 才可用）': 'Step 2: Environment setup (available if status is completed)',
        '步骤3：开始模拟（只有状态为 completed 且有 simulation_id 才可用）': 'Step 3: Simulation (available if completed and simulation_id exists)',
        '步骤4：报告生成（只要有 report_id 就可用）': 'Step 4: Report generation (available if report_id exists)',
        '步骤5：深度互动（只要有 report_id 就可用）': 'Step 5: Interaction (available if report_id exists)',
        '导航到图谱构建': 'Navigate to graph construction',
        '导航到环境搭建': 'Navigate to environment setup',
        '导航到开始模拟': 'Navigate to simulation run',
        '导航到报告生成': 'Navigate to report view',
        '导航到深度互动': 'Navigate to interaction view',
        '加载历史项目列表': 'Load history project list',
        'Step 04: 初始激活编排': 'Step 04: Initial Activation Orchestration',
        '叙事方向': 'Narrative Direction',
        '热点话题': 'Hot Topics',
        '初始帖子流': 'Initial Posts Feed',
        'Step 05: 准备完成': 'Step 05: Preparation Complete',
        '模拟轮数配置 - 只有在配置生成完成且轮数计算出来后才显示': 'Simulation rounds configuration - shown when config is ready',
        '基本信息': 'Basic Information',
        '简介': 'Biography',
        '关注话题': 'Interested Topics',
        '详细人设': 'Detailed Persona',
        '人设维度概览': 'Persona Dimensions Overview',
        '日志去重：记录上一次输出的关键信息': 'Log deduplication: track last message',
        '模拟轮数配置': 'Simulation rounds configuration',
        '生成Agent人设': 'generating_profiles',
        '生成模拟配置': 'generating_config',
        '准备模拟脚本': 'copying_scripts',
        'FOLLOW: 关注用户': 'FOLLOW: Follow User',
        'DO_NOTHING: 无操作（静默）': 'DO_NOTHING: Silent',
        '通用回退：未知类型或有 content 但未被上述处理': 'Fallback: unknown type or content',
        '按时间顺序显示动作（最新的在最后面，即底部）': 'Display actions in chronological order',
        '各平台动作计数': 'Platform action count',
        '格式化模拟流逝时间（根据轮次和每轮分钟数计算）': 'Format simulation elapsed time',
        'Twitter平台的模拟流逝时间': 'Twitter simulated elapsed time',
        'Reddit平台的模拟流逝时间': 'Reddit simulated elapsed time',
        '重置所有状态（用于重新启动模拟）': 'Reset state for simulation restart',
        '启动模拟': 'Start simulation',
        '先重置所有状态，确保不会受到上一次模拟的影响': 'Reset state before starting simulation',
        '停止模拟': 'Stop simulation',
        '轮询状态': 'Poll status',
        '追踪各平台的上一次轮次，用于检测变化并输出日志': 'Track previous round per platform',
        '分别检测各平台的轮次变化并输出日志': 'Detect round changes and log',
        '清理列表开始标签后的空白': 'Clean whitespace after list start tag',
        '清理列表结束标签前的空白': 'Clean whitespace before list end tag',
        '清理块级元素前后的 <br> 标签': 'Clean br tags around block elements',
        '清理 <p><br> 紧跟块级元素的情况（多余空行导致）': 'Clean extra empty lines before block elements',
        '清理连续的 <br> 标签': 'Clean consecutive br tags',
        '清理块级元素后紧跟的段落开始标签前的 <br>': 'Clean trailing br tags before block elements',
        '修复非连续有序列表的编号：当单项 <ol> 被段落内容隔开时，保持编号递增': 'Fix non-consecutive ordered list indices',
        '自动保存对话记录到缓存': 'Auto-save conversation to cache',
        '正确的数据路径: res.data.result.results 是一个对象字典': 'Data path: res.data.result.results object dictionary',
        '格式: {"twitter_0": {...}, "reddit_0": {...}} 或单平台 {"reddit_0": {...}}': 'Format: {"twitter_0": {...}, "reddit_0": {...}} or single platform',
        '将对象字典转换为数组，优先获取 reddit 平台的回复': 'Convert object dictionary to array, prefer Reddit responses',
        '优先使用 reddit 平台回复，其次 twitter': 'Prefer Reddit responses, then Twitter',
        '兼容数组格式': 'Array format compatibility',
        '格式: {"twitter_0": {...}, "reddit_0": {...}, "twitter_1": {...}, ...}': 'Format: {"twitter_0": {...}, "reddit_0": {...}, "twitter_1": {...}}'
    }

    for zh, en in comment_map.items():
        content = content.replace(zh, en)

    # General pattern for remaining <!-- ...中文... --> HTML comments
    def replace_html_comment(match):
        comment_text = match.group(1)
        if any('\u4e00' <= c <= '\u9fff' for c in comment_text):
            # Translate or remove Chinese inside HTML comment
            clean_text = re.sub(r'[\u4e00-\u9fff]+', '', comment_text).strip(' :：-—')
            return f'<!-- {clean_text if clean_text else "Section"} -->'
        return match.group(0)

    content = re.sub(r'<!--\s*(.*?)\s*-->', replace_html_comment, content)

    # General pattern for remaining // ...中文... JS comments
    def replace_js_comment(match):
        comment_text = match.group(1)
        if any('\u4e00' <= c <= '\u9fff' for c in comment_text):
            clean_text = re.sub(r'[\u4e00-\u9fff]+', '', comment_text).strip(' :：-—')
            return f'// {clean_text if clean_text else ""}'.rstrip()
        return match.group(0)

    content = re.sub(r'//\s*(.*)', replace_js_comment, content)

    # General pattern for remaining /* ...中文... */ CSS comments
    def replace_css_comment(match):
        comment_text = match.group(1)
        if any('\u4e00' <= c <= '\u9fff' for c in comment_text):
            clean_text = re.sub(r'[\u4e00-\u9fff]+', '', comment_text).strip(' :：-—')
            return f'/* {clean_text if clean_text else ""} */'.rstrip()
        return match.group(0)

    content = re.sub(r'/\*\s*(.*?)\s*\*/', replace_css_comment, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.vue') or file.endswith('.js'):
            translate_chinese_comments(os.path.join(root, file))

print("All frontend Vue & JS files processed.")
