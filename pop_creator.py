import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import platform

class PopCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ポップ作成ツール")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        
        self.background_image = None
        self.background_path = None
        self.preview_image = None
        
        # Text positioning (percentages of canvas size)
        self.text_positions = {
            'product_name': {'x': 50, 'y': 15},
            'quantity': {'x': 50, 'y': 28},
            'original_price': {'x': 50, 'y': 44},
            'discount_price': {'x': 50, 'y': 57},
            'tax_price': {'x': 50, 'y': 75},
            'tax_label': {'x': 50, 'y': 92}
        }
        
        # Text colors (default)
        self.text_colors = {
            'product_name': '#1a1a1a',
            'quantity': '#333333',
            'original_price': '#999999',
            'discount_price': '#e53e3e',
            'tax_price': '#c53030',
            'tax_label': '#c53030'
        }
        
        # Text sizes (base sizes that will be scaled)
        self.text_sizes = {
            'product_name': 120,
            'quantity': 80,
            'original_price': 70,
            'discount_price': 90,
            'tax_price': 180,
            'tax_label': 60
        }
        
        # Font selection
        self.selected_font = 'msgothic.ttc'
        self.available_fonts = {
            'MS Gothic': 'msgothic.ttc',
            'MS Mincho': 'msmincho.ttc',
            'Meiryo': 'meiryo.ttc',
            'Meiryo Bold': 'meiryob.ttc',
            'HG創英角ポップ体': 'HGRPP1.TTC',
            'HG創英角ゴシックUB': 'HGRSGU.TTC',
            'Arial': 'arial.ttf',
            'Arial Bold': 'arialbd.ttf',
            'Times New Roman': 'times.ttf',
            'Times New Roman Bold': 'timesbd.ttf',
            'Verdana': 'verdana.ttf',
            'Georgia': 'georgia.ttf'
        }
        
        # Font for each text element
        self.text_fonts = {
            'product_name': 'MS Gothic',
            'quantity': 'MS Gothic',
            'original_price': 'MS Gothic',
            'discount_price': 'MS Gothic',
            'tax_price': 'MS Gothic',
            'tax_label': 'MS Gothic'
        }
        
        # Selected text element for editing
        self.selected_element = None
        
        # Determine system font directory
        self.font_dir = self.get_font_directory()
        
        self.setup_ui()
    
    def get_font_directory(self):
        """Get the system font directory based on OS"""
        system = platform.system()
        if system == 'Windows':
            return 'C:\\Windows\\Fonts\\'
        elif system == 'Darwin':  # macOS
            return '/System/Library/Fonts/'
        else:  # Linux
            return '/usr/share/fonts/'
    
    def get_font_path(self, font_file):
        """Get full path to font file"""
        return os.path.join(self.font_dir, font_file)
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Input section
        left_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create scrollable frame for left panel
        left_canvas = tk.Canvas(left_frame, bg='white', highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        scrollable_left = tk.Frame(left_canvas, bg='white')
        
        scrollable_left.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=scrollable_left, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                left_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                left_canvas.yview_scroll(1, "units")
        
        # Bind mouse wheel events
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/Mac
        left_canvas.bind_all("<Button-4>", _on_mousewheel_linux)  # Linux scroll up
        left_canvas.bind_all("<Button-5>", _on_mousewheel_linux)  # Linux scroll down
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Title
        title_label = tk.Label(scrollable_left, text="🏪 ポップ作成ツール", 
                               font=('Arial', 20, 'bold'), bg='white', fg='#667eea')
        title_label.pack(pady=20)
        
        # Input fields container
        input_container = tk.Frame(scrollable_left, bg='white')
        input_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Background image upload
        tk.Label(input_container, text="背景画像", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(10, 5))
        
        upload_frame = tk.Frame(input_container, bg='white')
        upload_frame.pack(fill=tk.X, pady=5)
        
        self.upload_btn = tk.Button(upload_frame, text="画像を選択", 
                                    command=self.upload_background,
                                    bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                                    padx=20, pady=10, cursor='hand2')
        self.upload_btn.pack(side=tk.LEFT)
        
        self.file_label = tk.Label(upload_frame, text="未選択", bg='white', 
                                   fg='#666', font=('Arial', 9))
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Product name
        tk.Label(input_container, text="商品名", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 5))
        self.product_name = tk.Entry(input_container, font=('Arial', 11), width=40)
        self.product_name.pack(fill=tk.X, pady=5)
        self.product_name.bind('<KeyRelease>', lambda e: self.generate_pop())
        
        # Quantity type selection
        tk.Label(input_container, text="数量", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 5))
        
        quantity_type_frame = tk.Frame(input_container, bg='white')
        quantity_type_frame.pack(fill=tk.X, pady=5)
        
        self.quantity_type = tk.StringVar(value="個")
        tk.Radiobutton(quantity_type_frame, text="個", variable=self.quantity_type, 
                      value="個", bg='white', font=('Arial', 10),
                      command=self.generate_pop).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(quantity_type_frame, text="g", variable=self.quantity_type, 
                      value="g", bg='white', font=('Arial', 10),
                      command=self.generate_pop).pack(side=tk.LEFT)
        
        self.quantity = tk.Entry(input_container, font=('Arial', 11), width=40)
        self.quantity.pack(fill=tk.X, pady=5)
        self.quantity.bind('<KeyRelease>', lambda e: self.generate_pop())
        
        # Original price
        tk.Label(input_container, text="元値(税抜)", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 5))
        self.original_price = tk.Entry(input_container, font=('Arial', 11), width=40)
        self.original_price.pack(fill=tk.X, pady=5)
        self.original_price.bind('<KeyRelease>', lambda e: self.generate_pop())
        
        # Discount price
        tk.Label(input_container, text="割引値(税込)", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 5))
        self.discount_price = tk.Entry(input_container, font=('Arial', 11), width=40)
        self.discount_price.pack(fill=tk.X, pady=5)
        self.discount_price.bind('<KeyRelease>', lambda e: self.generate_pop())
        
        # Tax included price
        tk.Label(input_container, text="税抜価格", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 5))
        self.tax_included_price = tk.Entry(input_container, font=('Arial', 11), width=40)
        self.tax_included_price.pack(fill=tk.X, pady=5)
        self.tax_included_price.bind('<KeyRelease>', lambda e: self.generate_pop())
        
        # Separator
        separator1 = ttk.Separator(input_container, orient='horizontal')
        separator1.pack(fill=tk.X, pady=20)
        
        # Font and Color Settings
        tk.Label(input_container, text="フォント・色設定", font=('Arial', 14, 'bold'), 
                bg='white', fg='#667eea').pack(anchor='w', pady=(10, 10))
        
        # Define element options (used by multiple controls)
        element_options = ['商品名', '数量', '元値', '割引値', '税抜価格', '税抜ラベル']
        
        # Font selection
        font_frame = tk.Frame(input_container, bg='white')
        font_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(font_frame, text="フォントを変更する要素:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.font_element_var = tk.StringVar(value='商品名')
        self.font_element_combo = ttk.Combobox(font_frame, textvariable=self.font_element_var, 
                                               values=element_options, state='readonly', width=15)
        self.font_element_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.font_element_combo.bind('<<ComboboxSelected>>', self.load_element_font)
        
        font_select_frame = tk.Frame(input_container, bg='white')
        font_select_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(font_select_frame, text="フォント:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.font_var = tk.StringVar(value='MS Gothic')
        font_options = [
            'MS Gothic', 'MS Mincho', 'Meiryo', 'Meiryo Bold',
            'HG創英角ポップ体', 'HG創英角ゴシックUB',
            'Arial', 'Arial Bold', 'Times New Roman', 'Times New Roman Bold',
            'Verdana', 'Georgia'
        ]
        self.font_combo = ttk.Combobox(font_select_frame, textvariable=self.font_var, 
                                       values=font_options, state='readonly', width=25)
        self.font_combo.pack(side=tk.LEFT)
        self.font_combo.bind('<<ComboboxSelected>>', self.update_font)
        
        # Text element selector for color
        element_frame = tk.Frame(input_container, bg='white')
        element_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(element_frame, text="色を変更する要素:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.element_var = tk.StringVar(value='商品名')
        self.element_combo = ttk.Combobox(element_frame, textvariable=self.element_var, 
                                          values=element_options, state='readonly', width=15)
        self.element_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.color_btn = tk.Button(element_frame, text="色を選択", 
                                   command=self.choose_color,
                                   bg='#667eea', fg='white', font=('Arial', 9, 'bold'),
                                   padx=10, pady=5, cursor='hand2')
        self.color_btn.pack(side=tk.LEFT)
        
        # Text size control
        size_frame = tk.Frame(input_container, bg='white')
        size_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(size_frame, text="サイズを変更する要素:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.size_element_var = tk.StringVar(value='商品名')
        self.size_element_combo = ttk.Combobox(size_frame, textvariable=self.size_element_var, 
                                               values=element_options, state='readonly', width=15)
        self.size_element_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.size_element_combo.bind('<<ComboboxSelected>>', self.load_element_size)
        
        # Size slider
        size_slider_frame = tk.Frame(input_container, bg='white')
        size_slider_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(size_slider_frame, text="文字サイズ:", bg='white', font=('Arial', 10), width=12, anchor='w').pack(side=tk.LEFT)
        self.size_slider = tk.Scale(size_slider_frame, from_=20, to=300, orient=tk.HORIZONTAL, 
                                    bg='white', command=self.update_size)
        self.size_slider.set(120)
        self.size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.size_value_label = tk.Label(size_slider_frame, text="120", bg='white', font=('Arial', 10), width=5)
        self.size_value_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Separator
        separator2 = ttk.Separator(input_container, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        
        # Position Settings
        tk.Label(input_container, text="位置調整", font=('Arial', 14, 'bold'), 
                bg='white', fg='#667eea').pack(anchor='w', pady=(10, 10))
        
        # Element selector for position
        position_element_frame = tk.Frame(input_container, bg='white')
        position_element_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(position_element_frame, text="移動する要素:", bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.position_element_var = tk.StringVar(value='商品名')
        self.position_element_combo = ttk.Combobox(position_element_frame, textvariable=self.position_element_var, 
                                                   values=element_options, state='readonly', width=15)
        self.position_element_combo.pack(side=tk.LEFT)
        
        # X position slider
        x_frame = tk.Frame(input_container, bg='white')
        x_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(x_frame, text="横位置 (X):", bg='white', font=('Arial', 10), width=12, anchor='w').pack(side=tk.LEFT)
        self.x_slider = tk.Scale(x_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                bg='white', command=self.update_position)
        self.x_slider.set(50)
        self.x_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Y position slider
        y_frame = tk.Frame(input_container, bg='white')
        y_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(y_frame, text="縦位置 (Y):", bg='white', font=('Arial', 10), width=12, anchor='w').pack(side=tk.LEFT)
        self.y_slider = tk.Scale(y_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                bg='white', command=self.update_position)
        self.y_slider.set(50)
        self.y_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Update sliders when element selection changes
        self.position_element_combo.bind('<<ComboboxSelected>>', self.load_element_position)
        
        # Separator
        separator3 = ttk.Separator(input_container, orient='horizontal')
        separator3.pack(fill=tk.X, pady=20)
        
        # Buttons
        button_frame = tk.Frame(input_container, bg='white')
        button_frame.pack(fill=tk.X, pady=30)
        
        self.generate_btn = tk.Button(button_frame, text="ポップを生成", 
                                     command=self.generate_pop,
                                     bg='#667eea', fg='white', 
                                     font=('Arial', 12, 'bold'),
                                     padx=20, pady=12, cursor='hand2')
        self.generate_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.download_btn = tk.Button(button_frame, text="画像を保存", 
                                     command=self.save_pop,
                                     bg='#10b981', fg='white', 
                                     font=('Arial', 12, 'bold'),
                                     padx=20, pady=12, cursor='hand2',
                                     state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
        
        # Right panel - Preview section
        right_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        preview_label = tk.Label(right_frame, text="プレビュー", 
                                font=('Arial', 16, 'bold'), bg='white', fg='#333')
        preview_label.pack(pady=20)
        
        # Canvas for preview (will be resized dynamically)
        self.canvas_frame = tk.Frame(right_frame, bg='#f5f5f5')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Initial canvas with default size
        self.canvas = tk.Canvas(self.canvas_frame, width=432, height=768, 
                               bg='white', highlightthickness=1, 
                               highlightbackground='#ccc')
        self.canvas.pack(pady=10)
        
    def choose_color(self):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.element_var.get())
        if element_key:
            current_color = self.text_colors.get(element_key, '#000000')
            color = colorchooser.askcolor(title="色を選択", initialcolor=current_color)
            if color[1]:  # color[1] is the hex value
                self.text_colors[element_key] = color[1]
                self.generate_pop()
    
    def load_element_position(self, event=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.position_element_var.get())
        if element_key and element_key in self.text_positions:
            pos = self.text_positions[element_key]
            self.x_slider.set(pos['x'])
            self.y_slider.set(pos['y'])
    
    def load_element_size(self, event=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.size_element_var.get())
        if element_key and element_key in self.text_sizes:
            size = self.text_sizes[element_key]
            self.size_slider.set(size)
            self.size_value_label.config(text=str(size))
    
    def load_element_font(self, event=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.font_element_var.get())
        if element_key and element_key in self.text_fonts:
            font_name = self.text_fonts[element_key]
            self.font_var.set(font_name)
    
    def update_position(self, value=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.position_element_var.get())
        if element_key:
            self.text_positions[element_key] = {
                'x': self.x_slider.get(),
                'y': self.y_slider.get()
            }
            self.generate_pop()
    
    def update_size(self, value=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.size_element_var.get())
        if element_key:
            size = int(self.size_slider.get())
            self.text_sizes[element_key] = size
            self.size_value_label.config(text=str(size))
            self.generate_pop()
    
    def update_font(self, event=None):
        element_map = {
            '商品名': 'product_name',
            '数量': 'quantity',
            '元値': 'original_price',
            '割引値': 'discount_price',
            '税抜価格': 'tax_price',
            '税抜ラベル': 'tax_label'
        }
        
        element_key = element_map.get(self.font_element_var.get())
        if element_key:
            font_name = self.font_var.get()
            self.text_fonts[element_key] = font_name
            self.generate_pop()
    
    def upload_background(self):
        file_path = filedialog.askopenfilename(
            title="背景画像を選択",
            filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp *.gif"), 
                      ("すべてのファイル", "*.*")]
        )
        
        if file_path:
            try:
                self.background_image = Image.open(file_path)
                self.background_path = file_path
                filename = os.path.basename(file_path)
                self.file_label.config(text=filename, fg='#10b981')
                self.generate_pop()
            except Exception as e:
                messagebox.showerror("エラー", f"画像を読み込めませんでした: {str(e)}")
    
    def generate_pop(self):
        # Determine canvas size based on background image
        if self.background_image:
            canvas_width, canvas_height = self.background_image.size
        else:
            # Default size if no background
            canvas_width, canvas_height = 1920, 1080
        
        # Create image
        pop_image = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(pop_image)
        
        # Draw background if available
        if self.background_image:
            pop_image.paste(self.background_image, (0, 0))
            draw = ImageDraw.Draw(pop_image)
        
        # Load fonts (use default if custom fonts not available)
        # Scale font sizes based on image height
        scale = canvas_height / 1080
        
        # Load fonts for each text element individually
        # Try to load the selected font, fallback to MS Gothic, then to default
        def load_font_for_element(element_key, size):
            font_name = self.text_fonts.get(element_key, 'MS Gothic')
            font_file = self.available_fonts.get(font_name, 'msgothic.ttc')
            font_path = self.get_font_path(font_file)
            
            for fallback_font in [font_path, self.get_font_path('msgothic.ttc'), self.get_font_path('arial.ttf')]:
                try:
                    return ImageFont.truetype(fallback_font, int(size * scale))
                except Exception as e:
                    continue
            
            # Final fallback to PIL default font
            return ImageFont.load_default()
        
        font_title = load_font_for_element('product_name', self.text_sizes['product_name'])
        font_quantity = load_font_for_element('quantity', self.text_sizes['quantity'])
        font_original = load_font_for_element('original_price', self.text_sizes['original_price'])
        font_discount = load_font_for_element('discount_price', self.text_sizes['discount_price'])
        font_tax_price = load_font_for_element('tax_price', self.text_sizes['tax_price'])
        font_tax_label = load_font_for_element('tax_label', self.text_sizes['tax_label'])
        
        # Get values
        product_name = self.product_name.get()
        quantity = self.quantity.get()
        quantity_type = self.quantity_type.get()
        original_price = self.original_price.get()
        discount_price = self.discount_price.get()
        tax_included_price = self.tax_included_price.get()
        
        # Draw product name
        if product_name:
            bbox = draw.textbbox((0, 0), product_name, font=font_title)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['product_name']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), product_name, fill=self.text_colors['product_name'], font=font_title)
        
        # Draw quantity
        if quantity:
            quantity_text = f"{quantity}{quantity_type}"
            bbox = draw.textbbox((0, 0), quantity_text, font=font_quantity)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['quantity']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), quantity_text, fill=self.text_colors['quantity'], font=font_quantity)
        
        # Draw original price with strikethrough
        if original_price:
            original_text = f"{original_price}円(税抜)"
            bbox = draw.textbbox((0, 0), original_text, font=font_original)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['original_price']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), original_text, fill=self.text_colors['original_price'], font=font_original)
            
            # Draw strikethrough
            line_y = y + int(30 * scale)
            draw.line([(x, line_y), (x + text_width, line_y)], fill='#ff0000', width=int(8 * scale))
        
        # Draw discount price
        if discount_price:
            discount_text = f"{discount_price}円(税込)"
            bbox = draw.textbbox((0, 0), discount_text, font=font_discount)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['discount_price']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), discount_text, fill=self.text_colors['discount_price'], font=font_discount)
        
        # Draw tax included price (largest)
        if tax_included_price:
            tax_text = f"{tax_included_price}円"
            bbox = draw.textbbox((0, 0), tax_text, font=font_tax_price)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['tax_price']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), tax_text, fill=self.text_colors['tax_price'], font=font_tax_price)
            
            # Draw "税抜" label
            tax_label = "税抜"
            bbox = draw.textbbox((0, 0), tax_label, font=font_tax_label)
            text_width = bbox[2] - bbox[0]
            pos = self.text_positions['tax_label']
            x = int((canvas_width * pos['x'] / 100) - text_width / 2)
            y = int(canvas_height * pos['y'] / 100)
            draw.text((x, y), tax_label, fill=self.text_colors['tax_label'], font=font_tax_label)
        
        # Save for export
        self.current_pop = pop_image
        
        # Update canvas size based on image
        max_preview_width = 600
        max_preview_height = 700
        
        aspect_ratio = canvas_width / canvas_height
        
        if aspect_ratio > max_preview_width / max_preview_height:
            # Width is limiting factor
            preview_width = max_preview_width
            preview_height = int(max_preview_width / aspect_ratio)
        else:
            # Height is limiting factor
            preview_height = max_preview_height
            preview_width = int(max_preview_height * aspect_ratio)
        
        # Resize canvas to match preview
        self.canvas.config(width=preview_width, height=preview_height)
        
        # Create preview
        preview = pop_image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(preview)
        
        # Display on canvas (centered)
        self.canvas.delete("all")
        self.canvas.create_image(preview_width // 2, preview_height // 2, image=self.preview_image)
        
        # Enable download button
        self.download_btn.config(state=tk.NORMAL)
    
    def save_pop(self):
        if not hasattr(self, 'current_pop'):
            messagebox.showwarning("警告", "まずポップを生成してください")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG画像", "*.png"), ("JPEG画像", "*.jpg"), ("すべてのファイル", "*.*")],
            initialfile=f"pop_{self.product_name.get() or 'output'}.png"
        )
        
        if file_path:
            try:
                self.current_pop.save(file_path, quality=95)
                messagebox.showinfo("成功", f"画像を保存しました:\n{file_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"保存に失敗しました: {str(e)}")

def main():
    root = tk.Tk()
    app = PopCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
