import datetime

def subscription_confirmation_template(user_first_name: str, user_email: str, plan_name: str, payment_date: str, amount_paid: str, manage_subscription_link: str) -> str:
    current_year = datetime.datetime.now().year
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liberal Subscription Confirmation</title>
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
        
        .details-section {{
            background-color: #2a2a2a; /* Slightly lighter background for details */
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 5px;
            border: 1px solid #444444;
        }}
        
        .details-section p {{
            margin-bottom: 8px; /* Reduced spacing in details */
            font-size: 14px;
            color: #DDDDDD; /* Slightly lighter text for details */
        }}
        
        .details-section p strong {{
            color: white; /* Make labels stand out */
            min-width: 80px; /* Align values */
            display: inline-block;
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
             .details-section p strong {{
                min-width: 60px; 
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
            <h1>Subscription Activated!</h1>

            <p>Hello {user_first_name},</p>

            <p>Thank you for subscribing! Your payment was successful and your Liberal <strong>{plan_name}</strong> plan is now active.</p>
            
            <div class="details-section">
                <p><strong>Plan:</strong> {plan_name}</p>
                <p><strong>Status:</strong> Active</p>
                <p><strong>Amount Billed:</strong> {amount_paid}</p>
                <p><strong>Date:</strong> {payment_date}</p>
            </div>

            <p>You can now enjoy all the features included in your plan. You can manage your subscription anytime from your <a href="{manage_subscription_link}">account settings</a>.</p>


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
""".format(user_first_name=user_first_name, user_email=user_email, plan_name=plan_name, payment_date=payment_date, amount_paid=amount_paid, manage_subscription_link=manage_subscription_link, current_year=current_year)

# Example usage:
# user_name = "Bob"
# email_address = "bob.s@example.com"
# purchased_plan = "Pro Monthly"
# date_paid = "April 22, 2025"
# paid_amount = "$19.99"
# manage_link = "https://cli.menosi.net/account/billing" 
# html_content = subscription_confirmation_template(user_name, email_address, purchased_plan, date_paid, paid_amount, manage_link)
# print(html_content)