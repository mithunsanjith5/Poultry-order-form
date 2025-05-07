from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import math
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
lw = 0.25
ww = 0.25
fw = 1.0
wc = {"l": 2, "w": 2, "f": 1}
class Order(BaseModel):
    l: int
    w: int
    f: int
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/process_order")
async def process_order(order: Order):
    cl = math.ceil(order.l / wc["l"])
    cw = math.ceil(order.w / wc["w"])
    cf = math.ceil(order.f / wc["f"])
    tc = max(cl, cw, cf)
    orderweight = order.l * lw + order.w * ww + order.f * fw
    totalparts = {"l": tc * wc["l"],"w": tc * wc["w"],"f": tc * wc["f"]}
    rp = {"l": totalparts["l"] - order.l,"w": totalparts["w"] - order.w,"f": totalparts["f"] - order.f}
    remaining_weight = rp["l"] * lw + rp["w"] * ww + rp["f"] * fw
    return {
        "order_weight": round(orderweight, 2),
        "chickens_needed": tc,
        "remaining": rp,
        "remaining_weight": round(remaining_weight, 2)
    }
