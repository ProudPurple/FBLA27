# PyInstaller spec: builds a single-file .exe with the React build bundled in.
# Run `npm run build` in frontend/ first (outputs to backend/frontend_dist),
# then from backend/: `pyinstaller build.spec`
#
# Note: this does NOT bundle Playwright's browser binaries. Run
# `playwright install chromium` on the target machine, or see
# https://playwright.dev/python/docs/browsers#install-system-dependencies
# for distributing them alongside the .exe.

a = Analysis(
    ["run.py"],
    pathex=[],
    binaries=[],
    datas=[("frontend_dist", "frontend_dist")],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="SignUpGeniusTracker",
    console=False,
    onefile=True,
)
