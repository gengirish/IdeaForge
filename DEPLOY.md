# IdeaForge deployment

## Live URLs

| Service | URL |
|---------|-----|
| Web (Vercel) | https://thesis-radar-seven.vercel.app |
| API (Fly.io) | https://thesis-radar-api.fly.dev |

## Deploy commands (from repo root)

```bash
npm run deploy:web    # Vercel production
npm run deploy:api    # Fly.io
```

## GitHub → Vercel auto-deploy

1. **Create the repo** (one-time) at https://github.com/new as `gengirish/IdeaForge` (empty, no README).

2. **Re-auth GitHub CLI** if `gh` token is expired:
   ```bash
   gh auth login -h github.com
   gh auth switch -u gengirish
   ```

3. **Push:**
   ```bash
   git push -u origin main
   ```

4. **Connect Vercel to GitHub:**
   ```bash
   vercel git connect
   ```
   Pushes to `main` will then trigger automatic Vercel production deploys.

## Clerk (auth)

Add these **Allowed redirect URLs** in [Clerk Dashboard](https://dashboard.clerk.com) → Configure → Paths / URLs:

- `https://thesis-radar-seven.vercel.app/*`
- `http://localhost:3000/*`

Vercel env vars (already set for production):

- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `CLERK_SECRET_KEY`
- `NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in`
- `NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up`
- `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard`
- `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard`

## Fly.io API secrets

```bash
fly secrets set DATABASE_URL=... NVIDIA_NIM_API_KEY=... --app thesis-radar-api
```
