import pyodbc
import os
def insert_logs(id, instruction, response, model, category, created_date):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.0.65.166;DATABASE=NxDev;UID=sa;PWD=NTQ@2023')

    cursor = conn.cursor()

    query = """
    INSERT INTO InstructionDB (ID, Instruction, Response, Model, Category, CreatedDate)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(query, id, instruction, response, model, category,created_date)

    conn.commit()

    cursor.close()
    conn.close()
def checkid(id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.0.65.166;DATABASE=NxDev;UID=sa;PWD=NTQ@2023')
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM InstructionDB WHERE ID = '{id}'")
    # Fetch the result
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    # If the count is 1, the ID exists in the table
    if result[0] == 1:
        return True
    else:
        return False

import hashlib

def string_to_id(input_string):
    hash_object = hashlib.md5(input_string.encode())
    return str(hash_object.hexdigest())

if __name__ == "__main__":
    from datetime import datetime
    import os, json
    # res_list = os.listdir("data/Evol-Instruction-66k")
    # for filename in res_list:
    #     with open(f"data/Evol-Instruction-66k/{filename}","r",encoding="utf-8") as fr:
    #         tmp = json.load(fr)
    #         now = datetime.now()
    #         insert_logs(filename.split(".")[0],tmp["input"],tmp["output"],'Gemini Ultra','Coding',now)
    with open(f"data/sft_code_data.json","r",encoding="utf-8") as fr:
        data= json.load(fr)
    for e in data:
        if len(e["answer_correction"])==0:
            continue
        if e["answer_correction"][0]["status"]!="submitted":
            continue
        if (not e["answer_correction"][0]["value"].startswith("Absolutely!")) and (not e["answer_correction"][0]["value"].startswith("Here's")):
            continue
        now = datetime.now()
        id_ = string_to_id(e["question"])
        if checkid(id_):
            continue
        else:
            insert_logs(id_,e["question"],e["answer_correction"][0]["value"],'Gemini Ultra','Evol-Instruction',now)