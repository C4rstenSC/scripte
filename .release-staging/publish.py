import hashlib, json, pathlib, shutil, subprocess, tempfile
root = pathlib.Path.cwd()
stage = root / ".release-staging"
metadata = json.loads((stage / "publish.json").read_text())
package = stage / "Raspi-Scripte.zip.enc"
with package.open("wb") as out:
    for part in sorted((stage / "parts").glob("[0-9][0-9][0-9][0-9]")):
        out.write(part.read_bytes())
for filename, expected in metadata["hashes"].items():
    actual = hashlib.sha256((stage / filename).read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError("Package hash mismatch: " + filename)
staged_copy = pathlib.Path(tempfile.mkdtemp(prefix="raspi-release-")) / "staging"
shutil.copytree(stage, staged_copy)
stage = staged_copy
def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()
git("fetch", "origin", "main")
if git("rev-parse", "origin/main") != metadata["expected_head"]:
    raise RuntimeError("main changed; release must be reviewed against the new head")
git("checkout", "-b", "publish-complete", "origin/main")
for source, target in metadata["files"].items():
    dest = root / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(stage / source, dest)
git("config", "user.name", "github-actions[bot]")
git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
git("add", "--", *metadata["files"].values())
git("commit", "-m", "Raspi-Scripte 0.6.45 und Witty Add-on 0.6.55 veröffentlichen")
git("push", "origin", "HEAD:main")
print("Published complete release", git("rev-parse", "HEAD"))

