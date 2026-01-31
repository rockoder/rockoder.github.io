---
title: "Dockerizing Your Product"
date: 2017-02-12T16:36:00.000+05:30
author: "Ganesh Pagade"
tags: ["docker", "devops"]
draft: false
---

So you are planning to containerize your product. You read the Docker docs, watched few videos and played around with basic Docker commands. But you are wondering, now what? How do you start containerizing this monolithic, legacy, enterprise product?

Here are few steps that could help you through the process and get you a starting point. This would be a three part article. This part covers the information you need to gather before starting to write the Dockerfile.

# Understand the Product Installation

![]({{ site.url }}/images/posts/2017-02-12-dockerizing-your-product/product+installation.png)

In this section, we'll talk about the research you need to do and data that you need to collect which will be useful later while creating the Dockerfile and other scripts.

## 1. Identify System Prerequisites

Best place to start is look for the System Requirements section of the Product Documentation. Go find the documentation. Pray you have one. 

Note the base OS on which the product is deployed. If you support multiple operating systems, start with the most popular Linux based OS on which the product is deployed. Docker on Windows is still at nascent stage and you don't want to add one more unknown parameter in your research. Prefer Debian based OS like Ubuntu just for its ease of package management and installation.

Identify additional software and libraries which your product assumes to be present on the system before you being the product installation.

Also note the sizing guidelines for the server on which you deploy the product. Note the memory, CPU requirements. Preferably start with the smallest size supported.

## 2. Identify Binaries Added

What software are installed when you deploy or install the product? Are there third party software bundled with the setup. Transitive dependencies? Do you need JRE?

## 3. Identify Inputs Taken

What inputs do you provide during the installation process? What are the default values during silent installation? What things are assumed and currently not configurable?

1. DB details - Server details, DB credentials
1. User credentials
1. Installation location - location to put the binaries
1. Product configurations - log level, heap sizes etc

## 4. Identify Configurations

Where are the product configuration files stored? What all things are configurable? What are the default values? What configurations are asked to the user during installation?

## 5. Identify Order of Initialization

Does your product spawns multiple processes or daemons running in background? What are they? In what order are those started? In what order do they stop?

Do not think about splitting the product right now. You would do it eventually, but not now. Right now the focus is on getting the product containerized.
