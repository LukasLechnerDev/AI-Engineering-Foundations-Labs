# Enable Multi-Factor Authentication (MFA)

In order to secure your AWS root account, you should enable Multi-Factor Authentication (MFA).

## Why this matters

Your root account has unrestricted access to everything in your AWS account. If an attacker gets in, they could:

- Launch expensive resources (for example, virtual machines for crypto mining) that get billed to your credit card
- Steal customer data from your databases
- Get access to API keys and passwords
- Delete resources from your account

Unlike OpenAI, where you pre-pay a small amount of credits and your loss is capped, AWS has no hard spending limit that protects you by default. So even for small hobby projects, take root account security seriously.

## Steps

1. Head over to https://aws.amazon.com
2. Click "Sign in to the Console", then "Sign in using root user email"
3. Enter your root email address and password
4. In the top right, click on your account name, then on "Security credentials"
5. Scroll down to the "Multi-factor authentication (MFA)" section
6. Click on "Assign MFA device"
7. Enter a name for your device
8. Select the MFA device type. AWS recommends a **passkey**, which is the recommended choice here too, since almost all popular password managers support passkeys. An authenticator app or a hardware token work as well.
9. Optionally customize the display name of the passkey, then click "Next"
10. Follow the passkey creation process of your password manager or device

## Optional: add a second MFA device

You can assign a second MFA device as a backup. If you ever lose access to your primary MFA method, you can still log in with the second one.
