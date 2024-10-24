# Redis Project

This project demonstrates how to use Redis for basic operations and as a simple cache using Python. The project is structured to follow best practices in coding style and documentation.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
  - [redis_basic.py](#redis_basicpy)
  - [redis_cache.py](#redis_cachepy)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to set up the project on Ubuntu 18.04 LTS.

### Step 1: Install Redis

```bash
sudo apt-get -y install redis-server
pip3 install redis
sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
