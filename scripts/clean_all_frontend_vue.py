import re

def clean_file(path, replacements):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for orig, repl in replacements:
        content = content.replace(orig, repl)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {path}")

def clean_history_database():
    path = 'frontend/src/components/HistoryDatabase.vue'
    replacements = [
        ('<!-- 背景装饰：技术网格线（只在有项目时显示） -->', '<!-- Background decoration: grid lines (shown only when projects exist) -->'),
        ('<!-- 标题区域 -->', '<!-- Title Area -->'),
        ('<!-- 卡片容器（只在有项目时显示） -->', '<!-- Card container (shown only when projects exist) -->'),
        ('<!-- 卡片头部：simulation_id 和 功能可用状态 -->', '<!-- Card header: simulation_id and feature status -->'),
        ('<!-- 文件列表区域 -->', '<!-- File list area -->'),
        ('<!-- 角落装饰 - 取景框风格 -->', '<!-- Corner decoration -->'),
        ('<!-- 文件列表 -->', '<!-- File list -->'),
        ('<!-- 如果有更多文件，显示提示 -->', '<!-- Hint if more files exist -->'),
        ('<!-- 无文件时的占位 -->', '<!-- Placeholder when no files exist -->'),
        ('<!-- 卡片标题（使用模拟需求的前20字作为标题） -->', '<!-- Card title -->'),
        ('const selectedProject = ref(null)  // 当前选中的项目（用于弹窗）', 'const selectedProject = ref(null)  // Currently selected project'),
        ('let isAnimating = false  // 动画锁，防止闪烁', 'let isAnimating = false  // Animation lock to prevent flicker'),
        ('let expandDebounceTimer = null  // 防抖定时器', 'let expandDebounceTimer = null  // Debounce timer'),
        ('let pendingState = null  // 记录待执行的目标状态', 'let pendingState = null  // Pending target state'),
        ("console.error('加载历史项目失败:', error)", "console.error('Failed to load project history:', error)"),
        ('/* 图谱构建 - 蓝色 */', '/* Graph Construction - Blue */'),
        ('/* 环境搭建 - 橙色 */', '/* Environment Setup - Orange */'),
        ('/* 分析报告 - 绿色 */', '/* Analysis Report - Green */'),
        ('/* 已完成 - 绿色 */', '/* Completed - Green */'),
        ('/* 进行中 - 橙色 */', '/* In Progress - Orange */'),
        ('/* 未开始 - 灰色 */', '/* Not Started - Gray */'),
    ]
    clean_file(path, replacements)

def clean_step2_env_setup():
    path = 'frontend/src/components/Step2EnvSetup.vue'
    replacements = [
        ('<!-- Step 01: 模拟实例 -->', '<!-- Step 01: Simulation Instance -->'),
        ('<!-- Step 02: 生成 Agent 人设 -->', '<!-- Step 02: Generate Agent Profiles -->'),
        ('<!-- Step 03: 生成双平台模拟配置 -->', '<!-- Step 03: Generate Simulation Config -->'),
        ('<!-- 时间配置 -->', '<!-- Time Configuration -->'),
        ('<!-- Agent 配置 -->', '<!-- Agent Configuration -->'),
        ('<!-- 卡片头部 -->', '<!-- Card Header -->'),
        ('<!-- 活跃时间轴 -->', '<!-- Activity Timeline -->'),
        ('<!-- 行为参数 -->', '<!-- Behavior Parameters -->'),
        ('<!-- 平台配置 -->', '<!-- Platform Configuration -->'),
        ('<!-- LLM 配置推理 -->', '<!-- LLM Configuration Inference -->'),
        ('simulationId: String,  // 从父组件传入', 'simulationId: String,  // Passed from parent component'),
        ('const phase = ref(0) // 0: 初始化, 1: 生成人设, 2: 生成配置, 3: 完成', 'const phase = ref(0) // 0: Init, 1: Generate Profiles, 2: Generate Config, 3: Complete'),
        ('const useCustomRounds = ref(false) // 默认使用自动配置轮数', 'const useCustomRounds = ref(false) // Default auto rounds'),
        ('const customMaxRounds = ref(40)   // 默认推荐40轮', 'const customMaxRounds = ref(40)   // Default recommended 40 rounds'),
        ('phase.value = 2 // 仍属于配置阶段', 'phase.value = 2 // Belongs to config phase'),
        ('return null // 配置未生成时返回 null', 'return null // Return null if config not generated'),
        ('return null // 配置数据不完整时返回 null', 'return null // Return null if config incomplete'),
        ("console.warn('轮询状态失败:', err)", "console.warn('Polling status failed:', err)"),
        ("console.warn('获取 Profiles 失败:', err)", "console.warn('Failed to get profiles:', err)"),
        ("console.warn('获取 Config 失败:', err)", "console.warn('Failed to get config:', err)")
    ]
    clean_file(path, replacements)

def clean_step3_simulation():
    path = 'frontend/src/components/Step3Simulation.vue'
    replacements = [
        ('<!-- Twitter 平台进度 -->', '<!-- Twitter Platform Progress -->'),
        ('<!-- 可用动作提示 -->', '<!-- Available Actions Hint -->'),
        ('<!-- Reddit 平台进度 -->', '<!-- Reddit Platform Progress -->'),
        ('<!-- CREATE_POST: 发布帖子 -->', '<!-- CREATE_POST: Create Post -->'),
        ('<!-- QUOTE_POST: 引用帖子 -->', '<!-- QUOTE_POST: Quote Post -->'),
        ('<!-- REPOST: 转发帖子 -->', '<!-- REPOST: Repost -->'),
        ('<!-- LIKE_POST: 点赞帖子 -->', '<!-- LIKE_POST: Like Post -->'),
        ('<!-- CREATE_COMMENT: 发表评论 -->', '<!-- CREATE_COMMENT: Create Comment -->'),
        ('<!-- SEARCH_POSTS: 搜索帖子 -->', '<!-- SEARCH_POSTS: Search Posts -->'),
        ('maxRounds: Number, // 从Step2传入的最大轮数', 'maxRounds: Number, // Max rounds passed from Step 2'),
        ('default: 30 // 默认每轮30分钟', 'default: 30 // Default 30 min per round'),
        ('const phase = ref(0) // 0: 未开始, 1: 运行中, 2: 已完成', 'const phase = ref(0) // 0: Not Started, 1: Running, 2: Completed'),
        ('const allActions = ref([]) // 所有动作（增量累积）', 'const allActions = ref([]) // All actions (incremental)'),
        ('const actionIds = ref(new Set()) // 用于去重的动作ID集合', 'const actionIds = ref(new Set()) // Set for deduplicating action IDs'),
        ('stopPolling()  // 停止之前可能存在的轮询', 'stopPolling()  // Stop existing polling'),
        ('force: true,  // 强制重新开始', 'force: true,  // Force restart'),
        ('enable_graph_memory_update: true  // 开启动态图谱更新', 'enable_graph_memory_update: true  // Enable dynamic graph memory update'),
        ("startError.value = res.error || '启动失败'", "startError.value = res.error || 'Failed to start'"),
        ("console.warn('获取运行状态失败:', err)", "console.warn('Failed to get run status:', err)"),
        ("console.warn('获取详细状态失败:', err)", "console.warn('Failed to get detailed status:', err)")
    ]
    clean_file(path, replacements)

def clean_step4_report():
    path = 'frontend/src/components/Step4Report.vue'
    replacements = [
        ("h('div', { class: 'reason-label' }, '选择理由')", "h('div', { class: 'reason-label' }, 'Selection Reason')"),
        ("return steps[0] || { noLabel: '--', title: '等待开始', status: 'todo', meta: '' }", "return steps[0] || { noLabel: '--', title: 'Waiting to start', status: 'todo', meta: '' }"),
        ("icon: 'lightbulb' // 灯泡图标 - 代表洞察", "icon: 'lightbulb' // Lightbulb icon - insights"),
        ("icon: 'globe' // 地球图标 - 代表全景搜索", "icon: 'globe' // Globe icon - panorama search"),
        ("icon: 'users' // 用户图标 - 代表对话", "icon: 'users' // Users icon - interviews"),
        ("icon: 'zap' // 闪电图标 - 代表快速", "icon: 'zap' // Zap icon - quick summary"),
        ("icon: 'chart' // 图表图标 - 代表统计", "icon: 'chart' // Chart icon - statistics"),
        ("icon: 'database' // 数据库图标 - 代表实体", "icon: 'database' // Database icon - entities"),
        ("/* 深灰色，不随状态变化 */", "/* Dark gray, fixed */"),
        ("currentSectionIndex.value = null  // 确保清除 loading 状态", "currentSectionIndex.value = null  // Clear loading state"),
        ("if (log.includes('ERROR') || log.includes('错误')) return 'error'", "if (log.includes('ERROR') || log.includes('Error')) return 'error'"),
        ("if (log.includes('WARNING') || log.includes('警告')) return 'warning'", "if (log.includes('WARNING') || log.includes('Warning')) return 'warning'"),
        ("<!-- Next Step Button - 在完成后显示 -->", "<!-- Next Step Button - show on completion -->"),
        ("<!-- Section Content Generated (内容生成完成，但整个章节可能还没完成) -->", "<!-- Section Content Generated -->"),
        ("<!-- Section Complete (章节生成完成) -->", "<!-- Section Complete -->"),
        ("<!-- 当是最终答案时，显示特殊提示 -->", "<!-- Final answer notice -->"),
        ("// 保存按钮相对于视口的位置", "// Save button position relative to viewport"),
        ("// 切换状态", "// Toggle state"),
        ("// 等待 DOM 更新后，调整滚动位置以保持按钮在相同位置", "// Adjust scroll position after DOM update"),
        ("// 调整滚动位置", "// Adjust scroll position"),
        ("// 只有已完成的章节才能折叠", "// Only completed sections can be collapsed"),
        ("const queryMatch = text.match(/分析问题:\\s*(.+?)(?:\\n|$)/)", "const queryMatch = text.match(/(?:Analysis Question|分析问题):\\s*(.+?)(?:\\n|$)/i)"),
        ("const reqMatch = text.match(/预测场景:\\s*(.+?)(?:\\n|$)/)", "const reqMatch = text.match(/(?:Scenario|预测场景):\\s*(.+?)(?:\\n|$)/i)"),
        ("const factMatch = text.match(/相关预测事实:\\s*(\\d+)/)", "const factMatch = text.match(/(?:Relevant Facts|相关预测事实):\\s*(\\d+)/i)"),
        ("const entityMatch = text.match(/涉及实体:\\s*(\\d+)/)", "const entityMatch = text.match(/(?:Entities Involved|涉及实体):\\s*(\\d+)/i)"),
        ("const relMatch = text.match(/关系链:\\s*(\\d+)/)", "const relMatch = text.match(/(?:Relationship Chain|关系链):\\s*(\\d+)/i)"),
        ("const subQSection = text.match(/### 分析的子问题\\n([\\s\\S]*?)(?=\\n###|$)/)", "const subQSection = text.match(/### (?:Sub-questions Analyzed|分析的子问题)\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const factsSection = text.match(/### 【关键事实】[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/)", "const factsSection = text.match(/### (?:【Key Facts】|【关键事实】)[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const entitySection = text.match(/### 【核心实体】\\n([\\s\\S]*?)(?=\\n###|$)/)", "const entitySection = text.match(/### (?:【Core Entities】|【核心实体】)\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const relSection = text.match(/### 【关系链】\\n([\\s\\S]*?)(?=\\n###|$)/)", "const relSection = text.match(/### (?:【Relationship Chain】|【关系链】)\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const queryMatch = text.match(/查询:\\s*(.+?)(?:\\n|$)/)", "const queryMatch = text.match(/(?:Query|查询):\\s*(.+?)(?:\\n|$)/i)"),
        ("const nodesMatch = text.match(/总节点数:\\s*(\\d+)/)", "const nodesMatch = text.match(/(?:Total Nodes|总节点数):\\s*(\\d+)/i)"),
        ("const edgesMatch = text.match(/总边数:\\s*(\\d+)/)", "const edgesMatch = text.match(/(?:Total Edges|总边数):\\s*(\\d+)/i)"),
        ("const activeMatch = text.match(/当前有效事实:\\s*(\\d+)/)", "const activeMatch = text.match(/(?:Active Facts|当前有效事实):\\s*(\\d+)/i)"),
        ("const histMatch = text.match(/历史\\/过期事实:\\s*(\\d+)/)", "const histMatch = text.match(/(?:Historical Facts|历史\\/过期事实):\\s*(\\d+)/i)"),
        ("const activeSection = text.match(/### 【当前有效事实】[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/)", "const activeSection = text.match(/### (?:【Active Facts】|【当前有效事实】)[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const histSection = text.match(/### 【历史\\/过期事实】[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/)", "const histSection = text.match(/### (?:【Historical Facts】|【历史\\/过期事实】)[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const entitySection = text.match(/### 【涉及实体】\\n([\\s\\S]*?)(?=\\n###|$)/)", "const entitySection = text.match(/### (?:【Involved Entities】|【涉及实体】)\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const topicMatch = text.match(/\\*\\*采访主题:\\*\\*\\s*(.+?)(?:\\n|$)/)", "const topicMatch = text.match(/\\*\\*(?:Interview Topic|采访主题):\\*\\*\\s*(.+?)(?:\\n|$)/i)"),
        ("const countMatch = text.match(/\\*\\*采访人数:\\*\\*\\s*(\\d+)\\s*\\/\\s*(\\d+)/)", "const countMatch = text.match(/\\*\\*(?:Interviewees|采访人数):\\*\\*\\s*(\\d+)\\s*\\/\\s*(\\d+)/i)"),
        ("const reasonMatch = text.match(/### 采访对象选择理由\\n([\\s\\S]*?)(?=\\n---\\n|\\n### 采访实录)/)", "const reasonMatch = text.match(/### (?:Interview Selection Reasons|采访对象选择理由)\\n([\\s\\S]*?)(?=\\n---\\n|\\n### (?:Interview Transcript|采访实录))/i)"),
        ("const summaryMatch = text.match(/### 采访摘要与核心观点\\n([\\s\\S]*?)$/)", "const summaryMatch = text.match(/### (?:Interview Summary & Core Views|采访摘要与核心观点)\\n([\\s\\S]*?)$/i)"),
        ("const queryMatch = text.match(/搜索查询:\\s*(.+?)(?:\\n|$)/)", "const queryMatch = text.match(/(?:Search Query|搜索查询):\\s*(.+?)(?:\\n|$)/i)"),
        ("const countMatch = text.match(/找到\\s*(\\d+)\\s*条/)", "const countMatch = text.match(/(?:Found|找到)\\s*(\\d+)\\s*(?:results|条)/i)"),
        ("const factsSection = text.match(/### 相关事实:\\n([\\s\\S]*)$/)", "const factsSection = text.match(/### (?:Relevant Facts|相关事实):\\n([\\s\\S]*)$/i)"),
        ("const edgesSection = text.match(/### 相关边:\\n([\\s\\S]*?)(?=\\n###|$)/)", "const edgesSection = text.match(/### (?:Relevant Edges|相关边):\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const nodesSection = text.match(/### 相关节点:\\n([\\s\\S]*?)(?=\\n###|$)/)", "const nodesSection = text.match(/### (?:Relevant Nodes|相关节点):\\n([\\s\\S]*?)(?=\\n###|$)/i)"),
        ("const chineseFinalMatch = response.match(/最终答案[:：]\\s*\\n*([\\s\\S]*)$/i)", "const chineseFinalMatch = response.match(/(?:Final Answer|最终答案)[:：]\\s*\\n*([\\s\\S]*)$/i)")
    ]
    clean_file(path, replacements)

def clean_step5_interaction():
    path = 'frontend/src/components/Step5Interaction.vue'
    replacements = [
        ("chatHistoryCache = ref({}) // 缓存所有对话记录: { 'report_agent': [], 'agent_0': [", "chatHistoryCache = ref({}) // Cache conversation logs: { 'report_agent': [], 'agent_0': ["),
        (".map(msg => `${msg.role === 'user' ? '提问者' : '你'}：${msg.content}`)", ".map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`)"),
        ("prompt = `以下是我们之前的对话：\\n${historyContext}\\n\\n现在我的新问题是：${message}`", "prompt = `Here is our conversation history:\\n${historyContext}\\n\\nMy new question is: ${message}`"),
        ('// 保存当前对话记录到缓存', '// Save conversation to cache'),
        ('// 保存当前对话记录', '// Save current conversation'),
        ('// 恢复 Report Agent 的对话记录', '// Restore Report Agent conversation'),
        ('// 恢复该 Agent 的对话记录', '// Restore agent conversation'),
        ('// 处理列表 - 支持子列表', '// Process lists - support sub-lists'),
        ('// 包装无序列表', '// Wrap unordered list'),
        ('// 包装有序列表', '// Wrap ordered list'),
        ('// 清理列表项之间的所有空白', '// Clean whitespace between list items')
    ]
    clean_file(path, replacements)

if __name__ == '__main__':
    clean_history_database()
    clean_step2_env_setup()
    clean_step3_simulation()
    clean_step4_report()
    clean_step5_interaction()
