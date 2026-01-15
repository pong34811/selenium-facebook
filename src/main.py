import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def start_facebook_automation():
    # 1. ตั้งค่า Chrome Options (ใส่เพื่อให้ Browser ไม่ปิดตัวเองทันที)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    # 2. ติดตั้งและเปิด Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 3. ไปที่หน้า Facebook
        print("กำลังเปิด Facebook...")
        driver.get("https://www.facebook.com")

        # 4. หยุดรอให้ผู้ใช้ทำรายการเอง
        print("-" * 30)
        print("คำแนะนำ:")
        print("1. กรุณาพิมพ์ Username/Password และ Login ในหน้า Browser ให้เรียบร้อย")
        print("2. หากติด 2FA (รหัสยืนยันตัวตน) ให้จัดการให้เสร็จจนถึงหน้า Feed")
        print("3. เมื่อ Login สำเร็จแล้ว ให้กลับมาที่หน้าจอนี้แล้วกด Enter")
        print("-" * 30)
        
        input(">>> Login เสร็จแล้วใช่ไหม? ถ้าใช่แล้ว กด Enter เพื่อไปที่กลุ่มต่อได้เลย...")

        # 5. ไปที่ลิงก์กลุ่มที่คุณต้องการ
        group_url = "https://www.facebook.com/groups/831395294760364"
        print(f"กำลังย้ายไปที่กลุ่ม: {group_url}")
        driver.get(group_url)

        print("ขณะนี้คุณอยู่ที่หน้ากลุ่มเรียบร้อยแล้ว!")
        time.sleep(2)

        # 6. กดปุ่ม "เขียนอะไรสักหน่อย..."
        try:
            print("กำลังค้นหาปุ่มโพสต์...")
            wait = WebDriverWait(driver, 10)
            # ใช้ XPath เพื่อหา Element ที่มีคำว่า 'เขียนอะไรสักหน่อย'
            post_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'เขียนอะไรสักหน่อย')]")))
            post_btn.click()
            print("กดปุ่ม 'เขียนอะไรสักหน่อย...' เรียบร้อยแล้ว!")
        except Exception as click_err:
            print(f"หาปุ่มไม่เจอ หรือกดไม่ได้: {click_err}")
        time.sleep(2)
        # 7. พิมพ์ข้อความ
        try:
            print("กำลังรอช่องใส่ข้อความ...")
            # รอให้กล่องข้อความปรากฏ (หาจาก aria-placeholder)
            text_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-placeholder='สร้างโพสต์สาธารณะ...']")))
            text_box.click() # คลิกเพื่อให้แน่ใจว่า focus
            text_box.send_keys("ฝากกดติดตามผมด้วยนะครับ")
            print("พิมพ์ข้อความเรียบร้อยแล้ว!")
        except Exception as type_err:
            print(f"หาช่องข้อความไม่เจอ หรือพิมพ์ไม่ได้: {type_err}")
        time.sleep(2)
        # 8. กดปุ่มโพสต์ (Post)
        try:
            print("กำลังค้นหาปุ่มโพสต์ (ขั้นตอนสุดท้าย)...")
            # ใช้วิธีหาจาก aria-label="โพสต์" ที่เป็น role="button"
            final_post_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='โพสต์' and @role='button']")))
            final_post_btn.click()
            print("กดโพสต์เรียบร้อยแล้ว! (เสร็จสิ้น)")
        except Exception as post_err:
            print(f"กดปุ่มโพสต์ไม่ได้: {post_err}")
        time.sleep(2)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    start_facebook_automation()