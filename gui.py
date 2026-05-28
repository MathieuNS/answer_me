import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from main import send_email

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_FILE = os.path.join(BASE_DIR, "template.json")


def load_all_templates() -> dict:
    if not os.path.exists(TEMPLATE_FILE):
        return {}
    with open(TEMPLATE_FILE, "r", encoding="UTF8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_all_templates(templates: dict) -> None:
    with open(TEMPLATE_FILE, "w", encoding="UTF8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=4)


class TemplateEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Answer Me !!!!!!!")
        self.geometry("720x680")
        self.templates = load_all_templates()
        self._build_widgets()
        self._refresh_template_list()

    def _build_widgets(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        ttk.Label(top, text="Template existant :").pack(side="left")
        self.template_combo = ttk.Combobox(top, state="readonly")
        self.template_combo.pack(side="left", padx=5)
        ttk.Button(top, text="Charger", command=self.on_load).pack(side="left", padx=5)
        ttk.Button(top, text="Nouveau", command=self.on_new).pack(side="left", padx=5)

        form = ttk.Frame(self, padding=10)
        form.pack(fill="both", expand=True)

        ttk.Label(form, text="Nom du template :").grid(row=0, column=0, sticky="w", pady=3)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var).grid(row=0, column=1, sticky="we", pady=3)

        ttk.Label(form, text="Votre email :").grid(row=1, column=0, sticky="w", pady=3)
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var).grid(row=1, column=1, sticky="we", pady=3)

        ttk.Label(form, text="Destinataires (séparés par ;) :").grid(row=2, column=0, sticky="w", pady=3)
        self.recipients_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.recipients_var).grid(row=2, column=1, sticky="we", pady=3)

        ttk.Label(form, text="Objet :").grid(row=3, column=0, sticky="w", pady=3)
        self.subject_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.subject_var).grid(row=3, column=1, sticky="we", pady=3)

        ttk.Label(form, text="Service :").grid(row=4, column=0, sticky="w", pady=3)
        self.service_combo = ttk.Combobox(form, values=["outlook"], state="readonly")
        self.service_combo.grid(row=4, column=1, sticky="we", pady=3)
        self.service_combo.set("outlook")

        ttk.Label(form, text="Nombre d'envoi :").grid(row=5, column=0, sticky="w", pady=3)
        self.days_var = tk.StringVar(value="1")
        ttk.Entry(form, textvariable=self.days_var, width=10).grid(row=5, column=1, sticky="w", pady=3)

        ttk.Label(form, text="Emails envoyés :").grid(row=6, column=0, sticky="w", pady=3)
        self.sent_var = tk.StringVar(value="0")
        ttk.Entry(form, textvariable=self.sent_var, width=10).grid(row=6, column=1, sticky="w", pady=3)

        ttk.Label(form, text="Message :").grid(row=7, column=0, sticky="nw", pady=3)
        self.message_text = tk.Text(form, height=15, wrap="word")
        self.message_text.grid(row=7, column=1, sticky="nsew", pady=3)

        form.columnconfigure(1, weight=1)
        form.rowconfigure(7, weight=1)

        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Enregistrer le template", command=self.on_save).pack(side="right")
        ttk.Button(bottom, text="Envoyer", command=self.on_send).pack(side="right", padx=5)

    def _refresh_template_list(self):
        names = list(self.templates.keys())
        self.template_combo["values"] = names
        if names:
            self.template_combo.set(names[0])

    def on_load(self):
        name = self.template_combo.get()
        if not name or name not in self.templates:
            messagebox.showwarning("Aucun template", "Sélectionne un template à charger.")
            return
        model = self.templates[name]
        self.name_var.set(name)
        self.email_var.set(model.get("your_email", ""))
        self.recipients_var.set(";".join(model.get("recipients", [])))
        self.subject_var.set(model.get("subject", ""))
        self.service_combo.set(model.get("email_service", "outlook"))
        self.days_var.set(str(model.get("number_of_days", 1)))
        self.sent_var.set(str(model.get("number_of_email_sent", 0)))
        self.message_text.delete("1.0", "end")
        self.message_text.insert("1.0", "\n".join(model.get("message", [])))

    def on_new(self):
        self.name_var.set("")
        self.email_var.set("")
        self.recipients_var.set("")
        self.subject_var.set("")
        self.service_combo.set("outlook")
        self.days_var.set("1")
        self.sent_var.set("0")
        self.message_text.delete("1.0", "end")

    def on_send(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Nom manquant", "Donne un nom au template pour enregistrer la progression.")
            return

        recipients = [r.strip() for r in self.recipients_var.get().split(";") if r.strip()]
        subject = self.subject_var.get().strip()
        message = self.message_text.get("1.0", "end-1c").split("\n")

        if not recipients:
            messagebox.showwarning("Destinataires manquants", "Ajoute au moins un destinataire.")
            return

        try:
            days = int(self.days_var.get())
            sent = int(self.sent_var.get())
        except ValueError:
            messagebox.showerror("Valeur invalide", "Nombre de jours et emails envoyés doivent être des entiers.")
            return

        if not messagebox.askyesno(
            "Confirmer l'envoi",
            f"Envoyer {days} email(s) à :\n{', '.join(recipients)} ?",
        ):
            return

        try:
            send_email(recipients, subject, message, days, self.service_combo.get())
        except Exception as e:
            messagebox.showerror("Erreur d'envoi", str(e))
            return

        new_days = days + 1
        new_sent = sent + days
        self.days_var.set(str(new_days))
        self.sent_var.set(str(new_sent))

        self.templates[name] = {
            "your_email": self.email_var.get().strip(),
            "recipients": recipients,
            "subject": subject,
            "message": message,
            "number_of_days": new_days,
            "number_of_email_sent": new_sent,
            "email_service": self.service_combo.get(),
        }
        save_all_templates(self.templates)
        self._refresh_template_list()
        self.template_combo.set(name)

        messagebox.showinfo("Envoyé", f"{days} email(s) envoyé(s).")

    def on_save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Nom manquant", "Donne un nom au template.")
            return

        recipients = [r.strip() for r in self.recipients_var.get().split(";") if r.strip()]
        message = self.message_text.get("1.0", "end-1c").split("\n")

        try:
            days = int(self.days_var.get())
            sent = int(self.sent_var.get())
        except ValueError:
            messagebox.showerror("Valeur invalide", "Nombre de jours et emails envoyés doivent être des entiers.")
            return

        self.templates[name] = {
            "your_email": self.email_var.get().strip(),
            "recipients": recipients,
            "subject": self.subject_var.get().strip(),
            "message": message,
            "number_of_days": days,
            "number_of_email_sent": sent,
            "email_service": self.service_combo.get(),
        }
        save_all_templates(self.templates)
        self._refresh_template_list()
        self.template_combo.set(name)
        messagebox.showinfo("Enregistré", f"Template '{name}' enregistré.")


if __name__ == "__main__":
    TemplateEditor().mainloop()
