# Costs and Budgeting

Creating an AWS account required a credit card, so the obvious question is: how much
is deploying our portfolio project actually going to cost?

## What costs can I expect for deploying my first portfolio project on AWS?

Nothing, as long as you stay on the **Free plan**.

AWS does not charge your payment method while you are on the Free plan. Your usage is
deducted from your AWS credits instead. AWS can only charge your payment method after
you upgrade to the **Paid plan**.

AWS still asks for a credit card during signup to verify your identity and to prevent
abuse.

## What's included in the free tier?

When you create a new AWS account you receive **$100 in credits**. You can earn up to
**another $100** by completing five activities in the "Explore AWS" widget on the AWS
Management Console home page, worth $20 each. 

So a new customer can end up with up to $200 in credits.

You can see your remaining credits in the **Cost and usage** widget on the console home
page.

The Free plan ends when either of these happens first:

1. Six months have passed since you opened the account, or
2. You have used up all of your credits

Most popular AWS services are usable on the Free plan, including all the ones we need in
this course.

> Note: your credits expire twelve months after you open your account, independently of
> the six-month Free plan period.

## What can I do to not be surprised by a big bill once I am on the paid plan?

Set up an **AWS Budget**. It notifies you by email when your costs approach or exceed an
amount you define.

1. In the AWS Management Console, open **Billing and Cost Management**
2. Click on **Budgets** in the left sidebar
3. Click **Create budget**
4. Keep **Use a template (simplified)** selected
5. Choose the **Monthly cost budget** template
6. Enter a budget name, for example `Monthly Cost Budget Alert`
7. Enter the monthly amount you are comfortable spending, for example `5` dollars
8. Enter the email address that should receive the alerts
9. Click **Create budget**

With this template you get notified when your forecasted spend reaches 85% of the
amount, when your actual spend reaches 100%, and when your forecasted spend reaches
100%.

### A budget is an alert, not a spending limit

This is the most important thing to understand about budgets. Setting a $5 budget does
**not** mean AWS shuts everything down at $5. AWS keeps your services running and simply
warns you. There is no hard spending cap on AWS by default.

## What happens when the Free plan ends?

You need to upgrade to the Paid plan if you want to keep using your account and your
resources. If you do not upgrade, AWS closes the account and you lose access to your
resources. You have 90 days to upgrade before AWS permanently deletes the account and
everything in it.

Credits you have left are not lost when you upgrade. They can still be used for eligible
usage until they expire.

## More information

- AWS Free Tier: https://aws.amazon.com/free
- Choosing a plan: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- AWS Free Tier terms: https://aws.amazon.com/free/terms/
- Best practices for AWS Budgets: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html
