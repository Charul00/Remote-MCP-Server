from fastmcp import FastMCP
import os 
import sqlite3 
DB_PATH=os.path.join(os.path.dirname(__file__),"expenses.db")
categories_path=os.path.join(os.path.dirname(__file__),"categories.json")
mcp=FastMCP("Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                note TEXT default ''
                  )
                  
                  
            """)
               
init_db()

@mcp.tool 
def add_expenses(date,amount,category,subcategory="",note=""):
    with sqlite3.connect(DB_PATH) as c:
        cur=c.execute(
            "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES(?,?,?,?,?)",
            (date,amount,category,subcategory,note)
        )
        return {"status":"ok","id":cur.lastrowid}
    
@mcp.tool
def list_expenses(start_date,end_date):
    #list expenses 
    with sqlite3.connect(DB_PATH) as c:
        cur=c.execute(
            
            """
            Select id,date,amount,category,subcategory,note 
            from expenses 
            where date between ? and ? 
            order by id asc
            """,
            (start_date,end_date)
            )
        cols=[d[0] for d in cur.description]
        return[dict(zip(cols,row)) for row in cur.fetchall()]

@mcp.tool 
def summarize(start_date,end_date,category=None):
    #summarize the expenses
    with sqlite3.connect(DB_PATH)as c:
        cur=c.execute(
            """ 
        select category,sum(amount) as total from expenses 
        where date between ? and ? 
       
        """)
        params=[start_date,end_date]

        if category:
            cur=c.execute(
                """ 
            select category,sum(amount) as total from expenses 
            where date between ? and ? and category=?
            """,
            params=[start_date,end_date,category]

      
        
        
        )
        cols=[d[0] for d in cur.description]
        return[dict(zip(cols,row)) for row in cur.fetchall()]
            
       

@mcp.resource("expense://categories",mime_type="applicatin/json")
def categories():
    with open(categories_path,"r",encoding="utf-8") as f:
        return f.read()

         


    
if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
