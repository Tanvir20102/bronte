import subprocess
import sys
import os

def auto_install():
    pkgs = {
        'flask': 'flask',
        'flask_cors': 'flask-cors',
        'dotenv': 'python-dotenv'
    }
    for mod, pkg in pkgs.items():
        try:
            __import__(mod)
        except ImportError:
            print(f"  [+] Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

auto_install()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import webbrowser
import threading
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "").strip()
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "").strip()
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "").strip()
PORT = int(os.getenv("PORT", "5000"))


def send_via_gmail(name, sender_email, subject, message, phone="", city=""):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Reply-To"] = sender_email
    msg["Subject"] = f"Contact: {name} — {subject}"

    # ── Phone button ──
    phone_block = ""
    if phone:
        phone_block = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
            <tr>
                <td align="center" bgcolor="#16a34a" style="padding:20px 24px; border-radius:10px;">
                    <a href="tel:{phone}" style="color:#ffffff; text-decoration:none; font-size:26px; font-weight:bold; font-family:Arial,Helvetica,sans-serif;">
                        &#9742; {phone}
                    </a>
                </td>
            </tr>
        </table>"""

    # ── Email button ──
    email_block = ""
    if sender_email:
        email_block = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
            <tr>
                <td align="center" bgcolor="#ea580c" style="padding:20px 24px; border-radius:10px;">
                    <a href="mailto:{sender_email}" style="color:#ffffff; text-decoration:none; font-size:22px; font-weight:bold; font-family:Arial,Helvetica,sans-serif; word-break:break-all;">
                        &#9993; {sender_email}
                    </a>
                </td>
            </tr>
        </table>"""

    # ── Phone row ──
    phone_row = ""
    if phone:
        phone_row = f"""
        <tr>
            <td bgcolor="#f5f5f5" style="padding:16px 20px; font-weight:bold; color:#555; font-size:16px; font-family:Arial,Helvetica,sans-serif; width:110px;" valign="top">Phone</td>
            <td bgcolor="#ffffff" style="padding:16px 20px; font-size:18px; font-family:Arial,Helvetica,sans-serif;" valign="top">
                <a href="tel:{phone}" style="color:#ea580c; text-decoration:none; font-weight:bold;">{phone}</a>
            </td>
        </tr>"""

    # ── City row ──
    city_row = ""
    if city:
        city_row = f"""
        <tr>
            <td bgcolor="#f5f5f5" style="padding:16px 20px; font-weight:bold; color:#555; font-size:16px; font-family:Arial,Helvetica,sans-serif; width:110px;" valign="top">City</td>
            <td bgcolor="#ffffff" style="padding:16px 20px; font-size:18px; font-weight:bold; font-family:Arial,Helvetica,sans-serif;" valign="top">{city}</td>
        </tr>"""

    # ── Pura email ──
    html = f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#e8e8e8" style="padding:20px;">
        <tr>
            <td align="center" style="padding:20px 12px;">

                <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#1e1c5e" style="max-width:600px; border-radius:12px 12px 0 0;">
                    <tr>
                        <td style="padding:28px 24px; font-family:Arial,Helvetica,sans-serif;">
                            <h2 style="margin:0; color:#ffffff; font-size:22px; font-family:Arial,Helvetica,sans-serif;">New Contact Message</h2>
                            <p style="margin:8px 0 0; color:rgba(255,255,255,0.6); font-size:14px; font-family:Arial,Helvetica,sans-serif;">from Bronte Franchise Website</p>
                        </td>
                    </tr>
                </table>

                <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f9fafb" style="max-width:600px;">
                    <tr>
                        <td style="padding:24px 20px 20px; font-family:Arial,Helvetica,sans-serif;">
                            <p style="margin:0 0 16px; font-size:13px; font-weight:bold; color:#888; text-transform:uppercase; letter-spacing:1px; font-family:Arial,Helvetica,sans-serif;">Quick Contact — Tap to Call / Email</p>
                            {phone_block}
                            {email_block}
                        </td>
                    </tr>
                </table>

                <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#cccccc" style="max-width:600px;">
                    <tr>
                        <td style="padding:0; font-size:0; line-height:0;">&nbsp;</td>
                    </tr>
                </table>

                <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="max-width:600px;">
                    <tr>
                        <td bgcolor="#f5f5f5" style="padding:16px 20px; font-weight:bold; color:#555; font-size:16px; font-family:Arial,Helvetica,sans-serif; width:110px;" valign="top">Name</td>
                        <td bgcolor="#ffffff" style="padding:16px 20px; font-size:19px; font-weight:bold; color:#111; font-family:Arial,Helvetica,sans-serif;" valign="top">{name}</td>
                    </tr>
                    <tr>
                        <td bgcolor="#f5f5f5" style="padding:16px 20px; font-weight:bold; color:#555; font-size:16px; font-family:Arial,Helvetica,sans-serif; width:110px;" valign="top">Email</td>
                        <td bgcolor="#ffffff" style="padding:16px 20px; font-size:17px; font-family:Arial,Helvetica,sans-serif;" valign="top">
                            <a href="mailto:{sender_email}" style="color:#ea580c; text-decoration:none; font-weight:bold; font-size:17px;">{sender_email}</a>
                        </td>
                    </tr>
                    {phone_row}
                    {city_row}
                    <tr>
                        <td bgcolor="#f5f5f5" style="padding:16px 20px; font-weight:bold; color:#555; font-size:16px; font-family:Arial,Helvetica,sans-serif; width:110px;" valign="top">Message</td>
                        <td bgcolor="#ffffff" style="padding:16px 20px; font-size:16px; color:#333; line-height:1.7; white-space:pre-wrap; font-family:Arial,Helvetica,sans-serif;" valign="top">{message}</td>
                    </tr>
                </table>

                <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f5f5f5" style="max-width:600px; border-radius:0 0 12px 12px;">
                    <tr>
                        <td align="center" style="padding:16px 24px; font-size:12px; color:#aaa; font-family:Arial,Helvetica,sans-serif;">
                            Sent via Gmail SMTP — {time.strftime('%Y-%m-%d %H:%M:%S')}
                        </td>
                    </tr>
                </table>

            </td>
        </tr>
    </table>
    """

    text = f"Name: {name}\nEmail: {sender_email}\nPhone: {phone}\nCity: {city}\n\nMessage:\n{message}"

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # ── Method 1: TLS port 587 ──
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("  [OK] Email sent via TLS:587")
        return True, "Message sent successfully!"
    except smtplib.SMTPAuthenticationError:
        pass
    except Exception as e:
        if "Connection" in str(e) or "timed out" in str(e):
            pass
        else:
            return False, f"TLS Error: {str(e)}"

    # ── Method 2: SSL port 465 ──
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("  [OK] Email sent via SSL:465")
        return True, "Message sent successfully!"
    except smtplib.SMTPAuthenticationError:
        return False, (
            "GMAIL LOGIN FAIL: Password galat hai ya App Password chahiye.\n\n"
            "Agar 2-Step Verification ON hai → App Password banao:\n"
            "Google Account → Security → 2-Step Verification → App Passwords → Generate\n"
            "Wo 16-digit password .env mein SENDER_PASSWORD mein daalo.\n\n"
            "Agar 2-Step Verification OFF hai → direct Gmail password daalo."
        )
    except Exception as e:
        return False, f"SSL Error: {str(e)}"


@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(".", path)


@app.route("/send", methods=["POST"])
def handle_send():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        phone = data.get("phone", "").strip()
        city = data.get("city", "").strip()
        message = data.get("message", "").strip()

        if not name:
            return jsonify({"success": False, "message": "Name is required"}), 400
        if not email or "@" not in email:
            return jsonify({"success": False, "message": "Valid email is required"}), 400
        if not subject:
            return jsonify({"success": False, "message": "Subject is required"}), 400
        if not message:
            return jsonify({"success": False, "message": "Message is required"}), 400

        print(f"\n  [>] New request: {name} ({email})")
        print(f"  [>] Phone: {phone} | City: {city}")
        print(f"  [>] Subject: {subject}")

        ok, result_msg = send_via_gmail(name, email, subject, message, phone, city)

        if ok:
            print(f"  [OK] Delivered to {RECEIVER_EMAIL}\n")
            return jsonify({"success": True, "message": result_msg})
        else:
            print(f"  [FAIL] {result_msg}\n")
            return jsonify({"success": False, "message": result_msg}), 500

    except Exception as e:
        print(f"  [ERR] {str(e)}\n")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


def open_browser():
    time.sleep(2)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    print()
    print("=" * 55)
    print("     GMAIL SMTP SERVER — No API, No Outlook")
    print("=" * 55)

    missing = []
    if not SENDER_EMAIL: missing.append("SENDER_EMAIL")
    if not SENDER_PASSWORD: missing.append("SENDER_PASSWORD")
    if not RECEIVER_EMAIL: missing.append("RECEIVER_EMAIL")

    if missing:
        print(f"\n  [ERROR] .env mein ye missing hain: {', '.join(missing)}\n")
        print("  .env file aise banao:\n")
        print("  SENDER_EMAIL=tumhara@gmail.com")
        print("  SENDER_PASSWORD=tumhara_password")
        print("  RECEIVER_EMAIL=jisko_bhejna_hai@gmail.com")
        print("\n  Password guide:")
        print("  ──────────────────────────────────────────")
        print("  2FA OFF hai?  → direct Gmail password daalo")
        print("  2FA ON hai?   → App Password daalo (16 digit)")
        print("                  Google Account > Security > App Passwords")
        print("  ──────────────────────────────────────────")
        print()
        input("  Press Enter to exit...")
        sys.exit(1)

    print(f"\n  Sender  : {SENDER_EMAIL}")
    print(f"  To      : {RECEIVER_EMAIL}")
    print(f"  URL     : http://localhost:{PORT}")
    print("=" * 55)
    print("  Server starting... Browser auto-open hoga")
    print("  Ctrl+C se band karo\n")

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)