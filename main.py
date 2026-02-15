from fastapi import FastAPI, File, Form
from fastapi.responses import HTMLResponse
import csv
import os
# import shutil

app = FastAPI()
CSV_FILE = "books.csv"


if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["author", "tittle", "refrence", "price", "publisher", "pub_year", "link"]
        )


@app.get("/", response_class=HTMLResponse)
def home():
    name = "ABBASI BOOK STORE"

    # HTML read
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # CSV read (NO f.read())
    with open("books.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    html = html.replace("{{name}}", name)

    ft = ""
    for r in rows:
        ft += f"""
        <article class="card">
            <a href="{r["link"]}">
                <div class="card__img-container">
                    <img src="{r["refrence"]}" alt="{r["tittle"]}" class="card__img">
                </div>
            </a>

            <div class="card__content">
                <h3 class="card__title">{r["tittle"]}</h3>
                <p class="card__author">by {r["author"]}</p>
                
                <div class="card__footer">
                    <span class="card__price">${r["price"]}</span>
                    <button class="card__btn-cart" title="Add to cart">
                        <ion-icon name="cart-outline"></ion-icon>   
                    </button>
                </div>
            </div>
        </article>
        """

    html = html.replace("{{prod}}", ft)
    return html


@app.get("/upload", response_class=HTMLResponse)
def upload():
    name = "ABBASI BOOKS STORE"

    with open("index2.html", "r", encoding="utf-8") as File2:
        html = File2.read()

    html = html.replace("{{name}}", name)

    return html


@app.post("/submit")
async def submit(
    author: str = Form(...),
    tittle: str = Form(...),
    refrence: str = Form(...),
    price: float = Form(...),
    publisher: str = Form(...),
    pub_year: str = Form(...),
    link: str = File(...),
):
    # if not pdf.filename.endswith(".pdf"):
    #     return {"error": "Only PDF allowed"}

    # pdf_path = os.path.join(UPLOAD_DIR, pdf.filename)
    # with open(pdf_path, "wb") as buffer:
    #     shutil.copyfileobj(pdf.file, buffer)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([author, tittle, refrence, price, publisher, pub_year, link])

    return {"status": "success", "msg": "Book & PDF saved successfully ✅"}


@app.get("/data", response_class=HTMLResponse)
def view_data():
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    tr = ""
    for r in rows:
        tr += f"""
        <tr>
            <td>{r["author"]}</td>
            <td>{r["tittle"]}</td>
            <td>{r["refrence"]}</td>
            <td>{r["price"]}</td>
            <td>{r["publisher"]}</td>
            <td>{r["pub_year"]}</td>
            <td><a href="{r["link"]}">PDF</a></td>
        </tr>
        """

    return f"""
<html>
<body>
<h2 style="text-align:center;">All Books</h2>
<table border="1" cellpadding="8" style="margin:auto;">
<tr>
<th>Author</th><th>tittle</th><th>refrence</th><th>Price</th>
<th>Publisher</th><th>Year</th><th>PDF</th>
</tr>
{tr}
</table>
</body>
</html>
"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
