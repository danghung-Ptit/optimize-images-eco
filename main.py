from fastapi import FastAPI, UploadFile, File, Form
from optimize_images.data_structures import OutputConfiguration
from optimize_images.api import optimize_as_batch
import json
from PIL import Image
import io
import base64
import requests


import shutil
import tempfile
import uuid

import fastapi
import io

from PIL import Image
from starlette.responses import StreamingResponse, FileResponse
import magic
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
import base64


app = FastAPI()

@app.post("/optimize")
async def optimize_images(
    src_path: str = "tmp/saved_poster (1).png",
    watch_dir: bool = False,
    recursive: bool = True,
    quality: int = 35,
    remove_transparency: bool = False,
    reduce_colors: bool = False,
    max_colors: int = 256,
    max_w: int = 0,
    max_h: int = 0,
    keep_exif: bool = False,
    convert_all: bool = True,
    conv_big: bool = False,
    force_del: bool = False,
    grayscale: bool = False,
    ignore_size_comparison: bool = False,
    fast_mode: bool = True,
    jobs: int = 0,
):
    output_config = OutputConfiguration(show_only_summary=False, show_overall_progress=False, quiet_mode=False)
    bg_color = (255, 255, 255)
    print(src_path, quality)

    message_img_status, message_report = optimize_as_batch(
        src_path,
        watch_dir,
        recursive,
        quality,
        remove_transparency,
        reduce_colors,
        max_colors,
        max_w,
        max_h,
        keep_exif,
        convert_all,
        conv_big,
        force_del,
        bg_color,
        grayscale,
        ignore_size_comparison,
        fast_mode,
        jobs,
        output_config
    )

    result = {
        "message": message_report.strip()
    }

    # Chuyển đối tượng kết quả thành chuỗi JSON với định dạng đẹp
    json_result = json.dumps(result, indent=4)
    print(json_result)

    # Trả về chuỗi JSON trong phản hồi của API
    return json_result


@app.post("/optimize_images")
def query_api(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(file.file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")



# Đăng ký thư mục tĩnh để chứa các file tạm thời
app.mount("/tmp", StaticFiles(directory="tmp"), name="tmp")


@app.post('/api/optimize-image')
async def optimize_image(file: UploadFile = File(...)):
    """ Optimize a single image according to the parameters provided
    """
    tmp_filename = uuid.uuid4().hex + file.filename
    with open(f"tmp/{tmp_filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # img = Image.open(file.file)

    print(tmp_filename)

    mtype = magic.from_file(f"tmp/{tmp_filename}", mime=True)

    return FileResponse(f"tmp/{tmp_filename}", media_type=mtype)


templates = Jinja2Templates(directory="templates")

@app.get("/")
def dynamic_file(request: Request):
    return templates.TemplateResponse("dynamic.html", {"request": request})

@app.post("/upload")
def dynamic(request: Request, file: UploadFile = File()):
    data = file.file.read()
    # Image will be saved in the uploads folder prefixed with uploaded_
    with open("tmp/saved_" + file.filename, "wb") as f:
        f.write(data)
    file.file.close()




