# Quick Mode Switch Guide

## Current Status
Use the start script to check current mode:
```bash
./start_all.sh
```

Output will show: `🎭 Mode: DEMO MODE` or `🚀 Mode: REAL MODE`

## Switch to Demo Mode

```bash
# 1. Edit .env file - change API_MODE to demo
sed -i '' 's/API_MODE=real/API_MODE=demo/' .env

# 2. Start all services
./start_all.sh

# 3. Check mode changed
curl -s http://localhost:8000/api/health | grep mode
```

Expected output: `"mode": "demo"`

## Switch to Real Mode

```bash
# 1. Edit .env file - change API_MODE to real
sed -i '' 's/API_MODE=demo/API_MODE=real/' .env

# 2. Start all services
./start_all.sh

# 3. Check mode changed
curl -s http://localhost:8000/api/health | grep mode
```

Expected output: `"mode": "real"`

## Manual Edit (Alternative)

If you prefer editing manually:

1. Open `.env` file in editor
2. Change line: `API_MODE=demo` or `API_MODE=real`
3. Save file
4. Run: `./start_all.sh`
5. Browser will open automatically at http://localhost:3000

## Verify Mode in UI

After restarting, check the web UI at http://localhost:3000:
- Demo mode shows: **🎭 DEMO MODE** (blue badge)
- Real mode shows: **🚀 LIVE MODE** (green badge)

## Troubleshooting

### Servers Won't Start
```bash
# Force kill and restart everything
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9
sleep 2
./start_all.sh
```

### Mode Not Changing
```bash
# Verify .env file
grep API_MODE .env

# Check server is reading it
curl -s http://localhost:8000/api/health | python3 -m json.tool

# If mode is wrong, restart everything
./start_all.sh
```

### UI Shows Wrong Mode
1. Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Check backend health: `curl http://localhost:8000/api/health`
3. If backend shows correct mode but UI doesn't, restart frontend:
   ```bash
   cd ui
   npm start
   ```

## Quick Reference

| Task | Command |
|------|---------|
| Start everything | `./start_all.sh` |
| Check current mode | `./start_all.sh` (shows mode on start) |
| Switch to demo | `sed -i '' 's/API_MODE=real/API_MODE=demo/' .env && ./start_all.sh` |
| Switch to real | `sed -i '' 's/API_MODE=demo/API_MODE=real/' .env && ./start_all.sh` |
| Verify mode (API) | `curl -s http://localhost:8000/api/health \| grep mode` |
| Verify mode (UI) | Open http://localhost:3000 and look for badge |
| View logs | `tail -f logs/backend.log` |
| Kill server | `lsof -ti :8000 \| xargs kill -9` |

## Script Details

The `start_all.sh` script:
1. ✅ Kills all processes on ports 8000 and 3000
2. ✅ Waits for ports to be released
3. ✅ Verifies ports are free before starting
4. ✅ Starts backend API server (port 8000)
5. ✅ Activates virtual environment automatically
6. ✅ Starts frontend UI server (port 3000)
7. ✅ Waits for both services to be ready
8. ✅ Checks health endpoint and webpack compilation
9. ✅ Shows current mode (demo/real)
10. ✅ Provides helpful URLs, PIDs, and commands

This ensures reliable startup of both backend and frontend every time!
