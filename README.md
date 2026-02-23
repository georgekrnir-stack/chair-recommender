# 椅子レコメンドアプリ

AIが最適な椅子を提案するWebアプリケーション。

## 技術スタック

- **フロントエンド**: Next.js (TypeScript) + Tailwind CSS
- **バックエンド**: FastAPI (Python)
- **DB**: PostgreSQL
- **LLM**: Claude API (Anthropic)
- **デプロイ**: Railway

## セットアップ

### バックエンド

```bash
cd backend
pip install -r requirements.txt
# .env ファイルを作成して環境変数を設定
alembic upgrade head
python seed_prompts.py
uvicorn app.main:app --reload
```

### フロントエンド

```bash
cd frontend
npm install
# .env.local に NEXT_PUBLIC_API_URL を設定
npm run dev
```

### 環境変数

#### バックエンド
| 変数名 | 説明 |
|--------|------|
| `DATABASE_URL` | PostgreSQL接続URL |
| `ANTHROPIC_API_KEY` | Anthropic APIキー |
| `YOUTUBE_API_KEY` | YouTube Data API v3 キー |
| `ADMIN_PASSWORD` | 管理者パスワード |
| `SESSION_SECRET` | セッション署名用シークレット |
| `FRONTEND_URL` | フロントエンドURL（CORS用） |

#### フロントエンド
| 変数名 | 説明 |
|--------|------|
| `NEXT_PUBLIC_API_URL` | バックエンドAPIのURL |

## デプロイ

Railway にデプロイする場合は `chair-recommender-spec.md` の「手動セットアップマニュアル」を参照してください。
