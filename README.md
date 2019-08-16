# oB-WAF-verifier

For checking if WAF protections are working correctly for various sites.

### Author

[oBreak](mailto:obreakemail@gmail.com)

### Version 

0.1

### Compatibility

Compatible for Linux and Mac, re: directory functions for pulling in sites, need to test for Windows.

### Pre-requisites (Important or this will not work!)

- Python 3.6+ installed
- Network connectivity, assuming target is outside of local machine
- Install `requests` modules.

### Usage

Place target web address in .txt or .log files in the `/in/`
directory. One address per line.

Response text can be found in the `/out/` directory

