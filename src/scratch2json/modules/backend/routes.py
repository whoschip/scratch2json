from flask import Blueprint
from pathlib import Path
from scratch2json.modules.convert_project.convert_project import ConvertProject

backend_bp = Blueprint("backend", __name__)


@backend_bp.route("/upload", methods=["POST"])
def upload_zip():
    ck = ConvertProject()

    if 'file' not in request.files:
        return {"error": "no file found "}, 400

    zip_file = request.files['file']

    if not zip_file.filename.endswith(".sb3") and not zip_file.filename.endswith(".pmp"):
        return {"error": "nah that ain’t a scratch file 💀"}, 400

    dst = os.environ.get("SCRATCH2JSON_BACKEND_DST")
    if not dst:
        return {"error": "bro no dst was passed from CLI"}, 500

    with zipfile.ZipFile(io.BytesIO(zip_file.read())) as zip_ref:
        builddir = dst / "builddir"
        builddir.mkdir(parents=True, exist_ok=True)
        zip_ref.extractall(builddir)
        ck.convert(dst, builddir)

    return {"msg": f"✅ extracted to {builddir} twin 🔥"}
