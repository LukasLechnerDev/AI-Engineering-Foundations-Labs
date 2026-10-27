# Setting up a cron job for scheduled execution

Our job agent now runs on EC2, but we still have to start it manually. **Cron** lets us run commands
on a schedule, so we can receive a job digest every day or every week without logging in.
The instance must be running at the scheduled time for the job to run.

Run the commands below on the EC2 instance as `ec2-user`. The examples assume the repository is at
`/home/ec2-user/AI-Engineering-Foundations-Labs`. If you cloned it elsewhere, adjust the paths.
Run `pwd` inside the repository to check its location.

## Set the time zone

By default, cron's schedule follows the instance's time zone.
Amazon Linux EC2 instances use **UTC** by default, regardless of the AWS Region.

Check the current setting:

```bash
timedatectl
```

You can keep UTC or choose your local time zone. List the available names:

```bash
timedatectl list-timezones
```

Filter the list by a city or region. `grep -i` finds matching lines regardless of capitalization:

```bash
timedatectl list-timezones | grep -i asia
```

Choose a major city that follows the same time and daylight saving rules as your location.
Examples include `Europe/Vienna`, `Europe/London`, `America/New_York`, and `Asia/Kolkata`.

Set your chosen time zone, then check the result:

```bash
sudo timedatectl set-timezone Europe/Vienna
timedatectl
```

## Use a small helper script

Our [run-job-agent.sh](../../01-deploy-project/cron-job/run-job-agent.sh) script changes to the
project directory and starts the application with `uv`. Keeping these steps in a script makes the
cron entry easier to read and lets us test the same command manually.

Cron starts programs with a smaller environment than our terminal session. **`PATH`** lists the
directories searched for commands, and cron's `PATH` may not include the directory containing `uv`.
The script therefore uses `"$HOME/.local/bin/uv"` directly. `$HOME` is the home directory of the
user running the job. This assumes `uv` was installed there for that user.

## Test the helper script

Make sure the script is executable. `chmod +x` adds execute permission; Git may already have
restored this permission when you cloned the repository.

```bash
chmod +x ~/AI-Engineering-Foundations-Labs/4-deployment-on-aws/01-deploy-project/cron-job/run-job-agent.sh
```

Run it manually to check that the workflow completes and sends the expected email:

```bash
~/AI-Engineering-Foundations-Labs/4-deployment-on-aws/01-deploy-project/cron-job/run-job-agent.sh
```

`~` stands for your home directory. If you want to interrupt the run, press **Ctrl+C**.

## Enable cron

Amazon Linux 2023 does not include cron by default. Install `cronie`, then start its service and
enable it to start automatically after reboots:

```bash
sudo dnf install -y cronie
sudo systemctl enable --now crond
```

## Add the cron entry

A **crontab** stores a user's scheduled commands. Open yours in an editor:

```bash
crontab -e
```

Use `crontab -e` as `ec2-user`, without `sudo`, so the job runs as the same user who installed `uv`.
Each entry contains five scheduling fields followed by the command:

```text
minute hour day-of-month month day-of-week command
```

An asterisk (`*`) means every value for that field. For **every day at 08:00**, add this as one line:

```cron
0 8 * * * /home/ec2-user/AI-Engineering-Foundations-Labs/4-deployment-on-aws/01-deploy-project/cron-job/run-job-agent.sh >> /home/ec2-user/job-agent.log 2>&1
```

For **every Monday at 08:00**, use this line instead. `1` in the day-of-week field means Monday:

```cron
0 8 * * 1 /home/ec2-user/AI-Engineering-Foundations-Labs/4-deployment-on-aws/01-deploy-project/cron-job/run-job-agent.sh >> /home/ec2-user/job-agent.log 2>&1
```

Choose one schedule, then save and exit the editor. Both examples use the instance's time zone.

## Save normal output and errors

The end of the cron entry saves output that would otherwise appear in the terminal:

```bash
>> /home/ec2-user/job-agent.log 2>&1
```

- **`>>`** appends normal output to the log file, creating it if needed. A single `>` would overwrite it.
- **`1`** identifies standard output, such as Python's `print()` messages.
- **`2`** identifies standard error, such as Python tracebacks.
- **`2>&1`** sends error output to the same destination as normal output: our log file.

The order matters: first redirect normal output to the file, then send errors to that destination.

## Verify the scheduled run

List your saved entries:

```bash
crontab -l
```

To test without waiting until tomorrow, temporarily set the minute and hour to about five minutes
in the future, using the instance's current time from `date`. After that time, inspect the log:

```bash
tail -n 50 /home/ec2-user/job-agent.log
```

`tail -n 50` shows the last 50 lines. Check that the workflow completed and that you received the
job digest email, then restore your intended daily or weekly schedule with `crontab -e`.

## More information

- [EC2 time zone configuration](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/change-time-zone-of-instance.html)
- [Cron support on Amazon Linux 2023](https://docs.aws.amazon.com/linux/al2023/ug/cron.html)
- [Crontab syntax and environment](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [Bash output redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
