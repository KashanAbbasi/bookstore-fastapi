from fastapi import FastAPI, File, Form
from fastapi.responses import HTMLResponse
import sqlite3
import os
# import shutil

app = FastAPI()
DB_FILE = "books.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            tittle TEXT,
            refrence TEXT,
            price REAL,
            publisher TEXT,
            pub_year TEXT,
            link TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.get("/", response_class=HTMLResponse)
def home():
    name = "ABBASI BOOKS STORE"

    # HTML read
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Database read
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    html = html.replace("{{name}}", name)

    ft = ""
    for r in rows:
        ft += f"""
        <article class="card">
            <a href="{r["link"]}">
                <div class="card__img">
                    <img src="{r["refrence"]}" alt="">
                </div>
                <div class="card__name">
                    <p>{r["tittle"]}</p>
                </div>
            </a>

            <div class="card__precis">
                <span class="card__preci card__preci--before">Writer : {r["author"]}</span>
                <span class="card__preci card__preci--now">${r["price"]}.00</span>
                <a href="#" class="card__icon">
                    <ion-icon name="cart-outline"></ion-icon>   
                </a>
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

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (author, tittle, refrence, price, publisher, pub_year, link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (author, tittle, refrence, price, publisher, pub_year, link))
    conn.commit()
    conn.close()

    return {"status": "success", "msg": "Book & PDF saved successfully ✅"}


@app.get("/data", response_class=HTMLResponse)
def view_data():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

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
