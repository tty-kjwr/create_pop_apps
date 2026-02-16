# ポップ作成ツール

店頭POP（ポイント・オブ・パーチェス）を簡単に作成できるWindowsアプリケーションです。

## 機能

- 背景画像のアップロード
- 商品情報の入力（商品名、数量、価格など）
- 元値を赤い一重線で表示
- 税込価格を大きく目立たせて表示
- 1920×1080の高解像度PNG画像として保存
- リアルタイムプレビュー

## EXEファイルの作成方法

### 必要なもの
- Python 3.8以上がインストールされていること
- インターネット接続（初回のみ）

### ビルド手順

1. **簡単な方法（推奨）**
   ```
   build_exe.bat をダブルクリック
   ```
   
   このバッチファイルが自動的に：
   - 必要なライブラリをインストール
   - EXEファイルをビルド
   
   完成したEXEファイルは `dist\ポップ作成ツール.exe` に作成されます。

2. **手動でビルドする場合**
   
   コマンドプロンプトで以下を実行：
   
   ```bash
   # 1. 依存ライブラリをインストール
   pip install -r requirements.txt
   pip install pyinstaller
   
   # 2. EXEファイルをビルド
   pyinstaller --onefile --windowed --name "ポップ作成ツール" pop_creator.py
   ```

## 使い方

1. **背景画像を選択**
   - 「画像を選択」ボタンをクリック
   - お好みの背景画像を選択

2. **商品情報を入力**
   - 商品名
   - 個数またはg数（ラジオボタンで選択）
   - 元値（税抜）
   - 割引値（税抜）
   - 税込価格

3. **ポップを生成**
   - 入力すると自動的にプレビューが更新されます
   - 「ポップを生成」ボタンで再生成も可能

4. **画像を保存**
   - 「画像を保存」ボタンをクリック
   - 保存先とファイル名を指定
   - PNG形式（1920×1080）で保存されます

## 出力仕様

- **解像度**: 背景画像のサイズに自動的に合わせます
- **フォーマット**: PNG
- **表示内容**:
  - 商品名（上部）
  - 数量（個数/g数）
  - 元値（赤い二重線で取り消し）+ 円(税抜)
  - 割引値 + 円(税抜)
  - 税込価格（大きく表示）+ 円
  - 「税込」ラベル
- **フォントサイズ**: 画像サイズに応じて自動的にスケール調整

## トラブルシューティング

### フォントが正しく表示されない
- Windowsの場合、MS ゴシックフォントが使用されます
- フォントファイルが見つからない場合、デフォルトフォントにフォールバックします

### ビルドに失敗する
1. Pythonのバージョンを確認（3.8以上が必要）
2. すべてのファイル（pop_creator.py、requirements.txt、build_exe.bat）が同じフォルダにあるか確認
3. 管理者権限でコマンドプロンプトを実行してみる

## ファイル構成

```
ポップ作成ツール/
├── pop_creator.py          # メインプログラム
├── requirements.txt        # 依存ライブラリ
├── build_exe.bat          # EXEビルド用バッチファイル
└── README.md              # このファイル
```

## 開発環境で実行する場合

```bash
# 依存ライブラリをインストール
pip install -r requirements.txt

# プログラムを実行
python pop_creator.py
```

## License

This project is licensed under the MIT License.

Copyright (c) 2026 Tatsuya Kajiwara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

## ライセンス

本ソフトウェアは MIT License のもとで公開されています。

Copyright (c) 2026 カジワラ タツヤ

本ソフトウェアおよび関連文書ファイル（以下「本ソフトウェア」）の複製を取得したすべての人に対し、
本ソフトウェアを無償で使用、複製、改変、結合、公開、頒布、再許諾、および販売する権利を含む、
制限のない取り扱いを許可します。
ただし、以下の条件に従うものとします。

上記の著作権表示および本許諾表示を、本ソフトウェアのすべての複製または重要な部分に
記載しなければなりません。

本ソフトウェアは「現状のまま」で提供され、明示または黙示を問わず、
商品性、特定目的への適合性、および権利非侵害についての保証を含め、
いかなる保証も行いません。
著作者または著作権者は、本ソフトウェアの使用またはその他の取扱いから生じる
いかなる請求、損害、その他の責任についても責任を負いません。

