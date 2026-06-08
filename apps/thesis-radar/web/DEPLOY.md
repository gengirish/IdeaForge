# ThesisRadar Web — deployed via monorepo root

Deploy from **`IdeaForge/`** (repo root), not this directory:

```bash
# From D:\codebase\IdeaForge
npm run deploy:web
# or
vercel deploy --prod
```

Production URL: https://thesis-radar-seven.vercel.app

Vercel config: `vercel.json` at repo root points build output to `apps/thesis-radar/web/.next`.

Required Vercel env vars (Production):

| Variable | Example |
|----------|---------|
| `DATABASE_URL` | Neon connection string |
| `SIGNAL_ENGINE_API_URL` | `https://thesis-radar-api.fly.dev` |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk publishable key |
| `CLERK_SECRET_KEY` | Clerk secret key |
