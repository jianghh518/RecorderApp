#键盘鼠标动作录制器
# 这个程序使用tkinter创建一个简单的GUI应用程序，允许用户录制鼠标和键盘事件，并将其保存为JSON文件。
# 用户可以导入这些文件并回放录制的事件。程序还支持定时任务功能，可以在指定时间自动执行录制的动作。


import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import mouse, keyboard
import pyautogui
import time
import json
import threading
import schedule
from datetime import datetime

class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("动作录制器")
        self.recording = False
        self.events = []
        self.start_time = 0
        self.mouse_listener = None
        self.keyboard_listener = None

        # 界面组件
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)
        
        self.btn_start = tk.Button(self.frame, text="开始录制", command=self.start_recording)
        self.btn_start.pack(pady=5, fill=tk.X)
        
        self.btn_export = tk.Button(self.frame, text="导出录制", command=self.export_recording)
        self.btn_export.pack(pady=5, fill=tk.X)
        
        self.btn_import = tk.Button(self.frame, text="导入播放", command=self.import_and_play)
        self.btn_import.pack(pady=5, fill=tk.X)

        self.status_label = tk.Label(root, text="状态：空闲")
        self.status_label.pack(pady=5)

        # 定时任务设置
        schedule.every().day.at("06:00").do(self.run_scheduled_task)
        self.root.after(1000, self.check_schedule)

        # 事件绑定
        self.root.bind('<<StopRecording>>', self.on_stop_recording)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.root.withdraw()
            self.root.title("正在录制中...按ESC停止")
            self.status_label.config(text="状态：录制中...按ESC停止")
            self.events = []
            self.start_time = time.time()
            
            threading.Thread(target=self.start_listeners, daemon=True).start()

    def start_listeners(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press
        )
        with self.mouse_listener as m_listener, self.keyboard_listener as k_listener:
            m_listener.join()
            k_listener.join()

    def on_move(self, x, y):
        if self.recording:
            self.events.append({
                'type': 'mouse_move',
                'x': x,
                'y': y,
                'time': time.time() - self.start_time
            })

    def on_click(self, x, y, button, pressed):
        if self.recording and pressed:
            self.events.append({
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': button.name,
                'time': time.time() - self.start_time
            })

    def on_press(self, key):
        if self.recording:
            try:
                key_name = key.char
            except AttributeError:
                key_name = key.name
            
            if key == keyboard.Key.esc:
                # 使用after确保在主线程处理GUI操作
                self.root.after(0, self.root.event_generate, '<<StopRecording>>')
                return False  # 停止键盘监听器
            else:
                self.events.append({
                    'type': 'key_press',
                    'key': key_name,
                    'time': time.time() - self.start_time
                })

    def on_stop_recording(self, event):
        if self.recording:
            self.recording = False
            # 强制停止所有监听器
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            
            # 恢复窗口并置顶
            self.root.deiconify()
            self.root.title("动作录制器")
            self.root.lift()
            self.root.focus_force()
            self.status_label.config(text="状态：空闲（按导出按钮保存录制数据）")

    def export_recording(self):
        if not self.events:
            messagebox.showwarning("警告", "没有录制的数据可以导出！")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    json.dump(self.events, f, indent=2)
                messagebox.showinfo("成功", f"录制数据已保存到：\n{filepath}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败：{str(e)}")

    def import_and_play(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    events = json.load(f)
                self.status_label.config(text="状态：正在回放...")
                threading.Thread(target=self.replay_actions, args=(events,), daemon=True).start()
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败：{str(e)}")

    def replay_actions(self, events):
        try:
            start_time = time.time()
            last_time = 0
            pyautogui.PAUSE = 0.01  # 提高操作精度
            
            for event in events:
                current_delay = event['time'] - last_time
                if current_delay > 0:
                    time.sleep(current_delay)
                
                last_time = event['time']
                
                if event['type'] == 'mouse_move':
                    pyautogui.moveTo(event['x'], event['y'])
                elif event['type'] == 'mouse_click':
                    pyautogui.click(event['x'], event['y'], button=event['button'])
                elif event['type'] == 'key_press':
                    pyautogui.press(event['key'])
        finally:
            self.root.after(0, lambda: self.status_label.config(text="状态：空闲"))

    def run_scheduled_task(self):
        try:
            with open('actions.json', 'r') as f:
                events = json.load(f)
            self.replay_actions(events)
        except Exception as e:
            messagebox.showerror("错误", f"定时任务执行失败: {str(e)}")

    def check_schedule(self):
        schedule.run_pending()
        self.root.after(1000, self.check_schedule)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()