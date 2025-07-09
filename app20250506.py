from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify
from mydb20250506 import get_db_connection
from mysql.connector import Error as MySQLError
import os
import io
import mydb20250506 as mydb

app = Flask(__name__)
app.secret_key = "toshidai_tokyu_secret_key_2025"  # Secret key for session management

# Ensure DB is ready on server start
try:
    mydb.set_up()        # ← 新 set_up が内部で make_* も呼ぶ
except Exception as e:
    print(f"FATAL: Database setup failed: {e}")

@app.route("/api/reader_status")
def api_reader_status():
    """API endpoint to check IC card reader status."""
    try:
        status = mydb.check_reader_status()
        return jsonify({"connected": status})
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        print(f"Error checking reader status (code {code}): {e}")
        return jsonify({
            "connected": False,
            "error": str(e),
            "code": code
        }), 500

@app.route("/")
def index():
    """Home page - show options for card registration and usage check."""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student IC card."""
    if request.method == "POST":
        try:
            # When form is submitted to register, trigger card reading
            data = mydb.do()
            if data is True:
                # Card read successfully
                try:
                    ci = mydb.call_info()
                    # info.list に既存ユーザーIDが入っていれば「登録済み」、-2なら新規
                    if ci is not None and len(ci) > 6 and str(ci[6]) != "-2":
                        flash("この学生証は登録済みです。", "warning")
                    else:
                        # 新規登録処理完了
                        ci2 = mydb.call_info()
                        msg = "登録が完了しました。"
                        if ci2 is not None and len(ci2) > 6:
                            msg += f" (新規ID: {ci2[6]})"
                        else:
                            msg += " (新規ID: 不明)"
                        flash(msg, "success")
                except Exception as e:
                    if "Unknown column 'list'" in str(e):
                        flash("システムエラー: データベースのバージョンが異なります。管理者にご連絡ください。", "error")
                    else:
                        flash(f"登録処理中にエラーが発生しました: {e}", "error")
            else:
                # Card read failure
                flash("ICカードが読み取れませんでした。再試行してください。", "error")
        except Exception as e:
            code = e.errno if isinstance(e, MySQLError) else -1
            if "Unknown column 'list'" in str(e):
                flash(f"[コード {code}] システムエラー: データベースのバージョンが異なります。管理者にご連絡ください。", "error")
            else:
                flash(f"[コード {code}] ICカードの読み取り中にエラーが発生しました: {e}", "error")
        return redirect(url_for("register"))
    # GET request: show the registration page with instructions
    return render_template("register.html")

@app.route("/usage", methods=["GET", "POST"])
def usage():
    """Check usage status of a student via IC card."""
    reader_connected = False
    try:
        reader_connected = mydb.check_reader_status()
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] カードリーダーの状態確認中にエラーが発生しました: {e}", "error")
    
    if request.method == "POST":
        # 再接続ボタンが押された場合
        if not reader_connected or request.form.get("retry"):
            try:
                reader_connected = mydb.check_reader_status()
                if not reader_connected:
                    flash("ICカードリーダーが接続されていません。USBを確認してください。", "error")
                    return render_template("usage.html", reader_connected=False)
                # 再接続成功時は通常の利用状況確認フォームを表示
            except Exception as e:
                code = e.errno if isinstance(e, MySQLError) else -1
                flash(f"[コード {code}] カードリーダー再接続中にエラーが発生しました: {e}", "error")
                return render_template("usage.html", reader_connected=False)
            return render_template("usage.html", reader_connected=True)
        # 利用状況確認処理を共通関数に統一
        try:
            return check_usage()
        except Exception as e:
            code = e.errno if isinstance(e, MySQLError) else -1
            flash(f"[コード {code}] 利用状況確認中にエラーが発生しました: {e}", "error")
            return render_template("usage.html", reader_connected=False)
    return render_template("usage.html", reader_connected=reader_connected)

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Admin login (password check)."""
    if request.method == "POST":
        try:
            entered_pass = request.form.get("password", "")
            ci = mydb.call_info()
            actual_pass = ""
            if ci and len(ci) > 0:
                actual_pass = ci[0]  # info.pass is stored at index 0
            if entered_pass == actual_pass:
                session["admin_logged_in"] = True
                return redirect(url_for("admin_dashboard"))
            else:
                flash("パスワードが違います。", "error")
                return redirect(url_for("admin_login"))
        except Exception as e:
            if "Unknown column 'list'" in str(e):
                flash("システムエラー: データベースのバージョンが異なります。管理者にご連絡ください。", "error")
            else:
                flash(f"ログイン処理中にエラーが発生しました: {e}", "error")
            return redirect(url_for("admin_login"))
    # GET: render login form
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard showing summary and navigation links (if logged in)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        # We can display counts of users, units, etc.
        users = mydb.member_call()   # list of users like "0:cardid..."
        units = mydb.units_call()    # list of units like "1:unitName..."
        history = mydb.his_call()    # list of history entries
        return render_template("admin_dashboard.html", users=users, units=units, history=history)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] ダッシュボードの読み込み中にエラーが発生しました: {e}", "error")
        return render_template("admin_dashboard.html", users=[], units=[], history=[])

@app.route("/admin/users")
def admin_users():
    """List all users (admin view)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        users = mydb.call_user()  # get raw user data (list of tuples)
        return render_template("admin_users.html", users=users)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] ユーザーリストの取得中にエラーが発生しました: {e}", "error")
        return render_template("admin_users.html", users=[])

@app.route("/admin/user/<int:uid>", methods=["GET", "POST"])
def admin_user_detail(uid):
    """View or edit details of a specific user (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        # Align user IDs to current ordering (ensures uid is correct index)
        mydb.alignment_user()
        if request.method == "POST":
            # Update or delete user based on form input
            cardid = request.form.get("cardid", "").strip()
            stock = request.form.get("stock", "").strip()
            allow = request.form.get("allow", "").strip()
            if cardid == "":
                # Delete user if cardid is emptied
                mydb.delete_user(uid)
                flash("ユーザーを削除しました。", "info")
                return redirect(url_for("admin_users"))
            # Otherwise, update the user's info
            if allow == "":
                allow = None
            if stock == "":
                stock = None
            mydb.update_user(uid, 1, cardid)
            mydb.update_user(uid, 4, stock)
            mydb.update_user(uid, 2, allow)
            flash("ユーザー情報を更新しました。", "success")
            return redirect(url_for("admin_user_detail", uid=uid))
        # GET: retrieve user info to display
        users = mydb.call_user()
        user = next((u for u in users if u[0] == uid), None)

        if user is None:
            # If user not found (perhaps was deleted), redirect to list
            flash("指定されたユーザーが見つかりません。", "error")
            return redirect(url_for("admin_users"))
        # user tuple: (id, cardid, allow, entry, stock, today, total, last1...last10)
        return render_template("admin_user_detail.html", user=user)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] ユーザー情報の処理中にエラーが発生しました: {e}", "error")
        return redirect(url_for("admin_users"))

@app.route("/admin/units")
def admin_units():
    """List all child units (admin view)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        units = mydb.call_units()  # raw units data (list of tuples)
        return render_template("admin_units.html", units=units)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] 子機リストの取得中にエラーが発生しました: {e}", "error")
        return render_template("admin_units.html", units=[])

@app.route("/admin/unit/<int:uid>", methods=["GET", "POST"])
def admin_unit_detail(uid):
    """View or edit details of a specific unit (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        if request.method == "POST":
            # Update unit stock/availability
            stock = request.form.get("stock", "").strip()
            avail = request.form.get("available", "").strip()
            if stock == "":
                stock = None
            if avail == "":
                avail = None
            mydb.update_unit(uid, 3, stock)
            mydb.update_unit(uid, 5, avail)
            flash("子機情報を更新しました。", "success")
            return redirect(url_for("admin_unit_detail", uid=uid))
        units = mydb.call_units()
        unit = next((u for u in units if u[0] == uid), None)

        if unit is None:
            flash("指定された子機が見つかりません。", "error")
            return redirect(url_for("admin_units"))
        # unit tuple: (id, name, pass, stock, connect, available)
        return render_template("admin_unit_detail.html", unit=unit)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] 子機情報の処理中にエラーが発生しました: {e}", "error")
        return redirect(url_for("admin_units"))

@app.route("/admin/unit/new", methods=["GET", "POST"])
def admin_new_unit():
    """Add a new child unit (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        pwd = request.form.get("password", "").strip()
        stock = request.form.get("stock", "").strip()
        avail = request.form.get("available", "").strip()
        if name and pwd and stock and avail:
            try:
                mydb.make_unit(name, pwd, int(stock), int(avail))
                flash("新規子機を登録しました。", "success")
                return redirect(url_for("admin_units"))
            except ValueError:
                flash("在庫数と利用可否は数字で入力してください。", "error")
            except Exception as e:
                code = e.errno if isinstance(e, MySQLError) else -1
                flash(f"[コード {code}] 子機登録中にエラーが発生しました: {e}", "error")
        else:
            flash("全ての項目を入力してください。", "warning")
    return render_template("admin_new_unit.html")

@app.route("/admin/history")
def admin_history():
    """View usage history entries."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        history = mydb.call_his()  # raw history data (list of tuples)
        return render_template("admin_history.html", history=history)
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] 履歴の取得中にエラーが発生しました: {e}", "error")
        return render_template("admin_history.html", history=[])

@app.route("/admin/backup")
def admin_backup_download():
    """Trigger a data backup and send the backup Excel file to the user."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        mydb.make_backup()  # create backup Excel (likely named 'backup.xlsx')
        # Send the backup file to the client for download
        backup_filename = "データ復元時はファイル名を「backup」にしてください.xlsx"
        backup_path = os.path.join(os.getcwd(), backup_filename)
        if os.path.exists(backup_path):
            return send_file(backup_path, as_attachment=True)
        else:
            flash("バックアップファイルの作成に失敗しました。", "error")
            return redirect(url_for("admin_dashboard"))
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] バックアップ処理中にエラーが発生しました: {e}", "error")
        return redirect(url_for("admin_dashboard"))

@app.route("/admin/restore", methods=["GET", "POST"])
def admin_restore():
    """Restore data from an uploaded backup Excel file."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        file = request.files.get("backup_file")
        if file and file.filename != '':
            try:
                # Save uploaded file as 'backup.xlsx' which is expected by the db module
                file.save("backup.xlsx")
                mydb.copy_from_excel("backup")
                flash("バックアップからデータを復元しました。", "success")
            except Exception as e:
                code = e.errno if isinstance(e, MySQLError) else -1
                flash(f"[コード {code}] データ復元に失敗しました。ファイル形式を確認してください。エラー: {e}", "error")
        else:
            flash("ファイルが選択されていません。", "warning")
        return redirect(url_for("admin_dashboard"))
    # GET: show upload form
    return render_template("admin_restore.html")

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
        print(f"Error registering user: {e}")
        raise

# -------------------------------------------------------------
#  Web / Desktop 共通: 学生証をタッチして利用状況を得る
# -------------------------------------------------------------
def check_usage():
    try:
        mydb.id_do()                 # カード読み取り
        member_info = mydb.add_find()
        if not member_info:
            flash("学生証が登録されていません。", "warning")
            return render_template("usage.html", reader_connected=True)
        # 必要情報をテンプレートへ
        return render_template(
            "usage_result.html",
            cardid   = member_info[0],
            stock    = member_info[1],
            allow    = member_info[2],
            entry_at = member_info[3],
            total    = member_info[6],
        )
    except Exception as e:
        code = e.errno if isinstance(e, MySQLError) else -1
        flash(f"[コード {code}] 利用状況確認中にエラーが発生しました: {e}", "error")
        return render_template("usage.html", reader_connected=False)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
