# Answer Me

A small Windows desktop app to compose, save, and send emails through Microsoft Outlook from reusable templates. Each time you use it, you will send one more email than the last time.

Answer Me provides a simple Tkinter interface where you build email templates (sender, recipients, subject, body), store them in a local JSON file, and send them through your installed Outlook client. Each template keeps track of how many emails have been sent so you can resume a campaign over several days.

## Features

- **Template editor** — create, load, and save named email templates.
- **Outlook integration** — sends emails through the Outlook desktop client via COM automation.
- **Bulk sending** — send a configurable number of emails in one run, with a random delay between each send.
- **Progress tracking** — each template records the number of emails sent and the current day counter.
- **Local storage** — all templates are persisted in a human-readable `template.json` file.
- **Standalone build** — can be packaged into a single Windows executable with PyInstaller.

## Requirements

- **Windows** (the app relies on Outlook COM automation and `pywin32`).
- **Python 3.12+**
- **Microsoft Outlook** desktop client, installed and configured with an active account.
- Python dependency: [`pywin32`](https://pypi.org/project/pywin32/)

> Note: the graphical interface labels are currently in French.

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone <repository-url>
cd BNP_Email

python -m venv venv
venv\Scripts\activate

pip install pywin32
```

`tkinter` ships with the standard Python installer on Windows, so no extra install is needed.

## Usage

Run the graphical interface:

```bash
python gui.py
```

In the window:

1. Click **Nouveau** to start a new template, or pick an existing one and click **Charger**.
2. Fill in the fields: template name, your email, recipients (separated by `;`), subject, and message body.
3. Set **Nombre d'envoi** — the number of emails to send in one run.
4. Click **Enregistrer le template** to save without sending, or **Envoyer** to send and update the progress counters.

Templates are read from and written to `template.json` in the application folder.

## Template format

Templates are stored in `template.json` as a dictionary keyed by template name:

```json
{
    "Model1": {
        "your_email": "your_email@outlook.fr",
        "recipients": [
            "recipient_email@outlook.fr"
        ],
        "subject": "Model1 template's subject",
        "message": [
            "Bonjour,",
            "",
            "ceci est le model 1"
        ],
        "number_of_days": 1,
        "number_of_email_sent": 0,
        "email_service": "outlook"
    }
}
```

| Field | Description |
| --- | --- |
| `your_email` | Sender address (informational). |
| `recipients` | List of recipient email addresses. |
| `subject` | Email subject line. |
| `message` | Email body, stored as a list of lines. |
| `number_of_days` | Number of emails to send on the next run. |
| `number_of_email_sent` | Running total of emails sent for this template. |
| `email_service` | Mail backend to use. Currently only `outlook`. |

## Project structure

```
BNP_Email/
├── main.py          # send_email() — sends emails through Outlook
├── gui.py           # Tkinter interface and template management
├── template.json    # Saved templates
├── Aswer_Me.spec    # PyInstaller build specification
└── README.md
```

## Building a standalone executable

The project ships with a PyInstaller spec file. To build a single windowed executable:

```bash
pip install pyinstaller
pyinstaller Aswer_Me.spec
```

The resulting `Answer_Me.exe` is created in the `dist/` folder. Place a `template.json` next to the executable to provide starting templates.

## Notes & limitations

- Only the **Outlook** backend is implemented.
- Outlook must be installed and signed in; the app drives whatever account Outlook is configured with.
- Use responsibly and only to send emails to recipients who expect them.
