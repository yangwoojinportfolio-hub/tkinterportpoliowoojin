import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance

class CleanPhotoshop:
    def __init__(self, root):
        self.root = root
        self.root.title("파이썬 미니 포토샵")
        self.root.geometry("900x650")
        
        self.orig_img = None
        self.curr_img = None
        self.tk_img = None
        
        # 레이아웃 배치
        self.side_bar = tk.Frame(root, width=200, bg="#f0f0f0", relief="sunken", bd=2)
        self.side_bar.pack(side="left", fill="y", padx=5, pady=5)
        self.side_bar.pack_propagate(False)
        
        self.canvas = tk.Canvas(root, bg="#2b2b2b")
        self.canvas.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.create_menu()
        
    def create_menu(self):
        tk.Label(self.side_bar, text="🧰 포토샵 메뉴", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # 파일 버튼
        tk.Button(self.side_bar, text="📂 사진 가져오기", command=self.load_image, bg="#d1e7dd", width=20).pack(pady=3)
        tk.Button(self.side_bar, text="💾 사진 저장하기", command=self.save_image, bg="#cfe2ff", width=20).pack(pady=3)
        
        # 크기 및 회전
        tk.Frame(self.side_bar, height=1, bg="#ccc").pack(fill="x", pady=10)
        tk.Button(self.side_bar, text="확대 (+)", command=lambda: self.resize_img(1.2), width=20).pack(pady=2)
        tk.Button(self.side_bar, text="축소 (-)", command=lambda: self.resize_img(0.8), width=20).pack(pady=2)
        tk.Button(self.side_bar, text="회전 ↻", command=self.rotate_img, width=20).pack(pady=2)
        tk.Button(self.side_bar, text="좌우반전 ↔", command=self.flip_img, width=20).pack(pady=2)
        
        # 보정 슬라이더
        tk.Frame(self.side_bar, height=1, bg="#ccc").pack(fill="x", pady=10)
        tk.Label(self.side_bar, text="☀️ 밝기 조절", bg="#f0f0f0", font=("Arial", 9)).pack(anchor="w", padx=15)
        self.bright_scale = tk.Scale(self.side_bar, from_=0.2, to=2.0, resolution=0.1, orient="horizontal", command=self.update_effect)
        self.bright_scale.set(1.0)
        self.bright_scale.pack(fill="x", padx=15, pady=2)
        
        # 필터 및 문자
        tk.Frame(self.side_bar, height=1, bg="#ccc").pack(fill="x", pady=10)
        tk.Button(self.side_bar, text="🎨 흑백 필터", command=self.apply_gray, width=20).pack(pady=2)
        tk.Button(self.side_bar, text="📝 글자 넣기", command=self.add_text, bg="#fff3cd", width=20).pack(pady=2)
        
        # 리셋 버튼
        tk.Button(self.side_bar, text="🚨 전체 초기화", command=self.reset_img, bg="#f8d7da", width=20).pack(side="bottom", pady=15)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if path:
            self.orig_img = Image.open(path).convert("RGBA")
            self.orig_img.thumbnail((500, 500))
            self.curr_img = self.orig_img.copy()
            self.bright_scale.set(1.0)
            self.show()
            
    def save_image(self):
        if not self.curr_img: return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG 파일", "*.png"), ("JPG 파일", "*.jpg")])
        if path:
            out = self.curr_img.copy()
            if path.lower().endswith(('.jpg', '.jpeg')): out = out.convert("RGB")
            out.save(path)
            messagebox.showinfo("성공", "저장되었습니다!")

    def show(self):
        if self.curr_img:
            self.canvas.delete("all")
            self.tk_img = ImageTk.PhotoImage(self.curr_img)
            self.root.update_idletasks()
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            if w <= 1: w, h = 650, 600
            self.canvas.create_image(w // 2, h // 2, image=self.tk_img)

    def resize_img(self, factor):
        if self.curr_img:
            w, h = self.curr_img.size
            self.curr_img = self.curr_img.resize((int(w * factor), int(h * factor)))
            self.show()

    def rotate_img(self):
        if self.curr_img:
            self.curr_img = self.curr_img.rotate(-90, expand=True, fillcolor=(0,0,0,0))
            self.show()

    def flip_img(self):
        if self.curr_img:
            self.curr_img = self.curr_img.transpose(Image.FLIP_LEFT_RIGHT)
            self.show()

    def update_effect(self, event=None):
        if self.orig_img and self.curr_img:
            enhancer = ImageEnhance.Brightness(self.curr_img)
            self.curr_img = enhancer.enhance(self.bright_scale.get())
            self.show()

    def apply_gray(self):
        if self.curr_img:
            r, g, b, a = self.curr_img.split()
            gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b))).convert("RGBA")
            gray.putalpha(a)
            self.curr_img = gray
            self.show()

    def add_text(self):
        if not self.curr_img: return
        txt = simpledialog.askstring("글자 입력", "사진에 넣을 문구를 적으세요:")
        if txt:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(self.curr_img)
            try: font = ImageFont.truetype("malgun.ttf", 30) # 윈도우 맑은고딕
            except: font = ImageFont.load_default()
            w, h = self.curr_img.size
            draw.text((w // 2 - 40, h // 2), txt, fill=(255, 255, 255, 255), font=font)
            self.show()

    def reset_img(self):
        if self.orig_img:
            self.curr_img = self.orig_img.copy()
            self.bright_scale.set(1.0)
            self.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanPhotoshop(root)
    root.mainloop()
