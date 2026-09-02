# AWS Regions

AWS does not run one giant data center. It runs many of them, grouped into **regions** all over
the world: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/

## What is a region?

A region is a geographic area, for example "Europe (Stockholm)".

One dot on that map is not a single data center. Every region consists of at least three
**Availability Zones**, and each zone is one or more data centers with its own power, networking
and cooling. The zones are far enough apart that a fire or a power outage only hits one of them,
which is how AWS keeps a service running when a data center fails.

Regions are isolated from each other. Your data stays in the region you chose unless you move
it.

## Every resource lives in exactly one region

A **service** is a product AWS offers, like EC2. A **resource** is what you create with it, like
a single EC2 instance. Most services are regional, so every resource you create belongs to
exactly one region.

You select the region in the **top right corner** of the console. Whatever is selected there is
where your next resource gets created.

## Region names and region codes

Every region has a display name and a short **region code**:

| Display name          | Region code    |
| --------------------- | -------------- |
| Europe (Stockholm)    | `eu-north-1`   |
| Europe (Frankfurt)    | `eu-central-1` |
| US East (N. Virginia) | `us-east-1`    |
| Asia Pacific (Mumbai) | `ap-south-1`   |

The region code is what you find in ARNs (Amazon Resource Name) or endpoints

Example: `ec2-16-171-161-221.eu-north-1.compute.amazonaws.com`

## Which region should you choose?

- **Distance to your users** for low latency. Important for a website or web API, less so for
  our scheduled workflow, which nobody calls over the network.
- **Regulation and compliance**, for example customer data that has to stay inside the EU.
- **Cost**, because prices differ between regions.
- **Service availability**, because newer or specialized services are not everywhere.



## Global services

Some services are **global**, and the region selector shows "Global" for them. You already used
one: **IAM**. Our user and group belong to the AWS account and are valid in all regions.

## When a resource seems to have disappeared

A resource only shows up while its region is selected in the top right corner. If your EC2
instance is missing, check that you are looking at the region you created it in.

## More information

- Regions and Availability Zones: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
- Regions and Availability Zones (docs): https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html
- List of all region codes: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html
- Enabling a region: https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html
