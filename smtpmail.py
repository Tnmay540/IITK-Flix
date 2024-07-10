import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
from tkinter import filedialog
from email.mime.base import MIMEBase
from email import encoders

class Mail_client:
    def __init__(self, root):
        self.root = root
        self.root.title("IITK Flix mail client")

        self.smtp_server = "mmtp.iitk.ac.in"
        self.smtp_port = 25

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=0, column=0)

        self.logout_button = tk.Button(root, text="Logout", command=self.logout, state=tk.DISABLED)
        self.logout_button.grid(row=0, column=1)

        self.send = tk.Button(root, text="Send Mail", command=self.send_mail)
        self.send.grid(row=0, column=2)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username = tk.Entry(root, width=45)
        self.username.grid(row=1, column=1, columnspan=2)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password = tk.Entry(root, show="*", width=45)
        self.password.grid(row=2, column=1, columnspan=2)

        self.sender_label = tk.Label(root, text="Sender Email:")
        self.sender_label.grid(row=3, column=0)
        self.sender = tk.Entry(root, width=45)
        self.sender.grid(row=3, column=1, columnspan=2)

        self.recipient_label = tk.Label(root, text="Recipient Email:")
        self.recipient_label.grid(row=4, column=0)
        self.recipient = tk.Entry(root, width=45)
        self.recipient.grid(row=4, column=1, columnspan=2)

        self.cc_label = tk.Label(root, text="CC:")
        self.cc_label.grid(row=5, column=0)
        self.cc = tk.Entry(root, width=45)
        self.cc.grid(row=5, column=1, columnspan=2)

        self.bcc_label = tk.Label(root, text="BCC:")
        self.bcc_label.grid(row=6, column=0)
        self.bcc = tk.Entry(root, width=45)
        self.bcc.grid(row=6, column=1, columnspan=2)

        self.subject_label = tk.Label(root, text="Subject:")
        self.subject_label.grid(row=7, column=0)
        self.subject = tk.Entry(root, width=100)
        self.subject.grid(row=7, column=1, columnspan=2)

        self.message_label = tk.Label(root, text="Message:")
        self.message_label.grid(row=8, column=0)
        self.message = tk.Entry(root, width=100)
        self.message.grid(row=8, column=1, columnspan=2)

        self.attachment_label = tk.Label(root, text="Attachment:")
        self.attachment_label.grid(row=9, column=0)
        self.attachment_path = tk.Entry(root, width=100)
        self.attachment_path.grid(row=9, column=1)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=9, column=2)

        self.server = None

    def login(self):
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()#transport layer security
        self.server.login(self.username.get(), self.password.get())
        self.login_button["state"] = tk.DISABLED
        self.logout_button["state"] = tk.NORMAL

    def logout(self):
        if self.server:
            self.server.quit()
            self.server = None
            self.login_button["state"] = tk.NORMAL
            self.logout_button["state"] = tk.DISABLED

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.attachment_path.delete(0, tk.END)
        self.attachment_path.insert(0, file_path)

    def send_mail(self):
        if not self.server:
            messagebox.showerror("Error", "Please log in first.")
            return

        sender_email = self.sender.get()
        recipient_email = self.recipient.get()
        cc_email = self.cc.get()
        bcc_email = self.bcc.get()
        subject = self.subject.get()
        body = self.message.get()
        attachment_path = self.attachment_path.get()

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Cc'] = cc_email
        msg['Bcc'] = bcc_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            attachment = self.attach_file(attachment_path)
            if attachment:
                msg.attach(attachment)

        try:
            recipients = [recipient_email] + cc_email.split(',') + bcc_email.split(',')
            self.server.sendmail(sender_email, recipients, msg.as_string())

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def attach_file(self, file_path):
        try:
            attachment = MIMEBase("application", "octet-stream")
            with open(file_path, "rb") as file:
                attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename={file_path}")
            return attachment
        except Exception as e:
            messagebox.showerror("Error", f"Failed to attach file: {str(e)}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    mail_client = Mail_client(root)
    root.mainloop()