# Deployment Pipeline

This project is deployed automatically via GitHub Actions to GitHub Pages. It completely bypasses the legacy strategy of manually pushing built sites to a `gh-pages` branch.

## The Workflow (`.github/workflows/deploy.yml`)
1. **Trigger**: Any push or merge into the `main` branch.
2. **Setup**: Installs Node 22 (`npm install`).
3. **Build**: Runs `npm run build` locally. The output goes to the `dist/` directory.
4. **Deploy**: Uploads the `dist/` folder via the `actions/upload-pages-artifact` and `actions/deploy-pages@v4` actions.

## Custom Domain Management (`public/CNAME`)
The site hosts on `https://www.codebrains.co.in`.
GitHub Pages relies on a `CNAME` file to bind the custom domain to the repository.
**Critical Rule**: The `CNAME` file MUST live inside the `public/` directory (e.g. `public/CNAME`). 

If the `CNAME` file is placed at the root of the repository, Astro's `npm run build` process will ignore it. The resulting deployment will lack the custom domain setting, causing GitHub to detach the domain. This leads to `522 Connection Timed Out` errors via Cloudflare proxies.

## Local Testing
To preview the site locally before pushing:
```bash
npm run dev
```

To run a production-equivalent clean build to debug build errors (particularly for testing MDX issues):
```bash
npm run clean-build
```
