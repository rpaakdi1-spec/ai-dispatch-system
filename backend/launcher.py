"""
AI Dispatch System - GUI 런처
간단한 그래픽 인터페이스로 서버 시작/종료
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import sys
import os
from pathlib import Path

class DispatchLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 배차 시스템 런처")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.process = None
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 헤더
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🚛 AI 배차 시스템",
            font=("맑은 고딕", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # 상태 프레임
        status_frame = tk.Frame(self.root, bg="#ecf0f1", height=100)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="⚪ 서버 중지됨",
            font=("맑은 고딕", 14),
            bg="#ecf0f1"
        )
        self.status_label.pack(pady=10)
        
        self.url_label = tk.Label(
            status_frame,
            text="",
            font=("맑은 고딕", 10),
            bg="#ecf0f1",
            fg="#3498db",
            cursor="hand2"
        )
        self.url_label.pack()
        self.url_label.bind("<Button-1>", self.open_browser)
        
        # 버튼 프레임
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ 서버 시작",
            command=self.start_server,
            font=("맑은 고딕", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⬛ 서버 종료",
            command=self.stop_server,
            font=("맑은 고딕", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.docs_button = tk.Button(
            button_frame,
            text="📖 API 문서",
            command=self.open_docs,
            font=("맑은 고딕", 12),
            bg="#3498db",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.docs_button.pack(side=tk.LEFT, padx=5)
        
        # 로그 프레임
        log_frame = tk.LabelFrame(
            self.root,
            text="서버 로그",
            font=("맑은 고딕", 10),
            bg="white",
            padx=10,
            pady=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 푸터
        footer_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Made with ❤️ for efficient cold chain logistics",
            font=("맑은 고딕", 8),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        footer_label.pack(pady=10)
        
    def log(self, message, color=None):
        """로그 메시지 출력"""
        self.log_text.config(state=tk.NORMAL)
        if color:
            tag = f"color_{color}"
            self.log_text.tag_config(tag, foreground=color)
            self.log_text.insert(tk.END, message + "\n", tag)
        else:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def start_server(self):
        """서버 시작"""
        if self.is_running:
            return
            
        self.log("=" * 60)
        self.log("🚀 서버를 시작합니다...", "#27ae60")
        self.log("=" * 60)
        
        # Python 경로 찾기
        python_exe = sys.executable
        main_py = Path(__file__).parent / "main.py"
        
        if not main_py.exists():
            messagebox.showerror("오류", "main.py 파일을 찾을 수 없습니다!")
            return
        
        try:
            # 서버 프로세스 시작
            self.process = subprocess.Popen(
                [python_exe, str(main_py)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=str(main_py.parent)
            )
            
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="🟢 서버 실행 중", fg="#27ae60")
            self.url_label.config(text="📖 http://localhost:8000/docs (클릭하여 열기)")
            
            # 로그 읽기 스레드 시작
            threading.Thread(target=self.read_output, daemon=True).start()
            
            self.log("✅ 서버가 시작되었습니다!", "#27ae60")
            self.log("📖 API 문서: http://localhost:8000/docs", "#3498db")
            self.log("")
            
        except Exception as e:
            self.log(f"❌ 서버 시작 실패: {e}", "#e74c3c")
            self.is_running = False
            
    def stop_server(self):
        """서버 종료"""
        if not self.is_running or not self.process:
            return
            
        self.log("=" * 60)
        self.log("⬛ 서버를 종료합니다...", "#e74c3c")
        self.log("=" * 60)
        
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="⚪ 서버 중지됨", fg="#95a5a6")
        self.url_label.config(text="")
        
        self.log("✅ 서버가 종료되었습니다.", "#e74c3c")
        self.log("")
        
    def read_output(self):
        """서버 출력 읽기"""
        if not self.process:
            return
            
        for line in iter(self.process.stdout.readline, ''):
            if not line:
                break
            line = line.rstrip()
            
            # 색상 지정
            color = None
            if "ERROR" in line or "❌" in line:
                color = "#e74c3c"
            elif "INFO" in line or "✅" in line:
                color = "#27ae60"
            elif "WARNING" in line or "⚠️" in line:
                color = "#f39c12"
                
            self.log(line, color)
            
    def open_browser(self, event=None):
        """브라우저에서 API 문서 열기"""
        if self.is_running:
            import webbrowser
            webbrowser.open("http://localhost:8000/docs")
            
    def open_docs(self):
        """API 문서 열기"""
        if not self.is_running:
            messagebox.showinfo("알림", "서버를 먼저 시작해주세요!")
            return
        self.open_browser()
        
    def on_closing(self):
        """창 닫기"""
        if self.is_running:
            if messagebox.askokcancel("종료", "서버가 실행 중입니다. 종료하시겠습니까?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = DispatchLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
