import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import random

class AIAssistant:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.jokes = [
            "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 = Dec 25！",
            "有一个程序员去买菜，老婆说：买一斤苹果，如果看到西瓜，就买一个。结果程序员买了一斤苹果和一个西瓜。",
            "为什么Java程序员戴眼镜？因为他们看不到C#（C Sharp）！",
            "程序员的三大谎言：1. 这个Bug很容易修复 2. 马上就好 3. 我再也不写Bug了",
            "客户说：这个功能很简单，怎么实现？程序员说：你行你上啊！",
            "为什么程序员喜欢黑暗模式？因为光 attracts bugs（虫子/Bug）！",
            "一个SQL查询走进酒吧，看到两张表，问道：我能JOIN你们吗？",
            "程序员最讨厌的四件事：写注释、写文档、别人不写注释、别人不写文档"
        ]
    
    def load_knowledge_base(self):
        kb_path = Path(__file__).parent / "knowledge.csv"
        if kb_path.exists():
            try:
                df = pd.read_csv(kb_path, encoding='utf-8')
                return df.to_dict('records')
            except:
                return []
        return []
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()
        
        if any(word in user_input_lower for word in ['时间', '几点']):
            return f"现在是 {datetime.now().strftime('%H:%M:%S')}"
        
        if any(word in user_input_lower for word in ['日期', '今天', '几号']):
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            return f"今天是 {datetime.now().strftime('%Y年%m月%d日')} {weekdays[datetime.now().weekday()]}"
        
        if any(word in user_input_lower for word in ['笑话', '搞笑', '逗']):
            return random.choice(self.jokes)
        
        if any(word in user_input_lower for word in ['你好', '您好', 'hi', 'hello']):
            return "您好！我是AI智能助手，很高兴为您服务！有什么我可以帮助您的吗？"
        
        if any(word in user_input_lower for word in ['谢谢', '感谢']):
            return "不客气！如果还有其他问题，随时可以问我哦！😊"
        
        if any(word in user_input_lower for word in ['再见', '拜拜', 'bye']):
            return "再见！祝您一切顺利，期待下次为您服务！👋"
        
        if any(word in user_input_lower for word in ['知识库', '查询', '搜索']):
            return "您可以在左侧选择「📚 知识库」模块，输入关键词搜索专业知识。"
        
        if any(word in user_input_lower for word in ['任务', '提醒', '待办']):
            return "您可以在左侧选择「📋 任务管理」模块，添加和管理您的待办事项。"
        
        kb_results = self.search_knowledge(user_input)
        if kb_results:
            best_match = kb_results[0]
            return f"【{best_match['category']}】\n{best_match['answer']}"
        
        return "我理解您的问题了。您可以尝试：\n\n1. 使用「📚 知识库」搜索专业知识\n2. 使用「📋 任务管理」管理待办事项\n3. 或者直接告诉我您想了解的具体内容\n\n我会尽力为您提供帮助！"
    
    def handle_quick_action(self, action):
        if '查询知识库' in action:
            return "您可以在左侧选择「📚 知识库」模块，输入关键词搜索专业知识。当前知识库包含多个领域的专业内容。"
        
        if '讲个笑话' in action:
            return random.choice(self.jokes)
        
        if '当前时间' in action:
            return f"现在是 {datetime.now().strftime('%H:%M:%S')}"
        
        if '今日日期' in action:
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            return f"今天是 {datetime.now().strftime('%Y年%m月%d日')} {weekdays[datetime.now().weekday()]}"
        
        if '关于助手' in action:
            return """我是AI智能助手，具有以下功能：

✨ **智能对话** - 与您进行自然语言交流
📚 **知识库查询** - 提供专业知识解答
📋 **任务管理** - 帮助您管理待办事项
💡 **娱乐功能** - 讲笑话、查询时间日期

随时为您服务，请告诉我您需要什么帮助！"""
        
        return "我收到了您的请求，请告诉我具体需要什么帮助。"
    
    def search_knowledge(self, query):
        query_lower = query.lower()
        results = []
        
        for item in self.knowledge_base:
            if query_lower in item.get('question', '').lower() or \
               query_lower in item.get('answer', '').lower() or \
               query_lower in item.get('category', '').lower():
                results.append(item)
        
        return results[:5]
    
    def get_categories(self):
        categories = set()
        for item in self.knowledge_base:
            if 'category' in item:
                categories.add(item['category'])
        return sorted(list(categories))
    
    def get_category_count(self, category):
        count = 0
        for item in self.knowledge_base:
            if item.get('category') == category:
                count += 1
        return count