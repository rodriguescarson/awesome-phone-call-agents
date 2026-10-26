# Hosted demo: retired on 26 Oct 2026

The CALL-E "Your Code Is Calling" hackathon closed on 14 Sep 2026 and announced its winners in
mid-October; this entry did not place. The hosted demo on Google Cloud Run only served crawlers
after that, and Carson wants nothing billing for it, so it was deleted. What the judges saw is
preserved as a static snapshot:

**https://call-review-console.rodriguescarson.workers.dev**

The snapshot is the same `static/index.html`, with the authenticated `fetch` wrapper pointed at
JSON files captured from the console running against its five fixture calls (`snapshot/api/`),
the token gate bypassed, and the "note for the record" buttons turned into a notice. Each call
is captured twice, with and without `?llm=true`; with no model key configured both are the
deterministic review, which is also what the hosted demo served.

## What ran on Cloud Run (for the record)

| Setting | Value |
|---|---|
| Service | `call-review-console`, project `mealstogo-76a00`, region `us-central1` |
| URL | `https://call-review-console-q62ufgdryq-uc.a.run.app` (dead) |
| Source | this directory, deployed from source with Cloud Build (`cloud-run-source-deploy` repository) |
| Resources | 1 vCPU, 512 MiB, max 20 instances, scale to zero, startup CPU boost |
| Service account | the project's default compute service account |
| Env | `CRC_DEMO=true` (the gate hands visitors the demo token via `/api/ping`), `CRC_CONSOLE_TOKEN` (set), `CRC_DATA_DIR`, `GOOGLE_GENAI_USE_VERTEXAI=true`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` |
| Not set | `CALLE_API_KEY` (live fetch off), `CRC_USE_LLM` (deterministic review only), `CRC_WEBHOOK_TOKEN` |
| Revisions | 9 (`call-review-console-00001` to `-00009`), first deployed 5 Sep 2026 |

Deleted on 26 Oct 2026: the service, its 9 container images in Artifact Registry and its 9
build-source archives. Nothing of this app remains on Google Cloud.

## Rebuilding the snapshot

```bash
# run the console locally with a known token, then capture
CRC_DEMO=true CRC_CONSOLE_TOKEN=snap uvicorn crc.app:app --port 8765
python scripts/build_snapshot.py http://127.0.0.1:8765 snap
cd snapshot && npx wrangler deploy      # Cloudflare Workers static assets
```
