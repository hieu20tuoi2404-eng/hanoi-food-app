# Ăn Gì Hà Nội?

Ứng dụng web local tổng hợp món ăn Hà Nội, gamified theo phong cách "Trưa Nay Ăn Gì?": **Hòm tiếp tế** (mở hòm quay món theo ngân sách), **Quẻ trưa** (xin quẻ bói món), hệ thống **độ hiếm** (CỰC PHẨM / ĐẶC BIỆT / HIẾM / QUỐC DÂN / TỐI MẬT) + danh sách món theo bữa, quán + Google Maps, công thức và đánh giá 1-10.

**Stack:** React + Vite (frontend) · FastAPI (backend) · SQLite (database)

> ⚠️ Toàn bộ dữ liệu seed là **Demo / Chưa xác minh** — không bịa ảnh, địa chỉ, giá, đánh giá hay công thức. Mọi ảnh, địa chỉ và công thức đều có trường `source`. Khi có dữ liệu thật, hãy cập nhật lại bản ghi.

## Tính năng nổi bật

- 📦 **Hòm tiếp tế** — chọn ngân sách + loại bữa, nhấn "MỞ HÒM" để quay ngẫu nhiên một món (hiệu ứng mở hòm + hạt bắn tung)
- 🔮 **Quẻ trưa** — xin quẻ bói trưa ăn gì kèm lời "duyên vị" vui vẻ (`/api/fortunes`)
- 💎 **Độ hiếm** tính từ điểm đánh giá: ≥9 CỰC PHẨM · ≥8.5 ĐẶC BIỆT · ≥8.0 HIẾM · ≥7.0 QUỐC DÂN · còn lại TỐI MẬT
- 🎨 Ảnh minh hoạ SVG tự tạo cho từng món (`frontend/public/images/*.svg`, script tại `frontend/scripts/generate_images.py`)
- 🔎 Tìm kiếm món theo từ khoá + lọc theo quận, giá, điểm
- 🏪 Chi tiết món: quán kèm Google Maps, công thức nấu, đánh giá + form gửi đánh giá

## Cấu trúc

```
hanoi-food-app/
├── backend/
│   ├── database.py      # SQLite schema + connection
│   ├── models.py        # Pydantic models + hệ thống độ hiếm (RARITY_TIERS)
│   ├── seed.py          # 30 món demo + quán + công thức + đánh giá
│   ├── main.py          # FastAPI app & routes
│   ├── test_backend.py  # pytest (33 tests)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── scripts/generate_images.py   # sinh SVG ảnh món ăn
│   ├── public/images/               # SVG tự tạo cho 30 món
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       ├── components/ (Navbar, DishCard, FilterBar, RarityBadge, LootBox, QuaTrua)
│       └── pages/ (Home, DishDetail)
├── data/                # hanoi_food.db (tạo tự động khi chạy)
├── docker-compose.yml
└── .env.example
```

## API

| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| GET | `/api/health` | Trạng thái + số món |
| GET | `/api/categories` | Danh sách nhóm bữa |
| GET | `/api/dishes` | DS món (bộ lọc: `meal`, `district`, `min_price`, `max_price`, `min_rating`, `search`) — kèm `rarity` |
| GET | `/api/dishes/{slug}` | Chi tiết món (quán + công thức + đánh giá + `rarity`) |
| GET | `/api/dishes/random?meal=&min_price=&max_price=` | Quay random món theo bữa/ngân sách |
| GET | `/api/fortunes?meal=` | Quẻ trưa: ngẫu nhiên món + lời quẻ vui |
| GET | `/api/dishes/{id}/restaurants` | DS quán bán món |
| GET | `/api/dishes/{id}/recipe` | Công thức |
| GET | `/api/dishes/{id}/reviews` | DS đánh giá |
| POST | `/api/dishes/{id}/reviews` | Tạo đánh giá (rating 1-10, comment ≥3 ký tự) |

## Chạy trên Windows bằng PowerShell (không Docker)

### 1. Backend

```powershell
cd C:\Users\NC\Documents\Default Project\hanoi-food-app
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend chạy tại http://localhost:8000 — tài liệu API tại http://localhost:8000/docs

### 2. Frontend (cửa sổ PowerShell thứ hai)

```powershell
cd C:\Users\NC\Documents\Default Project\hanoi-food-app
cd frontend
npm install
npm run dev
```

Mở trình duyệt tại http://localhost:5173

> Lưu ý: `npm` phải có sẵn trên máy (cài Node.js 18+). Nếu chưa có, dùng cách Docker bên dưới.

## Chạy bằng Docker Compose

```powershell
cd C:\Users\NC\Documents\Default Project\hanoi-food-app
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs

Dừng: `Ctrl+C` hoặc `docker compose down`.

## Chạy test

```powershell
cd C:\Users\NC\Documents\Default Project\hanoi-food-app\backend
.\.venv\Scripts\Activate.ps1
python -m pytest test_backend.py -v
```

Test phủ: random món, lọc theo bữa/ngân sách, định dạng Google Maps URL, tạo đánh giá + validation lỗi, hệ thống độ hiếm, và endpoint quẻ trưa.

## Sinh lại ảnh món ăn

Ảnh (SVG) tự sinh bằng `frontend/scripts/generate_images.py` — gradient theo bữa + emoji món ăn + tên món. Để tạo lại:

```powershell
cd C:\Users\NC\Documents\Default Project\hanoi-food-app\frontend
python ..\backend\.venv\Scripts\generate_images.py   # hoặc python scripts\generate_images.py
```

> Lưu ý: script imports `seed` từ `backend`, nên chạy với Python có `aiosqlite` (dùng venv của backend).

## Deploy lên Render (production)

**Link public:** https://hanoi-food-app-ttko.onrender.com

Repo GitHub: https://github.com/hieu20tuoi2404-eng/hanoi-food-app

- `Dockerfile` (root) — multi-stage: build frontend bằng Node → backend FastAPI serve cả API + static
- `render.yaml` — blueprint Web Service (free tier, tự auto-deploy khi push)

Cập nhật code mới: commit + push lên `master` → Render tự build lại. Mọi thay đổi trong `frontend/`, `backend/` đều tự động. Lưu ý free tier: service "ngủ" sau ~15 phút không truy cập, mở lại mất ~30s; SQLite lưu tạm trong container (seed lại sau mỗi restart).

Chạy deploy thủ công bằng Docker:
```powershell
docker build -t an-gi-ha-noi .
docker run -p 8000:8000 an-gi-ha-noi   # mở http://localhost:8000
```

## Google Maps

Địa chỉ quán dùng link chuẩn:

```
https://www.google.com/maps/search/?api=1&query=<tên_quán>+<địa_chỉ>+Hà+Nội
```

## Cấu hình

Copy `.env.example` thành `.env` (tuỳ chọn). Không có secret trong source code.