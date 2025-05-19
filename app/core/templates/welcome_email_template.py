import datetime

def welcome_email_template(user_first_name: str, user_email: str, getting_started_link: str, documentation_link: str) -> str:
    current_year = datetime.datetime.now().year
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Menosi CLI</title>
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
        
        .action-button {{
            display: inline-block;
            background-color: #BE1522;
            color: white !important;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 5px;
            margin: 15px 0 25px 0;
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            border: none;
        }}

        .content a {{
            color: #CCCCCC;
            text-decoration: underline;
        }}
        
        .content a:hover {{
            color: #FFFFFF;
        }}
        
        /* Specific style for the action button link text */
        .action-button a, .action-button a:link, .action-button a:visited {{
             color: white !important;
             text-decoration: none;
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
             .action-button {{
                 padding: 10px 20px;
                 font-size: 15px;
            }}
        }}

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://cli.menosi.net/images/logo/white-red.png" alt="Menosi CLI Logo" class="logo">
        </div>

        <div class="content">
            <h1>Welcome to Menosi CLI!</h1>

            <p>Hello {user_first_name},</p>

            <p>We're excited to have you on board! Your Menosi CLI account associated with {user_email} has been successfully created.</p>
            
            <p>Menosi CLI helps you instantly generate 80%' of your code while respecting best coding practices. Menosi CLI also supports multiple frameworks.</p>

            <p>One order, one time saving!</p>

            <p style="text-align: center;">
                <a href="{getting_started_link}" class="action-button">Get Started</a>
            </p>

            <p>If you have any questions, feel free to check out our <a href="{documentation_link}">documentation</a> or contact our support team.</p>


            <div class="support-info">
                <p>Need help? Contact our support team:</p>
                <p>📧 <a href="mailto:cli.support@menosi.net">cli.support@menosi.net</a></p>
                <p>📞 +237 651 519 814</p>
            </div>
        </div>

        <div class="footer">
            <p>This email was sent to {user_email}</p>
            <p>© {current_year} Menosi CLI. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
""".format(user_first_name=user_first_name, user_email=user_email, getting_started_link=getting_started_link, documentation_link=documentation_link, current_year=current_year)

# Example usage:
# user_name = "Alice"
# email_address = "alice.dev@example.com"
# start_link = "https://cli.menosi.net/login" 
# doc_link = "https://cli.menosi.net/docs"
# html_content = welcome_email_template(user_name, email_address, start_link, doc_link)
# print(html_content)