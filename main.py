from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import psycopg2
import os

app = FastAPI()

# Vercel me ye environment variable se aayega
DATABASE_URL = os.getenv("postgresql://postgres:t3Cq8l1TK5kjjgau@db.grwsqddifkdhupfkxbrb.supabase.co:5432/postgres")  # set this in Vercel

def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.get("/", response_class=HTMLResponse)
def home():
    name = "ABBASI BOOK STORE"

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author, tittle, refrence, price, publisher, pub_year, link FROM books")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    html = html.replace("{{name}}", name)

    ft = ""
    for r in rows:
        ft += f"""
        <article class="card">
            <a href="{r[6]}">
                <div class="card__img-container">
                    <img src="{r[2]}" alt="{r[1]}" class="card__img">
                </div>
            </a>

            <div class="card__content">
                <h3 class="card__title">{r[1]}</h3>
                <p class="card__author">by {r[0]}</p>
                
                <div class="card__footer">
                    <span class="card__price">${r[3]}</span>
                    <button class="card__btn-cart">
                        Add to cart
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
def submit(
    author: str = Form(...),
    tittle: str = Form(...),
    refrence: str = Form(...),
    price: float = Form(...),
    publisher: str = Form(...),
    pub_year: str = Form(...),
    link: str = Form(...),
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO books (author, tittle, refrence, price, publisher, pub_year, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (author, tittle, refrence, price, publisher, pub_year, link))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success", "msg": "Book saved successfully ✅"}


@app.get("/data", response_class=HTMLResponse)
def view_data():

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author, tittle, refrence, price, publisher, pub_year, link FROM books")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tr = ""
    for r in rows:
        tr += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>{r[3]}</td>
            <td>{r[4]}</td>
            <td>{r[5]}</td>
            <td><a href="{r[6]}">PDF</a></td>
        </tr>
        """

    return f"""
<html>
<body>
<h2 style="text-align:center;">All Books</h2>
<table border="1" cellpadding="8" style="margin:auto;">
<tr>
<th>Author</th><th>Title</th><th>Reference</th><th>Price</th>
<th>Publisher</th><th>Year</th><th>PDF</th>
</tr>
{tr}
</table>
</body>
</html>
"""
