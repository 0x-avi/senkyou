# Senkyou — Course Search Platform

A full-stack course discovery platform where users can search lectures semantically, preview courses videos for 40 seconds, and unlock full access by paying with crypto (Monad testnet).

---

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14, Tailwind CSS, Privy (embedded wallets), Wagmi |
| Backend | FastAPI, Qdrant (vector DB), sentence-transformers |
| Blockchain | Monad Testnet |

---

## Project Structure

```
project/
├── .env                        # Backend environment variables
├── main.py                     # FastAPI entry point
├── handlers.py                 # Route handler factories
├── routes.py                   # Route registration
├── qdrant/
│   ├── __init__.py             # QdrantManager
│   ├── search.py               # search, search_by_language, keyword_search_lecture
│   └── indexes.py              # create_indexes (language KEYWORD, lectureTitle TEXT)
└── frontend/
    ├── .env.local              # Frontend environment variables
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   └── page.tsx        # Main search + course listing page
    │   ├── components/
    │   │   └── Header.tsx
    │   ├── hooks/
    │   │   ├── useEmbeddedWallet.ts
    │   │   └── useMyContract.ts
    │   └── providers/
    │       └── Providers.tsx   # Privy + Wagmi + React Query
    └── package.json
```

---

## Setup

### 1. Backend

**Install dependencies**
```bash
pip install fastapi uvicorn qdrant-client sentence-transformers python-dotenv
```

**Configure `.env`**
```env
QDRANT_URL=https://your-qdrant-instance.cloud
QDRANT_API_KEY=your_qdrant_api_key
COLLECTION_NAME=courses
EMBEDDING_MODEL=sentence-transformers/all-minilm-l6-v2
FRONTEND_URL=http://localhost:3000
```

**Run**
```bash
uvicorn main:app --reload --port 8000
```

---

### 2. Frontend

**Install dependencies**
```bash
cd frontend
npm install
```

**Configure `frontend/.env.local`**
```env
NEXT_PUBLIC_FASTAPI_URL=http://localhost:8000
NEXT_PUBLIC_PRIVY_APP_ID=your_privy_app_id
NEXT_PUBLIC_PAYMENT_ADDRESS=0xYourWalletAddress
```

**Run**
```bash
npm run dev
```

Frontend runs at `http://localhost:3000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/search?query=&top_k=` | Semantic search across all courses |
| `GET` | `/search_by_language?query=&language=&top_k=` | Semantic search filtered by language code |
| `GET` | `/search_lecture?keyword=&top_k=` | Phrase/keyword search in lecture titles |
| `GET` | `/health` | Health check |

---

Indexes created automatically on startup:
- `language` — KEYWORD index (exact match filter)
- `lectureTitle` — TEXT index with `phrase_matching: true` (word tokenizer)

---

## How Payments Work

1. User clicks a locked lecture and watches a free 40-second preview
2. After preview ends (or at any time), user clicks **Pay & Watch**
3. A transaction is sent to `NEXT_PUBLIC_PAYMENT_ADDRESS` for `0.001 ETH` on Monad testnet
4. On confirmed transaction, the full video is unlocked for that session

> To wire up real payments, replace the `increaseCounter()` call in `handlePay` inside `page.tsx` with:
> ```ts
> sendTransaction({ to: PAYMENT_ADDRESS, value: parseEther(UNLOCK_PRICE_ETH) })
> ```

---

## Running Both Together

```bash
# Terminal 1 — backend (from project root)
uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```
