import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from openai import OpenAI

# Replace with your API key (DO NOT commit real keys)
api_key = "your_API_key"
client = OpenAI(api_key=api_key)

def summarize_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not filepath:
        return

    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            summaries = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": f"Summarize this:\n{text}"}
                        ]
                    )
                    summary = response.choices[0].message.content
                    summaries.append(f"\n--- Page {i+1} ---\n{summary}")

            output.delete("1.0", tk.END)
            output.insert(tk.END, "\n".join(summaries))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("PDF Summarizer with OpenAI")
root.geometry("700x500")

btn = tk.Button(root, text="Select PDF and Summarize", command=summarize_pdf)
btn.pack(pady=10)

output = tk.Text(root, wrap="word", font=("Arial", 10))
output.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
