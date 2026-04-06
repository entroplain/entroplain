# Deploying Entroplain Website to Vercel

## Current Status
- ✅ Website code pushed to `website/` folder in main repo
- ✅ vercel.json added for deployment config
- ⏳ Needs Vercel project creation

## Option 1: Manual Deploy (Easiest)

1. Go to https://vercel.com/new
2. Import `https://github.com/entroplain/entroplain`
3. Set **Root Directory** to `website`
4. Click Deploy

## Option 2: CLI Deploy

```bash
cd C:\Users\josha\.openclaw\workspace\projects\entroplain\website
npx vercel
```

Follow prompts to link project.

## After Deploy

The site will be live at `https://entroplain.vercel.app` (or custom domain).

Update README links to point to the live site.

## Files
- `website/` - Next.js static site
- `vercel.json` - Deployment config (root level)
- `website/package.json` - Dependencies

## Design
Based on Vercel's own design system (from design-md collection):
- White canvas with `#171717` text
- Green accent (`#4ade80`)
- Tight letter-spacing on headings
- Shadow-as-border technique
- Minimal, engineering-focused aesthetic
