# Lazy-Edgexnet

Automated account registration tool for EdgeX Network platform with referral code support.

## Features

* Automatic account registration (main feature)
* Proxy support (HTTP protocol only)

## Discussion

If you have any questions, please join our discussion group:  
[https://t.me/sdsproject_chat](https://t.me/sdsproject_chat)

## Proxy Providers

Compatible proxy providers:

1. [Proxy-Cheap](https://app.proxy-cheap.com/r/mlShoy)
2. [DataImpulse](https://dataimpulse.com/?aff=48082) (`$1/GB for new users!`)
3. [ProxiesFO](https://app.proxies.fo/ref/c02fda06-da42-f640-7ef7-885127487ef0)

## Installation

### Requirements

* Python 3.8+
* Git
* EdgeX Network platform referral code

### Configuration

* Edit referral_code.txt  
  Enter your referral code in this file
* Edit proxies.txt  
  Add your proxies to this file if you want to use them. See [Proxy Providers](#proxy-providers) for recommended providers.

  Required proxy formats:

  For authenticated proxies:
  ```
  Format
  http://user:password@proxy_server:proxy_port

  Example
  http://admin:admin@192.168.1.1:8080
  ```

  For non-authenticated proxies:
  ```
  Format
  http://proxy_server:proxy_port

  Example
  http://192.168.1.1:8000
  ```

### Automated Registration

```bash
# Clone repository
git clone https://github.com/akasakaid/lazy-edgexnet

# Navigate to folder
cd lazy-edgexnet

# Install required libraries
python3 -m pip install -r requirements.txt

# Run register.py script
python3 register.py

# Enter the number of referrals/accounts you want to create!
```

## Thank You :3
