# Choosing the AMI

We gave our instance a name, so the next decision in the launch form is which operating system
comes pre-installed on the machine. That is what the **AMI** defines.

## What is an AMI?

**AMI** stands for **Amazon Machine Image**. It is a template that AWS uses to create the disk of
your new instance, and it contains the operating system plus any software that was installed when
the image was built.

There are thousands of AMIs to choose from. The launch form shows the most popular ones under
**Quick Start**: Amazon Linux, macOS, Ubuntu, Windows, Red Hat, SUSE Linux, and Debian.

## Why Linux?

The only hard requirement for our workflow is that the machine can run Python and uv, and Windows
and macOS can do that too. Still, Linux is the right choice here:

1. **Lightweight.** Linux runs fine without a graphical interface and without a lot of background
   processes, so it needs less CPU, memory, and disk. That means it also runs on cheaper hardware,
   which we pick in the next step when we choose the instance type.
2. **No licensing fee.** Most Linux distributions add no OS licensing cost, unlike Windows Server.
3. **Huge server and cloud ecosystem.** The tools we use in this course, like Docker, Python, Git,
   and the AWS tools, are all at home on Linux.

macOS is a special case. EC2 Mac instances run on Dedicated Hosts with a minimum allocation of 24
hours, so they are neither cheap nor convenient for a small workload like ours.

## Which Linux distribution?

Amazon Linux, Ubuntu, Debian, Red Hat, and SUSE are different **distributions**: same Linux kernel,
different package managers, defaults, release cycles, and support models.

We go with **Amazon Linux**, AWS's own distribution, which is built, tuned, and maintained
specifically for running on AWS.

## A note on the free tier

AMIs that carry a commercial subscription, like Red Hat Enterprise Linux or SUSE Linux Enterprise
Server, bundle the license fee into the hourly instance price, so the same instance costs more with
those images. Amazon Linux and Ubuntu have no such fee.

In the launch form, look for the **"Free tier eligible"** label on an AMI. Keep in mind that the AMI
is only one half of it: whether you actually stay free also depends on the **instance type** you
pick in the next step, and on which free tier your account is on.

- Account created **before July 15, 2025** and younger than 12 months: 750 hours per month of a
  `t2.micro` instance (`t3.micro` in regions without `t2.micro`).
- Account created **on or after July 15, 2025**: `t3.micro`, `t3.small`, `t4g.micro`, `t4g.small`,
  `c7i-flex.large`, and `m7i-flex.large` for 6 months or until your free credits are used up.

## Steps

1. In the **Application and OS Images** section, stay on the **Quick Start** tab
2. Select **Amazon Linux**
3. In the **Amazon Machine Image** dropdown below, leave the latest suggested Amazon Linux version
   selected
4. Check that the AMI is marked "Free tier eligible"

Now that the AMI is set, we can choose the instance type, which is the hardware our virtual machine
runs on.

## More information

- Amazon Machine Images: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html
- Amazon Linux: https://docs.aws.amazon.com/linux/al2023/ug/what-is-amazon-linux.html
- Free tier usage for EC2, before and after July 15, 2025: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html
