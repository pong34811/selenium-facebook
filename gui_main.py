import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class FacebookAutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Group Auto Poster")
        self.root.geometry("600x500")
        
        self.driver = None
        self.wait = None

        # Styles
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=5)
        style.configure("TLabel", font=("Segoe UI", 10))

        # --- UI Components ---

        # 1. Group URL
        url_frame = ttk.Frame(root, padding=10)
        url_frame.pack(fill=tk.X)
        ttk.Label(url_frame, text="Group URL:").pack(anchor=tk.W)
        self.url_var = tk.StringVar(value="https://www.facebook.com/groups/831395294760364")
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(fill=tk.X, pady=5)

        # 2. Message to Post
        msg_frame = ttk.Frame(root, padding=10)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(msg_frame, text="Message:").pack(anchor=tk.W)
        self.msg_text = tk.Text(msg_frame, height=5, font=("Segoe UI", 10))
        self.msg_text.insert("1.0", "ฝากกดติดตามผมด้วยนะครับ")
        self.msg_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # 3. Control Buttons
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=tk.X)
        
        self.btn_open = ttk.Button(btn_frame, text="1. Open Facebook & Login", command=self.open_browser)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        self.btn_post = ttk.Button(btn_frame, text="2. Start Posting", command=self.start_posting, state=tk.DISABLED)
        self.btn_post.pack(side=tk.LEFT, padx=5)

        # 4. Logs
        log_frame = ttk.LabelFrame(root, text="Logs", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, state='disabled', font=("Consolas", 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        def _log_update():
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, f"{message}\n")
            self.log_area.see(tk.END)
            self.log_area.config(state='disabled')
        self.root.after(0, _log_update)

    def open_browser(self):
        threading.Thread(target=self._open_browser_thread, daemon=True).start()

    def _open_browser_thread(self):
        try:
            self.log("Initializing Chrome Driver...")
            self.btn_open.config(state=tk.DISABLED)
            
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            
            # Disable notifications to prevent pops interfering
            chrome_options.add_argument("--disable-notifications")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)

            self.log("Opening Facebook...")
            self.driver.get("https://www.facebook.com")
            
            self.log("-" * 30)
            self.log("Please login manually in the browser.")
            self.log("If 2FA is required, complete it.")
            self.log("Once you see the News Feed, come back here and click 'Start Posting'.")
            self.log("-" * 30)

            # Enable the Post button
            self.root.after(0, lambda: self.btn_post.config(state=tk.NORMAL))
            
        except Exception as e:
            self.log(f"Error opening browser: {e}")
            self.root.after(0, lambda: self.btn_open.config(state=tk.NORMAL))

    def start_posting(self):
        if not self.driver:
            messagebox.showerror("Error", "Browser is not open!")
            return
        
        threading.Thread(target=self._post_thread, daemon=True).start()

    def _post_thread(self):
        try:
            self.btn_post.config(state=tk.DISABLED)
            target_group = self.url_var.get()
            message_content = self.msg_text.get("1.0", tk.END).strip()

            if not target_group:
                self.log("Error: Group URL is empty.")
                return

            self.log(f"Navigating to group: {target_group}")
            self.driver.get(target_group)
            
            time.sleep(3) # Wait for load

            # Join group check could be added here, but let's stick to original logic
            
            # 1. Click "Write something..."
            self.log("Looking for post button...")
            try:
                # Try multiple selectors for better robustness
                post_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'เขียนอะไรสักหน่อย')]")))
                post_btn.click()
                self.log("Clicked 'Write something...'")
            except Exception as e:
                self.log(f"Failed to find first post button: {e}")
                self.log("Trying alternative method...")
                # Could add fallback here if needed
                raise e

            time.sleep(2)

            # 2. Type message
            self.log("Waiting for text box...")
            try:
                # Based on original script logic
                text_box = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-placeholder='สร้างโพสต์สาธารณะ...']")))
                text_box.click()
                text_box.send_keys(message_content)
                self.log("Message typed.")
            except Exception as e:
                self.log(f"Failed to find text box: {e}")
                raise e

            time.sleep(2)

            # 3. Click Post
            self.log("Looking for final Post button...")
            try:
                final_post_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='โพสต์' and @role='button']")))
                final_post_btn.click()
                self.log("Clicked Post button! Success.")
                messagebox.showinfo("Success", "Post submited successfully!")
            except Exception as e:
                self.log(f"Failed to click final Post button: {e}")
                raise e

        except Exception as e:
            self.log(f"Error during posting: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.root.after(0, lambda: self.btn_post.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutoGUI(root)
    root.mainloop()
