# 椅子レコメンドアプリ 設計書・作業手順書

## 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [技術スタック](#2-技術スタック)
3. [リポジトリ構成](#3-リポジトリ構成)
4. [権限設計](#4-権限設計)
5. [データベース設計](#5-データベース設計)
6. [データパイプライン](#6-データパイプライン)
7. [初期DB構築手順](#7-初期db構築手順)
8. [推薦エンジン](#8-推薦エンジン)
9. [プロンプト一覧と仕様](#9-プロンプト一覧と仕様)
10. [画面一覧](#10-画面一覧)
11. [API設計](#11-api設計)
12. [手動セットアップマニュアル（Railway / GitHub）](#12-手動セットアップマニュアルrailway--github)
13. [Claude Codeへの作業指示手順](#13-claude-codeへの作業指示手順)

---

## 1. プロジェクト概要

### 背景
- 椅子紹介YouTuberが、視聴者からの「自分に合った椅子を教えて」という質問に回答している
- 現在は公式LINEのフォームで情報を集め、人力で回答している
- これをLLMを使ったアプリで自動化する

### アプリの機能
1. **推薦機能**：フォーム回答をコピペ → AIがおすすめの椅子を回答
2. **データ管理機能**：YouTube動画から椅子情報を自動抽出・構造化してDBを構築
3. **管理機能**：プロンプト編集、一括構築、名寄せ確認など

### 運用フロー
1. YouTube動画が投稿される
2. アプリが新着動画を検知 → 文字起こし → 椅子情報を抽出
3. YouTuberが管理画面で抽出結果を確認・承認
4. 視聴者がフォーム回答を貼り付け → AIが椅子マスタを参照しておすすめを回答

---

## 2. 技術スタック

| レイヤー | 技術 | 備考 |
|---------|------|------|
| フロントエンド | Next.js（TypeScript） | App Router使用 |
| バックエンド | FastAPI（Python） | |
| DB | PostgreSQL | Railway提供 |
| LLM | Claude API | Anthropic |
| 文字起こし | YouTube字幕API → Whisperフォールバック | |
| デプロイ | Railway | フロント・バック両方 |
| リポジトリ | GitHub | モノレポ |
| 認証 | 環境変数ベースのパスワード認証 | 初期段階はシンプルに |

---

## 3. リポジトリ構成

```
chair-recommender/
├── frontend/                    # Next.js
│   ├── app/
│   │   ├── page.tsx                    # 推薦画面（トップ）
│   │   ├── layout.tsx                  # 共通レイアウト
│   │   ├── login/
│   │   │   └── page.tsx                # 管理者ログイン
│   │   ├── admin/
│   │   │   ├── prompts/
│   │   │   │   └── page.tsx            # プロンプト編集（管理者のみ）
│   │   │   └── bulk-build/
│   │   │       └── page.tsx            # 一括構築（管理者のみ）
│   │   ├── chairs/
│   │   │   └── page.tsx                # 椅子マスタ管理
│   │   ├── videos/
│   │   │   └── page.tsx                # 動画一覧・処理ステータス
│   │   ├── aliases/
│   │   │   └── page.tsx                # 名寄せ確認・修正
│   │   ├── makers/
│   │   │   └── page.tsx                # メーカー商品一覧管理
│   │   └── logs/
│   │       ├── extraction/
│   │       │   └── page.tsx            # 抽出ログ
│   │       └── recommendation/
│   │           └── page.tsx            # 推薦ログ
│   ├── components/
│   │   ├── ui/                         # 共通UIコンポーネント
│   │   ├── RecommendForm.tsx           # 推薦フォーム
│   │   ├── ChairCard.tsx               # 椅子情報カード
│   │   ├── PromptEditor.tsx            # プロンプトエディタ
│   │   ├── AliasResolver.tsx           # 名寄せ確認UI
│   │   └── Navbar.tsx                  # ナビゲーション
│   ├── lib/
│   │   ├── api.ts                      # バックエンドAPI呼び出し
│   │   └── auth.ts                     # 認証ユーティリティ
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── Dockerfile
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── main.py                     # FastAPIアプリケーション
│   │   ├── config.py                   # 設定・環境変数
│   │   ├── database.py                 # DB接続
│   │   ├── routers/
│   │   │   ├── recommend.py            # 推薦API
│   │   │   ├── chairs.py               # 椅子マスタCRUD
│   │   │   ├── videos.py               # 動画管理
│   │   │   ├── aliases.py              # 名寄せ
│   │   │   ├── prompts.py              # プロンプト管理
│   │   │   ├── pipeline.py             # 一括構築・差分更新
│   │   │   ├── makers.py               # メーカー商品一覧
│   │   │   ├── logs.py                 # ログ参照
│   │   │   └── auth.py                 # 認証
│   │   ├── services/
│   │   │   ├── youtube.py              # YouTube API連携
│   │   │   ├── transcription.py        # 文字起こし
│   │   │   ├── llm.py                  # Claude API呼び出し（プロンプトDB参照）
│   │   │   ├── extraction.py           # 椅子情報抽出
│   │   │   ├── alias_resolution.py     # 名寄せ処理
│   │   │   ├── recommendation.py       # 推薦ロジック
│   │   │   └── scraper.py              # メーカーサイトスクレイピング
│   │   └── models/
│   │       ├── chair.py                # 椅子マスタ
│   │       ├── video.py                # 動画
│   │       ├── alias.py                # エイリアス
│   │       ├── prompt.py               # プロンプト
│   │       ├── extraction_log.py       # 抽出ログ
│   │       ├── recommendation_log.py   # 推薦ログ
│   │       └── maker_product.py        # メーカー商品
│   ├── alembic/                        # DBマイグレーション
│   │   └── versions/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
├── railway.toml
└── README.md
```

---

## 4. 権限設計

### エンドユーザー（未ログイン）
アクセス可能な画面：
- 推薦画面（フォーム貼り付け → 回答）
- 動画一覧・処理ステータス（閲覧のみ）
- メーカー商品一覧（閲覧のみ）
- 椅子マスタ管理（閲覧・編集）
- 名寄せ確認・修正
- 抽出ログ
- 推薦ログ
- 要確認リスト

### 管理者（ログイン済み）
上記に加えて：
- プロンプト編集画面
- 一括構築モード

### 認証方式（初期段階）
- 環境変数 `ADMIN_PASSWORD` にパスワードを設定
- `/login` 画面でパスワード入力 → セッションCookie発行
- 管理者専用ページはミドルウェアでセッション確認
- 未ログインで管理者ページにアクセス → ログイン画面にリダイレクト

---

## 5. データベース設計

### テーブル一覧

#### chairs（椅子マスタ）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| canonical_name | TEXT | 正式名称 |
| maker | TEXT | メーカー名 |
| model_number | TEXT | 型番（nullable） |
| price_range | TEXT | 価格帯 |
| features | JSONB | 特徴（座り心地、素材、調整機能等） |
| target_users | JSONB | 向いている人（体型、用途等） |
| pros | JSONB | メリット一覧 |
| cons | JSONB | デメリット一覧 |
| comparison_notes | TEXT | 他の椅子との比較メモ |
| is_recommendable | BOOLEAN | 紹介可否フラグ（デフォルト: false = 要確認） |
| source_video_ids | JSONB | 情報元の動画IDリスト |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

#### chair_aliases（エイリアス）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| chair_id | UUID | FK → chairs |
| alias | TEXT | 別名・通称 |
| source_video_id | UUID | どの動画で使われた表現か（nullable） |
| created_at | TIMESTAMP | |

#### videos（動画）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| youtube_video_id | TEXT | YouTubeの動画ID（UNIQUE） |
| title | TEXT | 動画タイトル |
| published_at | TIMESTAMP | 公開日 |
| url | TEXT | 動画URL |
| status | TEXT | 処理ステータス: pending / transcribed / extracted / reviewed |
| transcript | TEXT | 文字起こしテキスト |
| transcript_source | TEXT | youtube_caption / whisper |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

#### extraction_logs（抽出ログ）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| video_id | UUID | FK → videos |
| chair_id | UUID | FK → chairs（nullable、未紐づけの場合） |
| raw_mention | TEXT | 動画内での生の言及表現 |
| context | TEXT | 前後の文脈テキスト |
| timestamp_hint | TEXT | 動画内のおおよその位置 |
| confidence | TEXT | high / medium / low |
| status | TEXT | auto_matched / manually_matched / unresolved |
| created_at | TIMESTAMP | |

#### prompts（プロンプト）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| key | TEXT | プロンプト識別キー（UNIQUE） |
| name | TEXT | 表示名 |
| description | TEXT | 用途の説明 |
| content | TEXT | プロンプト本文 |
| version | INTEGER | バージョン番号 |
| is_active | BOOLEAN | 有効フラグ |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

#### prompt_versions（プロンプトバージョン履歴）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| prompt_id | UUID | FK → prompts |
| version | INTEGER | バージョン番号 |
| content | TEXT | その時点のプロンプト本文 |
| created_at | TIMESTAMP | |

#### recommendation_logs（推薦ログ）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| form_input | TEXT | 入力されたフォーム内容 |
| parsed_conditions | JSONB | パース後の構造化条件 |
| recommended_chair_ids | JSONB | 推薦した椅子のIDリスト |
| response_text | TEXT | 生成した推薦文 |
| created_at | TIMESTAMP | |

#### maker_products（メーカー商品一覧）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| maker | TEXT | メーカー名 |
| product_name | TEXT | 商品名 |
| model_number | TEXT | 型番（nullable） |
| source_url | TEXT | スクレイピング元URL |
| created_at | TIMESTAMP | |

#### maker_scrape_configs（メーカースクレイピング設定）
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | PK |
| maker | TEXT | メーカー名 |
| url | TEXT | 商品一覧ページURL |
| scrape_method | TEXT | スクレイピング方法のメモ |
| last_scraped_at | TIMESTAMP | |
| created_at | TIMESTAMP | |

---

## 6. データパイプライン

### 差分更新フロー（通常運用）

```
1. YouTube Data API でチャンネルの動画一覧を取得
2. DBの videos テーブルと比較 → 未登録の動画を検出
3. 未登録動画ごとに：
   a. 動画メタ情報をDBに登録（status: pending）
   b. YouTube字幕APIで文字起こし取得（なければWhisper）
   c. 文字起こしをDBに保存（status: transcribed）
   d. LLMで椅子言及を抽出（プロンプト①使用）
   e. 既存の椅子マスタ + エイリアス辞書と照合（プロンプト④使用）
   f. 抽出結果をextraction_logsに保存
   g. 自動マッチしたものはchair情報を更新
   h. マッチしなかったものは status: unresolved で保存
   i. 動画のstatus を extracted に更新
4. YouTuberが管理画面で確認 → status を reviewed に更新
```

### 一括構築モード（初期構築用）
上記と同じ処理を全動画に対して実行する。
管理画面から「一括構築開始」ボタンで起動。
進捗表示あり（全X本中Y本完了）。

---

## 7. 初期DB構築手順

### Phase 1: 全動画の文字起こし
- チャンネル内の全動画をリストアップ
- 各動画の文字起こしを取得（YouTube字幕 → Whisperフォールバック）
- DBに保存

### Phase 2: メーカー公式サイトから商品一覧をスクレイピング
- YouTuberがよく扱うメーカーのサイトURLを管理画面で登録
- スクレイピングして正式名称・型番リストを取得
- maker_products テーブルに保存
- この商品一覧はPhase 4の名寄せ時にLLMの参照情報として使用

### Phase 3: LLMで椅子言及を全件抽出
- 全動画の文字起こしに対してプロンプト①を実行
- 生の言及表現をそのまま抽出（正式名称に変換しない）
- タイムスタンプ・前後文脈も保持
- extraction_logs に保存

### Phase 4: LLMでクラスタリング・名寄せ
- Phase 3の全抽出結果 + Phase 2のメーカー商品一覧をプロンプト②に渡す
- 同一椅子と思われる言及をグルーピング
- 正式名称の候補を提示
- 確信度（高/中/低）を付与

### Phase 5: YouTuberが確認・修正
- 管理画面の名寄せ確認UIで：
  - グルーピングの正誤を確認
  - 正式名称を確定
  - 要確認・特定不能の言及を解決
  - 紹介可否フラグを設定

### Phase 6: DB投入
- 確定した椅子マスタ + エイリアス辞書をDBに投入
- 各椅子に対してプロンプト③で詳細情報を構造化抽出
- 初期構築完了

---

## 8. 推薦エンジン

### 処理フロー

```
1. ユーザーがフォーム回答テキストを貼り付け
2. プロンプト⑤でフォーム内容をパース → 構造化データ
3. プロンプト⑥で椅子マスタ（is_recommendable = true のみ）から候補をフィルタリング
4. プロンプト⑦で最終的な推薦文を生成
5. 結果を表示 + recommendation_logs に保存
```

### 推薦文に含める情報
- おすすめ椅子（1〜3脚）
- 各椅子の推薦理由（YouTuberの視点を反映）
- メリット・デメリット
- 該当動画へのリンク

---

## 9. プロンプト一覧と仕様

全プロンプトはDBの prompts テーブルに保存し、管理画面から編集可能。
バージョン履歴も保持する。

### データパイプライン系

#### ① 椅子言及抽出プロンプト（key: `extract_mentions`）
- **用途**: 文字起こしテキストから椅子に関する言及を抜き出す
- **入力**: 動画の文字起こし全文
- **出力**: 言及表現、タイムスタンプ、前後の文脈（JSON形式）
- **チューニング観点**:
  - 抽出漏れと過剰抽出のバランス
  - 椅子以外の家具（デスク等）を拾わないか
  - 「これ」「さっきの」のような指示語の扱い
  - 出力JSON形式の安定性

#### ② クラスタリング・名寄せプロンプト（key: `cluster_aliases`）
- **用途**: 抽出した言及表現を同一椅子ごとにグルーピング
- **入力**: 全動画の言及表現リスト ＋ メーカー商品一覧
- **出力**: グループ、正式名称候補、確信度（JSON形式）
- **チューニング観点**:
  - 分割エラー（同一椅子を別グループにしてしまう）
  - 統合エラー（別の椅子を同一グループにまとめてしまう）
  - メーカー商品一覧との照合精度
  - 確信度の適切さ

#### ③ 椅子情報構造化プロンプト（key: `structure_chair_info`）
- **用途**: 文字起こしから各椅子の特徴・評価・向いている人などを抽出
- **入力**: 文字起こしテキスト ＋ 対象椅子の正式名称
- **出力**: 特徴、評価コメント、メリット/デメリット、向いている体型・用途、価格帯、比較対象（JSON形式）
- **チューニング観点**:
  - YouTuberの主観的評価と客観的スペック情報の切り分け
  - 複数動画にまたがる情報の統合時の矛盾
  - 動画内で言っていないことを補完していないか（ハルシネーション）

#### ④ 差分更新プロンプト（key: `update_diff`）
- **用途**: 新動画追加時に既存マスタとの差分を処理
- **入力**: 新動画の文字起こし ＋ 既存椅子マスタ ＋ エイリアス辞書
- **出力**: 既存椅子への情報追加、新規椅子候補、エイリアス追加候補（JSON形式）
- **チューニング観点**:
  - 既存マスタとの整合性
  - 情報の上書きと追記の判断基準

### 推薦エンジン系

#### ⑤ フォーム入力パースプロンプト（key: `parse_form`）
- **用途**: コピペされたフォーム回答を構造化データに変換
- **入力**: フォーム回答テキスト
- **出力**: 体型、用途、予算、こだわりポイント等（JSON形式）
- **チューニング観点**:
  - フォーマットが多少崩れても正しくパースできるか
  - 未記入項目の扱い

#### ⑥ 椅子候補フィルタリングプロンプト（key: `filter_candidates`）
- **用途**: ユーザー条件に合う椅子を絞り込む
- **入力**: 構造化されたユーザー条件 ＋ 椅子マスタ全件（紹介可のもの）
- **出力**: 候補椅子リスト（スコア・選定理由付き、JSON形式）
- **チューニング観点**:
  - 条件の優先度判断（予算厳守 vs 多少超えてもベスト）
  - 該当なしの場合の振る舞い
  - 候補数の適切さ

#### ⑦ 推薦文生成プロンプト（key: `generate_recommendation`）
- **用途**: 最終的なおすすめ回答を生成
- **入力**: ユーザー条件 ＋ 候補椅子 ＋ 各椅子の評価情報 ＋ 動画リンク
- **出力**: YouTuberの口調に沿った推薦文（テキスト）
- **チューニング観点**:
  - YouTuberのトーン再現度
  - 推薦理由の説得力
  - 動画への誘導の自然さ
  - 断定の強さの調整
  - 複数候補の比較の仕方

### 管理・品質系

#### ⑧ 抽出結果検証プロンプト（key: `verify_extraction`）
- **用途**: 他のプロンプトの出力をセルフチェック
- **入力**: 抽出結果 ＋ 元の文字起こし
- **出力**: 矛盾点、ハルシネーションの疑い、確信度の再評価（JSON形式）
- **チューニング観点**:
  - チェックの厳しさ
  - 偽陽性（正しいのに疑わしいと判定）の頻度
- **優先度**: 初期リリース後でもOK

---

## 10. 画面一覧

### 共通画面（エンドユーザー・管理者共通）

#### 推薦画面（トップ: `/`）
- テキストエリア：フォーム回答の貼り付け
- 「おすすめを聞く」ボタン
- 回答表示エリア（おすすめ椅子、推薦理由、動画リンク）
- ローディング表示

#### 動画一覧（`/videos`）
- チャンネルの動画一覧
- 各動画の処理ステータス（pending / transcribed / extracted / reviewed）
- 差分更新の「新着チェック」ボタン
- 動画ごとの文字起こし閲覧

#### メーカー商品一覧（`/makers`）
- メーカーごとの商品リスト
- スクレイピング元URLの設定
- 「スクレイピング実行」ボタン
- 取得結果の確認・編集

#### 椅子マスタ管理（`/chairs`）
- 椅子一覧（正式名称、メーカー、紹介可否フラグ）
- 椅子詳細編集（特徴、ターゲット、メリット/デメリット等）
- エイリアス一覧・追加・削除
- 紹介可否フラグの切り替え

#### 名寄せ確認（`/aliases`）
- 未解決の言及一覧
- 各言及に対して「どの椅子？」を選択 or 新規椅子として登録
- 前後文脈・動画リンクの表示
- 一括承認機能

#### 抽出ログ（`/logs/extraction`）
- どの動画のどの発言からどの椅子を抽出したかのトレース
- フィルタ：動画別、椅子別、確信度別、ステータス別

#### 推薦ログ（`/logs/recommendation`）
- 過去の推薦結果一覧
- 入力内容・パース結果・推薦椅子・生成文の全履歴

### 管理者専用画面

#### プロンプト編集（`/admin/prompts`）
- 全8種のプロンプト一覧
- プロンプトごとの編集エディタ（シンタックスハイライト付き）
- バージョン履歴の閲覧・ロールバック
- テスト実行機能（サンプル入力で試せる）

#### 一括構築（`/admin/bulk-build`）
- Phase 1〜6 の各ステップを順に実行するUI
- 進捗表示（全X本中Y本完了）
- 各フェーズの開始・停止ボタン
- エラー発生時の再実行機能

### ナビゲーション
- サイドバー形式
- 管理者ログイン時のみ「プロンプト編集」「一括構築」メニューを表示
- 未ログイン時でも他の全メニューにアクセス可能

---

## 11. API設計

### 認証
| Method | Path | 説明 |
|--------|------|------|
| POST | `/api/auth/login` | 管理者ログイン |
| POST | `/api/auth/logout` | ログアウト |
| GET | `/api/auth/me` | 現在のセッション確認 |

### 推薦
| Method | Path | 説明 |
|--------|------|------|
| POST | `/api/recommend` | フォーム内容を送信 → 推薦結果を取得 |

### 椅子マスタ
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/chairs` | 椅子一覧取得 |
| GET | `/api/chairs/{id}` | 椅子詳細取得 |
| POST | `/api/chairs` | 椅子新規登録 |
| PUT | `/api/chairs/{id}` | 椅子情報更新 |
| DELETE | `/api/chairs/{id}` | 椅子削除 |
| PATCH | `/api/chairs/{id}/recommendable` | 紹介可否フラグ切り替え |

### エイリアス
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/chairs/{id}/aliases` | 椅子のエイリアス一覧 |
| POST | `/api/chairs/{id}/aliases` | エイリアス追加 |
| DELETE | `/api/aliases/{id}` | エイリアス削除 |

### 動画
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/videos` | 動画一覧取得 |
| GET | `/api/videos/{id}` | 動画詳細（文字起こし含む） |
| POST | `/api/videos/sync` | 新着動画チェック実行 |

### メーカー商品
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/makers` | メーカー一覧 |
| GET | `/api/makers/{maker}/products` | メーカーの商品一覧 |
| POST | `/api/makers/scrape` | スクレイピング実行 |
| POST | `/api/makers/configs` | スクレイピング設定追加 |
| PUT | `/api/makers/configs/{id}` | スクレイピング設定更新 |

### パイプライン
| Method | Path | 説明 |
|--------|------|------|
| POST | `/api/pipeline/bulk-build` | 一括構築開始（管理者のみ） |
| GET | `/api/pipeline/bulk-build/status` | 一括構築の進捗（管理者のみ） |
| POST | `/api/pipeline/extract/{video_id}` | 特定動画の抽出実行 |
| POST | `/api/pipeline/cluster` | クラスタリング・名寄せ実行 |

### 名寄せ
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/extraction-logs?status=unresolved` | 未解決の言及一覧 |
| PATCH | `/api/extraction-logs/{id}/resolve` | 言及を椅子に紐づけ |
| POST | `/api/extraction-logs/{id}/ignore` | 言及を無視 |

### プロンプト（管理者のみ）
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/prompts` | プロンプト一覧 |
| GET | `/api/prompts/{key}` | プロンプト詳細 |
| PUT | `/api/prompts/{key}` | プロンプト更新（バージョン自動インクリメント） |
| GET | `/api/prompts/{key}/versions` | バージョン履歴 |
| POST | `/api/prompts/{key}/rollback/{version}` | 特定バージョンにロールバック |
| POST | `/api/prompts/{key}/test` | テスト実行 |

### ログ
| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/logs/extraction` | 抽出ログ一覧 |
| GET | `/api/logs/recommendation` | 推薦ログ一覧 |

---

## 12. 手動セットアップマニュアル（Railway / GitHub）

ここではClaude Codeでは自動化しにくい部分を手動で行います。
所要時間：15〜20分程度。

### 前提条件
- GitHubアカウントを持っていること
- Railwayアカウントを持っていること（https://railway.app でサインアップ。GitHubアカウントで登録可）
- Anthropic APIキーを取得済みであること（https://console.anthropic.com）
- YouTube Data API キーを取得済みであること（手順は下記参照）

### Step 0: YouTube Data APIキーの取得

1. https://console.cloud.google.com にアクセス（Googleアカウントでログイン）
2. 画面上部の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例: `chair-recommender`）→「作成」
4. 左メニューの「APIとサービス」→「ライブラリ」をクリック
5. 検索欄で「YouTube Data API v3」と検索
6. 「YouTube Data API v3」をクリック →「有効にする」ボタンをクリック
7. 左メニューの「APIとサービス」→「認証情報」をクリック
8. 「＋ 認証情報を作成」→「APIキー」をクリック
9. 表示されるAPIキーをコピーして安全な場所に保存
10. （推奨）「キーを制限」をクリック → 「APIの制限」で「YouTube Data API v3」のみ選択 → 保存

### Step 1: Railwayでプロジェクト作成

1. https://railway.app にログイン
2. ダッシュボード画面で「**New Project**」ボタンをクリック
3. 「**Empty Project**」を選択
4. プロジェクトが作成される。画面上部にプロジェクト名が表示されるので、クリックして名前を変更（例: `chair-recommender`）

### Step 2: PostgreSQLの追加

1. プロジェクト画面の右上「**+ New**」ボタンをクリック
2. 「**Database**」→「**Add PostgreSQL**」を選択
3. PostgreSQLのサービスが追加される
4. 追加されたPostgreSQLサービスをクリック
5. 「**Variables**」タブをクリック
6. `DATABASE_URL` の値をコピーしてメモ帳等に保存（後で使います）

### Step 3: バックエンドサービスの作成

1. プロジェクト画面の「**+ New**」→「**GitHub Repo**」を選択
2. 初回の場合、GitHubとの連携認証を求められるので許可する
3. リポジトリ一覧が表示される。ここではまだリポジトリがないので、**Step 5の後に再度この手順を行います**
4. （Step 5の後に）リポジトリ `chair-recommender` を選択
5. サービスが作成されたら、サービス名をクリック →「**Settings**」タブ
6. 「**Root Directory**」に `backend` と入力
7. 「**Variables**」タブで以下の環境変数を追加：

| 変数名 | 値 |
|--------|-----|
| `DATABASE_URL` | Step 2でコピーしたもの |
| `ANTHROPIC_API_KEY` | Anthropic APIキー |
| `YOUTUBE_API_KEY` | YouTube Data APIキー |
| `ADMIN_PASSWORD` | 任意の管理者パスワード |
| `SESSION_SECRET` | 任意のランダム文字列（30文字以上推奨） |
| `FRONTEND_URL` | （Step 4の後にフロントエンドのURLを設定） |

### Step 4: フロントエンドサービスの作成

1. プロジェクト画面の「**+ New**」→「**GitHub Repo**」を選択
2. 同じリポジトリ `chair-recommender` を選択
3. サービスが作成されたら、サービス名をクリック →「**Settings**」タブ
4. 「**Root Directory**」に `frontend` と入力
5. 「**Variables**」タブで以下の環境変数を追加：

| 変数名 | 値 |
|--------|-----|
| `NEXT_PUBLIC_API_URL` | バックエンドサービスのURL（Settingsタブの「Networking」→「Public Networking」で生成されるURL） |

### Step 5: GitHubリポジトリの作成（Claude Codeで実行）

この手順はClaude Codeが行います。Claude Codeがリポジトリを作成・pushした後に、Step 3 と Step 4 に戻ってGitHubリポジトリとの連携を行ってください。

### Step 6: 公開URLの設定

1. バックエンドサービスをクリック →「**Settings**」→「**Networking**」
2. 「**Public Networking**」の「**Generate Domain**」をクリック
3. 生成されたURL（例: `chair-recommender-backend-production.up.railway.app`）をコピー
4. フロントエンドの環境変数 `NEXT_PUBLIC_API_URL` にこのURLを設定（`https://` 付き）
5. フロントエンドサービスも同様に「**Generate Domain**」を実行
6. バックエンドの環境変数 `FRONTEND_URL` にフロントエンドのURLを設定

### Step 7: デプロイ確認

1. GitHubにpushすると自動的にデプロイが始まる
2. 各サービスの「**Deployments**」タブでデプロイ状況を確認
3. 「**Success**」と表示されれば完了
4. フロントエンドのURLにアクセスしてアプリが表示されることを確認

### トラブルシューティング

**デプロイが失敗する場合**
- 「Deployments」タブでログを確認
- 環境変数の設定漏れがないか確認
- Root Directoryが正しく設定されているか確認

**DBに接続できない場合**
- PostgreSQLサービスの「Variables」で `DATABASE_URL` を再確認
- バックエンドの環境変数にコピーしたURLが正しいか確認

**画面が表示されない場合**
- Public Networkingが有効になっているか確認
- `NEXT_PUBLIC_API_URL` が正しいか確認（`https://` が付いているか）

---

## 13. Claude Codeへの作業指示手順

### 前提
- Claude Codeがインストール済みであること
- ターミナル（Mac: ターミナル.app、Windows: PowerShell）が使えること

### 手順

#### 1. 作業ディレクトリの準備

ターミナルを開いて以下を実行：

```bash
mkdir chair-recommender
cd chair-recommender
```

#### 2. この設計書を配置

このファイル（`chair-recommender-spec.md`）を上記ディレクトリ内に配置します。

#### 3. Claude Codeを起動

```bash
claude
```

#### 4. 設計書を読み込ませて作業開始

Claude Codeが起動したら、以下のように指示します：

```
chair-recommender-spec.md を読んで、このプロジェクトの初期構築を行ってください。

以下の順番で進めてください：

1. GitHubリポジトリの作成（gh repo create）
2. リポジトリ構成に従ってディレクトリ・ファイルを作成
3. バックエンド（FastAPI）の実装
4. フロントエンド（Next.js）の実装
5. Dockerfile・railway.tomlの作成
6. DBマイグレーションファイルの作成
7. 初期プロンプトデータの投入スクリプト作成
8. commit & push

まず設計書を確認して、質問があれば聞いてください。
なければ順番に進めてください。
```

#### 5. 作業の進行

- Claude Codeが順に作業を進めます
- 途中で質問が来た場合は回答してください
- エラーが発生した場合は、エラー内容を貼り付ければ対処してくれます

#### 6. push後のRailway設定

Claude Codeがpushを完了したら、**Step 3〜Step 7**（手動セットアップマニュアル）に戻って、RailwayでのGitHub連携と環境変数の設定を行います。

#### 7. 動作確認

デプロイが完了したら：
1. フロントエンドのURLにアクセス
2. 管理者ログインを試す
3. YouTubeチャンネルURLを設定して動画の取り込みを試す

---

## 補足：開発時のTips

### Claude Codeに追加作業を依頼する場合

```
chair-recommender-spec.md のセクションXXを参照して、○○の機能を修正してください
```

のように、設計書のどの部分に対応する作業かを明示すると精度が上がります。

### プロンプトの初期値について

初期プロンプトは一旦仮の内容で作成し、実際のYouTubeチャンネルのデータで試しながらチューニングしていく形になります。Claude Codeに「プロンプト①の初期版を作って」と依頼すれば、設計書の仕様に基づいて作成してくれます。

### 段階的な開発

一度に全機能を完成させる必要はありません。以下の順序で段階的に進めるのがおすすめです：

1. **Phase 1**: バックエンド基盤（DB、認証、基本API）＋フロントエンド骨格
2. **Phase 2**: データパイプライン（YouTube連携、文字起こし、抽出）
3. **Phase 3**: 初期DB構築機能（一括構築、名寄せ）
4. **Phase 4**: 推薦エンジン
5. **Phase 5**: プロンプト管理・チューニング機能
6. **Phase 6**: ログ・モニタリング
