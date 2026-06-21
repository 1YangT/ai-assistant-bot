import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from ai_engine import AIAssistant
from task_manager import TaskManager

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

st.set_page_config(
    page_title="AI智能助手",
    page_icon="🤖",
    layout="wide"
)

CSS_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans SC', sans-serif;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fc;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    .message-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: white;
        margin-right: 2rem;
    }
    
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .user-avatar {
        background: #667eea;
        color: white;
    }
    
    .bot-avatar {
        background: #f0f0f0;
        color: #667eea;
    }
    
    .message-content {
        flex: 1;
        line-height: 1.6;
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.25rem;
    }
    
    .function-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }
    
    .function-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }
    
    .function-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
    }
    
    .task-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .task-priority-high {
        border-left: 4px solid #e74c3c;
    }
    
    .task-priority-medium {
        border-left: 4px solid #f39c12;
    }
    
    .task-priority-low {
        border-left: 4px solid #27ae60;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    .input-container {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .quick-action {
        background: #f8f9fc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
    }
    
    .quick-action:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
</style>
"""

def init_session_state():
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    if 'task_manager' not in st.session_state:
        st.session_state.task_manager = TaskManager()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = 'chat'

def render_chat_message(role, content, timestamp):
    if role == 'user':
        st.markdown(f"""
        <div class="message-card user-message">
            <div class="avatar user-avatar">👤</div>
            <div class="message-content">
                <div>{content}</div>
                <div class="message-time">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-card bot-message">
            <div class="avatar bot-avatar">🤖</div>
            <div class="message-content">
                <div>{content}</div>
                <div class="message-time">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_chat_interface():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;">
        <h1 style="color: white; font-size: 1.75rem; font-weight: 700; margin: 0;">💬 智能对话</h1>
        <p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">AI助手随时为您解答问题</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        render_chat_message(msg['role'], msg['content'], msg['timestamp'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "输入您的问题",
            key="chat_input",
            placeholder="例如：什么是人工智能？",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("发送", use_container_width=True):
            if user_input.strip():
                timestamp = get_beijing_time().strftime("%H:%M:%S")
                
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': timestamp
                })
                
                response = st.session_state.ai_assistant.get_response(user_input)
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': get_beijing_time().strftime("%H:%M:%S")
                })
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #718096; font-size: 0.9rem; margin-bottom: 0.5rem;">快捷操作：</p>', unsafe_allow_html=True)
    
    quick_actions = [
        "📚 查询知识库",
        "💡 讲个笑话",
        "⏰ 当前时间",
        "📅 今日日期",
        "🌟 关于助手"
    ]
    
    cols = st.columns(len(quick_actions))
    for i, action in enumerate(quick_actions):
        with cols[i]:
            if st.button(action, key=f"quick_{i}"):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': action,
                    'timestamp': get_beijing_time().strftime("%H:%M:%S")
                })
                
                response = st.session_state.ai_assistant.handle_quick_action(action)
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': get_beijing_time().strftime("%H:%M:%S")
                })
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_task_manager():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;">
        <h1 style="color: white; font-size: 1.75rem; font-weight: 700; margin: 0;">📋 任务管理</h1>
        <p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">管理您的待办事项和提醒</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(st.session_state.task_manager.tasks)}</div>
            <div class="stat-label">总任务数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pending = len([t for t in st.session_state.task_manager.tasks if t['status'] == 'pending'])
        st.markdown(f"""
        <div class="stat-box" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);">
            <div class="stat-value">{pending}</div>
            <div class="stat-label">待完成</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed = len([t for t in st.session_state.task_manager.tasks if t['status'] == 'completed'])
        st.markdown(f"""
        <div class="stat-box" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);">
            <div class="stat-value">{completed}</div>
            <div class="stat-label">已完成</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="card" style="background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">', unsafe_allow_html=True)
    st.subheader("➕ 添加新任务")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        task_title = st.text_input("任务标题", placeholder="例如：完成项目报告")
    
    with col2:
        task_priority = st.selectbox("优先级", ["低", "中", "高"])
    
    with col3:
        task_due = st.date_input("截止日期", get_beijing_time() + timedelta(days=7))
    
    if st.button("添加任务", use_container_width=True):
        if task_title.strip():
            st.session_state.task_manager.add_task(
                title=task_title,
                priority=task_priority,
                due_date=task_due.strftime("%Y-%m-%d")
            )
            st.success("✅ 任务添加成功！")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card" style="background: white; border-radius: 12px; padding: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("📝 任务列表")
    
    for i, task in enumerate(st.session_state.task_manager.tasks):
        priority_class = f"task-priority-{task['priority'].lower()}"
        status_icon = "✅" if task['status'] == 'completed' else "⏳"
        
        st.markdown(f"""
        <div class="task-card {priority_class}">
            <div style="font-size: 1.25rem;">{status_icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 500; color: #2d3748;">{task['title']}</div>
                <div style="font-size: 0.85rem; color: #718096;">
                    优先级: {task['priority']} | 截止: {task['due_date']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if task['status'] == 'pending':
                if st.button("完成", key=f"complete_{i}"):
                    st.session_state.task_manager.complete_task(i)
                    st.rerun()
        with col2:
            if st.button("删除", key=f"delete_{i}"):
                st.session_state.task_manager.delete_task(i)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_knowledge_base():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;">
        <h1 style="color: white; font-size: 1.75rem; font-weight: 700; margin: 0;">📚 知识库</h1>
        <p style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">查询和浏览知识库内容</p>
    </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("搜索知识", placeholder="输入关键词搜索...")
    
    if search_query.strip():
        results = st.session_state.ai_assistant.search_knowledge(search_query)
        
        if results:
            st.markdown(f'<p style="color: #718096;">找到 {len(results)} 条相关知识：</p>', unsafe_allow_html=True)
            
            for result in results:
                st.markdown(f"""
                <div class="card" style="background: white; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;">
                    <div style="font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">{result['category']}</div>
                    <div style="color: #2d3748; font-weight: 500;">{result['question']}</div>
                    <div style="color: #718096; margin-top: 0.5rem; line-height: 1.6;">{result['answer']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("未找到相关知识，请尝试其他关键词")
    
    st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("📂 知识分类")
    
    categories = st.session_state.ai_assistant.get_categories()
    
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            count = st.session_state.ai_assistant.get_category_count(category)
            st.markdown(f"""
            <div class="function-card">
                <div style="font-weight: 600; color: #2d3748;">{category}</div>
                <div style="font-size: 0.85rem; color: #718096;">{count} 条知识</div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <span style="color: white; font-size: 1.2rem; font-weight: 600;">🤖 AI智能助手</span>
        </div>
        """, unsafe_allow_html=True)
        
        modes = {
            '💬 智能对话': 'chat',
            '📋 任务管理': 'task',
            '📚 知识库': 'knowledge'
        }
        
        selected_mode = st.radio("功能模块", list(modes.keys()))
        st.session_state.current_mode = modes[selected_mode]
        
        st.divider()
        
        st.markdown("""
        <div style="background: #f8f9fc; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #2d3748; margin-bottom: 0.5rem;">💡 使用提示</div>
            <div style="color: #718096; font-size: 0.85rem; line-height: 1.6;">
                • 智能对话：与AI助手聊天<br>
                • 任务管理：管理待办事项<br>
                • 知识库：查询专业知识
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

def main():
    st.markdown(CSS_STYLE, unsafe_allow_html=True)
    
    init_session_state()
    
    render_sidebar()
    
    current_mode = st.session_state.current_mode
    
    if current_mode == 'chat':
        render_chat_interface()
    elif current_mode == 'task':
        render_task_manager()
    elif current_mode == 'knowledge':
        render_knowledge_base()

if __name__ == '__main__':
    main()