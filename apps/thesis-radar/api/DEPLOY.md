# Deploy API (from repo root):
#   fly deploy --config apps/thesis-radar/api/fly.toml
#
# Set secrets:
#   fly secrets set DATABASE_URL=... NVIDIA_NIM_API_KEY=... --app thesis-radar-api

[build]
dockerfile = "apps/thesis-radar/api/Dockerfile"

# Required secrets (set via fly secrets set):
#   DATABASE_URL
#   NVIDIA_NIM_API_KEY
#   GEMINI_API_KEY          (optional fallback)

# Optional:
#   CORS_ORIGINS            (comma-separated, e.g. https://your-app.vercel.app)
