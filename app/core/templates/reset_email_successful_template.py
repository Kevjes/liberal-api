import datetime

def password_change_alert_template(user_first_name: str, user_email: str, reset_date_time: str) -> str:
    current_year = datetime.datetime.now().year
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Alert - Liberal Password Changed</title>
    <style>
        body, p, h1, h2, h3 {{
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
        }}

        body {{
            line-height: 1.6;
            color: white;
            background-color: #1E1E1E;
            padding: 20px 0;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #1E1E1E;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #444444;
        }}

        .header {{
            background-color: #BE1522;
            padding: 25px;
            text-align: center;
        }}

        .logo {{
            max-width: 180px;
            height: auto;
            display: block;
            margin: 0 auto;
        }}

        .content {{
            padding: 30px 40px;
            color: white;
        }}

        h1 {{
            color: white;
            font-size: 22px;
            margin-bottom: 20px;
            font-weight: bold;
        }}

        p {{
            margin-bottom: 18px;
            font-size: 15px;
            color: white;
        }}

        .content a {{
            color: #CCCCCC;
            text-decoration: underline;
        }}
        
        .content a:hover {{
            color: #FFFFFF;
        }}

        .footer {{
            background-color: #1E1E1E;
            padding: 25px 40px;
            text-align: center;
            font-size: 12px;
            color: #777777;
            border-top: 1px solid #444444;
        }}

        .footer p {{
            color: #777777;
            margin-bottom: 8px;
            font-size: 12px;
        }}
        
        .footer a {{
            color: #999999;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}

        .support-info {{
            margin-top: 30px;
            border-top: 1px solid #444444;
            padding-top: 25px;
            color: #CCCCCC;
        }}
        
        .support-info p {{
             color: #CCCCCC;
             margin-bottom: 10px;
             font-size: 14px;
        }}

        .support-info a {{
            color: #CCCCCC;
            text-decoration: none;
        }}
        
        .support-info a:hover {{
            color: #FFFFFF;
            text-decoration: underline;
        }}

        @media screen and (max-width: 600px) {{
            .content {{
                padding: 20px 25px;
            }}
            .footer {{
                 padding: 20px 25px;
            }}
            h1 {{
                font-size: 20px;
            }}
            p {{
                font-size: 14px;
            }}
        }}

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://cli.menosi.net/images/logo/white-red.png" alt="Liberal Logo" class="logo">
        </div>

        <div class="content">
            <h1>Password Successfully Changed</h1>

            <p>Hello {user_first_name},</p>

            <p>This email confirms that the password for your Liberal account associated with {user_email} was successfully changed on {reset_date_time}.</p>

            <p>If you did not request this change, please contact our support team immediately to secure your account.</p>

            <div class="support-info">
                <p>Need help? Contact our support team:</p>
                <p>📧 <a href="mailto:cli.support@menosi.net">cli.support@menosi.net</a></p>
                <p>📞 +237 651 519 814</p>
            </div>
        </div>

        <div class="footer">
            <p>This email was sent to {user_email}</p>
            <p>© {current_year} Liberal. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
""".format(user_first_name=user_first_name, user_email=user_email, reset_date_time=reset_date_time, current_year=current_year)

# Example usage:
# user_name = "Jane"
# email_address = "jane.doe@example.com"
# timestamp = "April 22, 2025 at 11:40 AM WAT" 
# html_content = password_change_alert_template(user_name, email_address, timestamp)
# print(html_content)