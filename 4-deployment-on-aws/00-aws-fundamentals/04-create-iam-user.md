# Create an IAM User for Day-to-Day Work

The root user should only be used for a few rare tasks. For everything else, you should use a separate user with fewer permissions.

## Why this matters

- The more often you enter your root credentials, the higher the chance that an attacker gets access to them or hijacks your session.
- If your day-to-day user ever gets compromised, you can still log in as root and delete that user.

The AWS service for managing who can access what is called **IAM** (Identity and Access Management).

## Create the user

1. In the AWS Management Console, search for "IAM" and open the service
2. Click on "Users" in the left sidebar
3. Click the orange "Create user" button
4. Enter a user name (for example your first name)
5. Check "Provide user access to the AWS Management Console"
6. Let AWS generate a password for you, or create your own
7. Uncheck "Users must create a new password at next sign-in"
8. Click "Next"

## Create a user group with permissions

In AWS you normally do not attach permissions directly to a user. Instead you create a **user group**, attach **policies** (the documents that define permissions) to the group, and put your users in that group. That makes permissions much easier to maintain.

1. On the permissions step, choose "Add user to group" and click "Create group"
2. Name the group `ai-engineers`
3. Attach these AWS managed policies:
   - `AmazonEC2FullAccess`
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonECS_FullAccess`
   - `AmazonEventBridgeSchedulerFullAccess`
   -`AmazonSSMFullAccess`
4. Click "Create user group"
5. Select the new group, click "Next", review, and click "Create user"

> Note on least privilege: in a real company, an administrator would define much more fine-grained permissions instead of granting full access to these services. We keep it simple here so we can focus on deploying our project. 
## Save the credentials and the sign-in link

1. Store the user name and password in your password manager
2. Copy the console sign-in link and bookmark it. It contains your **AWS account ID**, the 12 digit number that identifies your account. You can also find it in the top right of the console.

## Enable MFA for the new user

This user can still launch EC2 instances, so protect it as well.

1. Open the new user in IAM
2. Select the "Security credentials" tab
3. Click "Assign MFA device" and follow the same steps as for the root user (a passkey is recommended, an authenticator app works too)

## Log in with the new user

Sign out of the root user and sign in with the sign-in link and the new credentials.

From now on, use this user for everything in this module.
