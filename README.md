<!--
README: Oiteru Registration System
最終更新日: 2025-07-09
-->

# オイテル登録システム

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Tkinter-標準-FFDB4D?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql" />
  <img src="https://img.shields.io/badge/nfcpy-1.x-26A8DF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Raspberry%20Pi-子機対応-C51A4A?style=for-the-badge&logo=raspberrypi" />
</p>

---

## 目次
1. [概要](#概要)
2. [主な機能](#主な機能)
3. [システム構成図](#システム構成図)
4. [ディレクトリ構成](#ディレクトリ構成)
5. [セットアップ手順](#セットアップ手順)
6. [コマンド一覧](#コマンド一覧)
7. [トラブルシューティング](#トラブルシューティング)
8. [アップデート履歴](#アップデート履歴)

---

## 概要

東京都市大学×東急グループによる学生ICカード登録・利用管理システムです。NFCリーダーで学生証を登録・管理し、利用状況の確認や履歴管理、データバックアップ/リストア、Raspberry Pi子機連携など、学内の貸出・利用管理を一元化します。

- **Webアプリ（Flask）** と **デスクトップアプリ（Tkinter）** の両方を提供
- **Raspberry Pi子機** で遠隔ICカード利用も可能
- 管理者ダッシュボード・履歴・バックアップ・多彩な管理機能

---

## 主な機能

- **ICカード登録・重複防止**: NFCリーダーで学生証をタップするだけで登録。既存カードは「登録済み」と明示。
- **利用状況確認**: 残り利用回数や利用可否を即時表示。
- **管理者ダッシュボード**: ユーザー・子機・履歴・設定・バックアップ管理。
- **Raspberry Pi子機連携**: 遠隔地でもICカード利用・物理フィードバック。
- **自動DBマイグレーション/バックアップ**: 初回起動時に全テーブル作成・スキーマ移行・バックアップ。
- **エラー通知強化**: MySQLエラーやバージョン不一致時はGUI/WEBで詳細通知。
- **ブランドデザイン**: 東京都市大学ロゴ・東急グループカラー（#26A8DF）採用。

---

## システム構成図

```
+---------------------------+      +---------------------------+
| Desktop App (Tkinter)     |      | Web App (Flask)           |
| home20250506.py           |      | app20250506.py            |
+---------------------------+      +---------------------------+
           |                                 |
           +-------------+-------------------+
                         |
              +---------------------+
              |  MySQL Database     |
              |  mydb20250506.py    |
              +---------------------+
                         |
           +-------------+-------------------+
           |                                 |
+---------------------------+      +---------------------------+
| Subunit (Raspberry Pi)    |      | 管理者ダッシュボード        |
| subunit/unit.py           |      | (Web/GUI共通)              |
+---------------------------+      +---------------------------+
```

---

## ディレクトリ構成

```
.
├── app20250506.py                # Flask Webアプリ本体
├── home20250506.py               # Tkinterデスクトップアプリ本体
├── mydb20250506.py               # DBインターフェース・共通ロジック
├── home2025.py                   # 旧版デスクトップアプリ（参考用）
├── requirements.txt              # Python依存パッケージ一覧
├── データ復元時はファイル名を「backup」にしてください.xlsx # バックアップExcelサンプル
├── backup/                       # 自動バックアップ保存先
│   └── info_last.bak
├── static/                       # 静的ファイル（画像・CSS）
│   ├── css/
│   │   └── style20250506.css     # Web用スタイルシート
│   └── img/
│       └── logo20250506.png      # 東京都市大学ロゴ画像
├── templates/                    # Flask用HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── usage.html
│   ├── usage_result.html
│   ├── usage_status.html
│   ├── usage_error.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_users.html
│   ├── admin_user_detail.html
│   ├── admin_units.html
│   ├── admin_unit_detail.html
│   ├── admin_new_unit.html
│   ├── admin_history.html
│   └── admin_restore.html
├── subunit/                      # 子機（Raspberry Pi）用
│   ├── unit.py                   # 子機アプリ本体
│   ├── mydb2025.py               # 子機用DBインターフェース
│   ├── mydb.py                   # 旧版子機用DB（参考）
│   └── testcode0425/             # テスト・バックアップ
│       └── ひらめき資料関係/
│           └── home2025.py
└── README.md                     # 本ドキュメント
```

---

## セットアップ手順

### 1. 必要環境
- Python 3.11 以上
- MySQL 8.x（`userdb` DBが必要）
- nfcpy対応NFCリーダー（SONY RC-S380等推奨）
- Raspberry Pi（子機利用時）

### 2. 依存パッケージのインストール
1. 仮想環境（推奨）
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Mac/Linux
    ```
2. 必要パッケージをインストール
    ```bash
    pip install -r requirements.txt
    ```

### 3. データベース初期化
1. MySQLサーバーを起動し、`userdb` データベースを作成
    ```sql
    CREATE DATABASE userdb;
    ```
2. アプリ初回起動時に自動でテーブル作成・マイグレーション・バックアップが実行されます
    - DB接続情報は `mydb20250506.py` 内で設定（デフォルト: `localhost`, `root`, `Hiramekigo@1`）
    - デフォルト管理者パスワードは `Hiramekigo@2`（`info`テーブル）

### 4. 静的ファイル
- `static/img/logo20250506.png` に大学ロゴ画像を配置

### 5. アプリ起動
- デスクトップ: `python home20250506.py`
- Web: `python app20250506.py` → http://127.0.0.1:5000/
- 子機: `cd subunit && python unit.py`

---

## コマンド一覧

| 用途         | コマンド例                        |
|--------------|------------------------------------|
| Web起動      | python app20250506.py              |
| GUI起動      | python home20250506.py             |
| 子機起動     | cd subunit && python unit.py       |
| 依存追加     | pip install <パッケージ名>         |
| DB初期化     | アプリ初回起動で自動               |
| バックアップ | 管理画面 or backup.xlsxダウンロード |

---

## トラブルシューティング

- **NFCリーダーが認識されない**
    - nfcpy対応機種か確認、USB接続を再確認、ドライバの再インストール
    - Windowsの場合はRC-S380推奨。Mac/Linuxはroot権限が必要な場合あり
- **MySQL接続エラー**
    - DB名・ユーザー・パスワード・ポート・ホストを確認
    - MySQLサーバーが起動しているか、ファイアウォールでブロックされていないか確認
    - `pymysql.err.OperationalError` などのエラー内容を確認
- **Web画面が真っ白/エラー**
    - テンプレートファイルの有無、依存パッケージを再確認
    - ブラウザのキャッシュクリア、サーバー再起動
- **登録済みカードが再登録される**
    - 2025年7月以降は「info.list」フィールドで厳密判定。`call_info()[6] != "-2"` なら登録済み扱い
- **バックアップ/リストアが失敗する**
    - Excelファイル名・形式が正しいか確認（`backup.xlsx`）
    - ファイルが開いたままになっていないか、権限があるか確認
- **管理者パスワードを忘れた**
    - MySQLで `info` テーブルの `pass` を直接書き換え可能
- **子機（Raspberry Pi）が動作しない**
    - GPIOライブラリ・nfcpy・ネットワーク設定を再確認
    - Windowsでテストする場合はモック実装が使われる
- **依存パッケージのバージョン不整合**
    - `pip install -r requirements.txt --upgrade` で再インストール
- **その他のエラー**
    - エラーメッセージ・スタックトレースを確認し、`mydb20250506.py` の接続情報やパスを見直す
    - 公式ドキュメント・GitHub Issuesも参照

---

<p align="right">(<a href="#top">トップへ</a>)</p>