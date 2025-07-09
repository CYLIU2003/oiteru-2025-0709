import tkinter as tk
from tkinter import ttk
import datetime
import os
import base64
from tkinter import messagebox
import mydb20250506 as mydb
from mydb20250506 import get_db_connection

# ── 1. まず root を生成 ─────────────────────────────────────
root = tk.Tk()
root.title("オイテル登録システム - Tokyo City University / Tokyu Group")
root.minsize(900, 700)
root.configure(bg="#FAFAFA")

# ── 2. Style 設定 ─────────────────────────────────────────
style = ttk.Style(root)
try:
    style.theme_use("clam")
except tk.TclError:
    pass

# ── 3. データベース初期化 ───────────────────────────────────
mydb.set_up()

# ── 4. 日次処理タイマー定義 ─────────────────────────────────
def daycheck():
    mydb.set_up()
    root.after(24*60*60*1000, daycheck)

# 00:30 を考慮して起動後90秒で一度呼び出し、以降24hごと
root.after(90*1000, daycheck)

# --- Backend -------------------------------------------------
mydb.set_up()          # 再度呼んでも影響なし

# 起動時セットアップ（DB 作成・バックアップ）
def register_user(card_id, user_name, grade, user_class):
    try:
        db = mydb.create_server_connection("localhost", "root", "Hiramekigo@1", "userdb")
        cursor = db.cursor()
        sql = "INSERT INTO users (card_id, user_name, grade, class) VALUES (%s, %s, %s, %s)"
        val = (card_id, user_name, grade, user_class)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        show_error("ユーザー登録エラー", f"ユーザー登録中にエラーが発生しました: {e}")

# --- 日次処理 ------------------------------------------------
def daycheck():
    """毎日 1 回 DB を整理 & バックアップ（00:30 に実行）"""
    mydb.set_up()          # 再度呼んでも影響なし
    root.after(24*60*60*1000, daycheck)

# 00:30 抜けを考慮して 90 秒後に一度走らせ、以降は 24 h 毎
root.after(90*1000, daycheck)

# Define a modern color scheme reflecting Tokyo City University (Toshidai) and Tokyu Group
PRIMARY_COLOR = "#1976D2"    # Material Design Blue 700
SECONDARY_COLOR = "#26A8DF"  # Original bright blue (from Toshidai logo)
ACCENT_COLOR = "#FF5722"     # Material Design Deep Orange
DARK_TEXT = "#212121"        # Material Design Grey 900
LIGHT_TEXT = "#757575"       # Material Design Grey 600
LIGHT_BG = "#FAFAFA"         # Material Design Grey 50
CARD_BG = "#FFFFFF"          # Pure white for cards
SUCCESS_COLOR = "#4CAF50"    # Material Design Green
ERROR_COLOR = "#F44336"      # Material Design Red
FONT_FAMILY = "Segoe UI"     # Modern, consistent font
FONT_SIZE_LARGE = 16
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10

# Base64-encoded Tokyo City University logo (with Tokyu Group tagline)
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAABAAAAACeCAYAAACsPnijAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAcGVYSWZNTQAqAAAACAABBj9x
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAcGVYSWZNTQAqAAAACAABBj9x
AAAAGYktHRQAAGGzCgApAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEZ0lEQVR42u3cwW7UMBBF0Xk0
d72k5zaKITXFBPd0PwD83+coOiP0qtbACkuAQAAAAAAAAAAAAAAAAAAAHBPu7t7nK5uR5crV65c
Z/l3cM5j1PT3/Z4HAAAAAAAAAAAAAABgB9KeBgAAAAAAAAAAAACQLf8BAP7BZO5O3ZmXAAAAAElF
TkSuQmCC
""".strip()

# Initialize Tkinter root window
root = tk.Tk()
root.title("オイテル登録システム - Tokyo City University / Tokyu Group")
root.minsize(900, 700)
root.configure(bg=LIGHT_BG)

# Configure modern style
style = ttk.Style(root)
try:
    style.theme_use("clam")
except:
    pass

# Configure modern styles for widgets
style.configure("TFrame", background=LIGHT_BG, relief="flat")
style.configure("Card.TFrame", background=CARD_BG, relief="solid", borderwidth=1)
style.configure("TLabel", background=LIGHT_BG, foreground=DARK_TEXT, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
style.configure("Title.TLabel", background=LIGHT_BG, foreground=DARK_TEXT, font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"))
style.configure("Subtitle.TLabel", background=LIGHT_BG, foreground=LIGHT_TEXT, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
style.configure("Card.TLabel", background=CARD_BG, foreground=DARK_TEXT, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
style.configure("CardTitle.TLabel", background=CARD_BG, foreground=DARK_TEXT, font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"))

# Button styles
style.configure("Primary.TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL), foreground="white", background=PRIMARY_COLOR, relief="flat", padding=(20, 10))
style.configure("Secondary.TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL), foreground=PRIMARY_COLOR, background=CARD_BG, relief="solid", borderwidth=1, padding=(15, 8))
style.configure("Success.TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL), foreground="white", background=SUCCESS_COLOR, relief="flat", padding=(15, 8))
style.configure("Danger.TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL), foreground="white", background=ERROR_COLOR, relief="flat", padding=(15, 8))

# Button hover effects
style.map("Primary.TButton", background=[("active", "#1565C0")], relief=[("pressed", "flat"), ("!pressed", "flat")])
style.map("Secondary.TButton", background=[("active", "#E3F2FD")], relief=[("pressed", "flat"), ("!pressed", "solid")])
style.map("Success.TButton", background=[("active", "#388E3C")], relief=[("pressed", "flat"), ("!pressed", "flat")])
style.map("Danger.TButton", background=[("active", "#D32F2F")], relief=[("pressed", "flat"), ("!pressed", "flat")])

# Entry styles
style.configure("TEntry", font=(FONT_FAMILY, FONT_SIZE_NORMAL), fieldbackground=CARD_BG, relief="solid", borderwidth=1, padding=8)
style.configure("TCombobox", font=(FONT_FAMILY, FONT_SIZE_NORMAL), fieldbackground=CARD_BG, relief="solid", borderwidth=1, padding=8)

# Listbox and Scrollbar styles
style.configure("TListbox", font=(FONT_FAMILY, FONT_SIZE_NORMAL), fieldbackground=CARD_BG, relief="solid", borderwidth=1)
style.configure("TScrollbar", background=LIGHT_BG, troughcolor=LIGHT_BG, borderwidth=0, arrowcolor=LIGHT_TEXT)

# Load logo image from base64
logo_image = None
try:
    logo_image = tk.PhotoImage(data=logo_base64)
except Exception as e:
    logo_image = None

# Create main container with padding
main_container = ttk.Frame(root, padding=20)
main_container.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# --- Status Bar ---
status_frame = ttk.Frame(main_container, style="Card.TFrame", padding=(10, 5))
status_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 0))

status_light = tk.Canvas(status_frame, width=20, height=20, bg=CARD_BG, highlightthickness=0)
status_light.pack(side="left", padx=(5, 10))
status_light_indicator = status_light.create_oval(5, 5, 15, 15, fill="red", outline="")

status_label = ttk.Label(status_frame, text="ICカードリーダー未接続", style="Card.TLabel")
status_label.pack(side="left")

# Create frames with card-like appearance
frame_style = {"style": "Card.TFrame", "padding": 30}
home_frame = ttk.Frame(main_container, **frame_style)
entry_frame = ttk.Frame(main_container, **frame_style)
entry_done_frame = ttk.Frame(main_container, **frame_style)
error_frame = ttk.Frame(main_container, **frame_style)
exists_frame = ttk.Frame(main_container, **frame_style)
passcheck_frame = ttk.Frame(main_container, **frame_style)
setting_frame = ttk.Frame(main_container, padding=20)
simple_info_frame = ttk.Frame(main_container, **frame_style)
user_info_frame = ttk.Frame(main_container, **frame_style)
make_unit_frame = ttk.Frame(main_container, **frame_style)
unit_info_frame = ttk.Frame(main_container, **frame_style)

# Place all frames in the same location
for frame in (home_frame, entry_frame, entry_done_frame, error_frame, exists_frame,
              passcheck_frame, setting_frame, simple_info_frame, user_info_frame,
              make_unit_frame, unit_info_frame):
    frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=1)

# --- Home Frame (Main Menu) ---
# Create header section
header_frame = ttk.Frame(home_frame, style="Card.TFrame")
header_frame.pack(fill="x", pady=(0, 30))

if logo_image:
    logo_label = ttk.Label(header_frame, image=logo_image, style="Card.TLabel")
    logo_label.image = logo_image
    logo_label.pack(pady=(0, 15))

title_label = ttk.Label(header_frame, text="オイテル登録システム", style="Title.TLabel")
title_label.pack(pady=(0, 5))

subtitle_label = ttk.Label(header_frame, text="Tokyo City University – Tokyu Group", style="Subtitle.TLabel")
subtitle_label.pack(pady=(0, 10))

# Create button section with improved spacing
button_frame = ttk.Frame(home_frame, style="Card.TFrame")
button_frame.pack(fill="x")

button_register = ttk.Button(button_frame, text="🎓 学生証を登録する", style="Primary.TButton", width=35, command=lambda: entry_frame.tkraise())
button_usage = ttk.Button(button_frame, text="📊 利用状況の確認", style="Secondary.TButton", width=35, command=lambda: (simple_info_frame.tkraise(), show_usage_check_buttons()))
button_admin = ttk.Button(button_frame, text="⚙️ 詳細設定を開く (管理者)", style="Secondary.TButton", width=35, command=lambda: passcheck_frame.tkraise())

button_register.pack(pady=(0, 15), padx=20)
button_usage.pack(pady=(0, 15), padx=20)
button_admin.pack(pady=(0, 0), padx=20)

# --- Entry Frame (IC card registration) ---
entry_content = ttk.Frame(entry_frame, style="Card.TFrame")
entry_content.pack(expand=True, fill="both")

entry_icon = ttk.Label(entry_content, text="💳", font=(FONT_FAMILY, 48), style="Card.TLabel")
entry_icon.pack(pady=(0, 20))

entry_label = ttk.Label(entry_content, text="学生証をカードリーダーにタッチしてください", style="CardTitle.TLabel")
entry_label.pack(pady=(0, 30))

entry_button = ttk.Button(entry_content, text="ICカードを置いた", style="Primary.TButton", command=lambda: iccall())
entry_button.pack(pady=(0, 15))

entry_cancel = ttk.Button(entry_content, text="ホームに戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())
entry_cancel.pack()

# --- Entry Done Frame (Registration success) ---
done_content = ttk.Frame(entry_done_frame, style="Card.TFrame")
done_content.pack(expand=True, fill="both")

done_icon = ttk.Label(done_content, text="✅", font=(FONT_FAMILY, 48), style="Card.TLabel")
done_icon.pack(pady=(0, 20))

done_label = ttk.Label(done_content, text="登録が完了しました！", style="CardTitle.TLabel")
done_label.pack(pady=(0, 10))

done_sublabel = ttk.Label(done_content, text="自動的にホーム画面に戻ります", style="Card.TLabel")
done_sublabel.pack()

# --- Error Frame (Read error) ---
error_content = ttk.Frame(error_frame, style="Card.TFrame")
error_content.pack(expand=True, fill="both")

error_icon = ttk.Label(error_content, text="❌", font=(FONT_FAMILY, 48), style="Card.TLabel")
error_icon.pack(pady=(0, 20))

error_label = ttk.Label(error_content, text="ICカードが読み取れません", style="CardTitle.TLabel")
error_label.pack(pady=(0, 10))

error_sublabel = ttk.Label(error_content, text="ホーム画面に戻ります", style="Card.TLabel")
error_sublabel.pack()

# --- Exists Frame (Already registered) ---
exists_content = ttk.Frame(exists_frame, style="Card.TFrame")
exists_content.pack(expand=True, fill="both")

exists_icon = ttk.Label(exists_content, text="⚠️", font=(FONT_FAMILY, 48), style="Card.TLabel")
exists_icon.pack(pady=(0, 20))

exists_label = ttk.Label(exists_content, text="この学生証は既に登録されています", style="CardTitle.TLabel")
exists_label.pack(pady=(0, 10))

exists_sublabel = ttk.Label(exists_content, text="ホーム画面に戻ります", style="Card.TLabel")
exists_sublabel.pack()

# --- Password Check Frame ---
pass_content = ttk.Frame(passcheck_frame, style="Card.TFrame")
pass_content.pack(expand=True, fill="both")

pass_icon = ttk.Label(pass_content, text="🔒", font=(FONT_FAMILY, 48), style="Card.TLabel")
pass_icon.pack(pady=(0, 20))

pass_label = ttk.Label(pass_content, text="管理者パスワードを入力してください", style="CardTitle.TLabel")
pass_label.pack(pady=(0, 20))

pass_input_frame = ttk.Frame(pass_content, style="Card.TFrame")
pass_input_frame.pack(pady=(0, 20))

pass_entry = ttk.Entry(pass_input_frame, show="•", font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=25)
pass_entry.pack(side="left", padx=(0, 10))

pass_button = ttk.Button(pass_input_frame, text="認証", style="Primary.TButton", command=lambda: check_password())
pass_button.pack(side="left")

pass_cancel = ttk.Button(pass_content, text="ホームに戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())
pass_cancel.pack()

# --- Setting Frame (Admin Dashboard) ---
setting_container = ttk.Frame(setting_frame)
setting_container.pack(fill="both", expand=True)

# Create admin dashboard header
admin_header = ttk.Frame(setting_container, style="Card.TFrame", padding=20)
admin_header.pack(fill="x", pady=(0, 20))

admin_title = ttk.Label(admin_header, text="管理者ダッシュボード", style="Title.TLabel")
admin_title.pack()

# Create dashboard grid
dashboard_grid = ttk.Frame(setting_container)
dashboard_grid.pack(fill="both", expand=True)

# Configure grid weights
dashboard_grid.grid_rowconfigure(0, weight=1)
dashboard_grid.grid_rowconfigure(1, weight=1)
dashboard_grid.grid_columnconfigure(0, weight=1)
dashboard_grid.grid_columnconfigure(1, weight=1)
dashboard_grid.grid_columnconfigure(2, weight=1)

# Users section
users_frame = ttk.LabelFrame(dashboard_grid, text="👥 利用者一覧", style="Card.TFrame", padding=15)
users_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")

lb_users_var = tk.StringVar(value=[])
lb_users = tk.Listbox(users_frame, listvariable=lb_users_var, font=(FONT_FAMILY, FONT_SIZE_NORMAL), 
                      width=25, height=15, bg=CARD_BG, fg=DARK_TEXT, selectbackground=SECONDARY_COLOR)
sb_users = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=lb_users.yview)
lb_users.configure(yscrollcommand=sb_users.set)
lb_users.grid(row=0, column=0, sticky="nsew")
sb_users.grid(row=0, column=1, sticky="ns")

btn_view_user = ttk.Button(users_frame, text="選択ユーザー詳細", style="Primary.TButton", command=lambda: open_user_details())
btn_view_user.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

users_frame.grid_rowconfigure(0, weight=1)
users_frame.grid_columnconfigure(0, weight=1)

# Units section
units_frame = ttk.LabelFrame(dashboard_grid, text="📱 子機一覧", style="Card.TFrame", padding=15)
units_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

lb_units_var = tk.StringVar(value=[])
lb_units = tk.Listbox(units_frame, listvariable=lb_units_var, font=(FONT_FAMILY, FONT_SIZE_NORMAL), 
                      width=25, height=8, bg=CARD_BG, fg=DARK_TEXT, selectbackground=SECONDARY_COLOR)
sb_units = ttk.Scrollbar(units_frame, orient=tk.VERTICAL, command=lb_units.yview)
lb_units.configure(yscrollcommand=sb_units.set)
lb_units.grid(row=0, column=0, sticky="nsew")
sb_units.grid(row=0, column=1, sticky="ns")

btn_view_unit = ttk.Button(units_frame, text="選択子機詳細", style="Primary.TButton", command=lambda: open_unit_details())
btn_view_unit.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="ew")

btn_new_unit = ttk.Button(units_frame, text="新規子機の登録", style="Success.TButton", command=lambda: make_unit_frame.tkraise())
btn_new_unit.grid(row=2, column=0, columnspan=2, pady=(5, 0), sticky="ew")

units_frame.grid_rowconfigure(0, weight=1)
units_frame.grid_columnconfigure(0, weight=1)

# History section
history_frame = ttk.LabelFrame(dashboard_grid, text="📋 利用履歴", style="Card.TFrame", padding=15)
history_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

lb_history_var = tk.StringVar(value=[])
lb_history = tk.Listbox(history_frame, listvariable=lb_history_var, font=(FONT_FAMILY, FONT_SIZE_SMALL), 
                        width=35, height=8, bg=CARD_BG, fg=DARK_TEXT, selectbackground=SECONDARY_COLOR)
sb_history = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=lb_history.yview)
lb_history.configure(yscrollcommand=sb_history.set)
lb_history.grid(row=0, column=0, sticky="nsew")
sb_history.grid(row=0, column=1, sticky="ns")

btn_export_history = ttk.Button(history_frame, text="履歴をエクスポート", style="Primary.TButton", command=lambda: export_history())
btn_export_history.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="ew")

history_frame.grid_rowconfigure(0, weight=1)
history_frame.grid_columnconfigure(0, weight=1)

# Settings section
settings_frame = ttk.LabelFrame(dashboard_grid, text="⚙️ システム設定", style="Card.TFrame", padding=15)
settings_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

# Password change section
pass_change_frame = ttk.Frame(settings_frame, style="Card.TFrame")
pass_change_frame.pack(fill="x", pady=(0, 15))

cur_pass_label = ttk.Label(pass_change_frame, text="現在のパスワード:", style="Card.TLabel")
cur_pass_value = ttk.Label(pass_change_frame, text="", style="Card.TLabel")
new_pass_label = ttk.Label(pass_change_frame, text="新しいパスワード:", style="Card.TLabel")
new_pass_entry1 = ttk.Entry(pass_change_frame, font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=15)
new_pass_entry2 = ttk.Entry(pass_change_frame, font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=15)
btn_change_pass = ttk.Button(pass_change_frame, text="変更", style="Success.TButton", command=lambda: change_password())

cur_pass_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
cur_pass_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)
new_pass_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
new_pass_entry1.grid(row=1, column=1, padx=5, pady=5)
new_pass_entry2.grid(row=1, column=2, padx=5, pady=5)
btn_change_pass.grid(row=1, column=3, padx=5, pady=5)

# Usage settings
usage_frame = ttk.Frame(settings_frame, style="Card.TFrame")
usage_frame.pack(fill="x", pady=(0, 15))

keep_label = ttk.Label(usage_frame, text="保持上限:", style="Card.TLabel")
keep_entry = ttk.Entry(usage_frame, width=8)
freq_label = ttk.Label(usage_frame, text="増加日数:", style="Card.TLabel")
freq_entry = ttk.Entry(usage_frame, width=8)

keep_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
keep_entry.grid(row=0, column=1, padx=5, pady=5)
freq_label.grid(row=0, column=2, sticky="e", padx=5, pady=5)
freq_entry.grid(row=0, column=3, padx=5, pady=5)

# Backup and restore
backup_frame = ttk.Frame(settings_frame, style="Card.TFrame")
backup_frame.pack(fill="x")

btn_backup = ttk.Button(backup_frame, text="📥 データバックアップ", style="Primary.TButton", command=lambda: mydb.make_backup())
btn_restore = ttk.Button(backup_frame, text="📤 バックアップから復元", style="Secondary.TButton", command=lambda: restore_from_backup())

btn_backup.pack(side="left", padx=(0, 10))
btn_restore.pack(side="left")

# Back to home button
back_home_frame = ttk.Frame(setting_container, style="Card.TFrame", padding=10)
back_home_frame.pack(fill="x", pady=(20, 0))

btn_setting_home = ttk.Button(back_home_frame, text="ホーム画面に戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())
btn_setting_home.pack()

# --- Simple User Info Frame ---
info_content = ttk.Frame(simple_info_frame, style="Card.TFrame")
info_content.pack(expand=True, fill="both")

info_header = ttk.Frame(info_content, style="Card.TFrame")
info_header.pack(fill="x", pady=(0, 30))

info_icon = ttk.Label(info_header, text="📊", font=(FONT_FAMILY, 48), style="Card.TLabel")
info_icon.pack(pady=(0, 15))

info_prompt = ttk.Label(info_header, text="学生証をリーダーに置いて「確認」ボタンを押してください", style="CardTitle.TLabel")
info_prompt.pack(pady=(0, 20))

# --- 追加: リーダー接続状態管理 ---
info_error_label = ttk.Label(info_header, text="", style="Card.TLabel", foreground=ERROR_COLOR)
# ── ボタン変数を初期化 ──
info_btn_check = None
info_btn_retry = None

# ── 利用状況取得ロジック ──
def check_usage():
    try:
        # カード読み取り／DB検索
        mydb.id_do()
        member_info = mydb.add_find()
        if member_info and len(member_info) > 0:
            cardid, stock, allow, entry, *rest = member_info
            status = "利用可能" if allow == 1 else "利用停止中"
            # 次の利用可能日までの日数を取得
            ci = mydb.call_info()
            if ci and len(ci) > 3:
                days_until = ci[3] - ci[2]
            else:
                days_until = None
            # 画面に反映
            val_cardid.config   (text=str(cardid))
            val_status.config   (text=status)
            val_entrydate.config(text=str(entry))
            val_stock.config    (text=str(stock))
            val_next.config     (text=f"{days_until}日後" if isinstance(days_until, int) else "--")
        else:
            # 読み取り失敗時
            error_frame.tkraise()
            root.after(2500, home_frame.tkraise)
    except Exception as e:
        show_error("利用状況確認エラー", f"利用状況の確認中にエラーが発生しました: {e}")

def show_usage_check_buttons():
    global info_btn_check, info_btn_retry
    if info_btn_check is not None:
        return
    # 既存ボタンを消す
    if info_btn_check:
        info_btn_check.pack_forget()
    if info_btn_retry:
        info_btn_retry.pack_forget()
    info_error_label.pack_forget()
    # 接続状態チェック
    if mydb.check_reader_status():
        # 接続OK: 通常の確認ボタン
        info_btn_check = ttk.Button(info_header, text="利用状況を確認", style="Primary.TButton", command=on_check_usage)
        info_btn_check.pack()
    else:
        # 未接続: エラーと再接続ボタン
        info_error_label.config(text="ICカードリーダーが接続されていません。USBを確認してください。")
        info_error_label.pack(pady=(0, 10))
        info_btn_retry = ttk.Button(info_header, text="リーダー再接続を試す", style="Primary.TButton", command=lambda: (
            status_label.config(text="ICカードリーダー再接続中…"),
            root.after(100, on_check_usage)
        ))
        info_btn_retry.pack()

def on_check_usage():
    # 利用状況確認処理
    try:
        if not mydb.check_reader_status():
            show_usage_check_buttons()
            return
        check_usage()
    except Exception as e:
        show_error("利用状況確認エラー", f"利用状況の確認中にエラーが発生しました: {e}")

def on_retry_reader():
    show_usage_check_buttons()

# Info display section
info_display = ttk.Frame(info_content, style="Card.TFrame", padding=20)
info_display.pack(fill="x", pady=(30, 0))

info_grid = ttk.Frame(info_display, style="Card.TFrame")
info_grid.pack()

# Create info labels with better formatting
info_labels = [
    ("カードID:", "val_cardid"),
    ("利用状況:", "val_status"),
    ("登録日:", "val_entrydate"),
    ("残り利用回数:", "val_stock"),
    ("次の利用可能日まで:", "val_next")
]

info_widgets = {}
for i, (label_text, var_name) in enumerate(info_labels):
    label = ttk.Label(info_grid, text=label_text, style="Card.TLabel")
    value = ttk.Label(info_grid, text="", style="CardTitle.TLabel")
    label.grid(row=i, column=0, sticky="e", padx=(0, 15), pady=8)
    value.grid(row=i, column=1, sticky="w", padx=0, pady=8)
    info_widgets[var_name] = value

# Unpack widgets for easier access
val_cardid = info_widgets["val_cardid"]
val_status = info_widgets["val_status"]
val_entrydate = info_widgets["val_entrydate"]
val_stock = info_widgets["val_stock"]
val_next = info_widgets["val_next"]

btn_back_home = ttk.Button(info_content, text="ホームに戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())
btn_back_home.pack(pady=(30, 0))

# --- User Info Frame (Detailed user info & edit) ---
user_content = ttk.Frame(user_info_frame, style="Card.TFrame")
user_content.pack(expand=True, fill="both")

user_header = ttk.Label(user_content, text="👤 ユーザー詳細情報", style="Title.TLabel")
user_header.pack(pady=(0, 20))

user_form = ttk.Frame(user_content, style="Card.TFrame")
user_form.pack(fill="x", pady=(0, 20))

# User form fields
user_fields = [
    ("カードID:", "ui_val_cardid", "entry"),
    ("利用回数ストック:", "ui_val_stock", "entry"),
    ("許可 (1=可, 0=不可):", "ui_val_allow", "entry"),
    ("登録日:", "ui_val_entry", "label"),
    ("累計利用回数:", "ui_val_total", "label"),
    ("今日の利用回数:", "ui_val_today", "label")
]

user_widgets = {}
for i, (label_text, var_name, widget_type) in enumerate(user_fields):
    label = ttk.Label(user_form, text=label_text, style="Card.TLabel")
    if widget_type == "entry":
        widget = ttk.Entry(user_form, font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=25)
    else:
        widget = ttk.Label(user_form, text="", style="Card.TLabel")
    
    label.grid(row=i, column=0, sticky="e", padx=(0, 15), pady=10)
    widget.grid(row=i, column=1, sticky="w", padx=0, pady=10)
    user_widgets[var_name] = widget

# Unpack user widgets
ui_val_cardid = user_widgets["ui_val_cardid"]
ui_val_stock = user_widgets["ui_val_stock"]
ui_val_allow = user_widgets["ui_val_allow"]
ui_val_entry = user_widgets["ui_val_entry"]
ui_val_total = user_widgets["ui_val_total"]
ui_val_today = user_widgets["ui_val_today"]

# Recent history section
history_section = ttk.Frame(user_content, style="Card.TFrame", padding=15)
history_section.pack(fill="x", pady=(0, 20))

ui_lbl_recent = ttk.Label(history_section, text="📋 最近の利用履歴", style="CardTitle.TLabel")
ui_lbl_recent.pack(anchor="w", pady=(0, 10))

history_grid = ttk.Frame(history_section, style="Card.TFrame")
history_grid.pack(fill="x")

# Create history labels
history_widgets = {}
for i in range(1, 6):
    hist_label = ttk.Label(history_grid, text=f"{i}:", style="Card.TLabel")
    hist_value = ttk.Label(history_grid, text="", style="Card.TLabel")
    hist_label.grid(row=i-1, column=0, sticky="e", padx=(0, 10), pady=2)
    hist_value.grid(row=i-1, column=1, sticky="w", padx=0, pady=2)
    history_widgets[f"ui_val_hist{i}"] = hist_value

# Unpack history widgets
ui_val_hist1 = history_widgets["ui_val_hist1"]
ui_val_hist2 = history_widgets["ui_val_hist2"]
ui_val_hist3 = history_widgets["ui_val_hist3"]
ui_val_hist4 = history_widgets["ui_val_hist4"]
ui_val_hist5 = history_widgets["ui_val_hist5"]

# User action buttons
user_buttons = ttk.Frame(user_content, style="Card.TFrame")
user_buttons.pack(fill="x")

btn_save_user = ttk.Button(user_buttons, text="設定を変更する", style="Success.TButton", command=lambda: save_user_changes())
btn_user_back = ttk.Button(user_buttons, text="戻る", style="Secondary.TButton", command=lambda: setting_frame.tkraise())
btn_user_home = ttk.Button(user_buttons, text="ホーム画面に戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())

btn_save_user.pack(side="right", padx=(10, 0))
btn_user_back.pack(side="left")
btn_user_home.pack(side="right")

# --- Make Unit Frame ---
unit_content = ttk.Frame(make_unit_frame, style="Card.TFrame")
unit_content.pack(expand=True, fill="both")

unit_header = ttk.Label(unit_content, text="📱 新規子機登録", style="Title.TLabel")
unit_header.pack(pady=(0, 30))

unit_form = ttk.Frame(unit_content, style="Card.TFrame")
unit_form.pack(fill="x", pady=(0, 30))

# Unit form fields
unit_field_data = [
    ("子機名:", "unit_name_entry"),
    ("パスワード:", "unit_pass_entry"),
    ("初期在庫数:", "unit_stock_entry"),
    ("利用可能か (1=可,0=不可):", "unit_avail_entry")
]

unit_form_widgets = {}
for i, (label_text, var_name) in enumerate(unit_field_data):
    label = ttk.Label(unit_form, text=label_text, style="Card.TLabel")
    entry = ttk.Entry(unit_form, font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=25)
    label.grid(row=i, column=0, sticky="e", padx=(0, 15), pady=10)
    entry.grid(row=i, column=1, sticky="w", padx=0, pady=10)
    unit_form_widgets[var_name] = entry

# Unpack unit form widgets
unit_name_entry = unit_form_widgets["unit_name_entry"]
unit_pass_entry = unit_form_widgets["unit_pass_entry"]
unit_stock_entry = unit_form_widgets["unit_stock_entry"]
unit_avail_entry = unit_form_widgets["unit_avail_entry"]

# Unit action buttons
unit_buttons = ttk.Frame(unit_content, style="Card.TFrame")
unit_buttons.pack(fill="x")

btn_unit_create = ttk.Button(unit_buttons, text="子機を登録する", style="Success.TButton", command=lambda: create_unit())
btn_unit_back = ttk.Button(unit_buttons, text="戻る", style="Secondary.TButton", command=lambda: setting_frame.tkraise())
btn_unit_home = ttk.Button(unit_buttons, text="ホーム画面に戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())

btn_unit_create.pack(pady=(0, 15))
btn_unit_back.pack(side="left")
btn_unit_home.pack(side="right")

# --- Unit Info Frame ---
unit_info_content = ttk.Frame(unit_info_frame, style="Card.TFrame")
unit_info_content.pack(expand=True, fill="both")

unit_info_header = ttk.Label(unit_info_content, text="📱 子機詳細情報", style="Title.TLabel")
unit_info_header.pack(pady=(0, 30))

unit_info_form = ttk.Frame(unit_info_content, style="Card.TFrame")
unit_info_form.pack(fill="x", pady=(0, 30))

# Unit info form fields
unit_info_fields = [
    ("子機名:", "ui2_val_name", "label"),
    ("パスワード:", "ui2_val_pass", "label"),
    ("残り用品在庫:", "ui2_val_stock", "entry"),
    ("利用可能か (1/0):", "ui2_val_avail", "entry"),
    ("接続状態:", "ui2_val_conn", "label")
]

unit_info_widgets = {}
for i, (label_text, var_name, widget_type) in enumerate(unit_info_fields):
    label = ttk.Label(unit_info_form, text=label_text, style="Card.TLabel")
    if widget_type == "entry":
        widget = ttk.Entry(unit_info_form, font=(FONT_FAMILY, FONT_SIZE_NORMAL), width=25)
    else:
        widget = ttk.Label(unit_info_form, text="", style="Card.TLabel")
    
    label.grid(row=i, column=0, sticky="e", padx=(0, 15), pady=10)
    widget.grid(row=i, column=1, sticky="w", padx=0, pady=10)
    unit_info_widgets[var_name] = widget

# Unpack unit info widgets
ui2_val_name = unit_info_widgets["ui2_val_name"]
ui2_val_pass = unit_info_widgets["ui2_val_pass"]
ui2_val_stock = unit_info_widgets["ui2_val_stock"]
ui2_val_avail = unit_info_widgets["ui2_val_avail"]
ui2_val_conn = unit_info_widgets["ui2_val_conn"]

# Unit info action buttons
unit_info_buttons = ttk.Frame(unit_info_content, style="Card.TFrame")
unit_info_buttons.pack(fill="x")

btn_unit_save = ttk.Button(unit_info_buttons, text="設定を変更する", style="Success.TButton", command=lambda: save_unit_changes())
btn_unit_info_back = ttk.Button(unit_info_buttons, text="戻る", style="Secondary.TButton", command=lambda: setting_frame.tkraise())
btn_unit_info_home = ttk.Button(unit_info_buttons, text="ホーム画面に戻る", style="Secondary.TButton", command=lambda: home_frame.tkraise())

btn_unit_save.pack(side="right", padx=(10, 0))
btn_unit_info_back.pack(side="left")
btn_unit_info_home.pack(side="right")

# --- Generic Error Dialog ---
def show_error(title="エラー", message="予期せぬエラーが発生しました。"):
    messagebox.showerror(title, message)

# Function to check and update IC card reader status
def update_reader_status():
    try:
        if mydb.check_reader_status():
            status_light.itemconfig(status_light_indicator, fill=SUCCESS_COLOR)
            status_label.config(text="ICカードリーダー接続")
        else:
            status_light.itemconfig(status_light_indicator, fill=ERROR_COLOR)
            status_label.config(text="ICカードリーダー未接続")
    except Exception as e:
        status_light.itemconfig(status_light_indicator, fill=ERROR_COLOR)
        status_label.config(text="リーダー状態確認エラー")
    finally:
        root.after(5000, update_reader_status) # Check every 5 seconds

# Function to refresh lists in admin setting frame
def refresh_admin_lists():
    try:
        users = mydb.member_call()
        units = mydb.units_call()
        history = mydb.his_call()
        lb_users_var.set(users)
        lb_units_var.set(units)
        lb_history_var.set(history)
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("リスト更新エラー", f"リストの更新中にエラーが発生しました: {e}")

def iccall():
    try:
        data = mydb.do()
        ci = mydb.call_info()
        if data is True:
            # 既に登録済みカードかどうか判定 (info.list にユーザーID or -2 が入っている)
            if ci is not None and len(ci) > 6 and str(ci[6]) != "-2":
                # 登録済み
                exists_frame.tkraise()
                exists_frame.after(2000, home_frame.tkraise)
            else:
                # 新規登録
                try:
                    if ci is not None and len(ci) > 6:
                        lb_users.insert(tk.END, ci[6])
                    else:
                        lb_users.insert(tk.END, "新規登録")
                except Exception as e:
                    if "Unknown column 'list'" in str(e):
                        show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
                    elif "tuple index out of range" in str(e):
                        show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
                    else:
                        show_error("登録情報取得エラー", f"登録情報取得中にエラーが発生しました: {e}")
                entry_done_frame.tkraise()
                entry_done_frame.after(2000, home_frame.tkraise)
        else:
            error_frame.tkraise()
            error_frame.after(2500, home_frame.tkraise)
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("ICカード処理エラー", f"ICカードの読み取りまたは登録処理中にエラーが発生しました: {e}")
        home_frame.tkraise()

def check_password():
    try:
        entered = pass_entry.get()
        mydb.alignment_user()
        ci = mydb.call_info()
        actual_pass = ci[0] if ci and len(ci) > 0 else ""
        if entered == actual_pass:
            cur_pass_value.config(text=actual_pass)
            keep_entry.delete(0, tk.END)
            freq_entry.delete(0, tk.END)
            if ci and len(ci) > 4:
                keep_entry.insert(0, str(ci[4]))
                freq_entry.insert(0, str(ci[3]))
            refresh_admin_lists()
            setting_frame.tkraise()
        else:
            pass_entry.delete(0, tk.END)
            show_error("認証エラー", "パスワードが違います。")
            passcheck_frame.tkraise()
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("パスワード確認エラー", f"処理中にエラーが発生しました: {e}")

def open_user_details():
    try:
        sel = lb_users.curselection()
        if not sel:
            return
        idx = sel[0]
        user_str = lb_users.get(idx)
        uid = int(user_str.split(":")[0])
        mydb.update_info(6, str(uid))
        info = mydb.add_find()
        if info:
            try:
                ui_val_cardid.delete(0, tk.END); ui_val_cardid.insert(0, info[0])
                ui_val_stock.delete(0, tk.END); ui_val_stock.insert(0, str(info[1]))
                ui_val_allow.delete(0, tk.END); ui_val_allow.insert(0, str(info[2]))
                ui_val_entry.config(text=str(info[3]))
                ui_val_total.config(text=str(info[4]))
                ui_val_today.config(text=str(info[5]))
                recent = list(info[6:])
                hist_labels = [ui_val_hist1, ui_val_hist2, ui_val_hist3, ui_val_hist4, ui_val_hist5]
                for i in range(5):
                    if i < len(recent):
                        val = recent[i]
                        hist_labels[i].config(text=(str(val) if val != "記録なし" else "記録なし"))
                    else:
                        hist_labels[i].config(text="")
            except Exception as e:
                if "Unknown column 'list'" in str(e):
                    show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
                elif "tuple index out of range" in str(e):
                    show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
                else:
                    show_error("ユーザー詳細エラー", f"ユーザー情報の表示中にエラーが発生しました: {e}")
        user_info_frame.tkraise()
    except Exception as e:
        show_error("ユーザー詳細エラー", f"ユーザー情報の表示中にエラーが発生しました: {e}")

def save_user_changes():
    try:
        sel = lb_users.curselection()
        if not sel:
            setting_frame.tkraise(); return
        idx = sel[0]
        user_str = lb_users.get(idx)
        uid = int(user_str.split(":")[0])
        new_cardid = ui_val_cardid.get().strip()
        new_stock = ui_val_stock.get().strip()
        new_allow = ui_val_allow.get().strip()
        if new_allow == "":
            new_allow = None
        if new_stock == "":
            new_stock = None
        if new_cardid == "":
            mydb.delete_user(uid)
        else:
            mydb.update_user(uid, 1, new_cardid)
            mydb.update_user(uid, 4, new_stock)
            mydb.update_user(uid, 2, new_allow)
        mydb.make_backup()
        refresh_admin_lists()
        setting_frame.tkraise()
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("ユーザー情報保存エラー", f"ユーザー情報の保存中にエラーが発生しました: {e}")

def open_unit_details():
    try:
        sel = lb_units.curselection()
        if not sel:
            return
        idx = sel[0]
        unit_str = lb_units.get(idx)
        unit_id = int(unit_str.split(":")[0])
        units = mydb.units_call()
        if unit_id <= len(units):
            all_units = mydb.call_units()
            for u in all_units:
                if u[0] == unit_id:
                    try:
                        ui2_val_name.config(text=str(u[1]))
                        ui2_val_pass.config(text=str(u[2]))
                        ui2_val_stock.delete(0, tk.END); ui2_val_stock.insert(0, str(u[3]))
                        ui2_val_avail.delete(0, tk.END); ui2_val_avail.insert(0, str(u[5]))
                        ui2_val_conn.config(text=("接続OK" if u[4] == 1 else "接続NG"))
                    except Exception as e:
                        if "Unknown column 'list'" in str(e):
                            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
                        elif "tuple index out of range" in str(e):
                            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
                        else:
                            show_error("子機詳細エラー", f"子機情報の表示中にエラーが発生しました: {e}")
                    break
        unit_info_frame.tkraise()
    except Exception as e:
        show_error("子機詳細エラー", f"子機情報の表示中にエラーが発生しました: {e}")

def save_unit_changes():
    try:
        sel = lb_units.curselection()
        if not sel:
            setting_frame.tkraise(); return
        idx = sel[0]
        unit_str = lb_units.get(idx)
        unit_id = int(unit_str.split(":")[0])
        new_stock = ui2_val_stock.get().strip()
        new_avail = ui2_val_avail.get().strip()
        if new_stock == "":
            new_stock = None
        if new_avail == "":
            new_avail = None
        mydb.update_unit(unit_id, 3, new_stock)
        mydb.update_unit(unit_id, 5, new_avail)
        mydb.make_backup()
        refresh_admin_lists()
        setting_frame.tkraise()
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("子機情報保存エラー", f"子機情報の保存中にエラーが発生しました: {e}")

def create_unit():
    try:
        name = unit_name_entry.get().strip()
        pwd = unit_pass_entry.get().strip()
        stock = unit_stock_entry.get().strip()
        avail = unit_avail_entry.get().strip()
        if name == "" or pwd == "" or stock == "" or avail == "":
            show_error("入力エラー", "すべての日付を入力してください。")
            return
        try:
            mydb.make_unit(name, pwd, int(stock), int(avail))
        except Exception as e:
            if "Unknown column 'list'" in str(e):
                show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
            elif "tuple index out of range" in str(e):
                show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
            else:
                show_error("子機作成エラー", f"子機の作成中にエラーが発生しました: {e}")
            return
        unit_name_entry.delete(0, tk.END)
        unit_pass_entry.delete(0, tk.END)
        unit_stock_entry.delete(0, tk.END)
        unit_avail_entry.delete(0, tk.END)
        refresh_admin_lists()
        setting_frame.tkraise()
    except ValueError:
        show_error("入力エラー", "在庫数と利用可否は数字で入力してください。")
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("子機作成エラー", f"子機の作成中にエラーが発生しました: {e}")

def change_password():
    try:
        new1 = new_pass_entry1.get().strip()
        new2 = new_pass_entry2.get().strip()
        keep_val = keep_entry.get().strip()
        freq_val = freq_entry.get().strip()
        ci = mydb.call_info()
        current_pass = ci[0] if ci and len(ci) > 0 else ""
        if new1 == "" and new2 == "":
            new1 = current_pass
            new2 = current_pass
        if new1 == new2:
            mydb.update_info(0, new1)
            mydb.update_info(4, keep_val)
            mydb.update_info(3, freq_val)
            cur_pass_value.config(text=new1)
            new_pass_entry1.delete(0, tk.END)
            new_pass_entry2.delete(0, tk.END)
        else:
            show_error("パスワードエラー", "新しいパスワードが一致しません。")
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("設定保存エラー", f"設定の保存中にエラーが発生しました: {e}")

def export_history():
    try:
        mydb.make_his_backup()
        messagebox.showinfo("成功", "履歴が正常にエクスポートされました。")
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("エクスポートエラー", f"履歴のエクスポート中にエラーが発生しました: {e}")
        mydb.make_backup()

def restore_from_backup():
    try:
        mydb.copy_from_excel("backup")
        refresh_admin_lists()
        messagebox.showinfo("成功", "データが正常に復元されました。")
    except Exception as e:
        if "Unknown column 'list'" in str(e):
            show_error("システムエラー", "データベースのバージョンが異なります。管理者にご連絡ください。")
        elif "tuple index out of range" in str(e):
            show_error("データエラー", "データベースの情報が不足しています。管理者にご連絡ください。")
        else:
            show_error("復元エラー", f"バックアップからの復元に失敗しました。'backup.xlsx'が存在することを確認してください。: {e}")

# 初期セットアップ
try:
    mydb.set_up()
    mydb.make_user()
    mydb.make_his()
except Exception as e:
    show_error("DB初期化エラー", f"データベース初期化に失敗しました: {e}")
    root.destroy()

def daily_check():
    try:
        mydb.dayupdate()
        mydb.make_backup()
    except Exception as e:
        print(f"日次更新エラー: {e}") # Log to console, no need to alert user
    finally:
        root.after(3600000, daily_check)

daily_check()
update_reader_status()

# Show home frame at startup
home_frame.tkraise()
root.mainloop()
