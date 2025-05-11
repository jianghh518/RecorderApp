import tkinter as tk
import tkinter.messagebox as messagebox

class LoginApp:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("12306自动登录")
        self.root.geometry("600x400")
        self.root.configure(bg='white')
        self.root.resizable(False, False)  # 禁止窗口大小调整

        # 设置窗口位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")

        # 创建左侧视觉面板
        self.left_frame = tk.Frame(self.root, width=200, bg='lightblue')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.left_frame, text="欢迎使用", font=("Arial", 16), bg='lightblue').pack(pady=20)

        # 创建右侧登录面板
        self.right_frame = tk.Frame(self.root, width=400, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(self.right_frame, text="12306自动登录", font=("Arial", 16), bg='white').pack(pady=20)
        tk.Label(self.right_frame, text="用户名:", font=("Arial", 12), bg='white').pack(pady=5)
        self.username_entry = tk.Entry(self.right_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        tk.Label(self.right_frame, text="密码:", font=("Arial", 12), bg='white').pack(pady=5)
        self.password_entry = tk.Entry(self.right_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # 创建按钮
        self.login_button = tk.Button(self.right_frame, text="登录", command=self.login, font=("Arial", 12), bg='lightblue')
        self.login_button.pack(pady=10)
        self.clear_button = tk.Button(self.right_frame, text="清除", command=self.clear, font=("Arial", 12), bg='lightblue')
        self.clear_button.pack(pady=10)
        self.exit_button = tk.Button(self.right_frame, text="退出", command=self.exit, font=("Arial", 12), bg='lightblue')
        self.exit_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "" or password == "":
            messagebox.showwarning("输入错误", "请输入用户名和密码！")
        else:
            if username == "admire" and password == "O123456":
                messagebox.showinfo("登录成功", "欢迎回来！")
            else:
                messagebox.showerror("登录失败", "用户名或密码错误！")

    def clear(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("清除成功", "用户名和密码已清除！")

    def exit(self):
        self.root.quit()
        messagebox.showinfo("退出", "感谢使用！")

if __name__ == "__main__":
    app = LoginApp()
    app.root.mainloop()
